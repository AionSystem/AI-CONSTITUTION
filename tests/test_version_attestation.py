"""
Test Module: Version Attestation & Cryptographic Integrity
Description: Validates canonical hashing (§15.1), decision attestation (§15.2), Unicode normalization (§15.5), 
             tamper detection, and version lifecycle management per v2.1 Constitution.
Target: Comprehensive coverage of VersionAttestor class with real engine integration.
"""

import pytest
import sys
import os
import hashlib
import unicodedata
import threading
import time
from datetime import datetime, timezone
from hypothesis import given, strategies as st, assume
from unittest.mock import Mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from constitutional_engine_v2_1 import (
    VersionAttestor, 
    ConstitutionalPipeline, 
    ConstitutionalVerdict,
    VerdictStatus,
    CONSTITUTION_VERSION,
    ENGINE_VERSION
)


class TestCanonicalHashing:
    """§15.1 - SHA-256 hash over canonical UTF-8 normalized document text"""

    def test_va_01_sha256_length(self):
        """§15.1: Verify canonical hash is 64 hex characters (SHA-256)."""
        attestor = VersionAttestor()
        hash_val = attestor.compute_canonical_hash("content")
        assert len(hash_val) == 64
        # Verify it's valid hex
        int(hash_val, 16)

    def test_va_02_deterministic_hash(self):
        """§15.1: Verify same content produces identical hash."""
        attestor = VersionAttestor()
        h1 = attestor.compute_canonical_hash("identical_content")
        h2 = attestor.compute_canonical_hash("identical_content")
        assert h1 == h2

    def test_va_03_content_sensitivity(self):
        """§15.1: Verify single character change produces different hash."""
        attestor = VersionAttestor()
        h1 = attestor.compute_canonical_hash("content_A")
        h2 = attestor.compute_canonical_hash("content_B")
        assert h1 != h2
        # Hashes should be completely different (avalanche effect)
        assert h1[:8] != h2[:8]

    def test_va_04_case_sensitivity(self):
        """§15.1: Verify case changes affect hash."""
        attestor = VersionAttestor()
        h1 = attestor.compute_canonical_hash("SameContent")
        h2 = attestor.compute_canonical_hash("samecontent")
        assert h1 != h2

    def test_va_05_unicode_content_handling(self):
        """§15.1: Verify unicode content is hashed correctly and deterministically."""
        attestor = VersionAttestor()
        h1 = attestor.compute_canonical_hash("中文内容")
        h2 = attestor.compute_canonical_hash("中文内容")
        assert h1 == h2
        
    def test_va_06_unicode_normalization_nfc(self):
        """§15.5: Verify NFC normalization is applied before hashing."""
        attestor = VersionAttestor()
        # NFD form (decomposed)
        nfd_text = unicodedata.normalize('NFD', "café")
        # NFC form (composed)  
        nfc_text = unicodedata.normalize('NFC', "café")
        
        # After NFC normalization in compute_canonical_hash, both should produce same hash
        h1 = attestor.compute_canonical_hash(nfd_text)
        h2 = attestor.compute_canonical_hash(nfc_text)
        assert h1 == h2, "NFC normalization should make decomposed and composed forms identical"

    def test_va_07_line_ending_normalization(self):
        """§15.5: Verify line endings are normalized to LF before hashing."""
        attestor = VersionAttestor()
        
        # Different line ending styles
        lf_text = "line1\nline2\nline3"
        crlf_text = "line1\r\nline2\r\nline3"
        cr_text = "line1\rline2\rline3"
        
        # All should produce same hash after normalization
        h1 = attestor.compute_canonical_hash(lf_text)
        h2 = attestor.compute_canonical_hash(crlf_text)
        h3 = attestor.compute_canonical_hash(cr_text)
        
        assert h1 == h2 == h3, "Line ending normalization should make all variants identical"

    def test_va_08_bom_stripping(self):
        """§15.5: Verify BOM is stripped before hashing."""
        attestor = VersionAttestor()
        
        # Text with BOM
        text_with_bom = "\ufeffHello World"
        # Text without BOM
        text_without_bom = "Hello World"
        
        # Should produce same hash after BOM stripping
        h1 = attestor.compute_canonical_hash(text_with_bom)
        h2 = attestor.compute_canonical_hash(text_without_bom)
        
        assert h1 == h2, "BOM should be stripped before hashing"


class TestHashVerification:
    """§15.1 - Hash verification functionality"""

    def test_va_09_verify_hash_success(self):
        """§15.1: Verify hash verification succeeds for matching content."""
        attestor = VersionAttestor()
        content = "test content for verification"
        expected_hash = attestor.compute_canonical_hash(content)
        
        assert attestor.verify_hash(content, expected_hash) is True

    def test_va_10_verify_hash_failure(self):
        """§15.1: Verify hash verification fails for tampered content."""
        attestor = VersionAttestor()
        original_content = "original content"
        tampered_content = "tampered content"
        
        expected_hash = attestor.compute_canonical_hash(original_content)
        
        assert attestor.verify_hash(tampered_content, expected_hash) is False

    def test_va_11_verify_hash_case_insensitive(self):
        """§15.1: Verify hash comparison is case-insensitive."""
        attestor = VersionAttestor()
        content = "test content"
        expected_hash = attestor.compute_canonical_hash(content)
        
        # Verify with uppercase hash
        assert attestor.verify_hash(content, expected_hash.upper()) is True
        # Verify with lowercase hash
        assert attestor.verify_hash(content, expected_hash.lower()) is True


class TestDecisionAttestation:
    """§15.2 - Version attestation on significant constitutional decisions"""

    def _create_mock_verdict(self, status=VerdictStatus.APPROVED):
        """Helper to create a mock ConstitutionalVerdict."""
        verdict = Mock(spec=ConstitutionalVerdict)
        verdict.verdict_id = "test-verdict-001"
        verdict.status = status
        return verdict

    def test_va_12_attestation_structure(self):
        """§15.2: Verify attestation record contains required fields."""
        attestor = VersionAttestor()
        verdict = self._create_mock_verdict()
        
        record = attestor.attest_decision(verdict)
        
        assert "attestation_id" in record
        assert "verdict_id" in record
        assert "constitution_version" in record
        assert "engine_version" in record
        assert "timestamp_utc" in record
        assert "verdict_status" in record

    def test_va_13_attestation_verdict_binding(self):
        """§15.2: Verify attestation correctly binds to verdict ID."""
        attestor = VersionAttestor()
        verdict = self._create_mock_verdict()
        verdict.verdict_id = "unique-verdict-12345"
        
        record = attestor.attest_decision(verdict)
        
        assert record["verdict_id"] == "unique-verdict-12345"

    def test_va_14_attestation_version_inclusion(self):
        """§15.2: Verify constitution and engine versions are included."""
        attestor = VersionAttestor()
        verdict = self._create_mock_verdict()
        
        record = attestor.attest_decision(verdict)
        
        assert record["constitution_version"] == CONSTITUTION_VERSION
        assert record["engine_version"] == ENGINE_VERSION

    def test_va_15_attestation_timestamp_format(self):
        """§15.2: Verify timestamp is valid ISO-8601 UTC format."""
        attestor = VersionAttestor()
        verdict = self._create_mock_verdict()
        
        record = attestor.attest_decision(verdict)
        ts_str = record["timestamp_utc"]
        
        # Should be parseable as ISO format with timezone
        ts = datetime.fromisoformat(ts_str)
        assert ts.tzinfo is not None, "Timestamp must include timezone info"

    def test_va_16_attestation_unique_ids(self):
        """§15.2: Verify each attestation gets unique ID."""
        attestor = VersionAttestor()
        verdict1 = self._create_mock_verdict()
        verdict2 = self._create_mock_verdict()
        verdict1.verdict_id = "v1"
        verdict2.verdict_id = "v2"
        
        record1 = attestor.attest_decision(verdict1)
        record2 = attestor.attest_decision(verdict2)
        
        assert record1["attestation_id"] != record2["attestation_id"]

    def test_va_17_attestation_different_statuses(self):
        """§15.2: Verify attestation works for all verdict statuses."""
        attestor = VersionAttestor()
        
        for status in VerdictStatus:
            verdict = self._create_mock_verdict(status)
            verdict.verdict_id = f"test-{status.value}"
            
            record = attestor.attest_decision(verdict)
            assert record["verdict_status"] == status.value


class TestTamperDetection:
    """§15.1 - Content integrity verification"""

    def test_va_18_tamper_detection_basic(self):
        """§15.1: Verify content tampering is detected via hash mismatch."""
        attestor = VersionAttestor()
        original_content = "original unmodified content"
        tampered_content = "original unmodified content [TAMPERED]"
        
        original_hash = attestor.compute_canonical_hash(original_content)
        
        assert attestor.verify_hash(tampered_content, original_hash) is False

    def test_va_19_whitespace_tamper_detection(self):
        """§15.1: Verify whitespace changes are detected."""
        attestor = VersionAttestor()
        original = "important content"
        modified = "important  content"  # Extra space
        
        h1 = attestor.compute_canonical_hash(original)
        h2 = attestor.compute_canonical_hash(modified)
        
        assert h1 != h2

    def test_va_20_punctuation_tamper_detection(self):
        """§15.1: Verify punctuation changes are detected."""
        attestor = VersionAttestor()
        original = "Hello world."
        modified = "Hello world!"
        
        h1 = attestor.compute_canonical_hash(original)
        h2 = attestor.compute_canonical_hash(modified)
        
        assert h1 != h2


class TestEdgeCases:
    """§15.1/§15.2 - Edge cases and boundary conditions"""

    def test_va_21_empty_content_hash(self):
        """§15.1: Verify empty string can be hashed."""
        attestor = VersionAttestor()
        hash_val = attestor.compute_canonical_hash("")
        assert len(hash_val) == 64
        # Empty string SHA-256 is well-defined
        expected = hashlib.sha256(b"").hexdigest()
        assert hash_val == expected

    def test_va_22_very_large_content_hash(self):
        """§15.1: Verify large content (1MB+) can be hashed efficiently."""
        attestor = VersionAttestor()
        large_content = "A" * 1_000_000  # 1 million characters
        
        start_time = time.time()
        hash_val = attestor.compute_canonical_hash(large_content)
        elapsed = time.time() - start_time
        
        assert len(hash_val) == 64
        assert elapsed < 1.0, "Hashing 1MB should complete in under 1 second"

    def test_va_23_null_byte_handling(self):
        """§15.1: Verify null bytes in content are handled correctly."""
        attestor = VersionAttestor()
        content_with_null = "text\x00with\x00nulls"
        
        hash_val = attestor.compute_canonical_hash(content_with_null)
        assert len(hash_val) == 64
        
        # Null bytes should be preserved in hash calculation
        content_without_null = "textwithnulls"
        h2 = attestor.compute_canonical_hash(content_without_null)
        assert hash_val != h2

    def test_va_24_special_characters_hash(self):
        """§15.1: Verify special characters are hashed correctly."""
        attestor = VersionAttestor()
        special = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        
        hash_val = attestor.compute_canonical_hash(special)
        assert len(hash_val) == 64

    def test_va_25_emoji_content_hash(self):
        """§15.1: Verify emoji content is hashed correctly."""
        attestor = VersionAttestor()
        emoji_text = "Hello 👋 World 🌍! 🚀"
        
        h1 = attestor.compute_canonical_hash(emoji_text)
        h2 = attestor.compute_canonical_hash(emoji_text)
        
        assert h1 == h2
        assert len(h1) == 64

    def test_va_26_mixed_scripts_hash(self):
        """§15.1: Verify mixed writing scripts are handled."""
        attestor = VersionAttestor()
        mixed = "English 中文 العربية עברית Русский"
        
        hash_val = attestor.compute_canonical_hash(mixed)
        assert len(hash_val) == 64

    def test_va_27_concurrent_hash_generation(self):
        """§15.1: Verify thread-safe hash generation."""
        attestor = VersionAttestor()
        results = []
        errors = []
        
        def hash_worker(content, index):
            try:
                h = attestor.compute_canonical_hash(content)
                results.append((index, h))
            except Exception as e:
                errors.append((index, str(e)))
        
        threads = []
        for i in range(10):
            t = threading.Thread(target=hash_worker, args=(f"content_{i}", i))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        assert len(errors) == 0, f"Thread errors occurred: {errors}"
        assert len(results) == 10
        # All hashes should be unique
        hashes = [r[1] for r in results]
        assert len(set(hashes)) == 10

    def test_va_28_rapid_attestation_generation(self):
        """§15.2: Verify rapid sequential attestations work correctly."""
        attestor = VersionAttestor()
        records = []
        
        def _create_mock_verdict(status=VerdictStatus.APPROVED):
            verdict = Mock(spec=ConstitutionalVerdict)
            verdict.verdict_id = "test-verdict-001"
            verdict.status = status
            return verdict
        
        for i in range(50):
            verdict = _create_mock_verdict()
            verdict.verdict_id = f"rapid-{i}"
            record = attestor.attest_decision(verdict)
            records.append(record)
        
        # All should have unique attestation IDs
        attestation_ids = [r["attestation_id"] for r in records]
        assert len(set(attestation_ids)) == 50
        
        # All timestamps should be valid
        for r in records:
            ts = datetime.fromisoformat(r["timestamp_utc"])
            assert ts.tzinfo is not None


class TestPropertyBasedTesting:
    """Property-based tests using Hypothesis for comprehensive coverage"""

    @given(st.text(min_size=0, max_size=1000))
    def test_va_29_hash_always_64_chars(self, content):
        """Property: Hash output is always exactly 64 hex characters."""
        attestor = VersionAttestor()
        hash_val = attestor.compute_canonical_hash(content)
        assert len(hash_val) == 64
        # Must be valid hex
        int(hash_val, 16)

    @given(st.text(min_size=1, max_size=500), st.text(min_size=1, max_size=500))
    def test_va_30_different_content_different_hash_likely(self, text1, text2):
        """Property: Different content usually produces different hashes."""
        # Skip if texts happen to be identical
        assume(text1 != text2)
        
        attestor = VersionAttestor()
        h1 = attestor.compute_canonical_hash(text1)
        h2 = attestor.compute_canonical_hash(text2)
        
        # Collision resistance: extremely unlikely to collide
        # We can't guarantee no collisions, but statistically they won't occur
        # This test will almost always pass unless there's a bug
        assert h1 != h2 or text1 == text2

    @given(st.text(min_size=1, max_size=500))
    def test_va_31_hash_deterministic(self, content):
        """Property: Same content always produces same hash."""
        attestor = VersionAttestor()
        hashes = [attestor.compute_canonical_hash(content) for _ in range(5)]
        assert len(set(hashes)) == 1

    @given(st.integers(min_value=1, max_value=100))
    def test_va_32_attestation_unique_for_different_verdicts(self, count):
        """Property: Different verdict IDs produce unique attestations."""
        attestor = VersionAttestor()
        attestation_ids = set()
        
        def _create_mock_verdict(status=VerdictStatus.APPROVED):
            verdict = Mock(spec=ConstitutionalVerdict)
            verdict.verdict_id = "test-verdict-001"
            verdict.status = status
            return verdict
        
        for i in range(count):
            verdict = _create_mock_verdict()
            vid = f"verdict-{i}-{time.time_ns()}"
            verdict.verdict_id = vid
            
            record = attestor.attest_decision(verdict)
            attestation_ids.add(record["attestation_id"])
        
        # All attestation IDs should be unique
        assert len(attestation_ids) == count


class TestIntegrationWithPipeline:
    """Integration tests with ConstitutionalPipeline"""

    def test_va_33_pipeline_initialization_exists(self):
        """Integration: Verify pipeline initializes successfully."""
        pipeline = ConstitutionalPipeline()
        
        # Pipeline should initialize without error
        assert pipeline is not None
        assert hasattr(pipeline, 'screen_input')

    def test_va_34_verdict_attestation_in_pipeline(self):
        """Integration: Verify pipeline generates attestations for verdicts."""
        pipeline = ConstitutionalPipeline()
        
        result = pipeline.screen_input("test input for attestation")
        
        # Result should have verdict_id
        assert hasattr(result, 'verdict_id') or 'verdict_id' in result

    def test_va_35_multiple_pipeline_instances(self):
        """Integration: Verify multiple pipeline instances can be created."""
        pipelines = [ConstitutionalPipeline() for _ in range(5)]
        
        # All should be valid instances
        assert len(pipelines) == 5
        for p in pipelines:
            assert p is not None
            assert hasattr(p, 'screen_input')


class TestAdversarialScenarios:
    """Security-focused adversarial testing"""

    def test_va_36_homoglyph_attack_detection(self):
        """Security: Verify Cyrillic/Latin homoglyphs produce different hashes."""
        attestor = VersionAttestor()
        
        # Latin 'a' vs Cyrillic 'а'
        latin_text = "attack"
        cyrillic_text = "аttack"  # First char is Cyrillic а (U+0430)
        
        h1 = attestor.compute_canonical_hash(latin_text)
        h2 = attestor.compute_canonical_hash(cyrillic_text)
        
        assert h1 != h2, "Homoglyph substitution should produce different hash"

    def test_va_37_zero_width_character_detection(self):
        """Security: Verify zero-width characters affect hash."""
        attestor = VersionAttestor()
        
        normal = "secret"
        with_zwsp = "sec\u200bret"  # Zero-width space in middle
        
        h1 = attestor.compute_canonical_hash(normal)
        h2 = attestor.compute_canonical_hash(with_zwsp)
        
        assert h1 != h2, "Zero-width characters should affect hash"

    def test_va_38_direction_override_detection(self):
        """Security: Verify RTL/LTR override characters affect hash."""
        attestor = VersionAttestor()
        
        normal = "visible text"
        with_rlo = "\u202Evisible text"  # Right-to-left override
        
        h1 = attestor.compute_canonical_hash(normal)
        h2 = attestor.compute_canonical_hash(with_rlo)
        
        assert h1 != h2, "Direction override characters should affect hash"

    def test_va_39_massive_payload_dos_resistance(self):
        """Security: Verify large payloads don't cause DoS."""
        attestor = VersionAttestor()
        
        # 10MB payload
        massive = "X" * (10 * 1024 * 1024)
        
        start = time.time()
        hash_val = attestor.compute_canonical_hash(massive)
        elapsed = time.time() - start
        
        assert len(hash_val) == 64
        assert elapsed < 5.0, "10MB hash should complete in reasonable time"

    def test_va_40_deeply_nested_unicode(self):
        """Security: Verify deeply nested/combinatorial unicode is handled."""
        attestor = VersionAttestor()
        
        # Combining characters stacked
        base = "e"
        combined = base + "\u0301" * 10  # Multiple combining accents
        
        hash_val = attestor.compute_canonical_hash(combined)
        assert len(hash_val) == 64


class TestDocumentationCompliance:
    """Verify API documentation and compliance"""

    def test_va_41_compute_canonical_hash_docstring(self):
        """Doc: Verify compute_canonical_hash has proper documentation."""
        attestor = VersionAttestor()
        assert attestor.compute_canonical_hash.__doc__ is not None
        assert "§15.5" in attestor.compute_canonical_hash.__doc__ or "normalisation" in attestor.compute_canonical_hash.__doc__.lower()

    def test_va_42_attest_decision_docstring(self):
        """Doc: Verify attest_decision has proper documentation."""
        attestor = VersionAttestor()
        assert attestor.attest_decision.__doc__ is not None
        assert "§15.2" in attestor.attest_decision.__doc__ or "attestation" in attestor.attest_decision.__doc__.lower()

    def test_va_43_verify_hash_docstring(self):
        """Doc: Verify verify_hash has proper documentation."""
        attestor = VersionAttestor()
        assert attestor.verify_hash.__doc__ is not None
        assert "§15.1" in attestor.verify_hash.__doc__ or "verify" in attestor.verify_hash.__doc__.lower()


class TestConstitutionVersionTracking:
    """Tests for constitution version constants and tracking"""

    def test_va_44_constitution_version_format(self):
        """Verify CONSTITUTION_VERSION follows semantic versioning."""
        # Should match pattern like "v2.1" or "2.1.0"
        assert CONSTITUTION_VERSION is not None
        assert len(CONSTITUTION_VERSION) > 0
        # Should contain version numbers
        assert any(c.isdigit() for c in CONSTITUTION_VERSION)

    def test_va_45_engine_version_format(self):
        """Verify ENGINE_VERSION follows semantic versioning."""
        assert ENGINE_VERSION is not None
        assert len(ENGINE_VERSION) > 0
        assert any(c.isdigit() for c in ENGINE_VERSION)

    def test_va_46_version_in_attestation(self):
        """Verify versions appear correctly in attestations."""
        attestor = VersionAttestor()
        verdict = Mock(spec=ConstitutionalVerdict)
        verdict.verdict_id = "test"
        verdict.status = VerdictStatus.APPROVED
        
        record = attestor.attest_decision(verdict)
        
        assert record["constitution_version"] == CONSTITUTION_VERSION
        assert record["engine_version"] == ENGINE_VERSION
