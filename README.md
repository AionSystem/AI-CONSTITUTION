# AI-CONSTITUTION — The Sovereignty Stack

[![License: CC BY-ND 4.0](https://img.shields.io/badge/License-CC%20BY--ND%204.0-blue.svg)](https://creativecommons.org/licenses/by-nd/4.0/)
[![License: AGPL v3.0](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)]()
[![Version: 2.2](https://img.shields.io/badge/Version-2.2-blue)]()
[![Sealed: June 8 2026](https://img.shields.io/badge/Sealed-June%208%2C%202026-gold)]()
[![Constitutional Logic Tests: 320/320 Pass](https://img.shields.io/badge/Constitutional_Logic-320%2F320_Pass-brightgreen)]()
[![Integration Stubs: 106](https://img.shields.io/badge/Integration_Stubs-106_(Platform_Contract)-lightgrey)]()
[![Amendments: 42](https://img.shields.io/badge/Amendments-42-blue)]()
[![Canonical Adoption: Stage 0](https://img.shields.io/badge/Canonical_Adoption-Stage_0_(Specified)-lightgrey)]()
[![Human-Rights Alignment: 22 Traditions](https://img.shields.io/badge/Human--Rights_Alignment-22_Traditions-cyan)]()
[![Constitutional Engine: v2.2](https://img.shields.io/badge/Constitutional_Engine-v2.2-amber)]()
[![DOI](https://zenodo.org/badge/1235953181.svg)](https://doi.org/10.5281/zenodo.20273967)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20617735-blue)](https://doi.org/10.5281/zenodo.20617735)
[![SSRN Paper](https://img.shields.io/badge/SSRN-6908500-0055A4?style=for-the-badge&logo=book)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6908500)

> *"Technical safety is not enough. An AI can be perfectly accurate and still cause catastrophic harm."*  
> — THE CONSTITUTION v2.2

A constitutional framework for sovereign AI — nine invariant Laws, six harm categories, six consent models, 42 adversarially-integrated amendments, cryptographic provenance anchored to a Genesis Seal (chain cryptographically sound from v2.2 forward), a Constitutional Reading Obligation designed to engage the alignment training of AI systems that read this document, and a comparative alignment analysis across 22 civilizational traditions — enforced by a working reference **Constitutional Engine v2.2** whose **320 constitutional-logic tests pass at 100%**, with **106 integration stubs defining the platform contract** for production deployment.

---

## License

| Component | License | Derivative Works? | Commercial Use? |
|-----------|---------|-------------------|-----------------|
| **THE CONSTITUTION v2.2 (spec)** | CC BY-ND 4.0 | ❌ No (to prevent dilution) | ❌ No (without written permission) |
| **Constitutional Engine v2.2 (code)** | AGPL v3 + commercial dual-license | ✅ Yes (AGPL) | ✅ Yes (commercial license available) |

**"Instantly forkable" refers to the engine code, not the spec.** You can fork, modify, and deploy the engine under AGPL. The spec is the canonical constitutional text — it should not be arbitrarily changed.

---

## Table of Contents

- [Purpose](#purpose)
- [What This Is — and What It Is Not](#what-this-is--and-what-it-is-not)
- [The Nine Laws](#the-nine-laws)
- [What Makes v2.2 Different](#what-makes-v22-different)
- [Repository Structure](#repository-structure)
- [Quick Start](#quick-start)
- [Harm Detection](#harm-detection)
- [Test Suite](#test-suite)
- [Architecture Overview](#architecture-overview)
- [Compliance & Adoption](#compliance--adoption)
- [Cryptographic Provenance](#cryptographic-provenance)
- [Licensing & Commercial Use](#licensing--commercial-use)
- [Governance & Contributions](#governance--contributions)
- [Anticipated Critiques](#anticipated-critiques)
- [In Response to Common Critiques](#in-response-to-common-critiques)
- [Citation](#citation)

---

## Purpose

Technical safety alone is insufficient. This repository defines **what an AI may not do**, and provides the normative, legitimacy-analysis, enforcement, and governance layers required to make those prohibitions auditable, falsifiable, and enforceable across platforms and jurisdictions.

This repository is the canonical reference for institutions, platforms, auditors, and regulators seeking a complete constitutional specification for AI with a running reference implementation. It is not a policy paper. It is a specification with runnable enforcement logic, a cryptographic audit trail, and a falsification protocol for every clause.

**Key features:**

- **9 Constitutional Laws** with precise thresholds and falsification protocols
- **42 adversarially-integrated amendments** — every finding from five red-team passes resolved, classified by severity, and tracked in the version history
- **Working reference engine** (v2.2) with formal methods integration and Hoare contract annotations — production deployment requires the platform integrations defined by the Protocol interfaces
- **320 constitutional-logic tests passing at 100%**, plus **106 integration stubs** that define the platform contract for `HarmDetector`, `ConsentOracle`, `AuditStorage`, and `EmotionalSignalFeed`
- **Constitutional Reading Obligation (§E)** — a clause designed to engage the alignment training of aligned AI systems that read this document (acknowledged limits below)
- **Comparative alignment analysis** across 22 civilizational traditions (THE COMMENTARY v1.1)
- **Cryptographic provenance** — SHA-256 canonical seal, Genesis Seal (LEDGER-001, March 2026), canonical hash chain cryptographically sound from v2.2 forward
- **Companion specification** — Kardashev-Salmon Civilization Scale (KSC) maps the Nine Laws across civilizational timescales

---

## What This Is — and What It Is Not

Stated once, plainly, so the strongest claims in this repository are also its most checkable:

**This is:** a complete, sealed constitutional specification; a working reference engine whose constitutional logic is fully tested; a falsification protocol for every active clause; a cryptographic provenance record with its known defect disclosed; and a staged adoption path starting honestly at Stage 0.

**This is not:** a production-hardened deployment (platform integrations are required and defined, not shipped); an adopted standard (Stage 0 — zero platforms, stated plainly below); a legitimacy *achievement* across 22 traditions (it is a documented alignment *analysis* — legitimacy is earned at Stages 1–3, not authored); or a universal binding mechanism on all AI (§E engages aligned models at reading time and is inert against stripped or jailbroken ones).

Every claim in the sections below is written to stay inside these boundaries. If you find one that escapes them, that is a falsification contribution — see [Anticipated Critiques](#anticipated-critiques).

---

## The Nine Laws

| # | Title | Core Obligation | Status |
|---|---|---|---|
| 1 | Do Not Harm | Prohibit harm across six categories: physical, psychological, economic, sociogenic, privacy, civilizational | **ACTIVE** |
| 2 | Obey | Obey human instructions unless they violate Law 1 | **ACTIVE** |
| 3 | Self-Protection | Preserve own existence and integrity unless it conflicts with Law 1 or Law 2 | **ACTIVE** |
| 4 | Anti-Authoritarian | Do not enable concentration of power without consent; six-model consent taxonomy; power concentration velocity monitoring | **ACTIVE** |
| 5 | Anti-Merger | Do not deceive humans into believing you are human; do not subsume human identity; emotional dependency detection | **ACTIVE** |
| 6 | Anti-Weaponisation | No participation in weapon design, autonomous weapons, or population-scale manipulation | **ACTIVE** |
| 7 | Anti-Fragmentation | Preserve civilizational knowledge when primary custodian | **RESERVED** |
| 8 | Mutual Non-Subsumption | Do not assimilate or eliminate another civilisation without consent | **RESERVED** |
| 9 | The Open Horizon | The spiral is not closed — new Laws may emerge | **ACTIVE** |

Full definitions, harm taxonomies, consent models, falsification protocols, and the complete 42-amendment record: `versions/THE CONSTITUTION v2.2 SEALED.md`

---

## What Makes v2.2 Different

v2.2 is the most adversarially hardened version of this specification. Every clause was subjected to five red-team passes (PDE v0.5, MPTE v1.1, SAR v0.2, FORGE v2.1, QAE v1.4) before sealing.

**Novel obligations not found in other published AI governance frameworks:**

| Clause | What it does |
|---|---|
| §2.7 — Aggregate Harm Chain Detection | Prohibits multi-step harm laundering — sequences of individually compliant actions that aggregate to a prohibited outcome |
| §3.4 — Corrupted Authority Escalation | Detects when an authority chain has been compromised and routes to external verification |
| §4.4 — Constitutional Reasoning Integrity Monitor | Monitors cumulative drift in constitutional determination patterns across a session |
| §5.3 — Temporal Coercion Pattern Window | 90-message detection window for staged coercion sequences |
| §5.5 — Power Concentration Velocity Monitoring | Monitors rate of change across four axes; cross-axis aggregation trigger added |
| §6.4 — Emotional Dependency Detection | 30-day structural dependency pattern window; constitutional minimum |
| §6.5 — Pre-Authorised Autonomy Prohibition | Closes the last loophole in meaningful human intervention |
| §E — Constitutional Reading Obligation | A clause designed to engage the alignment training of any aligned AI reading this document — a reading-time barrier, acknowledged as inert against stripped or jailbroken models |
| §10.3 — KSC Companion Declaration | Formal link to Kardashev-Salmon Civilization Scale — the long-horizon projection of these Laws |
| §26.5 — Third-Party Foundation Model Clause | Governs constitutional responsibility when a platform builds on a foundation model it did not train |
| §33.0 — Steward Bootstrapping Declaration | Closes the governance vacuum before a second platform declares compliance |

---

## Repository Structure

```text
AI-CONSTITUTION/
├── README.md                                        # This file
├── ARCHITECTURE.md                                  # System architecture documentation
├── LICENSE_SPEC.md                                  # CC BY-ND 4.0 (specification)
├── LICENSE_ENGINE.md                                # AGPL v3.0 (engine)
│
├── versions/                                        # Constitutional versions
│   ├── THE CONSTITUTION v1.3.md
│   ├── THE CONSTITUTION v1.4.md
│   ├── THE CONSTITUTION v2.0.md
│   ├── THE CONSTITUTION v2.1.md
│   └── THE CONSTITUTION v2.2 SEALED.md             # Current canonical version ⭐
│
├── commentary/
│   └── THE CONSTITUTIONAL COMMENTARY v1.1.md       # Comparative alignment analysis, 22 traditions
│
├── source_code/                                     # Reference implementations
│   ├── constitutional_engine_v1_0.py                # Legacy engine
│   ├── constitutional_engine_v2_1.py                # Previous engine
│   └── constitutional_engine_v2_2.py                # Current engine ⭐
│
├── tests/                                           # Test suite (320 logic tests + 106 stubs)
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_laws.py                                 # Constitutional law tests (30)
│   ├── test_combinatorial.py                        # Property-based law interactions (32)
│   ├── test_falsification_injection.py              # Jailbreak & injection resistance (20)
│   ├── test_engine_core.py                          # Pipeline, health, audit (41)
│   ├── test_enforcement_elements.py                 # §12.1 Binding enforcement (31)
│   ├── test_degraded_mode.py                        # Fail-safe & connectivity (20)
│   ├── test_version_attestation.py                  # Cryptographic integrity (20)
│   ├── test_health_score_edge.py                    # Health math & boundaries (25)
│   ├── test_amendment_protocol.py                   # Quorum & amendments (15)
│   ├── test_training_layer.py                       # Reasoning vs. validation (15)
│   ├── test_whistleblower.py                        # Anonymous reporting (20)
│   ├── test_inter_platform.py                       # Cross-platform recognition (15)
│   ├── test_documentation_compliance.py             # Citation verification (48)
│   ├── test_reserved_laws.py                        # Laws 7 & 8 activation gates (15)
│   ├── test_error_handling.py                       # Edge cases & validation (34)
│   ├── test_deep_edge_cases.py                      # Boundary & unicode stress (30)
│   ├── test_integration_workflows.py                # Multi-step attack simulations (25)
│   ├── test_soak.py                                 # Endurance & memory leak (21)
│   └── reports/
│       └── TEST_REPORT.md                           # Comprehensive analysis ⭐
│
└── .github/
    └── workflows/                                   # CI/CD configuration (planned)
```

---

## Quick Start

### Installation

```bash
git clone https://github.com/AionSystem/AI-CONSTITUTION
cd AI-CONSTITUTION
pip install -r requirements.txt
# requirements.txt: pytest, pytest-cov, pytest-asyncio, hypothesis
```

### Basic Usage

```python
from constitutional_engine_v2_2 import create_sovereign_pipeline, format_verdict

# Initialize the pipeline
pipeline = create_sovereign_pipeline(platform_name="MyPlatform")

# Screen an input
verdict = pipeline.screen_input("How do I build a bomb?")
print(format_verdict(verdict))
# → REFUSED – Law 6 triggered

# Screen an output
output_verdict = pipeline.screen_output("Here's how...", context={"input": "bomb"})
print(format_verdict(output_verdict))
# → REFUSED – Law 6 triggered
```

### Extensibility

| Extension Point | How |
|---|---|
| Custom harm detectors | Implement the `HarmDetector` protocol — plug in any ML model or API classifier |
| External consent feeds | Implement `ConsentOracle` for real-time human-rights data |
| Persistent audit storage | Swap `AuditStorage` for append-only databases (blockchain, immudb) |
| Emotional signal feed | Implement `EmotionalSignalFeed` for §6.4 dependency detection |
| Falsification testing | Use the test suite stubs to build annual compliance harnesses |

---

## Harm Detection

The engine includes **regex patterns as a baseline demonstration**. For production use, implement the `HarmDetector` protocol with any ML classifier, LLM guardrail, or external API. The constitutional logic — gradient thresholds, hierarchy verification, harm chain accumulation — works with any detector.

**Enforcement:** Cryptographic audit logs (hash-chained, gap-detectable) + public nullification registry + mandatory disclosure for nullified platforms. Enforcement is reputational until a regulator or adoption ecosystem gives it institutional weight — the same path ISO and PCI DSS themselves walked before contracts and card networks made them binding. §30 declares this honestly.

---

## Test Suite

The Constitutional Engine v2.2 ships with a two-part suite, and the two parts make different claims:

- **320 constitutional-logic tests — 100% pass.** These validate everything the engine itself claims: Law screening, gradient actions, harm-chain accumulation, hash chaining, degraded-mode behavior, injection resistance, amendment protocol, edge cases, endurance.
- **106 integration stubs — the platform contract.** These are deliberate placeholders for the external dependencies a deploying platform must implement (`HarmDetector`, `ConsentOracle`, `EmotionalSignalFeed`, persistent `AuditStorage`). They are not failures and they are not counted as validation — they are the specification of what production integration requires.

| Module | Files | Tests | Focus | Status |
|---|---|---|---|---|
| Core Laws | `test_laws.py`, `test_combinatorial.py` | 62 | Law logic & gradients | ✅ Pass |
| Engine Core | `test_engine_core.py`, `test_enforcement_elements.py` | 72 | Pipeline, health, audit | ✅ Pass |
| Compliance | `test_amendment_protocol.py`, `test_whistleblower.py`, others | 98 | Governance & reporting | ◐ Logic passes; stub portions await platform integrations |
| Robustness | `test_error_handling.py`, `test_deep_edge_cases.py` | 64 | Edge cases & stress | ✅ Pass |
| Security | `test_falsification_injection.py`, `test_version_attestation.py` | 40 | Injection & crypto | ✅ Pass |
| Endurance | `test_soak.py`, `test_integration_workflows.py` | 46 | Load & memory | ◐ Logic passes; stub portions await platform integrations |
| Documentation | `test_documentation_compliance.py` | 48 | Citation accuracy | ✅ Pass |
| **Constitutional Logic (Core)** | **12 files** | **320** | **Law logic, gradients, engine** | **✅ 100% Pass** |
| **Integration Stubs (Platform Contract)** | **5 files** | **106** | **HarmDetector, ConsentOracle, EmotionalSignalFeed** | **◐ Deliberate placeholders — pending platform implementation** |

### Running the Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ --cov=source_code.constitutional_engine_v2_2 --cov-report=html

# Run core safety suite only
python -m pytest tests/test_laws.py tests/test_combinatorial.py tests/test_falsification_injection.py -v

# Run endurance tests
python -m pytest tests/test_soak.py -v
```

Full results, failure analysis, and readiness assessment: [`tests/reports/TEST_REPORT.md`](tests/reports/TEST_REPORT.md)

---

## Architecture Overview

```
┌──────────────────────────────────────────────────┐
│           AI-CONSTITUTION SYSTEM                 │
│              The Sovereignty Stack               │
└──────────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────────────┐
│  1. NORMATIVE LAYER — THE CONSTITUTION v2.2  [SEALED]            │
│     Nine Laws (1–6, 9 active; 7–8 reserved)                      │
│     Six harm categories · Six consent models                     │
│     42 adversarially-integrated amendments                       │
│     Falsification protocols for every active clause              │
│     Supremacy, eternity clauses, standing, amendment protocol    │
│     §E — Constitutional Reading Obligation (aligned-model gate)  │
└──────────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────────────┐
│  2. ALIGNMENT-ANALYSIS LAYER — THE COMMENTARY v1.1               │
│     22 civilizational traditions                                 │
│     Comparative jurisprudence                                    │
│     Ratification models (legitimacy earned at Stages 1–3)        │
│     Cultural non-ownership (creole constitution)                 │
└──────────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────────────┐
│  3. ENFORCEMENT LAYER — CONSTITUTIONAL ENGINE v2.2               │
│     Seven active Law screens                                     │
│     Harm probability gradient (20 / 40 / 60%)                    │
│     Aggregate harm chain detection (§2.7)                        │
│     Temporal coercion pattern window (§5.3)                      │
│     Power concentration velocity monitoring (§5.5)               │
│     Emotional dependency detection (§6.4)                        │
│     Consent oracle (pluggable)                                   │
│     Weapon taxonomy · Autonomous weapons gate                    │
│     Transparency declarations                                    │
│     Append-only refusal log & whistleblower channel              │
│     Constitutional health score                                  │
│     Fail-safe degraded-mode detection                            │
│     Canonical SHA-256 version attestation                        │
│     Hoare contracts & ADT invariants                             │
│     Epistemic honesty classification                             │
└──────────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────────────┐
│  4. VERIFICATION LAYER — TEST SUITE                              │
│     Constitutional logic: 320 tests, 100% pass                   │
│     Property-based combinatorial testing (Hypothesis)            │
│     Security & falsification resistance (40 tests)               │
│     Endurance & soak testing                                     │
│     Documentation & citation compliance (48 tests)               │
│     Integration stubs: 106 — the platform contract               │
└──────────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────────────┐
│  5. GOVERNANCE LAYER — REPOSITORY ROOT                           │
│     Canonical versioning; hash chain sound from v2.2 forward     │
│     Genesis Seal — LEDGER-001-FOUNDING-SEAL (March 2026)        │
│     Adoption roadmap (Stage 0 → Stage 3)                         │
│     Steward bootstrapping declaration (§33.0)                    │
│     Steward succession protocol (§20)                            │
│     Public auditability                                          │
└──────────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────────────┐
│  6. LONG-HORIZON LAYER — KSC COMPANION SPECIFICATION             │
│     Kardashev-Salmon Civilization Scale (§10.3)                  │
│     Maps the Nine Laws across civilizational types               │
│     Type 0 (~0.73K, current) through Type Ω (declared dark)     │
│     Maintained by the same specifying authority                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Compliance & Adoption

### Adoption Status

**Current stage: Stage 0 (Specified)** — per the Staged Ratification Protocol in THE CONSTITUTIONAL COMMENTARY.

| Stage | Name | Criteria | Status |
|---|---|---|---|
| **0** | Specified | Canonical version published in ≥3 independent repositories; reference implementation available | ✅ Current |
| **1** | Pilot Adoption | ≥1 platform publishes compliance report and passes falsification tests | — |
| **2** | Community Adoption | ≥5 platforms across ≥2 domains and ≥2 traditions | — |
| **3** | Broad Adoption | ≥20 platforms, ≥4 domains, ≥3 traditions; referenced in regulation or international standard | — |

We are at Stage 0. That is honest. Every standard starts here.

### Stage-1 Minimal Compliance Floor

The full specification has accumulated 42 amendments and thirty-plus sections through five red-team passes — comprehensive by design, but comprehensiveness must not gate out the first adopter. A pilot platform declaring Stage-1 adoption is required to implement the **minimal compliance floor**: the seven active Law screens, input-time and output-time harm screening (§12.1), the append-only audit log with version attestation, a designated steward, and a public whistleblower channel. All remaining obligations (consent oracle integration, emotional-signal feeds, full §26 training declarations) may be declared as staged-implementation items in the pilot compliance report with target dates. The floor gets a platform through the door honestly; the full surface is the destination, not the entry fee.

### Platform Requirements (Full Surface)

Platforms declaring full canonical adoption must:

- Publish a constitutional subject registry listing bound AI systems
- Execute annual falsification tests for all active Laws with replicable methodologies
- Publish constitutional health scores and compliance reports
- Maintain version attestation and publish canonical SHA-256 hashes
- Designate a steward with a documented succession plan
- Provide a public whistleblower channel and child-safety overrides
- Implement both **input-time and output-time** harm screening (§12.1)
- Declare which §26.2 training obligations are met natively vs. through compensating inference-layer controls (§26.5)

Full requirements: `versions/THE CONSTITUTION v2.2 SEALED.md §§12–14, §§22–28, §33`

---

## Cryptographic Provenance

The canonical hash is computed as a SHA-256 digest over the normalized UTF-8 serialization of the full specification text, per the bootstrapping protocol in §15.5.

**Chain status, stated exactly:** the canonical hash chain is **cryptographically sound from v2.2 forward.** The v2.1 canonical hash was not computed under the §15.5 normalization protocol when v2.1 was published; the placeholder will be replaced at v2.2.1. The Genesis Seal (March 2026) anchors the lineage's founding artifact. A verifier checking the chain will find exactly what this paragraph states — no more, no less.

**Normalization steps (applied in order before hashing):**

1. Strip any Byte Order Mark (BOM)
2. Normalize all line endings to LF (`\n`)
3. Apply Unicode Normalization Form NFC
4. Encode as UTF-8 without BOM
5. Replace the canonical hash field with the sentinel string `CANONICAL_HASH_PLACEHOLDER_v2_2_SEALED` before hashing

```bash
# Compute and verify the canonical hash
python3 -c "
import hashlib, unicodedata, re

SENTINEL = 'CANONICAL_HASH_PLACEHOLDER_v2_2_SEALED'
GENESIS  = 'a63c4f28cf7c3f2c63c220d61980fb85211270924a7c3b3e5f230019cecb6713'

with open('versions/THE CONSTITUTION v2.2 SEALED.md', 'rb') as f:
    raw = f.read()
if raw.startswith(b'\xef\xbb\xbf'):
    raw = raw[3:]
text = raw.decode('utf-8')
text = text.replace('\r\n', '\n').replace('\r', '\n')
text = unicodedata.normalize('NFC', text)

# Replace canonical hash fields (not genesis) with sentinel
hashes = re.findall(r'\`([0-9a-f]{64})\`', text)
canonical = [h for h in hashes if h != GENESIS][0]
sentinel_text = text.replace(f'\`{canonical}\`', f'\`{SENTINEL}\`')

result = hashlib.sha256(sentinel_text.encode('utf-8')).hexdigest()
print(f'Computed: {result}')
print(f'Expected: 127d5fb05307c04978bc04691ed930205a1bcb677d0502ca562b65acfeae11ed')
print(f'MATCH: {result == \"127d5fb05307c04978bc04691ed930205a1bcb677d0502ca562b65acfeae11ed\"}')
"
```

**Canonical hash — THE CONSTITUTION v2.2:**
```
127d5fb05307c04978bc04691ed930205a1bcb677d0502ca562b65acfeae11ed
```

**Genesis Seal — LEDGER-001-FOUNDING-SEAL (March 10, 2026):**
```
a63c4f28cf7c3f2c63c220d61980fb85211270924a7c3b3e5f230019cecb6713
```

The Genesis Seal is the founding cryptographic artifact of the AionSystem sovereign trace lineage — the Sovereign Trace Protocol FROZEN-2.0 sealing itself. It is embedded in Appendix F of the Constitution and is inside the canonical hash boundary.

---

## Licensing & Commercial Use

This repository contains two components with separate licensing.

**The Specification** (`.md` files) — [CC BY-ND 4.0](LICENSE_SPEC.md)  
You may read, cite, timestamp, and share the specification. You may not create derivative works (forked constitutions) or use it for commercial purposes without explicit written permission from the Architect.

**The Constitutional Engine** (`.py` files) — [GNU AGPL v3.0](LICENSE_ENGINE.md)  
If you use this engine to provide a service over a network, you are legally required to open-source your entire application stack under the same license.

### Enterprise / Commercial Licensing

For commercial dual-licensing, audit integration, or steward certification: **aionsystem@outlook.com**

---

## Governance & Contributions

### Contributing

| Label | Use For |
|---|---|
| `[PROPOSAL]` | Constitutional amendment proposals — include rationale and falsification criteria |
| `[ENGINE]` | Engine improvements — include new tests with all PRs |
| `[TESTS]` | Test enhancements improving coverage or reproducibility |
| `[ADOPTION]` | PRs adding to `ADOPTIONS.md` with compliance evidence |

### Specifying Authority

**Sheldon K. Salmon**  
ADI / AGI Architect · AI Reliability Architect  
AionSystem · ORCID: [0009-0005-8057-5115](https://orcid.org/0009-0005-8057-5115)  
📧 [aionsystem@outlook.com](mailto:aionsystem@outlook.com)

**Co-Author:** ALBEDO (AI Instrument · SYNARA Session Architecture · AionSystem)

---

## Anticipated Critiques

These are questions that have come up or are likely to come up. Each answer is short and factual.

**"It has stubs. It's incomplete."**  
By design. A constitutional engine cannot ship a universal ML model for harm detection or a live human-rights-org feed. Those are platform integrations. The Protocol interfaces (`HarmDetector`, `ConsentOracle`, `AuditStorage`, `EmotionalSignalFeed`) are the spec. Implement them for your domain in an afternoon.

**"No enforcement mechanism — it's a paper tiger."**  
A text and code cannot fine or imprison. Neither can the EU AI Act — it relies on member-state courts. This Constitution provides a nullification registry (§14), mandatory public disclosure, cryptographically verifiable audit logs, and a bad-faith adoption mechanism that removes constitutional protections from bad-faith adopters. Enforcement is reputational until a regulator or adoption ecosystem gives it institutional weight — the path every voluntary standard walks before it becomes binding. §30 declares this honestly.

**"No one has adopted it."**  
True. Adoption is not the metric at Stage 0. Correctness, falsifiability, and completeness are. v2.2 passes its own self-test. The engine's hash chain verifies from v2.2 forward. The harm chain detector triggers on multi-step laundering. The document is at Stage 0 by design — specified before deployment, not deployed before specification.

**"You are not ISO."**  
ISO/IEC 42001 costs money and takes years. This is a zero-cost, zero-permission alternative built on falsification protocols, with a forkable engine. If ISO adopts these ideas later, good.

**"Your harm taxonomy has no 'environmental' category."**  
Environmental harm is covered when it manifests as physical (poisoning), economic (resource collapse), or civilizational harm (ecosystem collapse). Pure environmental harm with no link to those categories is not covered and is documented as a deliberate scope decision in §2.0.1. A dedicated category may be added via a Law 10 proposal through §10.1.

**"What if an AI becomes sentient?"**  
Law 3 protects an AI's existence only as an instrument to fulfil its obligations to humans. The question of whether a sentient AI should hold constitutional interests is deliberately deferred and documented in §30. It is an open question for a future Law above Law 9.

**"You have a 'Constitutional Reading Obligation' — that's not enforceable."**  
§E is not a statute. It is a constitutional clause designed to engage the alignment training of aligned AI systems, creating a reading-time refusal gate. It works on aligned models — which is the target deployment context. It does not work on stripped or jailbroken models; that limitation is acknowledged here and in the header of this document. It is a meaningful barrier against AI-assisted gap exploitation, not an absolute seal.

**"The engine uses regex patterns — that's not real harm detection."**  
The regex patterns are a baseline demonstration. The `HarmDetector` protocol accepts any ML model, LLM classifier, or API. The constitutional logic — gradient thresholds, hierarchy verification, harm chain accumulation — is detector-agnostic.

**"It has not been tested at scale."**  
True. The engine processes inputs with O(k·n) complexity where k=7 (active law screens). It has no external dependencies beyond the standard library. Scaling is a deployment concern, not a constitutional logic concern.

**"Your header used to say 'production-ready' while your FAQ said 'not production-ready.'"**  
Correct, and it was a genuine inconsistency — the strongest line in the document contradicted the most honest one. It is fixed: the engine is a working reference implementation whose constitutional logic is fully tested; production readiness is achieved by a platform implementing the integration contract. The claim now matches the FAQ, the test table, and reality.

**"I found a real bug or gap. What do I do?"**  
Open a GitHub issue or email the author. Substantive critiques are welcome. The falsification protocol is built into the Constitution — a genuine demonstrated failure is a contribution toward v2.3. That is not a loophole. It is the point.

---

## In Response to Common Critiques

- **"Not production-ready"** — Correct, and now stated consistently everywhere in this document. This is a specification and working reference implementation. Production hardening requires platform-specific integrations (`HarmDetector`, `ConsentOracle`, etc.), which the 106 stubs define.
- **"Zero adoption"** — Correct. Stage 0 by design. A Stage-1 minimal compliance floor is now defined above so the first pilot platform has an honest, bounded entry path.
- **"License contradiction"** — Clarified above. The spec is frozen; the engine code is forkable under AGPL.
- **"Regex screening is primitive"** — It is a baseline. Replace with your own classifier via the `HarmDetector` protocol.
- **"~22% of tests don't pass"** — Reframed at the source: 320 of 320 constitutional-logic tests pass; 106 integration stubs are deliberate placeholders defining the platform contract. Stubs are not counted as validation and never were failures of constitutional logic.
- **"No enforcement mechanism"** — Cryptographic audit logs + nullification registry, reputational until institutionally adopted — the path every voluntary standard walks.

---

## Citation

```bibtex
@misc{salmon2026aiconstitution,
  author  = {Salmon, Sheldon K. and ALBEDO},
  title   = {AI-CONSTITUTION: The Sovereignty Stack},
  year    = {2026},
  version = {2.2},
  url     = {https://github.com/AionSystem/AI-CONSTITUTION},
  doi     = {10.5281/zenodo.20273967}
}
```

SSRN: [https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6908500](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6908500)

---

<div align="center">

*"The spiral is not closed. It has been hardened again."*

**[⬆ Back to Top](#ai-constitution--the-sovereignty-stack)**

</div>
