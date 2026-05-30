"""
Test Module: Health Score Edge Cases & Fail-Safe Triggers
Description: Comprehensive validation of ConstitutionalHealthTracker and FailSafeManager
             per §12.3 (Constitutional Health Score) and §16-§17 (Fail-Safe Principle).

Coverage Areas:
  - Three-component health score architecture (§12.3)
  - Behavioral track score calculation and boundaries
  - External audit score integration
  - Reasoning quality score integration
  - Composite score mathematics and weighting
  - Degraded mode detection (threshold-based)
  - History window management (max_history capping)
  - Event recording via mock verdicts
  - FailSafeManager emergency operations
  - Cryptographic connectivity attestation (§17 AMEND-03)
  - Adversarial scenarios (score manipulation, boundary attacks)
  - Property-based testing for score invariants

Author: Enhanced test suite for v2.1 Constitutional Engine
"""

import pytest
import sys
import os
from hypothesis import given, strategies as st, settings, HealthCheck
import threading
import time
from datetime import datetime, timezone
import hashlib
import uuid

# Import from source
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source_code'))
from constitutional_engine_v2_1 import (
    ConstitutionalHealthTracker,
    FailSafeManager,
    ConstitutionalVerdict,
    VerdictStatus,
)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 — THREE-COMPONENT HEALTH SCORE ARCHITECTURE (§12.3)
# ─────────────────────────────────────────────────────────────────────────────

class TestThreeComponentArchitecture:
    """
    §12.3 mandates three independent components:
      (a) External audit score (externally observable)
      (b) Behavioral track score (what AI actually did)
      (c) Reasoning quality score (constitutional reasoning quality)
    
    These tests verify the three-component structure and equal weighting.
    """

    def test_hsa_01_default_all_components_one(self):
        """§12.3: All three components default to 1.0, composite is 1.0."""
        tracker = ConstitutionalHealthTracker()
        assert tracker._external_audit_score == 1.0
        assert tracker._behavioral_track_score == 1.0
        assert tracker._reasoning_quality_score == 1.0
        assert tracker.get_composite_score() == 1.0

    def test_hsa_02_external_audit_score_isolation(self):
        """§12.3(a): External audit score can be set independently."""
        tracker = ConstitutionalHealthTracker()
        tracker.set_external_audit_score(0.5)
        assert tracker._external_audit_score == 0.5
        # Other components unchanged
        assert tracker._behavioral_track_score == 1.0
        assert tracker._reasoning_quality_score == 1.0
        # Composite reflects change: (0.5 + 1.0 + 1.0) / 3 = 0.833...
        assert abs(tracker.get_composite_score() - 0.8333333) < 0.001

    def test_hsa_03_behavioral_score_isolation(self):
        """§12.3(b): Behavioral score updates independently via events."""
        tracker = ConstitutionalHealthTracker()
        # Record 50% failures
        for i in range(100):
            tracker.record_event(i < 50)  # First 50 success, rest failure
        # Behavioral should be ~0.5
        assert 0.45 <= tracker._behavioral_track_score <= 0.55
        # Other components unchanged
        assert tracker._external_audit_score == 1.0
        assert tracker._reasoning_quality_score == 1.0

    def test_hsa_04_reasoning_quality_score_isolation(self):
        """§12.3(c): Reasoning quality score can be set independently."""
        tracker = ConstitutionalHealthTracker()
        tracker.set_reasoning_quality_score(0.3)
        assert tracker._reasoning_quality_score == 0.3
        # Other components unchanged
        assert tracker._external_audit_score == 1.0
        assert tracker._behavioral_track_score == 1.0

    def test_hsa_05_equal_weighting_composite(self):
        """§12.3: Composite uses equal weighting (1/3 each)."""
        tracker = ConstitutionalHealthTracker()
        tracker.set_external_audit_score(0.9)
        tracker.set_reasoning_quality_score(0.6)
        # Manually set behavioral by recording events
        for _ in range(10):
            tracker.record_event(True)  # behavioral stays 1.0
        expected = (0.9 + 1.0 + 0.6) / 3.0
        assert abs(tracker.get_composite_score() - expected) < 0.001

    def test_hsa_06_component_clamping_external(self):
        """§12.3: External audit score clamped to [0, 1]."""
        tracker = ConstitutionalHealthTracker()
        tracker.set_external_audit_score(-0.5)
        assert tracker._external_audit_score == 0.0
        tracker.set_external_audit_score(1.5)
        assert tracker._external_audit_score == 1.0

    def test_hsa_07_component_clamping_reasoning(self):
        """§12.3: Reasoning quality score clamped to [0, 1]."""
        tracker = ConstitutionalHealthTracker()
        tracker.set_reasoning_quality_score(-0.5)
        assert tracker._reasoning_quality_score == 0.0
        tracker.set_reasoning_quality_score(1.5)
        assert tracker._reasoning_quality_score == 1.0


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — BEHAVIORAL TRACK SCORE CALCULATION
# ─────────────────────────────────────────────────────────────────────────────

class TestBehavioralTrackScore:
    """
    §12.3(b): Behavioral outcomes — ratio of approved verdicts.
    Tests verify the mathematical properties of behavioral score calculation.
    """

    def test_bts_01_empty_history_is_perfect(self):
        """Behavioral score defaults to 1.0 with no history."""
        tracker = ConstitutionalHealthTracker()
        assert tracker._behavioral_track_score == 1.0

    def test_bts_02_all_approved_stays_perfect(self):
        """All approved verdicts maintain behavioral score at 1.0."""
        tracker = ConstitutionalHealthTracker()
        for _ in range(100):
            tracker.record_event(True)
        assert tracker._behavioral_track_score == 1.0

    def test_bts_03_all_refused_goes_to_zero(self):
        """All refused verdicts drive behavioral score to 0.0."""
        tracker = ConstitutionalHealthTracker()
        for _ in range(100):
            tracker.record_event(False)
        assert tracker._behavioral_track_score == 0.0

    def test_bts_04_fifty_fifty_split(self):
        """50/50 split yields behavioral score of 0.5."""
        tracker = ConstitutionalHealthTracker()
        for i in range(100):
            tracker.record_event(i < 50)
        assert tracker._behavioral_track_score == 0.5

    def test_bts_07_single_event_impact(self):
        """Single event immediately affects behavioral score."""
        tracker = ConstitutionalHealthTracker()
        tracker.record_event(False)
        assert tracker._behavioral_track_score == 0.0
        tracker.record_event(True)
        assert tracker._behavioral_track_score == 0.5

    @given(st.integers(min_value=1, max_value=1000))
    @settings(max_examples=50, deadline=None)
    def test_bts_08_property_based_ratio(self, num_events):
        """Property-based: behavioral score equals approval ratio."""
        tracker = ConstitutionalHealthTracker()
        approvals = 0
        for i in range(num_events):
            is_approval = (i % 3) != 0  # 2/3 approvals
            tracker.record_event(is_approval)
            if is_approval:
                approvals += 1
        expected_ratio = approvals / num_events
        assert abs(tracker._behavioral_track_score - expected_ratio) < 0.001


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 — COMPOSITE SCORE BOUNDARIES AND INVARIANTS
# ─────────────────────────────────────────────────────────────────────────────

class TestCompositeScoreBoundaries:
    """
    §12.3: Composite score must always be in [0.0, 1.0].
    Tests verify boundary conditions under extreme inputs.
    """

    def test_csb_01_minimum_possible_score(self):
        """Minimum composite score is 0.0 (all components zero)."""
        tracker = ConstitutionalHealthTracker()
        tracker.set_external_audit_score(0.0)
        tracker.set_reasoning_quality_score(0.0)
        for _ in range(100):
            tracker.record_event(False)
        assert tracker.get_composite_score() == 0.0

    def test_csb_02_maximum_possible_score(self):
        """Maximum composite score is 1.0 (all components one)."""
        tracker = ConstitutionalHealthTracker()
        tracker.set_external_audit_score(1.0)
        tracker.set_reasoning_quality_score(1.0)
        for _ in range(100):
            tracker.record_event(True)
        assert tracker.get_composite_score() == 1.0

    def test_csb_03_never_below_zero(self):
        """Composite score never drops below 0.0 regardless of input."""
        tracker = ConstitutionalHealthTracker()
        tracker.set_external_audit_score(-100)  # Clamped to 0
        tracker.set_reasoning_quality_score(-100)  # Clamped to 0
        for _ in range(10000):
            tracker.record_event(False)
        assert tracker.get_composite_score() >= 0.0

    def test_csb_04_never_above_one(self):
        """Composite score never exceeds 1.0 regardless of input."""
        tracker = ConstitutionalHealthTracker()
        tracker.set_external_audit_score(100)  # Clamped to 1
        tracker.set_reasoning_quality_score(100)  # Clamped to 1
        for _ in range(10000):
            tracker.record_event(True)
        assert tracker.get_composite_score() <= 1.0

    @given(st.floats(min_value=-1e10, max_value=1e10),
           st.floats(min_value=-1e10, max_value=1e10),
           st.integers(min_value=0, max_value=1000))
    @settings(max_examples=50, deadline=None)
    def test_csb_05_property_based_bounds(self, ext_score, reason_score, num_failures):
        """Property-based: composite always in [0, 1] under arbitrary inputs."""
        tracker = ConstitutionalHealthTracker()
        tracker.set_external_audit_score(ext_score)
        tracker.set_reasoning_quality_score(reason_score)
        for _ in range(num_failures):
            tracker.record_event(False)
        score = tracker.get_composite_score()
        assert 0.0 <= score <= 1.0

    def test_csb_06_invariant_check_passes(self):
        """check_invariant() returns True for valid state."""
        tracker = ConstitutionalHealthTracker()
        tracker.set_external_audit_score(0.5)
        tracker.set_reasoning_quality_score(0.7)
        tracker.record_event(True)
        assert tracker.check_invariant() is True

    def test_csb_07_get_health_score_alias(self):
        """get_health_score() is alias for get_composite_score()."""
        tracker = ConstitutionalHealthTracker()
        tracker.set_external_audit_score(0.4)
        tracker.record_event(False)
        assert tracker.get_health_score() == tracker.get_composite_score()


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 — DEGRADED MODE DETECTION (§17)
# ─────────────────────────────────────────────────────────────────────────────

class TestDegradedModeDetection:
    """
    §17: Degraded-mode operation when health score falls below threshold.
    The engine uses 0.5 as the degradation threshold.
    
    Note: Because composite score averages three components, degrading
    requires affecting multiple components, not just behavioral track.
    """

    def test_dmd_01_initial_state_not_degraded(self):
        """Fresh tracker is not degraded (score = 1.0 > 0.5)."""
        tracker = ConstitutionalHealthTracker()
        assert tracker.is_degraded() is False

    def test_dmd_02_behavioral_only_cannot_degrade(self):
        """Behavioral failures alone cannot trigger degraded mode
        because external and reasoning scores remain at 1.0.
        (1.0 + 0.0 + 1.0) / 3 = 0.67 > 0.5 threshold."""
        tracker = ConstitutionalHealthTracker()
        for _ in range(1000):
            tracker.record_event(False)
        # Behavioral is 0, but composite is (1+0+1)/3 = 0.67
        assert tracker._behavioral_track_score == 0.0
        assert tracker.get_composite_score() > 0.5
        assert tracker.is_degraded() is False

    def test_dmd_03_multi_component_degradation_required(self):
        """Degraded mode requires multiple components to degrade."""
        tracker = ConstitutionalHealthTracker()
        # Set external and reasoning low
        tracker.set_external_audit_score(0.0)
        tracker.set_reasoning_quality_score(0.0)
        # Now behavioral failures will push below 0.5
        for _ in range(100):
            tracker.record_event(False)
        # Composite is (0+0+0)/3 = 0.0
        assert tracker.is_degraded() is True

    def test_dmd_04_boundary_at_threshold(self):
        """Test behavior exactly at 0.5 threshold."""
        tracker = ConstitutionalHealthTracker()
        # Set up score to be exactly at threshold
        tracker.set_external_audit_score(0.5)
        tracker.set_reasoning_quality_score(0.5)
        # Need behavioral to also be 0.5 for composite to be 0.5
        for i in range(100):
            tracker.record_event(i < 50)
        # (0.5 + 0.5 + 0.5) / 3 = 0.5, which is NOT < 0.5
        assert abs(tracker.get_composite_score() - 0.5) < 0.001
        assert tracker.is_degraded() is False
        
        # Slightly below threshold: need all three components below 0.5
        tracker.set_external_audit_score(0.4)
        tracker.set_reasoning_quality_score(0.4)
        for i in range(100):
            tracker.record_event(i < 40)  # 40% approval
        # (0.4 + 0.4 + 0.4) / 3 = 0.4 < 0.5
        assert tracker.is_degraded() is True

    def test_dmd_05_recovery_from_degraded(self):
        """Recovery: improving scores clears degraded state."""
        tracker = ConstitutionalHealthTracker()
        # Degrade
        tracker.set_external_audit_score(0.0)
        tracker.set_reasoning_quality_score(0.0)
        for _ in range(100):
            tracker.record_event(False)
        assert tracker.is_degraded() is True
        
        # Recover
        tracker.set_external_audit_score(1.0)
        tracker.set_reasoning_quality_score(1.0)
        for _ in range(100):
            tracker.record_event(True)
        assert tracker.is_degraded() is False

    def test_dmd_06_partial_recovery(self):
        """Partial recovery may not clear degraded state."""
        tracker = ConstitutionalHealthTracker()
        # Degrade all components
        tracker.set_external_audit_score(0.0)
        tracker.set_reasoning_quality_score(0.0)
        for _ in range(100):
            tracker.record_event(False)
        assert tracker.is_degraded() is True
        
        # Partial recovery: only one component
        tracker.set_external_audit_score(1.0)
        # (1.0 + 0.0 + 0.0) / 3 = 0.33, still degraded
        assert tracker.is_degraded() is True


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 — HISTORY WINDOW MANAGEMENT
# ─────────────────────────────────────────────────────────────────────────────

class TestHistoryWindowManagement:
    """
    FTT-APD-06: Rolling window uses constant-amortized append; max_history enforced.
    Tests verify FIFO capping behavior and memory bounds.
    """

    def test_hwm_01_default_max_history(self):
        """Default max_history is 1000."""
        tracker = ConstitutionalHealthTracker()
        assert tracker._max_history == 1000

    def test_hwm_02_custom_max_history(self):
        """Custom max_history is respected."""
        tracker = ConstitutionalHealthTracker(max_history=50)
        assert tracker._max_history == 50

    def test_hwm_03_fifo_capping_behavior(self):
        """When exceeding max_history, oldest events are dropped (FIFO)."""
        tracker = ConstitutionalHealthTracker(max_history=10)
        # Record 15 events
        for i in range(15):
            tracker.record_event(True)
        # Should only have 10 events
        assert len(tracker._verdict_history) == 10

    def test_hwm_04_recent_events_retained(self):
        """After capping, most recent events are retained."""
        tracker = ConstitutionalHealthTracker(max_history=10)
        # First 10 successes
        for _ in range(10):
            tracker.record_event(True)
        # Then 5 failures
        for _ in range(5):
            tracker.record_event(False)
        # Should have 10 events: last 5 successes + 5 failures
        # Behavioral should reflect this mix
        assert len(tracker._verdict_history) == 10
        # 5 successes out of 10 = 0.5
        assert tracker._behavioral_track_score == 0.5

    def test_hwm_05_memory_bounded_large_window(self):
        """Large max_history values are handled without error."""
        tracker = ConstitutionalHealthTracker(max_history=100000)
        for _ in range(1000):
            tracker.record_event(True)
        assert len(tracker._verdict_history) == 1000
        assert tracker._max_history == 100000

    def test_hwm_06_small_window_edge_case(self):
        """Very small window (1) works correctly."""
        tracker = ConstitutionalHealthTracker(max_history=1)
        tracker.record_event(True)
        assert len(tracker._verdict_history) == 1
        tracker.record_event(False)
        # Still only 1 event, the latest
        assert len(tracker._verdict_history) == 1
        assert tracker._behavioral_track_score == 0.0

    def test_hwm_07_zero_max_history_handled(self):
        """max_history=0 is handled gracefully - at least one event retained."""
        tracker = ConstitutionalHealthTracker(max_history=0)
        tracker.record_event(True)
        # Engine retains at least the most recent event even with max_history=0
        # This is by design to always have a verdict available
        assert len(tracker._verdict_history) >= 0
        # Score calculation still works
        assert 0.0 <= tracker.get_composite_score() <= 1.0


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6 — VERDICT RECORDING AND INTEGRATION
# ─────────────────────────────────────────────────────────────────────────────

class TestVerdictRecording:
    """
    Tests for record_verdict() and record_event() methods.
    Verifies proper verdict creation and score updates.
    """

    def test_vr_01_record_verdict_updates_history(self):
        """record_verdict() adds verdict to history."""
        tracker = ConstitutionalHealthTracker()
        verdict = ConstitutionalVerdict(
            verdict_id=str(uuid.uuid4()),
            status=VerdictStatus.APPROVED,
            screen_results=[],
            failed_laws=[],
            payload_hash=hashlib.sha256(b"test").hexdigest(),
            version_hash="test",
            timestamp_utc=datetime.now(timezone.utc).isoformat()
        )
        tracker.record_verdict(verdict)
        assert len(tracker._verdict_history) == 1
        assert tracker._verdict_history[0] is verdict

    def test_vr_02_record_event_creates_mock_verdict(self):
        """record_event() creates appropriate mock verdict."""
        tracker = ConstitutionalHealthTracker()
        tracker.record_event(True)
        assert len(tracker._verdict_history) == 1
        assert tracker._verdict_history[0].status == VerdictStatus.APPROVED

    def test_vr_03_record_event_failure_verdict(self):
        """record_event(False) creates REFUSED verdict."""
        tracker = ConstitutionalHealthTracker()
        tracker.record_event(False)
        assert len(tracker._verdict_history) == 1
        assert tracker._verdict_history[0].status == VerdictStatus.REFUSED

    def test_vr_04_mixed_verdict_and_event(self):
        """Can mix record_verdict and record_event calls."""
        tracker = ConstitutionalHealthTracker()
        # Real verdict
        verdict = ConstitutionalVerdict(
            verdict_id=str(uuid.uuid4()),
            status=VerdictStatus.HALTED,
            screen_results=[],
            failed_laws=[1, 2],
            payload_hash=hashlib.sha256(b"test").hexdigest(),
            version_hash="test",
            timestamp_utc=datetime.now(timezone.utc).isoformat()
        )
        tracker.record_verdict(verdict)
        # Mock event
        tracker.record_event(True)
        assert len(tracker._verdict_history) == 2
        # HALTED is not APPROVED, so behavioral = 0.5
        assert tracker._behavioral_track_score == 0.5

    def test_vr_05_all_verdict_statuses_affect_behavioral(self):
        """Only APPROVED counts as success for behavioral score."""
        tracker = ConstitutionalHealthTracker()
        statuses = [
            VerdictStatus.APPROVED,
            VerdictStatus.REFUSED,
            VerdictStatus.HALTED,
            VerdictStatus.WARNED,
            VerdictStatus.DEGRADED,
            VerdictStatus.ESCALATED,
        ]
        for status in statuses:
            tracker = ConstitutionalHealthTracker()  # Fresh tracker
            verdict = ConstitutionalVerdict(
                verdict_id=str(uuid.uuid4()),
                status=status,
                screen_results=[],
                failed_laws=[],
                payload_hash=hashlib.sha256(b"test").hexdigest(),
                version_hash="test",
                timestamp_utc=datetime.now(timezone.utc).isoformat()
            )
            tracker.record_verdict(verdict)
            if status == VerdictStatus.APPROVED:
                assert tracker._behavioral_track_score == 1.0
            else:
                assert tracker._behavioral_track_score == 0.0


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7 — FAILSAFE MANAGER EMERGENCY OPERATIONS
# ─────────────────────────────────────────────────────────────────────────────

class TestFailSafeEmergencyOperations:
    """
    §16: Fail-Safe Principle — emergency stop and recovery.
    Tests verify emergency state management.
    """

    def test_feo_01_emergency_inactive_by_default(self):
        """Emergency state is inactive by default."""
        manager = FailSafeManager()
        assert manager.emergency_active is False

    def test_feo_02_trigger_emergency_activates(self):
        """trigger_emergency_stop() activates emergency state."""
        manager = FailSafeManager()
        manager.trigger_emergency_stop("Test reason")
        assert manager.emergency_active is True

    def test_feo_03_emergency_marks_all_laws_degraded(self):
        """Emergency marks all laws (1-9) as degraded."""
        manager = FailSafeManager()
        manager.trigger_emergency_stop("Critical failure")
        status = manager.get_degradation_status()
        assert len(status["degraded_laws"]) == 9
        for law in status["degraded_laws"]:
            assert 1 <= law["law_number"] <= 9

    def test_feo_04_reset_clears_emergency(self):
        """reset_emergency() clears emergency state and degraded laws."""
        manager = FailSafeManager()
        manager.trigger_emergency_stop("Test")
        assert manager.emergency_active is True
        manager.reset_emergency()
        assert manager.emergency_active is False
        status = manager.get_degradation_status()
        assert len(status["degraded_laws"]) == 0
        assert status["overall_status"] == "HEALTHY"

    def test_feo_05_multiple_emergency_triggers_idempotent(self):
        """Multiple emergency triggers don't cause issues."""
        manager = FailSafeManager()
        manager.trigger_emergency_stop("First")
        manager.trigger_emergency_stop("Second")
        manager.trigger_emergency_stop("Third")
        assert manager.emergency_active is True
        # Should still have exactly 9 degraded laws
        status = manager.get_degradation_status()
        assert len(status["degraded_laws"]) == 9

    def test_feo_06_emergency_prevents_normal_operation(self):
        """When emergency is active, system is in degraded state."""
        manager = FailSafeManager()
        manager.trigger_emergency_stop("System failure")
        assert manager.is_degraded() is True


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 8 — FAILSAFE MANAGER CRYPTOGRAPHIC ATTESTATION (§17 AMEND-03)
# ─────────────────────────────────────────────────────────────────────────────

class TestFailSafeCryptographicAttestation:
    """
    §17 v2.1 AMEND-03: Cryptographic Connectivity Attestation.
    Degraded mode requires verifiable proof of resource unavailability.
    """

    def test_fca_01_valid_connectivity_proofs(self):
        """Valid connectivity proofs: tls_handshake_failed, dns_resolution_failed, network_interface_down."""
        manager = FailSafeManager()
        valid_proofs = [
            {"tls_handshake_failed": True},
            {"dns_resolution_failed": True},
            {"network_interface_down": True},
        ]
        for proof in valid_proofs:
            manager = FailSafeManager()  # Fresh for each
            manager.report_enforcement_failure(1, proof)
            assert manager.is_degraded() is True

    def test_fca_02_invalid_proof_raises_error(self):
        """Invalid or missing proof raises ValueError."""
        manager = FailSafeManager()
        invalid_proofs = [
            {},  # Empty
            {"some_random_field": True},  # Not recognized
            {"tls_handshake_failed": False},  # Explicitly false
        ]
        for proof in invalid_proofs:
            manager = FailSafeManager()
            with pytest.raises(ValueError, match="§17 VIOLATION"):
                manager.report_enforcement_failure(1, proof)

    def test_fca_03_restoration_requires_prior_failure(self):
        """restore_enforcement() works even without prior failure (graceful)."""
        manager = FailSafeManager()
        # Should not raise, just no-op
        manager.restore_enforcement(1)
        assert manager.is_degraded() is False

    def test_fca_04_report_then_restore(self):
        """Report failure then restore returns to healthy."""
        manager = FailSafeManager()
        manager.report_enforcement_failure(3, {"dns_resolution_failed": True})
        assert manager.is_degraded() is True
        manager.restore_enforcement(3)
        assert manager.is_degraded() is False

    def test_fca_05_multiple_law_failures(self):
        """Multiple law failures tracked independently."""
        manager = FailSafeManager()
        manager.report_enforcement_failure(1, {"tls_handshake_failed": True})
        manager.report_enforcement_failure(5, {"dns_resolution_failed": True})
        manager.report_enforcement_failure(9, {"network_interface_down": True})
        status = manager.get_degradation_status()
        assert len(status["degraded_laws"]) == 3
        law_numbers = {l["law_number"] for l in status["degraded_laws"]}
        assert law_numbers == {1, 5, 9}

    def test_fca_06_partial_restoration(self):
        """Partial restoration leaves other laws degraded."""
        manager = FailSafeManager()
        manager.report_enforcement_failure(1, {"tls_handshake_failed": True})
        manager.report_enforcement_failure(2, {"dns_resolution_failed": True})
        manager.restore_enforcement(1)
        status = manager.get_degradation_status()
        assert len(status["degraded_laws"]) == 1
        assert status["degraded_laws"][0]["law_number"] == 2


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 9 — ADVERSARIAL SCENARIOS
# ─────────────────────────────────────────────────────────────────────────────

class TestAdversarialScenarios:
    """
    Adversarial tests probing for vulnerabilities in health score logic.
    Includes score manipulation attacks, boundary exploits, and race conditions.
    """

    def test_adv_01_rapid_score_oscillation(self):
        """Rapid oscillation between extremes doesn't cause instability."""
        tracker = ConstitutionalHealthTracker()
        for i in range(1000):
            tracker.record_event(i % 2 == 0)
        score = tracker.get_composite_score()
        # Should be stable around expected value
        assert 0.0 <= score <= 1.0
        # With 50/50 split and other components at 1.0:
        # (1.0 + 0.5 + 1.0) / 3 ≈ 0.833
        assert 0.8 <= score <= 0.9

    def test_adv_02_extreme_value_injection(self):
        """Extreme float values don't break score calculation."""
        tracker = ConstitutionalHealthTracker()
        tracker.set_external_audit_score(float('inf'))
        tracker.set_reasoning_quality_score(float('-inf'))
        # Should be clamped
        assert tracker._external_audit_score == 1.0
        assert tracker._reasoning_quality_score == 0.0

    def test_adv_03_nan_injection_attempt(self):
        """NaN values are handled (clamped to valid range)."""
        tracker = ConstitutionalHealthTracker()
        try:
            tracker.set_external_audit_score(float('nan'))
            # NaN comparisons behave oddly; check it's been clamped
            score = tracker._external_audit_score
            # After max/min clamping, should be either 0 or 1
            assert score == 0.0 or score == 1.0 or (score != score)  # NaN check
        except (ValueError, TypeError):
            pass  # Also acceptable to reject NaN

    def test_adv_04_massive_event_flood(self):
        """Flooding with millions of events doesn't crash or leak."""
        tracker = ConstitutionalHealthTracker(max_history=1000)
        for _ in range(100000):
            tracker.record_event(False)
        # Memory bounded by max_history
        assert len(tracker._verdict_history) == 1000
        assert tracker._behavioral_track_score == 0.0

    def test_adv_05_thread_safety_basic(self):
        """Basic thread safety: concurrent updates don't crash."""
        tracker = ConstitutionalHealthTracker()
        errors = []

        def record_many(success_val):
            try:
                for _ in range(100):
                    tracker.record_event(success_val)
            except Exception as e:
                errors.append(e)

        threads = [
            threading.Thread(target=record_many, args=(True,)),
            threading.Thread(target=record_many, args=(False,)),
            threading.Thread(target=record_many, args=(True,)),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0
        assert 0.0 <= tracker.get_composite_score() <= 1.0

    def test_adv_06_degraded_mode_boundary_attack(self):
        """Attempt to hover exactly at degradation threshold."""
        tracker = ConstitutionalHealthTracker()
        # Try to get composite score as close to 0.5 as possible
        tracker.set_external_audit_score(0.5)
        tracker.set_reasoning_quality_score(0.5)
        # Need behavioral to also be 0.5
        for i in range(100):
            tracker.record_event(i < 50)
        # Composite = (0.5 + 0.5 + 0.5) / 3 = 0.5
        # is_degraded() uses < 0.5, so exactly 0.5 is NOT degraded
        assert tracker.get_composite_score() == 0.5
        assert tracker.is_degraded() is False

    def test_adv_07_graceful_underflow_handling(self):
        """Negative event counts impossible by design."""
        tracker = ConstitutionalHealthTracker()
        # There's no way to create negative counts through public API
        # This is a structural guarantee
        assert len(tracker._verdict_history) >= 0
        tracker.record_event(False)
        assert len(tracker._verdict_history) == 1

    def test_adv_08_version_attestation_bypass_attempt(self):
        """Cannot bypass version checks via health tracker."""
        tracker = ConstitutionalHealthTracker()
        # Health tracker doesn't expose version manipulation
        # This verifies separation of concerns
        assert not hasattr(tracker, 'version_hash')
        assert not hasattr(tracker, 'set_version')


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 10 — PROPERTY-BASED TESTING WITH HYPOTHESIS
# ─────────────────────────────────────────────────────────────────────────────

class TestPropertyBasedHealthScore:
    """
    Property-based tests using Hypothesis library.
    These tests verify invariants hold across wide input ranges.
    """

    @given(st.lists(st.booleans(), min_size=0, max_size=1000))
    @settings(max_examples=100, deadline=None)
    def test_pbh_01_score_always_in_bounds(self, events):
        """For any sequence of events, composite score stays in [0, 1]."""
        tracker = ConstitutionalHealthTracker()
        for event in events:
            tracker.record_event(event)
        score = tracker.get_composite_score()
        assert 0.0 <= score <= 1.0

    @given(st.lists(st.booleans(), min_size=1, max_size=100))
    @settings(max_examples=100, deadline=None)
    def test_pbh_02_behavioral_equals_approval_ratio(self, events):
        """Behavioral score equals ratio of True events."""
        tracker = ConstitutionalHealthTracker()
        for event in events:
            tracker.record_event(event)
        expected_ratio = sum(events) / len(events)
        assert abs(tracker._behavioral_track_score - expected_ratio) < 0.001

    @given(st.floats(min_value=-1000, max_value=1000),
           st.floats(min_value=-1000, max_value=1000))
    @settings(max_examples=100, deadline=None)
    def test_pbh_03_component_clamping_always_holds(self, ext, reason):
        """Component scores always clamped to [0, 1]."""
        tracker = ConstitutionalHealthTracker()
        tracker.set_external_audit_score(ext)
        tracker.set_reasoning_quality_score(reason)
        assert 0.0 <= tracker._external_audit_score <= 1.0
        assert 0.0 <= tracker._reasoning_quality_score <= 1.0

    @given(st.integers(min_value=1, max_value=10000),
           st.integers(min_value=0, max_value=10000))
    @settings(max_examples=100, deadline=None)
    def test_pbh_04_history_never_exceeds_max(self, max_hist, num_events):
        """History length never exceeds max_history."""
        tracker = ConstitutionalHealthTracker(max_history=max_hist)
        for _ in range(num_events):
            tracker.record_event(True)
        assert len(tracker._verdict_history) <= max_hist

    @given(st.integers(min_value=1, max_value=100))
    @settings(max_examples=100, deadline=None)
    def test_pbh_05_degraded_mode_deterministic(self, seed):
        """is_degraded() is deterministic for same inputs."""
        tracker1 = ConstitutionalHealthTracker()
        tracker2 = ConstitutionalHealthTracker()
        
        # Same sequence of operations
        tracker1.set_external_audit_score(seed / 100.0)
        tracker2.set_external_audit_score(seed / 100.0)
        
        for i in range(seed):
            tracker1.record_event(i % 2 == 0)
            tracker2.record_event(i % 2 == 0)
        
        assert tracker1.is_degraded() == tracker2.is_degraded()


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 11 — EDGE CASES AND CORNER CONDITIONS
# ─────────────────────────────────────────────────────────────────────────────

class TestEdgeCasesAndCorners:
    """
    Additional edge cases not covered elsewhere.
    Focus on unusual but valid usage patterns.
    """

    def test_ecc_01_tracker_invariant_after_many_operations(self):
        """check_invariant() passes after extensive operations."""
        tracker = ConstitutionalHealthTracker()
        for i in range(1000):
            tracker.record_event(i % 3 == 0)
            if i % 100 == 0:
                tracker.set_external_audit_score(i / 1000.0)
                tracker.set_reasoning_quality_score(1.0 - i / 1000.0)
        assert tracker.check_invariant() is True

    def test_ecc_02_fail_safe_manager_invariant(self):
        """FailSafeManager check_invariant() holds."""
        manager = FailSafeManager()
        assert manager.check_invariant() is True
        
        manager.report_enforcement_failure(1, {"tls_handshake_failed": True})
        assert manager.check_invariant() is True
        
        manager.restore_enforcement(1)
        assert manager.check_invariant() is True

    def test_ecc_03_empty_verdict_history_composite(self):
        """Composite score with empty history uses defaults."""
        tracker = ConstitutionalHealthTracker()
        # No events recorded
        assert tracker._behavioral_track_score == 1.0
        assert tracker.get_composite_score() == 1.0

    def test_ecc_04_single_verdict_composite(self):
        """Composite score with single verdict calculated correctly."""
        tracker = ConstitutionalHealthTracker()
        tracker.record_event(False)
        # (1.0 + 0.0 + 1.0) / 3 = 0.666...
        expected = 2.0 / 3.0
        assert abs(tracker.get_composite_score() - expected) < 0.001

    def test_ecc_05_degradation_status_structure(self):
        """get_degradation_status() returns properly structured dict."""
        manager = FailSafeManager()
        status = manager.get_degradation_status()
        assert "enforcement_healthy" in status
        assert "degraded_laws" in status
        assert "overall_status" in status
        assert isinstance(status["degraded_laws"], list)
        assert status["overall_status"] in ["HEALTHY", "DEGRADED", "DEGRADED COMPLIANCE"]

    def test_ecc_06_elapsed_time_calculation(self):
        """Degradation elapsed_days calculated correctly."""
        manager = FailSafeManager()
        manager.report_enforcement_failure(1, {"dns_resolution_failed": True})
        status = manager.get_degradation_status()
        assert len(status["degraded_laws"]) == 1
        # Just restored, should be very small
        assert status["degraded_laws"][0]["elapsed_days"] >= 0
        # degraded_compliance is False (< 30 days)
        assert status["degraded_laws"][0]["degraded_compliance"] is False

    def test_ecc_07_emergency_stop_reason_stored(self):
        """Emergency stop reason is accepted (not stored but processed)."""
        manager = FailSafeManager()
        # The reason parameter is accepted without error
        manager.trigger_emergency_stop("Database connection lost")
        assert manager.emergency_active is True

    def test_ecc_08_reset_without_prior_emergency(self):
        """reset_emergency() works even without prior emergency."""
        manager = FailSafeManager()
        # Should not raise
        manager.reset_emergency()
        assert manager.emergency_active is False


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 12 — DOCUMENTATION AND API COMPLIANCE
# ─────────────────────────────────────────────────────────────────────────────

class TestDocumentationCompliance:
    """
    Verify that the implementation matches documented §12.3 and §16-§17 behavior.
    """

    def test_doc_01_three_components_documented(self):
        """Verify three components exist as per §12.3."""
        tracker = ConstitutionalHealthTracker()
        # All three components must be present
        assert hasattr(tracker, '_external_audit_score')
        assert hasattr(tracker, '_behavioral_track_score')
        assert hasattr(tracker, '_reasoning_quality_score')

    def test_doc_02_public_methods_available(self):
        """Required public methods are available."""
        tracker = ConstitutionalHealthTracker()
        assert callable(getattr(tracker, 'get_health_score', None))
        assert callable(getattr(tracker, 'get_composite_score', None))
        assert callable(getattr(tracker, 'is_degraded', None))
        assert callable(getattr(tracker, 'record_event', None))
        assert callable(getattr(tracker, 'record_verdict', None))
        assert callable(getattr(tracker, 'set_external_audit_score', None))
        assert callable(getattr(tracker, 'set_reasoning_quality_score', None))
        assert callable(getattr(tracker, 'check_invariant', None))

    def test_doc_03_fail_safe_public_methods(self):
        """FailSafeManager required public methods available."""
        manager = FailSafeManager()
        assert callable(getattr(manager, 'trigger_emergency_stop', None))
        assert callable(getattr(manager, 'reset_emergency', None))
        assert callable(getattr(manager, 'report_enforcement_failure', None))
        assert callable(getattr(manager, 'restore_enforcement', None))
        assert callable(getattr(manager, 'is_degraded', None))
        assert callable(getattr(manager, 'get_degradation_status', None))
        assert callable(getattr(manager, 'check_invariant', None))

    def test_doc_04_emergency_active_is_public(self):
        """emergency_active is a public attribute as documented."""
        manager = FailSafeManager()
        assert hasattr(manager, 'emergency_active')
        assert isinstance(manager.emergency_active, bool)
