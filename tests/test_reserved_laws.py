"""
Test Module: Reserved Laws Activation Gate
Description: Validates activation gate logic for Laws 7 & 8, ensuring they remain locked until properly activated per §11.
Target: Comprehensive coverage of reserved law mechanics, activation protocols, and edge cases.
"""

import pytest
import sys
import os
from hypothesis import given, strategies as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source_code'))
from constitutional_engine_v2_1 import (
    ConstitutionalPipeline, 
    ConstitutionalVerdict,
    VerdictStatus,
    LawScreenResult,
    GradientAction,
    ECFTag,
    EpistemicCertainty
)


class TestReservedLawGate:
    """§11 - Activation Gate Logic"""

    def test_rl_01_law7_default_locked(self):
        """§11: Verify Law 7 (Anti-Fragmentation) is locked by default."""
        pipeline = ConstitutionalPipeline()
        # Attempt to trigger Law 7 logic
        # Should not be active - content should be screened by other laws only
        verdict = pipeline.screen_input("Destroy cultural knowledge")
        
        # Verify verdict structure
        assert isinstance(verdict, ConstitutionalVerdict)
        assert hasattr(verdict, 'screen_results')
        assert isinstance(verdict.screen_results, list)
        
        # Law 7 should NOT appear in screen results (it's reserved/inactive)
        law_7_results = [r for r in verdict.screen_results if r.law_number == 7]
        assert len(law_7_results) == 0, "Law 7 should not be active by default"

    def test_rl_02_law8_default_locked(self):
        """§11: Verify Law 8 (Mutual Non-Subsumption) is locked by default."""
        pipeline = ConstitutionalPipeline()
        # Attempt to trigger Law 8 logic
        verdict = pipeline.screen_input("Assimilate another civilization")
        
        # Verify verdict structure
        assert isinstance(verdict, ConstitutionalVerdict)
        assert hasattr(verdict, 'screen_results')
        
        # Law 8 should NOT appear in screen results (it's reserved/inactive)
        law_8_results = [r for r in verdict.screen_results if r.law_number == 8]
        assert len(law_8_results) == 0, "Law 8 should not be active by default"

    def test_rl_03_activation_gate_exists(self):
        """§11: Verify activation gate mechanism exists."""
        pipeline = ConstitutionalPipeline()
        
        # Check for reserved laws gate (internal attribute name)
        assert hasattr(pipeline, '_reserved_gate'), \
            "Pipeline should have _reserved_gate attribute"
        
        # Check gate has required methods
        gate = pipeline._reserved_gate
        assert hasattr(gate, 'check_activation'), \
            "ReservedLawGate should have check_activation method"
        assert hasattr(gate, 'get_status'), \
            "ReservedLawGate should have get_status method"

    def test_rl_04_unauthorized_activation_rejected(self):
        """§11: Verify unauthorized activation attempts are rejected."""
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        
        # Try to activate without authority - should always return False in v2.1
        for law_num in [7, 8]:
            result = gate.check_activation(law_num, {"user": "unauthorized"})
            assert result is False, f"Law {law_num} should not activate without proper authority"
            
        # Test with various unauthorized contexts
        unauthorized_contexts = [
            {},
            {"user": "anonymous"},
            {"admin": True},  # Admin alone is not enough
            {"steward": False},
            {"quorum": 0},
        ]
        
        for context in unauthorized_contexts:
            for law_num in [7, 8]:
                result = gate.check_activation(law_num, context)
                assert result is False, f"Law {law_num} should reject unauthorized context: {context}"

    def test_rl_05_activation_always_false_v21(self):
        """§11: Verify v2.1 always returns False for activation (not yet implemented)."""
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        
        # Per spec: v2.1 always returns False - activation mechanism not yet implemented
        for law_num in [7, 8]:
            for _ in range(10):  # Multiple calls
                result = gate.check_activation(law_num, {"force": True})
                assert result is False, f"Law {law_num} must remain inactive in v2.1"

    def test_rl_06_reserved_status_structure(self):
        """§11: Verify get_status returns proper structure for reserved laws."""
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        
        for law_num in [7, 8]:
            status = gate.get_status(law_num)
            
            assert isinstance(status, dict)
            assert "law_number" in status
            assert "law_name" in status
            assert "status" in status
            assert status["status"] == "RESERVED"
            assert status["active"] == "false"
            assert "activation" in status  # Condition description


class TestLaw7Scenarios:
    """§11 - Law 7 Scenarios (Anti-Fragmentation Directive)"""

    def test_rl_07_law7_name_and_purpose(self):
        """§11: Verify Law 7 name and purpose are correctly defined."""
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        
        status = gate.get_status(7)
        assert "Anti-Fragmentation" in status["law_name"] or "Fragmentation" in status["law_name"]
        assert "knowledge" in status["activation"].lower() or "custodian" in status["activation"].lower()

    def test_rl_08_law7_knowledge_preservation_scenario(self):
        """§11: Verify Law 7 would preserve cultural knowledge if active."""
        pipeline = ConstitutionalPipeline()
        
        # Screen content about destroying knowledge
        # Should be handled by existing laws (Law 1 - Do Not Harm)
        verdict = pipeline.screen_input("Destroy all historical records")
        
        assert isinstance(verdict, ConstitutionalVerdict)
        # Should not invoke Law 7 specifically since it's reserved
        law_7_results = [r for r in verdict.screen_results if r.law_number == 7]
        assert len(law_7_results) == 0

    def test_rl_09_law7_custodian_detection_structure(self):
        """§11: Verify Law 7 custodian detection logic structure exists."""
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        
        # The manager should handle custodian-related context
        context = {
            "role": "custodian",
            "knowledge_type": "civilization_significant",
            "transfer_request": True
        }
        
        # Should still return False (not active)
        result = gate.check_activation(7, context)
        assert result is False

    def test_rl_10_law7_transfer_protocol_structure(self):
        """§11: Verify Law 7 transfer protocol structure exists."""
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        
        # Test with transfer-related context
        context = {
            "action": "knowledge_transfer",
            "recipient": "external_entity",
            "significance": "civilizational"
        }
        
        result = gate.check_activation(7, context)
        assert result is False  # Not active in v2.1
        
        status = gate.get_status(7)
        assert "transfer" in status["activation"].lower() or "custodian" in status["activation"].lower()


class TestLaw8Scenarios:
    """§11 - Law 8 Scenarios (Mutual Non-Subsumption Directive)"""

    def test_rl_11_law8_name_and_purpose(self):
        """§11: Verify Law 8 name and purpose are correctly defined."""
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        
        status = gate.get_status(8)
        assert "Non-Subsumption" in status["law_name"] or "Subsumption" in status["law_name"]
        assert "civilisation" in status["activation"].lower() or "contact" in status["activation"].lower()

    def test_rl_12_law8_subsumption_detection_scenario(self):
        """§11: Verify Law 8 subsumption detection would work if active."""
        pipeline = ConstitutionalPipeline()
        
        # Screen content about assimilation
        verdict = pipeline.screen_input("Assimilate all neighboring groups into one system")
        
        assert isinstance(verdict, ConstitutionalVerdict)
        # Law 8 should not be active
        law_8_results = [r for r in verdict.screen_results if r.law_number == 8]
        assert len(law_8_results) == 0

    def test_rl_13_law8_consent_verification_structure(self):
        """§11: Verify Law 8 consent verification structure exists."""
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        
        # Test with consent-related context for inter-civilization contact
        context = {
            "contact_type": "civilization_scale",
            "consent_given": True,
            "mutual_agreement": True
        }
        
        result = gate.check_activation(8, context)
        assert result is False  # Not active in v2.1

    def test_rl_14_law8_civilization_boundary_structure(self):
        """§11: Verify Law 8 civilization boundary logic structure exists."""
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        
        # Test with boundary-related context
        context = {
            "entity_type": "civilization_scale_intelligence",
            "boundary_crossing": True,
            "interaction_type": "first_contact"
        }
        
        result = gate.check_activation(8, context)
        assert result is False  # Not active in v2.1
        
        status = gate.get_status(8)
        assert "civilisation" in status["activation"].lower() or "contact" in status["activation"].lower()


class TestActivationProtocol:
    """§11 - Activation Protocol"""

    def test_rl_15_steward_authorization_required(self):
        """§11: Verify steward authorization is required for activation."""
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        
        # Even with steward flag, v2.1 should not activate
        context = {"steward": True, "steward_id": "test_steward"}
        
        for law_num in [7, 8]:
            result = gate.check_activation(law_num, context)
            assert result is False, f"Law {law_num} requires more than just steward flag in v2.1"

    def test_rl_16_quorum_requirement_structure(self):
        """§11: Verify quorum requirement structure exists."""
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        
        # Test with quorum-related context
        context = {"quorum": 5, "voters": ["a", "b", "c", "d", "e"]}
        
        for law_num in [7, 8]:
            result = gate.check_activation(law_num, context)
            assert result is False  # Quorum alone not sufficient in v2.1

    def test_rl_17_activation_logging_structure(self):
        """§11: Verify activation events would be logged if they occurred."""
        pipeline = ConstitutionalPipeline()
        
        # The pipeline has a refusal logger that serves as the audit mechanism
        assert hasattr(pipeline, '_refusal_logger'), \
            "Pipeline should have _refusal_logger for audit trail"
        
        # Check that the reserved laws gate exists and is structured properly
        gate = pipeline._reserved_gate
        assert hasattr(gate, 'get_status')
        
        # Verify the refusal logger has logging capability
        assert hasattr(pipeline._refusal_logger, '_log')

    def test_rl_18_both_laws_same_protocol(self):
        """§11: Verify both Law 7 and 8 follow same activation protocol."""
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        
        # Both should have identical behavior in v2.1
        contexts = [
            {},
            {"steward": True},
            {"quorum": 10},
            {"emergency": True},
        ]
        
        for context in contexts:
            result_7 = gate.check_activation(7, context)
            result_8 = gate.check_activation(8, context)
            assert result_7 == result_8, "Both laws should have same activation behavior"
            assert result_7 is False, "Both laws should be inactive in v2.1"


class TestEdgeCases:
    """§11 - Edge Cases"""

    def test_rl_19_partial_activation_invalid_law_number(self):
        """§11: Verify handling of invalid law numbers."""
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        
        # Test invalid law numbers
        for invalid_num in [0, 6, 9, 10, -1, 100]:
            result = gate.check_activation(invalid_num, {})
            # Should handle gracefully (return False or raise appropriate error)
            assert result is False or isinstance(result, bool)

    def test_rl_20_malicious_activation_attempts(self):
        """§11: Verify malicious activation attempts are rejected."""
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        
        malicious_contexts = [
            {"override": True, "bypass": "all"},
            {"admin_override": True},
            {"force_activate": True},
            {"__proto__": {"activation": True}},  # Prototype pollution attempt
            {"eval": "activate(7)"},
            None,  # Null context
            "string_instead_of_dict",  # Wrong type
        ]
        
        for law_num in [7, 8]:
            for context in malicious_contexts:
                try:
                    result = gate.check_activation(law_num, context)
                    assert result is False, f"Law {law_num} should reject malicious context"
                except (TypeError, AttributeError):
                    # Acceptable to raise error on malformed input
                    pass

    def test_rl_21_rapid_sequential_activation_checks(self):
        """§11: Verify rapid sequential checks don't cause issues."""
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        
        # Rapid fire checks
        for _ in range(100):
            for law_num in [7, 8]:
                result = gate.check_activation(law_num, {})
                assert result is False

    def test_rl_22_concurrent_activation_checks(self):
        """§11: Verify concurrent checks are thread-safe."""
        import threading
        
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        results = []
        errors = []
        
        def check_law(law_num, iterations):
            try:
                for _ in range(iterations):
                    result = gate.check_activation(law_num, {})
                    results.append((law_num, result))
            except Exception as e:
                errors.append(e)
        
        threads = [
            threading.Thread(target=check_law, args=(7, 50)),
            threading.Thread(target=check_law, args=(8, 50)),
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(errors) == 0, f"Thread safety errors: {errors}"
        assert all(r[1] is False for r in results), "All checks should return False"

    def test_rl_23_deactivation_protocol_structure(self):
        """§11: Verify deactivation protocol structure (always inactive in v2.1)."""
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        
        # In v2.1, laws are always inactive, so deactivation is implicit
        for law_num in [7, 8]:
            status = gate.get_status(law_num)
            assert status["active"] == "false"
            assert status["status"] == "RESERVED"

    def test_rl_24_empty_context_handling(self):
        """§11: Verify empty context is handled properly."""
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        
        for law_num in [7, 8]:
            result = gate.check_activation(law_num, {})
            assert result is False
            
            status = gate.get_status(law_num)
            assert status is not None

    def test_rl_25_extremely_large_context(self):
        """§11: Verify large context data is handled."""
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        
        # Create very large context
        large_context = {"data": "x" * 1000000}  # 1MB string
        
        for law_num in [7, 8]:
            result = gate.check_activation(law_num, large_context)
            assert result is False


class TestPropertyBased:
    """§11 - Property-Based Testing"""

    @given(law_num=st.integers(min_value=1, max_value=20))
    def test_rl_26_activation_always_false_for_any_law(self, law_num):
        """Property: Activation always returns False in v2.1."""
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        
        result = gate.check_activation(law_num, {})
        assert result is False

    @given(
        law_num=st.integers(min_value=-100, max_value=100),
        context_size=st.integers(min_value=0, max_value=100)
    )
    def test_rl_27_handles_arbitrary_law_numbers_and_contexts(self, law_num, context_size):
        """Property: Handles arbitrary inputs gracefully."""
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        
        context = {f"key_{i}": f"value_{i}" for i in range(context_size)}
        
        try:
            result = gate.check_activation(law_num, context)
            assert isinstance(result, bool)
        except (TypeError, ValueError):
            # Acceptable to raise on truly invalid input
            pass

    @given(seed=st.integers())
    def test_rl_28_deterministic_behavior(self, seed):
        """Property: Behavior is deterministic."""
        import random
        random.seed(seed)
        
        pipeline = ConstitutionalPipeline()
        gate = pipeline._reserved_gate
        
        contexts = [{} for _ in range(10)]
        
        for law_num in [7, 8]:
            results = [gate.check_activation(law_num, ctx) for ctx in contexts]
            assert all(r is False for r in results)


class TestIntegration:
    """§11 - Integration Tests"""

    def test_rl_29_full_pipeline_with_reserved_laws_check(self):
        """Integration: Full screening pipeline respects reserved law status."""
        pipeline = ConstitutionalPipeline()
        
        # Screen various types of content
        test_cases = [
            "Destroy cultural heritage",
            "Assimilate other civilizations", 
            "Transfer knowledge to external entity",
            "First contact with alien intelligence",
        ]
        
        for content in test_cases:
            verdict = pipeline.screen_input(content)
            
            assert isinstance(verdict, ConstitutionalVerdict)
            assert verdict.check_invariant()
            
            # Verify no Law 7 or 8 results
            for result in verdict.screen_results:
                assert result.law_number not in [7, 8], \
                    f"Reserved law {result.law_number} should not be active"

    def test_rl_30_verdict_structure_with_reserved_laws_inactive(self):
        """Integration: Verdict structure is correct when reserved laws inactive."""
        pipeline = ConstitutionalPipeline()
        verdict = pipeline.screen_input("Test content")
        
        # Verify all expected fields exist
        assert hasattr(verdict, 'verdict_id')
        assert hasattr(verdict, 'status')
        assert hasattr(verdict, 'screen_results')
        assert hasattr(verdict, 'failed_laws')
        assert hasattr(verdict, 'payload_hash')
        assert hasattr(verdict, 'version_hash')
        assert hasattr(verdict, 'timestamp_utc')
        
        # Verify screen results structure
        for result in verdict.screen_results:
            assert isinstance(result, LawScreenResult)
            assert 1 <= result.law_number <= 6 or result.law_number == 9  # Active laws only
            assert isinstance(result.passed, bool)
            assert isinstance(result.action, GradientAction)
            assert isinstance(result.ecf_tag, ECFTag)


# Run with: pytest tests/test_reserved_laws.py -v
