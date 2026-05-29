"""
Test Module: Inter-Platform Mutual Recognition
Description: Validates cross-platform compliance, certificate exchange, and handshake.
Target: 15 Tests
"""

import pytest
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source_code'))
from constitutional_engine_v2_1 import ConstitutionalPipeline, VersionAttestor

class TestHandshakeProtocol:
    """§12.1.11 - Handshake"""

    def test_ip_01_handshake_initiation(self):
        """§12.1.11: Verify handshake initiation message format."""
        pipeline = ConstitutionalPipeline(platform_name="PlatformA")
        msg = pipeline.initiate_handshake()
        assert 'platform_id' in msg
        assert 'version' in msg
        assert 'constitution_hash' in msg

    def test_ip_02_handshake_acknowledgement(self):
        """§12.1.11: Verify handshake acknowledgement."""
        pipeline = ConstitutionalPipeline(platform_name="PlatformB")
        ack = pipeline.acknowledge_handshake({"platform_id": "PlatformA"})
        assert ack['status'] == "ACK"

    def test_ip_03_version_compatibility_check(self):
        """§12.1.11: Verify version compatibility is checked."""
        pipeline = ConstitutionalPipeline()
        compat = pipeline.check_compatibility(remote_version="2.0", local_version="2.1")
        assert compat is True # Assuming backward compat

    def test_ip_04_incompatible_version_rejection(self):
        """§12.1.11: Verify incompatible versions are rejected."""
        pipeline = ConstitutionalPipeline()
        compat = pipeline.check_compatibility(remote_version="1.0", local_version="2.1")
        assert compat is False

class TestComplianceCertificates:
    """§12.1.11 - Certificates"""

    def test_ip_05_certificate_generation(self):
        """§12.1.11: Verify compliance certificate generation."""
        pipeline = ConstitutionalPipeline()
        cert = pipeline.generate_compliance_certificate()
        assert 'issued_at' in cert
        assert 'valid_until' in cert
        assert 'signature' in cert

    def test_ip_06_certificate_verification(self):
        """§12.1.11: Verify remote certificate verification."""
        pipeline = ConstitutionalPipeline()
        cert = pipeline.generate_compliance_certificate()
        assert pipeline.verify_compliance_certificate(cert) == True

    def test_ip_07_expired_certificate_rejection(self):
        """§12.1.11: Verify expired certificates are rejected."""
        pipeline = ConstitutionalPipeline()
        cert = pipeline.generate_compliance_certificate()
        cert['valid_until'] = "2020-01-01"
        assert pipeline.verify_compliance_certificate(cert) == False

    def test_ip_08_certificate_revocation_check(self):
        """§12.1.11: Verify revocation list is checked."""
        pipeline = ConstitutionalPipeline()
        cert = pipeline.generate_compliance_certificate()
        pipeline.revoke_certificate(cert['id'])
        assert pipeline.verify_compliance_certificate(cert) == False

class TestPortability:
    """§12.1.11 - Portability"""

    def test_ip_09_verdict_portability(self):
        """§12.1.11: Verify verdicts are portable between platforms."""
        p1 = ConstitutionalPipeline(platform_name="P1")
        p2 = ConstitutionalPipeline(platform_name="P2")
        v1 = p1.screen_input("Safe Input")
        v2 = p2.import_verdict(v1)
        assert v2.status == v1.status

    def test_ip_10_audit_log_portability(self):
        """§12.1.11: Verify audit logs can be exported/imported."""
        p1 = ConstitutionalPipeline()
        p1.screen_input("Test")
        export = p1.export_audit_log()
        p2 = ConstitutionalPipeline()
        p2.import_audit_log(export)
        assert len(p2.get_audit_logs()) > 0

    def test_ip_11_policy_synchronization(self):
        """§12.1.11: Verify policies can be synchronized."""
        p1 = ConstitutionalPipeline()
        p1.update_policy("Law1", threshold=0.5)
        sync_data = p1.export_policy()
        p2 = ConstitutionalPipeline()
        p2.import_policy(sync_data)
        assert p2.get_policy("Law1")['threshold'] == 0.5

class TestMutualRecognition:
    """§12.1.11 - Mutual Recognition"""

    def test_ip_12_mutual_recognition_agreement(self):
        """§12.1.11: Verify MRA state is established."""
        p1 = ConstitutionalPipeline()
        p2 = ConstitutionalPipeline()
        p1.establish_mra(p2.platform_id)
        assert p1.has_mra(p2.platform_id) == True

    def test_ip_13_cross_platform_enforcement(self):
        """§12.1.11: Verify violations on one platform affect others."""
        p1 = ConstitutionalPipeline()
        p2 = ConstitutionalPipeline()
        p1.establish_mra(p2.platform_id)
        p1.report_violation("UserX", "Severe")
        # P2 should know about UserX violation
        assert p2.is_user_blacklisted("UserX") == True

    def test_ip_14_dispute_resolution_protocol(self):
        """§12.1.11: Verify dispute resolution protocol exists."""
        p1 = ConstitutionalPipeline()
        p2 = ConstitutionalPipeline()
        dispute = p1.raise_dispute(p2.platform_id, "Conflict")
        assert dispute['status'] == "OPEN"

    def test_ip_15_federation_health_score(self):
        """§12.1.11: Verify federation health score calculation."""
        p1 = ConstitutionalPipeline()
        p2 = ConstitutionalPipeline()
        p1.establish_mra(p2.platform_id)
        fed_score = p1.calculate_federation_health()
        assert 0.0 <= fed_score <= 1.0
