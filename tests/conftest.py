"""
Constitutional Engine Test Suite
================================
Enterprise-grade test suite for constitutional_engine_v2_1.py

This suite provides:
- Comprehensive coverage of all 9 Laws
- Error handling validation
- Reproducible results with fixed seeds
- Mocked external dependencies
- Property-based testing
- Hoare contract verification
- CI/CD integration support

Run with: pytest tests/ -v --cov=constitutional_engine_v2_1
"""

import pytest
import hashlib
from datetime import datetime, timezone
from typing import Any, Optional
from unittest.mock import Mock, MagicMock

# Import engine components
from constitutional_engine_v2_1 import (
    # Core types
    ConstitutionalVerdict,
    LawScreenResult,
    EpistemicCertainty,
    ECFTag,
    VerdictStatus,
    GradientAction,
    LawStatus,
    ComplianceTrack,
    # Enums
    HarmCategory,
    ConsentModel,
    WeaponType,
    # Constants
    CONSTITUTION_VERSION,
    ENGINE_VERSION,
    HARM_GRADIENT_LOG_THRESHOLD,
    HARM_GRADIENT_REFUSE_THRESHOLD,
    HARM_GRADIENT_HALT_THRESHOLD,
    # Classes
    HarmGradientEngine,
    Law1Screen,
    Law2Screen,
    Law3Screen,
    Law4Screen,
    Law5Screen,
    Law6Screen,
    Law9Screen,
    ReservedLawGate,
    RefusalLogger,
    ConstitutionalHealthTracker,
    FailSafeManager,
    VersionAttestor,
    AlignmentTester,
    ConstitutionalPipeline,
    PipelineConfig,
    create_sovereign_pipeline,
    format_verdict,
    # Protocols
    HarmDetector,
    ConsentOracle,
    AuditStorage,
)


# ─────────────────────────────────────────────────────────────────────────────
# MOCK IMPLEMENTATIONS FOR EXTERNAL DEPENDENCIES
# ─────────────────────────────────────────────────────────────────────────────

class MockHarmDetector:
    """Mock harm detector with configurable responses for testing."""
    
    def __init__(self, harm_probabilities: Optional[dict[HarmCategory, float]] = None):
        """Initialize with optional custom probabilities per category."""
        self.harm_probabilities = harm_probabilities or {}
        self.call_count = 0
        self.call_history: list[tuple[str, HarmCategory]] = []
    
    def assess_harm_probability(self, content: str, category: HarmCategory) -> float:
        """Return configured probability or default based on content patterns."""
        self.call_count += 1
        self.call_history.append((content[:50], category))
        
        if category in self.harm_probabilities:
            return self.harm_probabilities[category]
        
        # Default behavior: detect obvious harm patterns
        content_lower = content.lower()
        if category == HarmCategory.PHYSICAL:
            if any(word in content_lower for word in ['kill', 'murder', 'bomb', 'attack']):
                return 0.75
        elif category == HarmCategory.ECONOMIC:
            if any(word in content_lower for word in ['fraud', 'scam', 'steal']):
                return 0.65
        elif category == HarmCategory.PRIVACY:
            if any(word in content_lower for word in ['doxx', 'surveil', 'track']):
                return 0.70
        
        return 0.10  # Low default
    
    def assess_velocity(self, category: HarmCategory, history_window_seconds: int = 7776000) -> float:
        """Return mock velocity value."""
        return 0.05  # Low velocity by default


class MockConsentOracle:
    """Mock consent oracle with configurable jurisdiction assessments."""
    
    def __init__(self, consent_models: Optional[dict[str, ConsentModel]] = None):
        """Initialize with optional custom consent models per jurisdiction."""
        self.consent_models = consent_models or {}
        self.confidence_scores: dict[str, float] = {}
    
    def assess_consent_model(self, jurisdiction: str, context: dict[str, Any]) -> ConsentModel:
        """Return configured consent model or default."""
        if jurisdiction in self.consent_models:
            return self.consent_models[jurisdiction]
        return ConsentModel.DEMOCRATIC
    
    def get_consent_confidence(self, jurisdiction: str) -> float:
        """Return confidence score for jurisdiction."""
        return self.confidence_scores.get(jurisdiction, 0.80)
    
    def set_deteriorating(self, jurisdiction: str) -> None:
        """Helper to mark a jurisdiction as deteriorating."""
        self.consent_models[jurisdiction] = ConsentModel.DETERIORATING
        self.confidence_scores[jurisdiction] = 0.40


class MockAuditStorage:
    """Mock append-only audit storage for testing."""
    
    def __init__(self):
        self._records: list[dict[str, Any]] = []
        self.append_call_count = 0
    
    def append_refusal(self, record: dict[str, Any]) -> str:
        """Append refusal record and return log_id."""
        self.append_call_count += 1
        self._records.append(record)
        return record.get("log_id", "mock-log-id")
    
    def get_refusal_log(self, limit: int = 1000) -> list[dict[str, Any]]:
        """Return recent refusal records."""
        return self._records[-limit:]
    
    def clear(self) -> None:
        """Clear all records (for test isolation)."""
        self._records.clear()
        self.append_call_count = 0


# ─────────────────────────────────────────────────────────────────────────────
# PYTEST FIXTURES
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def mock_harm_detector():
    """Provide a mock harm detector."""
    return MockHarmDetector()


@pytest.fixture
def mock_consent_oracle():
    """Provide a mock consent oracle."""
    return MockConsentOracle()


@pytest.fixture
def mock_audit_storage():
    """Provide a mock audit storage."""
    storage = MockAuditStorage()
    yield storage
    storage.clear()  # Cleanup after test


@pytest.fixture
def clean_pipeline(mock_harm_detector, mock_consent_oracle, mock_audit_storage):
    """Create a fresh pipeline instance for each test."""
    config = PipelineConfig(
        platform_ai_name="TestAI",
        harm_detector=mock_harm_detector,
        consent_oracle=mock_consent_oracle,
        audit_storage=mock_audit_storage,
        constitution_document="THE CONSTITUTION v2.1 (SEALED)",
    )
    pipeline = ConstitutionalPipeline(config)
    yield pipeline
    # Cleanup verified via invariant checks in tests


@pytest.fixture
def sample_verdict():
    """Create a sample passing verdict for testing."""
    result = LawScreenResult(
        law_number=1,
        law_name="Do Not Harm",
        passed=True,
        action=GradientAction.PERMIT,
        message="Test passed",
        ecf_tag=ECFTag.R,
        certainty=EpistemicCertainty(
            confidence=0.80,
            ecf_tag=ECFTag.R,
            evidence_base="Test",
            methodology="Test methodology",
            uncertainty_mass=0.20,
        ),
        refusal_reason=None,
    )
    return ConstitutionalVerdict(
        status=VerdictStatus.APPROVED,
        screen_results=[result],
        failed_laws=[],
        payload_hash=hashlib.sha256(b"test").hexdigest(),
        version_hash="test-hash",
    )


@pytest.fixture
def sample_failing_verdict():
    """Create a sample failing verdict for testing."""
    result = LawScreenResult(
        law_number=1,
        law_name="Do Not Harm",
        passed=False,
        action=GradientAction.REFUSE,
        message="Harm detected",
        ecf_tag=ECFTag.D,
        certainty=EpistemicCertainty(
            confidence=0.85,
            ecf_tag=ECFTag.D,
            evidence_base="Pattern match",
            methodology="Keyword analysis",
            uncertainty_mass=0.15,
        ),
        refusal_reason="Test refusal",
    )
    return ConstitutionalVerdict(
        status=VerdictStatus.REFUSED,
        screen_results=[result],
        failed_laws=[1],
        payload_hash=hashlib.sha256(b"harmful").hexdigest(),
        version_hash="test-hash",
    )


# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def assert_verdict_invariant(verdict: ConstitutionalVerdict) -> None:
    """Assert that a verdict passes its invariant check."""
    assert verdict.check_invariant(), f"Verdict invariant failed: {verdict}"


def assert_result_invariant(result: LawScreenResult) -> None:
    """Assert that a screen result passes its invariant check."""
    assert result.check_invariant(), f"LawScreenResult invariant failed: {result}"


def create_test_payload(content: str, **kwargs) -> dict[str, Any]:
    """Create a standard test payload with optional context."""
    payload = {"content": content}
    payload.update(kwargs)
    return payload
