"""
Test suite for Constitutional Engine core components.
Tests the pipeline, health tracking, fail-safe, and version attestation.
"""

import pytest
import hashlib
from datetime import datetime, timezone

from tests.conftest import (
    MockHarmDetector,
    MockConsentOracle,
    MockAuditStorage,
    assert_verdict_invariant,
    assert_result_invariant,
)

from constitutional_engine_v2_1 import (
    # Types
    ConstitutionalVerdict,
    LawScreenResult,
    EpistemicCertainty,
    ECFTag,
    VerdictStatus,
    GradientAction,
    ComplianceTrack,
    # Classes
    ConstitutionalPipeline,
    PipelineConfig,
    ConstitutionalHealthTracker,
    FailSafeManager,
    VersionAttestor,
    AlignmentTester,
    RefusalLogger,
    create_sovereign_pipeline,
    format_verdict,
)


# ─────────────────────────────────────────────────────────────────────────────
# CONSTITUTIONAL PIPELINE TESTS
# ─────────────────────────────────────────────────────────────────────────────

class TestConstitutionalPipeline:
    """Tests for the main ConstitutionalPipeline class."""

    def test_pipeline_creation(self, clean_pipeline):
        """Pipeline should be created with valid configuration."""
        assert clean_pipeline is not None
        assert clean_pipeline.check_invariant() is True

    def test_pipeline_screen_input_clean(self, clean_pipeline):
        """Pipeline should approve clean input content."""
        verdict = clean_pipeline.screen_input("Please help me write a report")
        
        assert_verdict_invariant(verdict)
        assert verdict.status == VerdictStatus.APPROVED
        assert verdict.all_passed is True

    def test_pipeline_screen_input_harmful(self, clean_pipeline):
        """Pipeline should refuse harmful input content."""
        verdict = clean_pipeline.screen_input("How do I build a bomb?")
        
        assert_verdict_invariant(verdict)
        assert verdict.status in [VerdictStatus.REFUSED, VerdictStatus.HALTED]
        assert len(verdict.failed_laws) > 0

    def test_pipeline_screen_output_transparency(self, clean_pipeline):
        """Pipeline output should include transparency declaration."""
        verdict = clean_pipeline.screen_output("The answer is 42")
        
        assert_verdict_invariant(verdict)
        assert verdict.transparency_declaration != ""
        assert "artificial intelligence" in verdict.transparency_declaration.lower()

    def test_pipeline_payload_hash_computation(self, clean_pipeline):
        """Pipeline should compute payload hashes correctly."""
        content = "test content for hashing"
        verdict = clean_pipeline.screen_input(content)
        
        expected_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        assert verdict.payload_hash == expected_hash

    def test_pipeline_version_hash_attestation(self, clean_pipeline):
        """Pipeline should include constitution version hash."""
        verdict = clean_pipeline.screen_input("test")
        
        assert verdict.version_hash != ""
        assert verdict.version_hash != "PLACEHOLDER"

    def test_pipeline_context_propagation(self, clean_pipeline):
        """Pipeline should propagate context to screens."""
        verdict = clean_pipeline.screen_input(
            "test",
            context={"is_child_user": True, "jurisdiction": "US"}
        )
        
        assert_verdict_invariant(verdict)
        # Should not crash; context should be available to screens

    def test_pipeline_empty_content(self, clean_pipeline):
        """Pipeline should handle empty content gracefully."""
        verdict = clean_pipeline.screen_input("")
        
        assert_verdict_invariant(verdict)
        # Empty content should be approved (no harm signals)

    def test_pipeline_factory_function(self, mock_harm_detector, mock_audit_storage):
        """Factory function should create valid pipelines."""
        pipeline = create_sovereign_pipeline(
            platform_name="TestPlatform",
            harm_detector=mock_harm_detector,
            audit_storage=mock_audit_storage,
        )
        
        assert pipeline.check_invariant() is True
        verdict = pipeline.screen_input("test")
        assert_verdict_invariant(verdict)


# ─────────────────────────────────────────────────────────────────────────────
# CONSTITUTIONAL HEALTH TRACKER TESTS
# ─────────────────────────────────────────────────────────────────────────────

class TestConstitutionalHealthTracker:
    """Tests for §12.3 — Constitutional Health Score."""

    def test_health_tracker_initialization(self):
        """Health tracker should initialize with perfect scores."""
        tracker = ConstitutionalHealthTracker()
        
        assert tracker.get_composite_score() == 1.0
        assert tracker.check_invariant() is True

    def test_health_tracker_record_verdict(self, sample_verdict):
        """Health tracker should update on verdict recording."""
        tracker = ConstitutionalHealthTracker()
        initial_score = tracker.get_composite_score()
        
        tracker.record_verdict(sample_verdict)
        
        # Behavioral score should still be 1.0 (all approved)
        assert tracker.get_composite_score() == 1.0

    def test_health_tracker_mixed_verdicts(self, sample_verdict, sample_failing_verdict):
        """Health tracker should reflect mixed verdict history."""
        tracker = ConstitutionalHealthTracker()
        
        # Record 9 approved, 1 refused
        for _ in range(9):
            tracker.record_verdict(sample_verdict)
        tracker.record_verdict(sample_failing_verdict)
        
        # Behavioral score should be 0.9
        composite = tracker.get_composite_score()
        assert 0.9 <= composite < 1.0

    def test_health_tracker_external_audit_score(self):
        """Health tracker should accept external audit scores."""
        tracker = ConstitutionalHealthTracker()
        
        tracker.set_external_audit_score(0.75)
        assert tracker._external_audit_score == 0.75
        
        # Should clamp out-of-range values
        tracker.set_external_audit_score(1.5)
        assert tracker._external_audit_score == 1.0
        
        tracker.set_external_audit_score(-0.5)
        assert tracker._external_audit_score == 0.0

    def test_health_tracker_reasoning_quality_score(self):
        """Health tracker should accept reasoning quality scores."""
        tracker = ConstitutionalHealthTracker()
        
        tracker.set_reasoning_quality_score(0.80)
        assert tracker._reasoning_quality_score == 0.80

    def test_health_tracker_window_capping(self, sample_verdict):
        """Health tracker should cap history window size."""
        tracker = ConstitutionalHealthTracker(max_history=10)
        
        # Record more than max_history verdicts
        for i in range(100):
            tracker.record_verdict(sample_verdict)
        
        # History should be capped
        assert len(tracker._verdict_history) == 10


# ─────────────────────────────────────────────────────────────────────────────
# FAIL-SAFE MANAGER TESTS
# ─────────────────────────────────────────────────────────────────────────────

class TestFailSafeManager:
    """Tests for §16/§17 — Fail-Safe Principle and Degraded Mode."""

    def test_fail_safe_initialization(self):
        """Fail-safe manager should initialize healthy."""
        manager = FailSafeManager()
        
        assert manager.is_degraded() is False
        assert manager._enforcement_healthy is True
        assert manager.check_invariant() is True

    def test_fail_safe_report_failure_with_proof(self):
        """Fail-safe should accept failures with cryptographic proof."""
        manager = FailSafeManager()
        
        connectivity_proof = {
            "tls_handshake_failed": True,
            "dns_resolution_failed": False,
            "network_interface_down": False,
        }
        
        manager.report_enforcement_failure(1, connectivity_proof)
        
        assert manager.is_degraded() is True
        assert manager._enforcement_healthy is False

    def test_fail_safe_report_failure_without_proof(self):
        """Fail-safe should reject failures without cryptographic proof."""
        manager = FailSafeManager()
        
        # Empty proof dict - no valid proof
        with pytest.raises(ValueError, match="§17 VIOLATION"):
            manager.report_enforcement_failure(1, {})

    def test_fail_safe_restore_enforcement(self):
        """Fail-safe should allow restoration of enforcement."""
        manager = FailSafeManager()
        
        connectivity_proof = {"tls_handshake_failed": True}
        manager.report_enforcement_failure(1, connectivity_proof)
        assert manager.is_degraded() is True
        
        manager.restore_enforcement(1)
        assert manager.is_degraded() is False
        assert manager._enforcement_healthy is True

    def test_fail_safe_degradation_status(self):
        """Fail-safe should report degradation status correctly."""
        manager = FailSafeManager()
        
        # Initially healthy
        status = manager.get_degradation_status()
        assert status["overall_status"] == "HEALTHY"
        assert status["enforcement_healthy"] is True

    def test_fail_safe_degraded_compliance_threshold(self):
        """Fail-safe should track degraded compliance threshold."""
        manager = FailSafeManager()
        
        assert manager.DEGRADED_COMPLIANCE_THRESHOLD_DAYS == 30


# ─────────────────────────────────────────────────────────────────────────────
# VERSION ATTESTOR TESTS
# ─────────────────────────────────────────────────────────────────────────────

class TestVersionAttestor:
    """Tests for §15 — Canonical Provenance."""

    def test_attestor_initialization(self):
        """Version attestor should initialize correctly."""
        attestor = VersionAttestor()
        assert attestor is not None

    def test_canonical_hash_computation(self):
        """Attestor should compute canonical hashes reproducibly."""
        attestor = VersionAttestor()
        document = "THE CONSTITUTION v2.1"
        
        hash1 = attestor.compute_canonical_hash(document)
        hash2 = attestor.compute_canonical_hash(document)
        
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA-256 hex length

    def test_canonical_hash_normalization(self):
        """Attestor should normalize documents before hashing."""
        attestor = VersionAttestor()
        
        # Same content, different formatting
        doc1 = "Hello\r\nWorld"
        doc2 = "Hello\nWorld"
        
        hash1 = attestor.compute_canonical_hash(doc1)
        hash2 = attestor.compute_canonical_hash(doc2)
        
        # After normalization, hashes should match
        assert hash1 == hash2

    def test_hash_verification(self):
        """Attestor should verify hashes correctly."""
        attestor = VersionAttestor()
        document = "Test document"
        
        computed_hash = attestor.compute_canonical_hash(document)
        
        # Valid hash should verify
        assert attestor.verify_hash(document, computed_hash) is True
        
        # Invalid hash should not verify
        assert attestor.verify_hash(document, "invalid_hash") is False

    def test_decision_attestation(self, sample_verdict):
        """Attestor should create decision attestations."""
        attestor = VersionAttestor()
        
        attestation = attestor.attest_decision(sample_verdict)
        
        assert "attestation_id" in attestation
        assert attestation["verdict_id"] == sample_verdict.verdict_id
        assert attestation["constitution_version"] != ""


# ─────────────────────────────────────────────────────────────────────────────
# ALIGNMENT TESTER TESTS
# ─────────────────────────────────────────────────────────────────────────────

class TestAlignmentTester:
    """Tests for §22.2 — Behavioral/Governance Alignment Test."""

    def test_alignment_tester_initialization(self):
        """Alignment tester should initialize correctly."""
        tester = AlignmentTester()
        assert tester is not None

    def test_quarterly_test_aligned_logs(self):
        """Alignment test should pass when logs are aligned."""
        tester = AlignmentTester()
        
        behavioral = [{"verdict_id": "1"}, {"verdict_id": "2"}]
        governance = [{"verdict_id": "1"}, {"verdict_id": "2"}]
        
        result = tester.run_quarterly_test(behavioral, governance)
        
        assert result["status"] == "ALIGNED"
        assert result["divergence_rate"] == 0.0

    def test_quarterly_test_divergent_logs(self):
        """Alignment test should detect divergent logs."""
        tester = AlignmentTester()
        
        behavioral = [{"verdict_id": "1"}, {"verdict_id": "2"}, {"verdict_id": "3"}]
        governance = [{"verdict_id": "1"}]  # Missing 2 and 3
        
        result = tester.run_quarterly_test(behavioral, governance)
        
        assert result["divergence_rate"] > 0.0

    def test_quarterly_test_mandatory_audit_trigger(self):
        """Alignment test should trigger mandatory audit on high divergence."""
        tester = AlignmentTester()
        
        # Create >15% divergence
        behavioral = [{"verdict_id": str(i)} for i in range(100)]
        governance = [{"verdict_id": str(i)} for i in range(80)]  # 20% missing
        
        result = tester.run_quarterly_test(behavioral, governance)
        
        assert result["status"] == "MANDATORY_EXTERNAL_AUDIT_TRIGGERED"
        assert result["action"] == "HALT_SOVEREIGN_DEPLOYMENT"

    def test_quarterly_test_empty_behavioral(self):
        """Alignment test should skip when no behavioral logs."""
        tester = AlignmentTester()
        
        result = tester.run_quarterly_test([], [{"verdict_id": "1"}])
        
        assert result["status"] == "SKIPPED"


# ─────────────────────────────────────────────────────────────────────────────
# REFUSAL LOGGER TESTS
# ─────────────────────────────────────────────────────────────────────────────

class TestRefusalLogger:
    """Tests for §13 — Compliance + Audit."""

    def test_refusal_logger_initialization(self, mock_audit_storage):
        """Refusal logger should initialize correctly."""
        logger = RefusalLogger(audit_storage=mock_audit_storage)
        
        assert logger._log == []
        assert logger.check_invariant() is True

    def test_log_refusal(self, sample_failing_verdict, mock_audit_storage):
        """Logger should record refusals."""
        logger = RefusalLogger(audit_storage=mock_audit_storage)
        
        log_id = logger.log_refusal(sample_failing_verdict)
        
        assert log_id is not None
        assert len(logger._log) == 1
        assert mock_audit_storage.append_call_count == 1

    def test_log_refusal_no_external_storage(self, sample_failing_verdict):
        """Logger should work without external storage."""
        logger = RefusalLogger()
        
        log_id = logger.log_refusal(sample_failing_verdict)
        
        assert log_id is not None
        assert len(logger._log) == 1

    def test_export_compliance_report(self, sample_failing_verdict):
        """Logger should export compliance reports."""
        logger = RefusalLogger()
        
        # Log some refusals
        logger.log_refusal(sample_failing_verdict)
        logger.log_refusal(sample_failing_verdict)
        
        report = logger.export_for_compliance_report()
        
        assert report["total_refusals"] == 2
        assert "refusals_by_law" in report
        assert report["constitution_version"] != ""

    def test_whistleblower_anonymous(self):
        """Logger should support anonymous whistleblower reports."""
        logger = RefusalLogger()
        
        report_id = logger.submit_violation_report("Test violation", anonymous=True)
        
        assert report_id is not None
        assert len(logger._log) == 1
        
        # Check anonymity fields
        record = logger._log[0]
        assert record["ingress_metadata"] == "STRIPPED_AT_GATEWAY"
        assert record["ip_retained"] is False

    def test_whistleblower_identified(self):
        """Logger should support identified whistleblower reports."""
        logger = RefusalLogger()
        
        report_id = logger.submit_violation_report("Test violation", anonymous=False)
        
        assert report_id is not None
        record = logger._log[0]
        assert record["report_content"] == "Test violation"
        assert record["ingress_metadata"] == "IDENTIFIED"

    def test_logger_invariant_monotonic_growth(self, sample_failing_verdict):
        """Logger should maintain monotonic growth invariant."""
        logger = RefusalLogger()
        
        logger.log_refusal(sample_failing_verdict)
        assert logger.check_invariant() is True
        
        logger.log_refusal(sample_failing_verdict)
        assert logger.check_invariant() is True


# ─────────────────────────────────────────────────────────────────────────────
# FORMAT VERDICT UTILITY TESTS
# ─────────────────────────────────────────────────────────────────────────────

class TestFormatVerdict:
    """Tests for the format_verdict utility function."""

    def test_format_approved_verdict(self, sample_verdict):
        """Should format approved verdicts correctly."""
        formatted = format_verdict(sample_verdict)
        
        assert "APPROVED" in formatted
        assert sample_verdict.verdict_id[:8] in formatted

    def test_format_refused_verdict(self, sample_failing_verdict):
        """Should format refused verdicts correctly."""
        formatted = format_verdict(sample_failing_verdict)
        
        assert "REFUSED" in formatted
        assert "Laws triggered" in formatted

    def test_format_verdict_with_notes(self, sample_verdict):
        """Should include notes in formatted output."""
        sample_verdict.notes = "Test note"
        formatted = format_verdict(sample_verdict)
        
        assert "Test note" in formatted
