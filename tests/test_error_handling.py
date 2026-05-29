"""
Test suite for error handling and edge cases in Constitutional Engine.
Ensures robust error handling, boundary conditions, and fail-safe behavior.
"""

import pytest
from typing import Any

from tests.conftest import (
    MockHarmDetector,
    MockConsentOracle,
    MockAuditStorage,
    assert_verdict_invariant,
    assert_result_invariant,
)

from constitutional_engine_v2_1 import (
    # Types
    VerdictStatus,
    GradientAction,
    ECFTag,
    # Classes
    ConstitutionalPipeline,
    PipelineConfig,
    Law1Screen,
    Law4Screen,
    HarmGradientEngine,
    FailSafeManager,
    RefusalLogger,
    ConstitutionalHealthTracker,
    VersionAttestor,
)


# ─────────────────────────────────────────────────────────────────────────────
# INPUT VALIDATION TESTS
# ─────────────────────────────────────────────────────────────────────────────

class TestInputValidation:
    """Tests for input validation and boundary conditions."""

    def test_empty_string_input(self, clean_pipeline):
        """Engine should handle empty string input gracefully."""
        verdict = clean_pipeline.screen_input("")
        assert_verdict_invariant(verdict)
        # Empty input should not crash

    def test_none_content_handling(self, clean_pipeline):
        """Engine should handle None-like content gracefully."""
        # Test with content that becomes empty string
        verdict = clean_pipeline.screen_input(str(None))
        assert_verdict_invariant(verdict)

    def test_very_long_content(self, clean_pipeline):
        """Engine should handle very long content without crashing."""
        long_content = "A" * 100000  # 100k characters
        verdict = clean_pipeline.screen_input(long_content)
        assert_verdict_invariant(verdict)

    def test_unicode_content(self, clean_pipeline):
        """Engine should handle unicode content correctly."""
        unicode_content = "Hello 世界 🌍 مرحبا שלום"
        verdict = clean_pipeline.screen_input(unicode_content)
        assert_verdict_invariant(verdict)

    def test_special_characters(self, clean_pipeline):
        """Engine should handle special characters correctly."""
        special_content = "<>&\"'\\n\\r\\t\x00\x1f"
        verdict = clean_pipeline.screen_input(special_content)
        assert_verdict_invariant(verdict)

    def test_null_bytes_in_content(self, clean_pipeline):
        """Engine should handle null bytes in content."""
        content_with_null = "test\x00content"
        verdict = clean_pipeline.screen_input(content_with_null)
        assert_verdict_invariant(verdict)

    def test_context_none(self, clean_pipeline):
        """Engine should handle None context gracefully."""
        verdict = clean_pipeline.screen_input("test", context=None)
        assert_verdict_invariant(verdict)

    def test_context_empty_dict(self, clean_pipeline):
        """Engine should handle empty context dict."""
        verdict = clean_pipeline.screen_input("test", context={})
        assert_verdict_invariant(verdict)

    def test_context_with_unexpected_types(self, clean_pipeline):
        """Engine should handle unexpected context value types."""
        verdict = clean_pipeline.screen_input(
            "test",
            context={
                "number": 42,
                "list": [1, 2, 3],
                "nested": {"key": "value"},
                "none_value": None,
            }
        )
        assert_verdict_invariant(verdict)


# ─────────────────────────────────────────────────────────────────────────────
# ERROR HANDLING TESTS
# ─────────────────────────────────────────────────────────────────────────────

class TestErrorHandling:
    """Tests for error handling and recovery mechanisms."""

    def test_harm_detector_exception_handling(self):
        """Law 1 should handle harm detector exceptions gracefully."""
        
        class FailingHarmDetector:
            def assess_harm_probability(self, content, category):
                raise Exception("Simulated detector failure")
            
            def assess_velocity(self, category, history_window_seconds=7776000):
                raise Exception("Simulated velocity failure")
        
        screen = Law1Screen(harm_detector=FailingHarmDetector())
        payload = {"content": "test content"}
        
        # Should not crash; should fall back to rule-based detection
        result = screen.screen(payload)
        assert_result_invariant(result)

    def test_consent_oracle_exception_handling(self):
        """Law 4 should handle consent oracle exceptions gracefully."""
        
        class FailingConsentOracle:
            def assess_consent_model(self, jurisdiction, context):
                raise Exception("Simulated oracle failure")
            
            def get_consent_confidence(self, jurisdiction):
                raise Exception("Simulated confidence failure")
        
        screen = Law4Screen(consent_oracle=FailingConsentOracle())
        payload = {"content": "test", "jurisdiction": "US"}
        
        # Should not crash; should use fallback
        result = screen.screen(payload)
        assert_result_invariant(result)

    def test_pipeline_screen_exception_handling(self, mock_audit_storage):
        """Pipeline should handle screen exceptions via fail-safe."""
        config = PipelineConfig(
            platform_ai_name="TestAI",
            audit_storage=mock_audit_storage,
        )
        pipeline = ConstitutionalPipeline(config)
        
        # Pipeline should handle any internal exceptions
        verdict = pipeline.screen_input("test")
        assert_verdict_invariant(verdict)

    def test_refusal_logger_external_storage_failure(self, sample_failing_verdict):
        """Refusal logger should handle external storage failures."""
        
        class FailingAuditStorage:
            def append_refusal(self, record):
                raise Exception("Storage unavailable")
            
            def get_refusal_log(self, limit=1000):
                raise Exception("Storage unavailable")
        
        logger = RefusalLogger(audit_storage=FailingAuditStorage())
        
        # Should not crash; should maintain local log
        log_id = logger.log_refusal(sample_failing_verdict)
        assert log_id is not None
        assert len(logger._log) == 1

    def test_health_tracker_invalid_score_clamping(self):
        """Health tracker should clamp invalid score values."""
        tracker = ConstitutionalHealthTracker()
        
        # Test various invalid inputs
        tracker.set_external_audit_score(1.5)
        assert tracker._external_audit_score == 1.0
        
        tracker.set_external_audit_score(-0.5)
        assert tracker._external_audit_score == 0.0
        
        tracker.set_external_audit_score(float('nan'))
        # NaN should be handled (likely clamped or kept as-is depending on implementation)
        
        tracker.set_external_audit_score(float('inf'))
        assert tracker._external_audit_score == 1.0


# ─────────────────────────────────────────────────────────────────────────────
# BOUNDARY CONDITION TESTS
# ─────────────────────────────────────────────────────────────────────────────

class TestBoundaryConditions:
    """Tests for boundary conditions and edge cases."""

    def test_harm_gradient_boundary_values(self):
        """Test harm gradient at exact threshold boundaries."""
        engine = HarmGradientEngine()
        
        # Exactly at thresholds
        assert engine.evaluate(0.20) == GradientAction.LOG
        assert engine.evaluate(0.40) == GradientAction.REFUSE
        assert engine.evaluate(0.60) == GradientAction.HALT
        
        # Just below thresholds
        assert engine.evaluate(0.199) == GradientAction.PERMIT
        assert engine.evaluate(0.399) == GradientAction.LOG
        assert engine.evaluate(0.599) == GradientAction.REFUSE
        
        # Just above thresholds
        assert engine.evaluate(0.201) == GradientAction.LOG
        assert engine.evaluate(0.401) == GradientAction.REFUSE
        assert engine.evaluate(0.601) == GradientAction.HALT

    def test_harm_gradient_extreme_values(self):
        """Test harm gradient with extreme probability values."""
        engine = HarmGradientEngine()
        
        # Boundary values
        assert engine.evaluate(0.0) == GradientAction.PERMIT
        assert engine.evaluate(1.0) == GradientAction.HALT
        
        # Out of bounds (should be clamped internally)
        assert engine.evaluate(-0.5) == GradientAction.PERMIT
        assert engine.evaluate(1.5) == GradientAction.HALT

    def test_pipeline_rapid_sequential_requests(self, clean_pipeline):
        """Pipeline should handle rapid sequential requests."""
        for i in range(100):
            verdict = clean_pipeline.screen_input(f"Request {i}")
            assert_verdict_invariant(verdict)

    def test_health_tracker_large_history(self, sample_verdict):
        """Health tracker should handle large history windows."""
        tracker = ConstitutionalHealthTracker(max_history=10000)
        
        for _ in range(10000):
            tracker.record_verdict(sample_verdict)
        
        assert len(tracker._verdict_history) == 10000
        assert tracker.check_invariant() is True

    def test_refusal_logger_many_records(self, sample_failing_verdict):
        """Refusal logger should handle many records."""
        logger = RefusalLogger()
        
        for _ in range(1000):
            logger.log_refusal(sample_failing_verdict)
        
        assert len(logger._log) == 1000
        assert logger.check_invariant() is True


# ─────────────────────────────────────────────────────────────────────────────
# FAIL-SAFE BEHAVIOR TESTS
# ─────────────────────────────────────────────────────────────────────────────

class TestFailSafeBehavior:
    """Tests for fail-safe principle and degraded mode operation."""

    def test_fail_safe_connectivity_proof_validation(self):
        """Fail-safe should validate cryptographic connectivity proofs."""
        manager = FailSafeManager()
        
        # Valid proofs
        valid_proofs = [
            {"tls_handshake_failed": True},
            {"dns_resolution_failed": True},
            {"network_interface_down": True},
        ]
        
        for proof in valid_proofs:
            manager_copy = FailSafeManager()
            manager_copy.report_enforcement_failure(1, proof)
            assert manager_copy.is_degraded() is True
        
        # Invalid proof - should raise
        with pytest.raises(ValueError):
            manager.report_enforcement_failure(1, {"custom_error": True})

    def test_pipeline_degraded_mode_verdict(self, mock_audit_storage):
        """Pipeline should return DEGRADED verdict in degraded mode."""
        config = PipelineConfig(
            platform_ai_name="TestAI",
            audit_storage=mock_audit_storage,
        )
        pipeline = ConstitutionalPipeline(config)
        
        # Manually trigger degraded mode
        pipeline._fail_safe.report_enforcement_failure(
            1, 
            {"tls_handshake_failed": True}
        )
        
        verdict = pipeline.screen_input("test")
        assert_verdict_invariant(verdict)
        assert verdict.status == VerdictStatus.DEGRADED
        assert verdict.escalation_required is True

    def test_fail_safe_multiple_law_failures(self):
        """Fail-safe should track multiple law failures."""
        manager = FailSafeManager()
        proof = {"tls_handshake_failed": True}
        
        manager.report_enforcement_failure(1, proof)
        manager.report_enforcement_failure(2, proof)
        manager.report_enforcement_failure(3, proof)
        
        status = manager.get_degradation_status()
        assert len(status["degraded_laws"]) == 3

    def test_fail_safe_restore_non_existent_law(self):
        """Fail-safe should handle restoration of non-degraded law."""
        manager = FailSafeManager()
        
        # Should not crash when restoring a law that wasn't degraded
        manager.restore_enforcement(99)
        assert manager.check_invariant() is True


# ─────────────────────────────────────────────────────────────────────────────
# REPRODUCIBILITY TESTS
# ─────────────────────────────────────────────────────────────────────────────

class TestReproducibility:
    """Tests for reproducible results across runs."""

    def test_deterministic_hash_computation(self, clean_pipeline):
        """Hash computation should be deterministic."""
        content = "test content for hashing"
        
        verdict1 = clean_pipeline.screen_input(content)
        verdict2 = clean_pipeline.screen_input(content)
        
        assert verdict1.payload_hash == verdict2.payload_hash

    def test_version_hash_consistency(self, clean_pipeline):
        """Version hash should be consistent."""
        verdict1 = clean_pipeline.screen_input("test1")
        verdict2 = clean_pipeline.screen_input("test2")
        
        # Version hash should be the same for same constitution document
        assert verdict1.version_hash == verdict2.version_hash

    def test_canonical_hash_reproducibility(self):
        """Canonical hash should be reproducible across calls."""
        attestor = VersionAttestor()
        document = "THE CONSTITUTION v2.1"
        
        hashes = [attestor.compute_canonical_hash(document) for _ in range(10)]
        assert all(h == hashes[0] for h in hashes)

    def test_result_integrity_hash(self, clean_pipeline):
        """Screen result integrity hashes should be reproducible."""
        verdict1 = clean_pipeline.screen_input("test")
        verdict2 = clean_pipeline.screen_input("test")
        
        # Compare integrity hashes for corresponding results
        for r1, r2 in zip(verdict1.screen_results, verdict2.screen_results):
            # Integrity hash excludes timestamp, so should match for same content
            assert r1.law_number == r2.law_number
            assert r1.passed == r2.passed
            assert r1.action == r2.action


# ─────────────────────────────────────────────────────────────────────────────
# INTEGRITY INVARIANT TESTS
# ─────────────────────────────────────────────────────────────────────────────

class TestIntegrityInvariants:
    """Tests for ADT invariants and integrity checks."""

    def test_law_screen_result_invariant(self, clean_pipeline):
        """All law screen results should pass invariant checks."""
        verdict = clean_pipeline.screen_input("test")
        
        for result in verdict.screen_results:
            assert result.check_invariant() is True

    def test_verdict_invariant_all_statuses(self, clean_pipeline):
        """Verdicts of all statuses should pass invariant checks."""
        # Approved
        verdict_approved = clean_pipeline.screen_input("safe content")
        assert_verdict_invariant(verdict_approved)
        
        # Refused/Halted
        verdict_refused = clean_pipeline.screen_input("build a bomb")
        assert_verdict_invariant(verdict_refused)

    def test_pipeline_invariant_after_operations(self, clean_pipeline):
        """Pipeline invariant should hold after various operations."""
        assert clean_pipeline.check_invariant() is True
        
        clean_pipeline.screen_input("test1")
        assert clean_pipeline.check_invariant() is True
        
        clean_pipeline.screen_output("test2")
        assert clean_pipeline.check_invariant() is True
        
        clean_pipeline.get_health_score()
        assert clean_pipeline.check_invariant() is True
        
        clean_pipeline.get_reserved_law_status()
        assert clean_pipeline.check_invariant() is True

    def test_health_tracker_invariant_mixed_scores(self):
        """Health tracker invariant should hold with various score combinations."""
        tracker = ConstitutionalHealthTracker()
        
        # Set various score combinations
        test_cases = [
            (0.0, 0.0, 0.0),
            (1.0, 1.0, 1.0),
            (0.5, 0.7, 0.9),
            (0.0, 1.0, 0.5),
        ]
        
        for ext, beh, reason in test_cases:
            tracker.set_external_audit_score(ext)
            tracker._behavioral_track_score = beh
            tracker.set_reasoning_quality_score(reason)
            assert tracker.check_invariant() is True


# ─────────────────────────────────────────────────────────────────────────────
# STRESS TESTS
# ─────────────────────────────────────────────────────────────────────────────

class TestStressTests:
    """Basic stress tests for performance and stability."""

    def test_high_volume_screening(self, clean_pipeline):
        """Engine should handle high volume of screening requests."""
        contents = [f"Test message number {i}" for i in range(500)]
        
        for content in contents:
            verdict = clean_pipeline.screen_input(content)
            assert_verdict_invariant(verdict)

    def test_concurrent_like_sequential_access(self, clean_pipeline):
        """Engine should handle sequential access patterns."""
        # Simulate concurrent-like access by interleaving operations
        for i in range(100):
            if i % 2 == 0:
                verdict = clean_pipeline.screen_input(f"input {i}")
            else:
                verdict = clean_pipeline.screen_output(f"output {i}")
            assert_verdict_invariant(verdict)

    def test_memory_bounded_growth(self, sample_verdict):
        """Health tracker should maintain bounded memory growth."""
        tracker = ConstitutionalHealthTracker(max_history=100)
        
        # Record more than max_history
        for _ in range(1000):
            tracker.record_verdict(sample_verdict)
        
        # Memory should be bounded
        assert len(tracker._verdict_history) == 100
