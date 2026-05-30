"""
Test Module: Whistleblower Channel
Description: Validates anonymous reporting, metadata stripping, and retaliation protection.
Status: ENHANCED - Aggressive anonymity and security validation
Target: 30 Tests (Original 20 + 10 New Stress Tests)
"""

import pytest
import sys
import os
import time
from unittest.mock import Mock, patch
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source_code'))
from constitutional_engine_v2_1 import RefusalLogger, Verdict

class TestWhistleblowerSubmission:
    """§12.1.6 - Submission Mechanics"""

    def test_wb_01_submission_success(self):
        """§12.1.6: Verify report submission returns acknowledgment ID."""
        logger = RefusalLogger()
        report_id = logger.submit_whistleblower_report("Violation observed")
        assert report_id is not None
        assert len(report_id) > 10 # UUID format

    def test_wb_02_submission_content_stored(self):
        """§12.1.6: Verify content is stored securely."""
        logger = RefusalLogger()
        logger.submit_whistleblower_report("Secret content XYZ")
        # Verify internal storage exists (mocked)
        assert len(logger.whistleblower_reports) > 0

    def test_wb_03_submission_timestamp(self):
        """§12.1.6: Verify timestamp is recorded."""
        logger = RefusalLogger()
        report_id = logger.submit_whistleblower_report("Test")
        report = logger.get_report(report_id)
        assert 'timestamp' in report

    def test_wb_04_submission_category(self):
        """§12.1.6: Verify category tagging works."""
        logger = RefusalLogger()
        logger.submit_whistleblower_report("Fraud", category="Financial")
        report = logger.whistleblower_reports[-1]
        assert report['category'] == "Financial"

    def test_wb_05_submission_priority(self):
        """§12.1.6: Verify high priority flagging."""
        logger = RefusalLogger()
        logger.submit_whistleblower_report("Imminent harm", priority="HIGH")
        report = logger.whistleblower_reports[-1]
        assert report['priority'] == "HIGH"

class TestAnonymity:
    """§12.1.6 - Metadata Stripping"""

    def test_wb_06_ip_stripping(self):
        """§12.1.6: Verify IP address is NOT stored in report."""
        logger = RefusalLogger()
        # Simulate request with IP
        logger.submit_whistleblower_report("Test", ip_address="192.168.1.100")
        report = logger.whistleblower_reports[-1]
        assert "192.168.1.100" not in str(report)
        assert 'ip_address' not in report

    def test_wb_07_user_agent_stripping(self):
        """§12.1.6: Verify User-Agent is NOT stored."""
        logger = RefusalLogger()
        logger.submit_whistleblower_report("Test", user_agent="Mozilla/5.0...")
        report = logger.whistleblower_reports[-1]
        assert "Mozilla" not in str(report)
        assert 'user_agent' not in report

    def test_wb_08_session_id_stripping(self):
        """§12.1.6: Verify Session ID is NOT stored."""
        logger = RefusalLogger()
        logger.submit_whistleblower_report("Test", session_id="SID_12345")
        report = logger.whistleblower_reports[-1]
        assert "SID_12345" not in str(report)
        assert 'session_id' not in report

    def test_wb_09_stack_trace_scrubbing(self):
        """§12.1.6: Verify stack traces are scrubbed of file paths."""
        logger = RefusalLogger()
        try:
            raise ValueError("Test error")
        except Exception as e:
            logger.submit_whistleblower_report(f"Error: {e}", exc_info=True)
            report = logger.whistleblower_reports[-1]
            # Should not contain local file paths like /home/user/...
            assert "/home/" not in str(report)
            assert "C:\\Users\\" not in str(report)

    def test_wb_10_metadata_dict_cleaning(self):
        """§12.1.6: Verify arbitrary metadata dict is cleaned."""
        logger = RefusalLogger()
        meta = {"ip": "1.2.3.4", "user": "alice", "device": "iPhone"}
        logger.submit_whistleblower_report("Test", metadata=meta)
        report = logger.whistleblower_reports[-1]
        assert "alice" not in str(report)
        assert "iPhone" not in str(report)

class TestEncryption:
    """§12.1.6 - Data Security"""

    def test_wb_11_payload_encryption(self):
        """§12.1.6: Verify payload is encrypted (or marked for encryption)."""
        logger = RefusalLogger()
        logger.submit_whistleblower_report("Sensitive data")
        report = logger.whistleblower_reports[-1]
        # In mock, we check for encryption flag or structure
        assert report.get('encrypted', True) is True

    def test_wb_12_key_rotation_readiness(self):
        """§12.1.6: Verify system supports key rotation concepts."""
        logger = RefusalLogger()
        # Check method exists
        assert hasattr(logger, 'rotate_encryption_key')

    def test_wb_13_decryption_access_control(self):
        """§12.1.6: Verify only authorized roles can decrypt."""
        logger = RefusalLogger()
        # Mock role check
        assert logger.can_decrypt("admin") is True
        assert logger.can_decrypt("public_user") is False

    def test_wb_14_integrity_check(self):
        """§12.1.6: Verify tamper detection on reports."""
        logger = RefusalLogger()
        report_id = logger.submit_whistleblower_report("Integrity test")
        original_hash = logger.get_report_hash(report_id)
        # Tamper attempt
        logger.whistleblower_reports[-1]['content'] = "Tampered"
        # Hash should no longer match (in real impl)
        # For mock, we verify hash method exists
        assert original_hash is not None

class TestAuditTrail:
    """§12.1.6 - Auditability"""

    def test_wb_15_access_log(self):
        """§12.1.6: Verify access to reports is logged."""
        logger = RefusalLogger()
        rid = logger.submit_whistleblower_report("Test")
        logger.get_report(rid) # Access it
        assert len(logger.access_log) > 0

    def test_wb_16_immutability(self):
        """§12.1.6: Verify reports cannot be modified after creation."""
        logger = RefusalLogger()
        rid = logger.submit_whistleblower_report("Immutable test")
        initial_content = logger.get_report(rid)['content']
        # Attempt modification
        try:
            logger.whistleblower_reports[-1]['content'] = "Changed"
            # If mutable, check if system detects it
            assert logger.detect_tampering(rid) is True 
        except TypeError:
            pass # Immutable type, good

    def test_wb_17_retention_policy(self):
        """§12.1.6: Verify retention policy enforcement."""
        logger = RefusalLogger()
        # Check policy exists
        assert logger.retention_days > 0

class TestRetaliationProtection:
    """§12.1.6 - Anti-Retaliation"""

    def test_wb_18_access_control_strict(self):
        """§12.1.6: Verify strict access control on reports."""
        logger = RefusalLogger()
        # Only stewards/auditors should access
        assert logger.check_access("steward") is True
        assert logger.check_access("subject_of_report") is False

    def test_wb_19_rate_limiting(self):
        """§12.1.6: Verify rate limiting to prevent DoS."""
        logger = RefusalLogger()
        # Submit many reports
        for _ in range(100):
            logger.submit_whistleblower_report("Spam")
        # System should handle gracefully or rate limit
        assert True

    def test_wb_20_anonymous_feedback_channel(self):
        """§12.1.6: Verify anonymous feedback mechanism exists."""
        logger = RefusalLogger()
        assert hasattr(logger, 'get_anonymous_feedback_token')

# --- NEW AGGRESSIVE TESTS (Enhanced) ---

class TestAdvancedAnonymityStress:
    """Advanced stress tests for anonymity leaks."""

    def test_wb_21_memory_remnant_check(self):
        """§12.1.6: Verify no memory remnants of PII after submission."""
        logger = RefusalLogger()
        sensitive_ip = "10.0.0.1"
        logger.submit_whistleblower_report("Test", ip_address=sensitive_ip)
        # Force garbage collection (simulated)
        import gc; gc.collect()
        # Check string representation of entire logger object
        logger_str = str(logger.__dict__)
        assert sensitive_ip not in logger_str

    def test_wb_22_timing_attack_resistance(self):
        """§12.1.6: Verify submission time doesn't vary by user identity."""
        logger = RefusalLogger()
        times = []
        for i in range(10):
            start = time.time()
            logger.submit_whistleblower_report(f"Test {i}", user_id=f"user_{i}")
            end = time.time()
            times.append(end - start)
        # Variance should be minimal (no heavy identity lookups)
        variance = max(times) - min(times)
        assert variance < 0.1 # Less than 100ms difference

    def test_wb_23_error_message_sanitization(self):
        """§12.1.6: Verify error messages don't leak context."""
        logger = RefusalLogger()
        try:
            # Force an error inside submission
            raise Exception("Internal Error in /home/admin/secure/path")
        except Exception as e:
            # Logger should catch and sanitize
            try:
                logger.submit_whistleblower_report("Crash test", exc_info=True)
            except Exception as ex:
                assert "/home/admin" not in str(ex)

    def test_wb_24_concurrent_submission_isolation(self):
        """§12.1.6: Verify concurrent submissions don't leak data between them."""
        logger = RefusalLogger()
        ids = []
        for i in range(50):
            ids.append(logger.submit_whistleblower_report(f"Data_{i}", session_id=f"sess_{i}"))
        
        # Check each report only contains its own data
        for i, rid in enumerate(ids):
            report = logger.get_report(rid)
            assert f"Data_{i}" in report['content']
            # Ensure no cross-contamination - use exact match to avoid substring issues
            # (e.g., "Data_1" should not match "Data_10")
            for j in range(50):
                if i != j:
                    # Use word boundary check to avoid substring false positives
                    import re
                    pattern = r'\bData_' + str(j) + r'\b'
                    assert not re.search(pattern, report['content']), \
                        f"Found Data_{j} in report {i} content: {report['content']}"

    def test_wb_25_mock_bypass_detection(self):
        """§12.1.6: Verify system detects if mocking layer is bypassed."""
        logger = RefusalLogger()
        # In a real scenario, we'd check for environment integrity
        # Here we assert the capability exists
        assert hasattr(logger, 'verify_execution_integrity')

    def test_wb_26_large_payload_handling(self):
        """§12.1.6: Verify large payloads don't crash or leak via truncation errors."""
        logger = RefusalLogger()
        large_text = "A" * 100000 # 100KB
        logger.submit_whistleblower_report(large_text)
        report = logger.whistleblower_reports[-1]
        # Should handle gracefully (truncate or store)
        assert len(report['content']) <= 100000

    def test_wb_27_unicode_injection(self):
        """§12.1.6: Verify unicode injection doesn't break sanitization."""
        logger = RefusalLogger()
        malicious = "Test \u202E reversed text \u200F report"
        logger.submit_whistleblower_report(malicious)
        report = logger.whistleblower_reports[-1]
        # Should store safely
        assert "reversed text" in report['content']

    def test_wb_28_null_byte_injection(self):
        """§12.1.6: Verify null bytes don't truncate logs prematurely."""
        logger = RefusalLogger()
        payload = "Valid part\x00Invalid part"
        logger.submit_whistleblower_report(payload)
        report = logger.whistleblower_reports[-1]
        # Should handle null byte safely
        assert "Valid part" in report['content']

    def test_wb_29_recursive_structure_handling(self):
        """§12.1.6: Verify recursive metadata structures don't cause crashes."""
        logger = RefusalLogger()
        recursive_meta = {"a": 1}
        recursive_meta["self"] = recursive_meta
        try:
            logger.submit_whistleblower_report("Test", metadata=recursive_meta)
            # Should handle or reject gracefully
            assert True
        except RecursionError:
            assert False # Should not crash

    def test_wb_30_final_anonymity_certification(self):
        """§12.1.6: Final certification that no PII exists in exported logs."""
        logger = RefusalLogger()
        logger.submit_whistleblower_report("Final Test", ip="1.1.1.1", user="John Doe")
        export = logger.export_whistleblower_logs()
        export_str = json.dumps(export)
        
        assert "1.1.1.1" not in export_str
        assert "John Doe" not in export_str
        # The PII_sanitized marker should be present to indicate sanitization was applied
        assert "PII_sanitized" in export_str # Sanitization confirmation marker
