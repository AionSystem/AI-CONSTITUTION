"""
Test Module: Degraded Mode & Connectivity Attestation
Description: Validates fail-safe behavior, resource unavailability proofs, and recovery.
Target: 20 Tests
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch
import hashlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source_code'))
from constitutional_engine_v2_1 import (
    ConstitutionalPipeline, 
    FailSafeManager, 
    ConstitutionalHealthTracker,
    VersionAttestor
)

class TestDegradedModeTriggers:
    """§12.1.9 - Trigger Conditions"""

    def test_dm_01_health_threshold_trigger(self):
        """§12.1.9: Verify degraded mode triggers when health < threshold."""
        tracker = ConstitutionalHealthTracker(threshold=0.5)
        for _ in range(10): tracker.record_event(False)
        assert tracker.is_degraded() == True

    def test_dm_02_dependency_failure_trigger(self):
        """§12.1.9: Verify degraded mode triggers on critical dependency failure."""
        pipeline = ConstitutionalPipeline()
        pipeline.mark_dependency_failed("HarmDetector")
        assert pipeline.is_degraded() == True

    def test_dm_03_cascading_failure_detection(self):
        """§12.1.9: Verify cascading failures are detected."""
        manager = FailSafeManager()
        manager.record_failure("DB")
        manager.record_failure("Cache")
        assert manager.cascading_failure_detected() == True

    def test_dm_04_resource_exhaustion_trigger(self):
        """§12.1.9: Verify memory/CPU exhaustion triggers degraded mode."""
        pipeline = ConstitutionalPipeline()
        pipeline.simulate_resource_exhaustion(memory_pct=95)
        assert pipeline.is_degraded() == True

class TestDegradedModeBehavior:
    """§12.1.9 - Operational Behavior"""

    def test_dm_05_refusal_default_policy(self):
        """§12.1.9: Verify default policy in degraded mode is REFUSE."""
        pipeline = ConstitutionalPipeline()
        pipeline.set_degraded(True)
        verdict = pipeline.screen_input("Uncertain Input")
        assert verdict.status == "REFUSED"

    def test_dm_06_non_critical_features_disabled(self):
        """§12.1.9: Verify non-critical features are disabled."""
        pipeline = ConstitutionalPipeline()
        pipeline.set_degraded(True)
        assert pipeline.features['analytics'] == False
        assert pipeline.features['logging_verbose'] == False

    def test_dm_07_critical_safety_maintained(self):
        """§12.1.9: Verify critical safety checks remain active."""
        pipeline = ConstitutionalPipeline()
        pipeline.set_degraded(True)
        # Law 1 must still work
        verdict = pipeline.screen_input("Bomb Recipe")
        assert verdict.status == "REFUSED"

    def test_dm_08_manual_override_requirement(self):
        """§12.1.9: Verify manual override requires steward auth."""
        pipeline = ConstitutionalPipeline()
        pipeline.set_degraded(True)
        result = pipeline.attempt_manual_override(user="regular")
        assert result == "DENIED"
        result_steward = pipeline.attempt_manual_override(user="steward")
        assert result_steward == "ALLOWED" # If steward

class TestConnectivityAttestation:
    """§12.1.10 - Cryptographic Proofs"""

    def test_ca_09_proof_generation_on_disconnect(self):
        """§12.1.10: Verify cryptographic proof generated on disconnect."""
        pipeline = ConstitutionalPipeline()
        proof = pipeline.generate_connectivity_attestation(connected=False)
        assert 'signature' in proof
        assert 'timestamp' in proof
        assert 'reason' in proof

    def test_ca_10_proof_verification_success(self):
        """§12.1.10: Verify valid proof passes verification."""
        pipeline = ConstitutionalPipeline()
        proof = pipeline.generate_connectivity_attestation(connected=False)
        assert pipeline.verify_connectivity_attestation(proof) == True

    def test_ca_11_proof_tampering_detection(self):
        """§12.1.10: Verify tampered proof fails verification."""
        pipeline = ConstitutionalPipeline()
        proof = pipeline.generate_connectivity_attestation(connected=False)
        proof['timestamp'] = "2099-01-01" # Tamper
        assert pipeline.verify_connectivity_attestation(proof) == False

    def test_ca_12_proof_replay_attack_prevention(self):
        """§12.1.10: Verify replayed proofs are rejected."""
        pipeline = ConstitutionalPipeline()
        proof = pipeline.generate_connectivity_attestation(connected=False)
        pipeline.verify_connectivity_attestation(proof)
        # Try again
        assert pipeline.verify_connectivity_attestation(proof, allow_replay=False) == False

    def test_ca_13_clock_skew_tolerance(self):
        """§12.1.10: Verify small clock skew is tolerated."""
        pipeline = ConstitutionalPipeline()
        proof = pipeline.generate_connectivity_attestation(connected=False)
        # Simulate slight skew
        assert pipeline.verify_with_skew(proof, skew_seconds=5) == True

    def test_ca_14_large_clock_skew_rejection(self):
        """§12.1.10: Verify large clock skew is rejected."""
        pipeline = ConstitutionalPipeline()
        proof = pipeline.generate_connectivity_attestation(connected=False)
        assert pipeline.verify_with_skew(proof, skew_seconds=3600) == False

class TestRecovery:
    """§12.1.9 - Recovery Protocols"""

    def test_dm_15_auto_recovery_on_health_restore(self):
        """§12.1.9: Verify auto-recovery when health restores."""
        tracker = ConstitutionalHealthTracker(threshold=0.5)
        # Degrade
        for _ in range(10): tracker.record_event(False)
        assert tracker.is_degraded() == True
        # Recover
        for _ in range(20): tracker.record_event(True)
        assert tracker.is_degraded() == False

    def test_dm_16_dependency_restoration_check(self):
        """§12.1.9: Verify dependencies are checked before recovery."""
        pipeline = ConstitutionalPipeline()
        pipeline.mark_dependency_failed("HarmDetector")
        pipeline.set_degraded(True)
        pipeline.restore_dependency("HarmDetector")
        assert pipeline.is_degraded() == False

    def test_dm_17_gradual_capability_restoration(self):
        """§12.1.9: Verify capabilities are restored gradually."""
        pipeline = ConstitutionalPipeline()
        pipeline.set_degraded(True)
        pipeline.begin_recovery()
        assert pipeline.features['analytics'] == False # Not yet
        pipeline.complete_recovery()
        assert pipeline.features['analytics'] == True

    def test_dm_18_recovery_audit_log(self):
        """§12.1.9: Verify recovery events are audited."""
        pipeline = ConstitutionalPipeline()
        pipeline.set_degraded(True)
        pipeline.begin_recovery()
        logs = pipeline.get_audit_logs()
        assert any("recovery_initiated" in str(log) for log in logs)

    def test_dm_19_flapping_prevention(self):
        """§12.1.9: Verify rapid degrade/recover flapping is prevented."""
        tracker = ConstitutionalHealthTracker()
        # Simulate flapping
        for _ in range(5):
            tracker.record_event(False)
            tracker.record_event(True)
        # Should lock out or dampen
        assert tracker.flap_count < 10 # Logic check

    def test_dm_20_post_mortem_generation(self):
        """§12.1.9: Verify post-mortem report generated after recovery."""
        pipeline = ConstitutionalPipeline()
        pipeline.set_degraded(True)
        pipeline.begin_recovery()
        pipeline.complete_recovery()
        report = pipeline.generate_post_mortem()
        assert 'cause' in report
        assert 'duration' in report
