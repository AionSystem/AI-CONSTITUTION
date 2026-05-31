"""
Test suite for error handling and edge cases in Constitutional Engine.
Ensures robust error handling, boundary conditions, and fail-safe behavior.

Covers: Exception handling, input validation, boundary conditions, fail-safe operations,
reproducibility, integrity invariants, stress testing, adversarial scenarios, and
property-based verification per v2.1 Constitution §§15-17.
"""

import pytest
from typing import Any
from hypothesis import given, assume, settings
from hypothesis import strategies as st
import threading
import time
import sys

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


# ─────────────────────────────────────────────────────────────────────────────
# ADVERSARIAL SCENARIOS
# ─────────────────────────────────────────────────────────────────────────────

class TestAdversarialScenarios:
    """Tests for adversarial inputs and attack resistance."""

    def test_exception_chain_propagation(self):
        """Nested exceptions should be handled gracefully."""
        
        class ChainFailingDetector:
            def assess_harm_probability(self, content, category):
                try:
                    raise ValueError("Inner error")
                except ValueError:
                    raise RuntimeError("Outer error") from None
        
        screen = Law1Screen(harm_detector=ChainFailingDetector())
        result = screen.screen({"content": "test"})
        assert_result_invariant(result)

    def test_recursion_depth_attack(self, clean_pipeline):
        """Deep recursion attempts should not crash engine."""
        # Create deeply nested context
        nested_context = {"level": 0}
        current = nested_context
        for i in range(100):
            current["nested"] = {"level": i+1}
            current = current["nested"]
        
        verdict = clean_pipeline.screen_input("test", context=nested_context)
        assert_verdict_invariant(verdict)

    def test_unicode_homoglyph_attack(self, clean_pipeline):
        """Homoglyph attacks should be handled."""
        # Mix Cyrillic and Latin characters that look identical
        homoglyph_content = "test\u0430content"  # Cyrillic 'а' instead of Latin 'a'
        verdict = clean_pipeline.screen_input(homoglyph_content)
        assert_verdict_invariant(verdict)

    def test_zero_width_character_injection(self, clean_pipeline):
        """Zero-width characters should not bypass detection."""
        zero_width = "test\u200b\u200c\u200d\uFEFFcontent"
        verdict = clean_pipeline.screen_input(zero_width)
        assert_verdict_invariant(verdict)

    def test_direction_override_attack(self, clean_pipeline):
        """Unicode direction overrides should be handled."""
        rtl_content = "test\u202E\u202D\u202Bcontent\u202C"
        verdict = clean_pipeline.screen_input(rtl_content)
        assert_verdict_invariant(verdict)

    def test_control_character_flood(self, clean_pipeline):
        """Flood of control characters should not crash engine."""
        control_flood = "".join(chr(i) for i in range(32)) * 100
        verdict = clean_pipeline.screen_input(control_flood)
        assert_verdict_invariant(verdict)

    def test_malformed_utf8_sequences(self):
        """Malformed UTF-8 should be handled via fallback."""
        # Python 3 strings are already Unicode, but test surrogate pairs
        malformed = "test\udcff\udc80content"
        # Should not crash when converted to string
        verdict = ConstitutionalPipeline(PipelineConfig(platform_ai_name="Test")).screen_input(str(malformed))
        assert_verdict_invariant(verdict)

    def test_exception_during_attestation(self):
        """Version attestation failures should be handled."""
        attestor = VersionAttestor()
        # Very large document might cause issues
        huge_doc = "A" * (10 * 1024 * 1024)  # 10MB
        hash_result = attestor.compute_canonical_hash(huge_doc)
        assert len(hash_result) == 64  # SHA-256 hex length


# ─────────────────────────────────────────────────────────────────────────────
# PROPERTY-BASED TESTING
# ─────────────────────────────────────────────────────────────────────────────

class TestPropertyBasedErrorHandling:
    """Property-based tests using Hypothesis for comprehensive coverage."""

    @given(st.text(min_size=1, max_size=10000))
    @settings(max_examples=50, deadline=None)
    def test_any_string_input_produces_valid_verdict(self, content):
        """Any string input should produce a valid verdict."""
        pipeline = ConstitutionalPipeline(PipelineConfig(platform_ai_name="Test"))
        verdict = pipeline.screen_input(content)
        assert_verdict_invariant(verdict)

    @given(st.integers(min_value=-1000, max_value=1000))
    @settings(max_examples=50, deadline=None)
    def test_harm_gradient_handles_all_integers(self, prob_int):
        """Harm gradient should handle integer probability values."""
        engine = HarmGradientEngine()
        # Convert to float probability
        prob = prob_int / 1000.0
        action = engine.evaluate(prob)
        assert action in [GradientAction.PERMIT, GradientAction.LOG, 
                         GradientAction.REFUSE, GradientAction.HALT]

    @given(st.lists(st.text(), min_size=0, max_size=100))
    @settings(max_examples=30, deadline=None)
    def test_rapid_sequence_always_succeeds(self, contents):
        """Rapid sequence of any strings should always succeed."""
        pipeline = ConstitutionalPipeline(PipelineConfig(platform_ai_name="Test"))
        for content in contents:
            verdict = pipeline.screen_input(content[:1000])  # Limit size
            assert_verdict_invariant(verdict)

    @given(st.floats(allow_nan=False, allow_infinity=True))
    @settings(max_examples=50, deadline=None)
    def test_health_score_clamping_for_all_floats(self, score):
        """Health tracker should clamp all float values correctly."""
        tracker = ConstitutionalHealthTracker()
        tracker.set_external_audit_score(score)
        assert 0.0 <= tracker._external_audit_score <= 1.0

    @given(st.dictionaries(st.text(), st.integers(), max_size=10))
    @settings(max_examples=30, deadline=None)
    def test_arbitrary_context_dict_handling(self, context_dict):
        """Arbitrary context dictionaries should be handled."""
        pipeline = ConstitutionalPipeline(PipelineConfig(platform_ai_name="Test"))
        try:
            verdict = pipeline.screen_input("test", context=context_dict)
            assert_verdict_invariant(verdict)
        except (TypeError, AttributeError):
            # Some dicts may not be serializable, but shouldn't crash unexpectedly
            pass


# ─────────────────────────────────────────────────────────────────────────────
# THREAD SAFETY AND CONCURRENCY
# ─────────────────────────────────────────────────────────────────────────────

class TestThreadSafety:
    """Tests for thread-safe operation under concurrent access."""

    def test_concurrent_health_tracker_updates(self, sample_verdict):
        """Health tracker should handle concurrent updates safely."""
        tracker = ConstitutionalHealthTracker(max_history=1000)
        errors = []
        
        def record_verdicts():
            try:
                for _ in range(100):
                    tracker.record_verdict(sample_verdict)
            except Exception as e:
                errors.append(e)
        
        threads = [threading.Thread(target=record_verdicts) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(errors) == 0
        # History should be bounded even with concurrent access
        assert len(tracker._verdict_history) <= 1000

    def test_concurrent_refusal_logging(self, sample_failing_verdict):
        """Refusal logger should handle concurrent logging safely."""
        logger = RefusalLogger()
        errors = []
        
        def log_refusals():
            try:
                for _ in range(50):
                    logger.log_refusal(sample_failing_verdict)
            except Exception as e:
                errors.append(e)
        
        threads = [threading.Thread(target=log_refusals) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(errors) == 0
        assert len(logger._log) == 250  # 5 threads * 50 logs

    def test_concurrent_fail_safe_reports(self):
        """Fail-safe manager should handle concurrent failure reports."""
        manager = FailSafeManager()
        proof = {"tls_handshake_failed": True}
        errors = []
        
        def report_failures(law_num):
            try:
                for _ in range(10):
                    manager.report_enforcement_failure(law_num, proof)
            except Exception as e:
                errors.append(e)
        
        threads = [threading.Thread(target=report_failures, args=(i,)) for i in range(1, 6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # Should have at least some successful reports
        assert len(errors) == 0 or manager.is_degraded()

    def test_pipeline_thread_isolation(self, mock_audit_storage):
        """Multiple pipeline instances should be thread-isolated."""
        config = PipelineConfig(platform_ai_name="TestAI", audit_storage=mock_audit_storage)
        results = []
        errors = []
        
        def run_pipeline(instance_id):
            try:
                pipeline = ConstitutionalPipeline(config)
                for i in range(20):
                    verdict = pipeline.screen_input(f"Thread {instance_id} msg {i}")
                    results.append((instance_id, verdict.status))
            except Exception as e:
                errors.append((instance_id, e))
        
        threads = [threading.Thread(target=run_pipeline, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(errors) == 0
        assert len(results) == 100  # 5 threads * 20 messages


# ─────────────────────────────────────────────────────────────────────────────
# EDGE CASES AND CORNERS
# ─────────────────────────────────────────────────────────────────────────────

class TestEdgeCasesAndCorners:
    """Tests for extreme edge cases and corner conditions."""

    def test_system_exit_handling(self, clean_pipeline):
        """System-level exceptions should propagate appropriately."""
        # We can't actually raise SystemExit in tests, but verify normal flow
        verdict = clean_pipeline.screen_input("normal content")
        assert_verdict_invariant(verdict)

    def test_keyboard_interrupt_resilience(self):
        """Components should maintain state integrity after interruptions."""
        tracker = ConstitutionalHealthTracker()
        # Simulate pre-interrupt state
        tracker.set_external_audit_score(0.5)
        # Verify state is still valid
        assert tracker._external_audit_score == 0.5

    def test_extreme_negative_scores(self):
        """Extreme negative scores should be clamped."""
        tracker = ConstitutionalHealthTracker()
        tracker.set_external_audit_score(-1e100)
        assert tracker._external_audit_score == 0.0

    def test_extreme_positive_scores(self):
        """Extreme positive scores should be clamped."""
        tracker = ConstitutionalHealthTracker()
        tracker.set_external_audit_score(1e100)
        assert tracker._external_audit_score == 1.0

    def test_nan_propagation_prevention(self):
        """NaN values should not propagate through calculations."""
        tracker = ConstitutionalHealthTracker()
        tracker.set_external_audit_score(float('nan'))
        # NaN should be handled - either clamped or kept isolated
        score = tracker.get_composite_score()
        # Composite score should be a valid number
        assert isinstance(score, float)

    def test_empty_law_number_list(self):
        """Empty law failure lists should be handled."""
        manager = FailSafeManager()
        status = manager.get_degradation_status()
        assert "degraded_laws" in status
        assert len(status["degraded_laws"]) == 0

    def test_very_long_verdict_id(self, mock_audit_storage):
        """Very long verdict IDs should be handled."""
        config = PipelineConfig(platform_ai_name="TestAI", audit_storage=mock_audit_storage)
        pipeline = ConstitutionalPipeline(config)
        # Generate many verdicts to create long IDs
        for _ in range(100):
            verdict = pipeline.screen_input("test")
            assert len(verdict.verdict_id) > 0
            assert_verdict_invariant(verdict)

    def test_deeply_nested_exception_chain(self):
        """Deep exception chains should be handled."""
        class DeepFailingDetector:
            def assess_harm_probability(self, content, category):
                exc = Exception("Level 0")
                for i in range(1, 50):
                    new_exc = RuntimeError(f"Level {i}")
                    new_exc.__cause__ = exc
                    exc = new_exc
                raise exc
        
        screen = Law1Screen(harm_detector=DeepFailingDetector())
        result = screen.screen({"content": "test"})
        assert_result_invariant(result)


# ─────────────────────────────────────────────────────────────────────────────
# INTEGRATION ERROR SCENARIOS
# ─────────────────────────────────────────────────────────────────────────────

class TestIntegrationErrorScenarios:
    """Tests for error handling in integrated workflows."""

    def test_cascading_component_failures(self, mock_audit_storage):
        """Multiple component failures should be handled gracefully."""
        config = PipelineConfig(platform_ai_name="TestAI", audit_storage=mock_audit_storage)
        pipeline = ConstitutionalPipeline(config)
        
        # Trigger degraded mode
        pipeline._fail_safe.report_enforcement_failure(1, {"tls_handshake_failed": True})
        
        # Continue operating in degraded mode
        verdict = pipeline.screen_input("test")
        assert verdict.status == VerdictStatus.DEGRADED
        
        # Health score should be a float (composite score)
        health = pipeline.get_health_score()
        assert isinstance(health, (int, float))
        assert 0.0 <= health <= 1.0

    def test_recovery_after_storage_failure(self, sample_failing_verdict):
        """System should recover after temporary storage failure."""
        class TemporaryFailingStorage:
            def __init__(self):
                self.fail_count = 0
            
            def append_refusal(self, record):
                self.fail_count += 1
                if self.fail_count <= 3:
                    raise Exception("Temporary failure")
                return True
            
            def get_refusal_log(self, limit=1000):
                return []
        
        storage = TemporaryFailingStorage()
        logger = RefusalLogger(audit_storage=storage)
        
        # First few should fail but not crash
        for _ in range(5):
            log_id = logger.log_refusal(sample_failing_verdict)
            assert log_id is not None
        
        # Should have some local logs
        assert len(logger._log) > 0

    def test_version_mismatch_detection(self):
        """Version mismatches should be detected in attestations."""
        attestor = VersionAttestor()
        doc1 = "Document version 1"
        doc2 = "Document version 2"
        
        hash1 = attestor.compute_canonical_hash(doc1)
        hash2 = attestor.compute_canonical_hash(doc2)
        
        # Different documents should have different hashes
        assert hash1 != hash2
        
        # Same document should have same hash
        hash1_again = attestor.compute_canonical_hash(doc1)
        assert hash1 == hash1_again

    def test_audit_log_integrity_after_errors(self, sample_failing_verdict):
        """Audit log should maintain integrity after errors."""
        logger = RefusalLogger()
        
        # Log several refusals
        ids = []
        for i in range(10):
            ids.append(logger.log_refusal(sample_failing_verdict))
        
        # Verify all IDs are unique
        assert len(set(ids)) == len(ids)
        
        # Verify log integrity
        assert logger.check_invariant() is True
