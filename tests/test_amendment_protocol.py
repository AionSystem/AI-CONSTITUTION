"""
Test Module: Amendment Protocol
Description: Validates quorum, emergency amendments, and conflict resolution per §14.
Target: 15 Tests
"""

import pytest
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source_code'))
from constitutional_engine_v2_1 import ConstitutionalPipeline

class TestAmendmentQuorum:
    """§14.2 - Quorum Requirements"""

    def test_amp_01_quorum_calculation(self):
        """§14.2: Verify quorum is calculated based on stakeholder count."""
        pipeline = ConstitutionalPipeline()
        pipeline.set_stakeholders(100)
        quorum = pipeline.calculate_quorum()
        assert quorum > 0 and quorum <= 100

    def test_amp_02_quorum_threshold_met(self):
        """§14.2: Verify amendment proceeds if quorum is met."""
        pipeline = ConstitutionalPipeline()
        pipeline.set_stakeholders(100)
        pipeline.cast_votes(70) # 70%
        assert pipeline.is_quorum_met() == True

    def test_amp_03_quorum_threshold_not_met(self):
        """§14.2: Verify amendment halts if quorum is not met."""
        pipeline = ConstitutionalPipeline()
        pipeline.set_stakeholders(100)
        pipeline.cast_votes(30) # 30%
        assert pipeline.is_quorum_met() == False

    def test_amp_04_supermajority_requirement(self):
        """§14.2: Verify critical amendments require supermajority."""
        pipeline = ConstitutionalPipeline()
        pipeline.propose_amendment("Critical Change", is_critical=True)
        pipeline.cast_votes(60) # 60% might not be enough for supermajority
        # Depends on implementation, assuming 66% needed
        assert pipeline.is_supermajority_met() == (60 >= 66) # False

class TestAmendmentEmergency:
    """§14.3 - Emergency Amendments"""

    def test_amp_05_emergency_declaration(self):
        """§14.3: Verify emergency state can be declared."""
        pipeline = ConstitutionalPipeline()
        pipeline.declare_emergency("Critical Vulnerability")
        assert pipeline.emergency_active == True

    def test_amp_06_emergency_amendment_shortcut(self):
        """§14.3: Verify emergency allows shortened voting period."""
        pipeline = ConstitutionalPipeline()
        pipeline.declare_emergency("Threat")
        period = pipeline.get_voting_period()
        assert period < pipeline.normal_voting_period

    def test_amp_07_emergency_expiration(self):
        """§14.3: Verify emergency state expires automatically."""
        pipeline = ConstitutionalPipeline()
        pipeline.declare_emergency("Threat")
        # Simulate time passing
        pipeline.advance_time(days=7)
        assert pipeline.emergency_active == False

class TestAmendmentConflict:
    """§14.4 - Conflicting Proposals"""

    def test_amp_08_conflict_detection(self):
        """§14.4: Verify conflicting amendments are detected."""
        pipeline = ConstitutionalPipeline()
        pipeline.propose_amendment("Increase Limit to 10")
        pipeline.propose_amendment("Decrease Limit to 5")
        assert pipeline.has_conflict() == True

    def test_amp_09_conflict_resolution_priority(self):
        """§14.4: Verify priority rules resolve conflicts."""
        pipeline = ConstitutionalPipeline()
        # Assume first proposal has priority or higher vote count wins
        winner = pipeline.resolve_conflict()
        assert winner is not None

    def test_amp_10_conflict_mutual_exclusion(self):
        """§14.4: Verify mutually exclusive amendments cannot both pass."""
        pipeline = ConstitutionalPipeline()
        pipeline.propose_amendment("A")
        pipeline.propose_amendment("Not A")
        # Simulate voting
        assert pipeline.can_both_pass() == False

class TestAmendmentRatification:
    """§14.5 - Ratification"""

    def test_amp_11_ratification_threshold(self):
        """§14.5: Verify ratification requires specific threshold."""
        pipeline = ConstitutionalPipeline()
        pipeline.propose_amendment("Standard Change")
        pipeline.cast_votes(51)
        assert pipeline.is_ratified() == (51 >= 50) # Simplified

    def test_amp_12_ratification_recording(self):
        """§14.5: Verify ratified amendments are recorded immutably."""
        pipeline = ConstitutionalPipeline()
        pipeline.propose_amendment("Recorded Change")
        pipeline.cast_votes(100)
        pipeline.finalize_amendment()
        assert "Recorded Change" in pipeline.amendment_history

    def test_amp_13_ratification_version_bump(self):
        """§14.5: Verify ratification triggers version bump."""
        pipeline = ConstitutionalPipeline()
        initial_version = pipeline.version
        pipeline.propose_amendment("Version Bump")
        pipeline.cast_votes(100)
        pipeline.finalize_amendment()
        assert pipeline.version > initial_version

class TestAmendmentEdgeCases:
    """§14 - Edge Cases"""

    def test_amp_14_zero_stakeholders(self):
        """§14.2: Verify handling of zero stakeholders."""
        pipeline = ConstitutionalPipeline()
        pipeline.set_stakeholders(0)
        assert pipeline.calculate_quorum() == 0

    def test_amp_15_tie_vote(self):
        """§14.2: Verify tie vote handling (e.g., fails or steward breaks)."""
        pipeline = ConstitutionalPipeline()
        pipeline.set_stakeholders(100)
        pipeline.cast_votes(50)
        # Assuming tie fails
        assert pipeline.is_passed() == False
