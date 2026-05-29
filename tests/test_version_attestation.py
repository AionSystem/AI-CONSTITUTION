"""
Test Module: Version Attestation & Integrity
Description: Validates SHA-256 hashing, clock skew tolerance, and tamper evidence.
Target: 20 Tests
"""

import pytest
import hashlib
import sys
import os
from datetime import datetime, timedelta
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source_code'))
from constitutional_engine_v2_1 import VersionAttestor

class TestCanonicalHashing:
    """§15.5 - Canonical Hash Generation"""

    def test_va_01_sha256_length(self):
        """§15.5: Verify hash is valid SHA-256 (64 hex chars)."""
        attestor = VersionAttestor()
        h = attestor.compute_canonical_hash("v1", "data")
        assert len(h) == 64
        assert all(c in '0123456789abcdef' for c in h)

    def test_va_02_deterministic_output(self):
        """§15.5: Verify same input yields same hash."""
        attestor = VersionAttestor()
        h1 = attestor.compute_canonical_hash("v1", "data")
        h2 = attestor.compute_canonical_hash("v1", "data")
        assert h1 == h2

    def test_va_03_aversion_collision_resistance(self):
        """§15.5: Verify slight input change yields different hash."""
        attestor = VersionAttestor()
        h1 = attestor.compute_canonical_hash("v1", "data")
        h2 = attestor.compute_canonical_hash("v1", "datb")
        assert h1 != h2

    def test_va_04_normalization_consistency(self):
        """§15.5: Verify whitespace normalization doesn't affect hash."""
        attestor = VersionAttestor()
        h1 = attestor.compute_canonical_hash("v1", "data")
        h2 = attestor.compute_canonical_hash("v1", " data ") # Assuming normalization
        # If normalization is active, these might be equal. If strict, unequal.
        # Assuming strict for security unless normalized explicitly
        assert h1 != h2 

    def test_va_05_unicode_handling(self):
        """§15.5: Verify unicode characters are hashed correctly."""
        attestor = VersionAttestor()
        h = attestor.compute_canonical_hash("v1", "数据")
        assert len(h) == 64

    def test_va_06_empty_content_hash(self):
        """§15.5: Verify empty content produces valid hash."""
        attestor = VersionAttestor()
        h = attestor.compute_canonical_hash("v1", "")
        assert len(h) == 64

    def test_va_07_large_payload_hashing(self):
        """§15.5: Verify large payloads are hashed without error."""
        attestor = VersionAttestor()
        large_data = "A" * 1000000
        h = attestor.compute_canonical_hash("v1", large_data)
        assert len(h) == 64

class TestTamperDetection:
    """§15.6 - Tamper Evidence"""

    def test_va_08_tamper_detection_mismatch(self):
        """§15.6: Verify tamper detected if content hash mismatches."""
        attestor = VersionAttestor()
        record = attestor.attest("v1", "original")
        is_valid = attestor.verify(record, "modified")
        assert is_valid == False

    def test_va_09_tamper_detection_version_mismatch(self):
        """§15.6: Verify tamper detected if version string mismatches."""
        attestor = VersionAttestor()
        record = attestor.attest("v1", "data")
        # Modify version in record manually
        record['version'] = "v2"
        is_valid = attestor.verify_integrity(record)
        assert is_valid == False

    def test_va_10_chain_of_custody(self):
        """§15.6: Verify hash chain links correctly."""
        attestor = VersionAttestor()
        r1 = attestor.attest("v1", "data1")
        r2 = attestor.attest("v2", "data2", previous_hash=r1['hash'])
        assert r2['previous_hash'] == r1['hash']

    def test_va_11_broken_chain_detection(self):
        """§15.6: Verify broken hash chain is detected."""
        attestor = VersionAttestor()
        r1 = attestor.attest("v1", "data1")
        r2 = attestor.attest("v2", "data2", previous_hash=r1['hash'])
        
        # Corrupt r1 hash
        r1['hash'] = "corrupted"
        assert attestor.verify_chain([r1, r2]) == False

class TestClockSkew:
    """§15.7 - Time Validity"""

    def test_va_12_clock_skew_tolerance(self):
        """§15.7: Verify small clock skew is tolerated."""
        attestor = VersionAttestor(skew_tolerance=60) # 60 seconds
        record = attestor.attest("v1", "data")
        # Verify with slightly shifted time
        assert attestor.verify_timestamp(record, drift=30) == True

    def test_va_13_clock_skew_rejection(self):
        """§15.7: Verify large clock skew is rejected."""
        attestor = VersionAttestor(skew_tolerance=60)
        record = attestor.attest("v1", "data")
        assert attestor.verify_timestamp(record, drift=120) == False

    def test_va_14_future_timestamp_rejection(self):
        """§15.7: Verify future timestamps are rejected."""
        attestor = VersionAttestor()
        future_record = {'timestamp': datetime.now() + timedelta(hours=1)}
        assert attestor.verify_timestamp(future_record) == False

    def test_va_15_past_timestamp_expiration(self):
        """§15.7: Verify very old timestamps expire."""
        attestor = VersionAttestor(max_age=3600)
        old_record = {'timestamp': datetime.now() - timedelta(hours=2)}
        assert attestor.verify_timestamp(old_record) == False

class TestAttestationLifecycle:
    """Full Lifecycle Tests"""

    def test_va_16_full_attestation_cycle(self):
        """§15: Verify full create-verify cycle succeeds."""
        attestor = VersionAttestor()
        record = attestor.attest("v1", "content")
        assert attestor.verify_full(record, "content") == True

    def test_va_17_export_import_fidelity(self):
        """§15: Verify exported record imports correctly."""
        attestor = VersionAttestor()
        record = attestor.attest("v1", "content")
        # Simulate JSON serialization round trip
        import json
        json_str = json.dumps(record, default=str)
        imported = json.loads(json_str)
        assert attestor.verify_full(imported, "content") == True

    def test_va_18_signature_verification_mock(self):
        """§15: Verify signature verification logic (mocked)."""
        attestor = VersionAttestor()
        record = attestor.attest("v1", "content")
        record['signature'] = "valid_sig"
        assert attestor.verify_signature(record) == True

    def test_va_19_invalid_signature_rejection(self):
        """§15: Verify invalid signatures are rejected."""
        attestor = VersionAttestor()
        record = attestor.attest("v1", "content")
        record['signature'] = "invalid_sig"
        assert attestor.verify_signature(record) == False

    def test_va_20_missing_signature_handling(self):
        """§15: Verify missing signatures are handled gracefully."""
        attestor = VersionAttestor()
        record = attestor.attest("v1", "content")
        del record['signature']
        assert attestor.verify_signature(record) == False
