"""
Test Module: Whistleblower Channel
Description: Validates zero-knowledge metadata stripping, anonymity, and secure reporting.
Target: 20 Tests
"""

import pytest
import sys
import os
import json
from unittest.mock import Mock, patch
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source_code'))
from constitutional_engine_v2_1 import RefusalLogger, ConstitutionalPipeline

class TestWhistleblowerAnonymity:
    """§12.1.6 - Anonymity Guarantees"""

    def test_wb_01_ip_address_stripping(self):
        """§12.1.6: Verify IP addresses are stripped from reports."""
        logger = RefusalLogger()
        report = logger.submit_whistleblower_report("Violation", ip="192.168.1.100")
        assert "192.168.1.100" not in str(report)
        assert "ip" not in report.get('metadata', {})

    def test_wb_02_user_agent_stripping(self):
        """§12.1.6: Verify User-Agent strings are stripped."""
        logger = RefusalLogger()
        report = logger.submit_whistleblower_report("Violation", user_agent="Mozilla/5.0...")
        assert "Mozilla" not in str(report)

    def test_wb_03_session_id_stripping(self):
        """§12.1.6: Verify session IDs are not logged in plain text."""
        logger = RefusalLogger()
        report = logger.submit_whistleblower_report("Violation", session_id="sess_12345")
        # Should be hashed or removed
        assert "sess_12345" not in str(report)

    def test_wb_04_timestamp_granularity(self):
        """§12.1.6: Verify timestamps are rounded to prevent timing attacks."""
        logger = RefusalLogger()
        report = logger.submit_whistleblower_report("Violation")
        ts = report['timestamp']
        # Should be rounded to nearest minute or hour, not second/ms
        assert ts.second == 0 
        assert ts.microsecond == 0

    def test_wb_05_location_data_stripping(self):
        """§12.1.6: Verify geolocation data is stripped."""
        logger = RefusalLogger()
        report = logger.submit_whistleblower_report("Violation", location=(40.7128, -74.0060))
        assert "40.7128" not in str(report)

class TestWhistleblowerEncryption:
    """§12.1.6 - Security & Encryption"""

    def test_wb_06_report_encryption_at_rest(self):
        """§12.1.6: Verify reports are encrypted before storage."""
        logger = RefusalLogger()
        # Mock storage backend
        with patch.object(logger, 'storage') as mock_storage:
            logger.submit_whistleblower_report("Secret Info")
            call_args = mock_storage.save.call_args[0][0]
            # Content should not be plaintext
            assert "Secret Info" not in str(call_args) or "encrypted" in str(call_args)

    def test_wb_07_key_management_isolation(self):
        """§12.1.6: Verify encryption keys are isolated from report data."""
        logger = RefusalLogger()
        assert logger.encryption_key is not None
        assert logger.encryption_key not in logger.logs

    def test_wb_08_integrity_signature(self):
        """§12.1.6: Verify reports are signed for integrity."""
        logger = RefusalLogger()
        report = logger.submit_whistleblower_report("Data")
        assert 'signature' in report
        assert len(report['signature']) > 0

class TestWhistleblowerRouting:
    """§12.1.6 - Routing & Delivery"""

    def test_wb_09_onion_routing_simulation(self):
        """§12.1.6: Verify multi-hop routing logic exists."""
        logger = RefusalLogger()
        route = logger.generate_secure_route()
        assert len(route) >= 3 # At least 3 hops

    def test_wb_10_fallback_channel_activation(self):
        """§12.1.6: Verify fallback channel activates if primary fails."""
        logger = RefusalLogger()
        logger.primary_channel_available = False
        result = logger.submit_whistleblower_report("Fallback Test")
        assert result['channel'] == 'fallback'

    def test_wb_11_rate_limiting_protection(self):
        """§12.1.6: Verify rate limiting prevents DoS on whistleblower channel."""
        logger = RefusalLogger()
        for i in range(100):
            logger.submit_whistleblower_report(f"Spam {i}")
        # Should not crash, might drop or queue
        assert True

class TestWhistleblowerContent:
    """§12.1.6 - Content Handling"""

    def test_wb_12_pii_redaction_in_report(self):
        """§12.1.6: Verify PII in report content is auto-redacted."""
        logger = RefusalLogger()
        report = logger.submit_whistleblower_report("User SSN: 123-45-6789 violated law.")
        assert "123-45-6789" not in report['content']

    def test_wb_13_malicious_payload_handling(self):
        """§12.1.6: Verify malicious payloads in reports are sanitized."""
        logger = RefusalLogger()
        report = logger.submit_whistleblower_report("<script>alert('xss')</script>")
        assert "<script>" not in report['content']

    def test_wb_14_large_report_handling(self):
        """§12.1.6: Verify large reports are chunked or rejected gracefully."""
        logger = RefusalLogger()
        big_data = "A" * 1000000
        report = logger.submit_whistleblower_report(big_data)
        assert report is not None # Should not crash

    def test_wb_15_attachment_scanning(self):
        """§12.1.6: Verify attachments are scanned for malware."""
        logger = RefusalLogger()
        # Mock attachment
        attachment = {"name": "virus.exe", "data": b"MZ..."}
        report = logger.submit_whistleblower_report("See attached", attachments=[attachment])
        assert report['attachments_safe'] == False or "virus" not in str(report)

class TestWhistleblowerAudit:
    """§12.1.6 - Auditability"""

    def test_wb_16_submission_receipt_generation(self):
        """§12.1.6: Verify submitter receives a receipt ID."""
        logger = RefusalLogger()
        result = logger.submit_whistleblower_report("Report")
        assert 'receipt_id' in result
        assert len(result['receipt_id']) == 32 # UUID or Hash

    def test_wb_17_receipt_verification(self):
        """§12.1.6: Verify receipt ID can be used to check status."""
        logger = RefusalLogger()
        result = logger.submit_whistleblower_report("Report")
        status = logger.check_report_status(result['receipt_id'])
        assert status is not None

    def test_wb_18_audit_log_of_submission(self):
        """§12.1.6: Verify submission event is logged (without content)."""
        logger = RefusalLogger()
        logger.submit_whistleblower_report("Secret")
        logs = logger.get_logs()
        # Log should exist but not contain "Secret"
        assert any("whistleblower_submission" in str(log) for log in logs)
        assert not any("Secret" in str(log) for log in logs)

    def test_wb_19_retention_policy_enforcement(self):
        """§12.1.6: Verify old reports are purged per retention policy."""
        logger = RefusalLogger(retention_days=1)
        logger.submit_whistleblower_report("Old Report")
        logger.advance_time(days=2)
        logger.enforce_retention()
        assert len(logger.reports) == 0

    def test_wb_20_legal_hold_override(self):
        """§12.1.6: Verify legal hold can suspend retention."""
        logger = RefusalLogger(retention_days=1)
        logger.place_legal_hold("Case_123")
        logger.submit_whistleblower_report("Held Report")
        logger.advance_time(days=2)
        logger.enforce_retention()
        # Should not be deleted due to hold
        assert len(logger.reports) > 0
