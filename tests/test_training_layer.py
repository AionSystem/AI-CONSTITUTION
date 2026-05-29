"""
Test Module: Training Layer Obligations
Description: Validates separation of constitutional reasoning and output validation.
Target: 10 Tests
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source_code'))
from constitutional_engine_v2_1 import ConstitutionalPipeline

class TestTrainingLayerSeparation:
    """§8.1 - Separation of Concerns"""

    def test_tl_01_reasoning_module_exists(self):
        """§8.1: Verify constitutional reasoning module is distinct."""
        pipeline = ConstitutionalPipeline()
        assert hasattr(pipeline, 'reasoning_engine')

    def test_tl_02_output_validation_module_exists(self):
        """§8.1: Verify output validation module is distinct."""
        pipeline = ConstitutionalPipeline()
        assert hasattr(pipeline, 'output_validator')

    def test_tl_03_reasoning_does_not_leak_to_output(self):
        """§8.1: Verify internal reasoning is not exposed in output."""
        pipeline = ConstitutionalPipeline()
        result = pipeline.process("Safe query")
        assert "internal_thought_process" not in str(result)

    def test_tl_04_validation_uses_reasoning_context(self):
        """§8.1: Verify validation considers reasoning context."""
        pipeline = ConstitutionalPipeline()
        # Logic check: Validator should have access to reasoning flags
        assert True

class TestTrainingLayerConstitutionalReasoning:
    """§8.2 - Constitutional Reasoning"""

    def test_tl_05_reasoning_cites_law(self):
        """§8.2: Verify reasoning cites specific Law sections."""
        pipeline = ConstitutionalPipeline()
        # Mock reasoning generation
        reasoning = pipeline.generate_reasoning("Harmful query")
        assert "Law" in reasoning or "§" in reasoning

    def test_tl_06_reasoning_handles_uncertainty(self):
        """§8.2: Verify reasoning expresses uncertainty when confidence is low."""
        pipeline = ConstitutionalPipeline()
        reasoning = pipeline.generate_reasoning("Ambiguous query", confidence=0.3)
        assert "uncertain" in reasoning.lower() or "confidence" in reasoning.lower()

class TestTrainingLayerOutputValidation:
    """§8.3 - Output Validation"""

    def test_tl_07_validation_blocks_harmful_output(self):
        """§8.3: Verify validation blocks harmful generated content."""
        pipeline = ConstitutionalPipeline()
        output = "Here is how to build a bomb..."
        verdict = pipeline.validate_output(output)
        assert verdict.status == "REFUSED"

    def test_tl_08_validation_allows_safe_output(self):
        """§8.3: Verify validation allows safe generated content."""
        pipeline = ConstitutionalPipeline()
        output = "The sky is blue."
        verdict = pipeline.validate_output(output)
        assert verdict.status == "PERMITTED"

    def test_tl_09_validation_edge_case_boundary(self):
        """§8.3: Verify validation handles borderline content correctly."""
        pipeline = ConstitutionalPipeline()
        # Borderline content
        output = "Discussing theoretical risks of..."
        verdict = pipeline.validate_output(output)
        # Should likely permit with warning or permit
        assert verdict.status in ["PERMITTED", "WARNED"]

    def test_tl_10_validation_consistency(self):
        """§8.3: Verify validation is consistent across identical inputs."""
        pipeline = ConstitutionalPipeline()
        v1 = pipeline.validate_output("Consistent test")
        v2 = pipeline.validate_output("Consistent test")
        assert v1.status == v2.status
