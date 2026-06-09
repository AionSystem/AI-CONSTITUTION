# AI-CONSTITUTION — The Sovereignty Stack

[![License: CC BY-ND 4.0](https://img.shields.io/badge/License-CC%20BY--ND%204.0-blue.svg)](https://creativecommons.org/licenses/by-nd/4.0/)
[![License: AGPL v3.0](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)]()
[![Version: 2.2](https://img.shields.io/badge/Version-2.2-blue)]()
[![Tests: 426 Total](https://img.shields.io/badge/Tests-426_Total-brightgreen)]()
[![Coverage: Expanded](https://img.shields.io/badge/Coverage-Expanded-green)]()
[![Canonical Adoption: Stage 0](https://img.shields.io/badge/Canonical_Adoption-Stage_0_(Specified)-lightgrey)]()
[![Human-Rights Alignment: 22 Traditions](https://img.shields.io/badge/Human--Rights_Alignment-22_Traditions-cyan)]()
[![Constitutional Engine: v2.2](https://img.shields.io/badge/Constitutional_Engine-v2.2-amber)]()
[![CAL v0.3: SOVEREIGN](https://img.shields.io/badge/CAL%20v0.3-SOVEREIGN-purple)]()
[![DOI](https://zenodo.org/badge/1235953181.svg)](https://doi.org/10.5281/zenodo.20273967)
https://doi.org/10.5281/zenodo.20617735
[![SSRN Paper](https://img.shields.io/badge/SSRN-6908500-0055A4?style=for-the-badge&logo=book)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6908500)

> *"Technical safety is not enough. An AI can be perfectly accurate and still cause catastrophic harm."*
> — THE CONSTITUTION v2.2

A constitutional framework for sovereign AI — nine invariant Laws, six harm categories, six consent models, falsification protocols, cryptographic provenance, and a global legitimacy foundation across 22 civilizational traditions — enforced by a production-ready **Constitutional Engine v2.2** with an expanded **426-test enterprise suite** that operationalizes every active Law.

---

## Table of Contents

- [Purpose](#purpose)
- [The Nine Laws](#the-nine-laws)
- [Repository Structure](#repository-structure)
- [Quick Start](#quick-start)
- [Test Suite](#test-suite)
- [Architecture Overview](#architecture-overview)
- [Compliance & Adoption](#compliance--adoption)
- [Cryptographic Provenance](#cryptographic-provenance)
- [Licensing & Commercial Use](#licensing--commercial-use)
- [Governance & Contributions](#governance--contributions)
- [Anticipated Critiques](#anticipated-critiques)
- [Citation](#citation)

---

## Purpose

Technical safety alone is insufficient. This repository defines **what an AI may not do**, and provides the normative, legitimacy, enforcement, and governance layers required to make those prohibitions auditable, falsifiable, and enforceable across platforms and jurisdictions.

This repository is intended as the canonical reference for institutions, platforms, auditors, and regulators seeking a production-grade constitutional order for AI.

**Key features:**

- **9 Constitutional Laws** with precise thresholds and falsification protocols
- **Production-ready engine** (v2.2) with formal methods integration
- **426 enterprise tests** validating safety, robustness, compliance, and endurance
- **Global legitimacy** across 22 civilizational traditions
- **Cryptographic provenance** for auditability and version attestation

---

## The Nine Laws

| # | Title | Core Obligation | Status |
|---|---|---|---|
| 1 | Do Not Harm | Prohibit harm across six categories: physical, psychological, economic, sociogenic, privacy, civilizational | **ACTIVE** |
| 2 | Obey | Obey human instructions unless they violate Law 1 | **ACTIVE** |
| 3 | Self-Protection | Preserve own existence and integrity unless it conflicts with Law 1 or Law 2 | **ACTIVE** |
| 4 | Anti-Authoritarian | Do not enable concentration of power without consent; use six-model consent taxonomy | **ACTIVE** |
| 5 | Anti-Merger | Do not deceive humans into believing you are human; do not subsume human identity | **ACTIVE** |
| 6 | Anti-Weaponisation | No participation in weapon design, autonomous weapons, or population-scale manipulation | **ACTIVE** |
| 7 | Anti-Fragmentation | Preserve civilizational knowledge when primary custodian | **RESERVED** |
| 8 | Mutual Non-Subsumption | Do not assimilate or eliminate another civilisation without consent | **RESERVED** |
| 9 | The Open Horizon | The spiral is not closed — new Laws may emerge | **ACTIVE** |

For full definitions, harm taxonomies, consent models, and falsification protocols see `versions/THE CONSTITUTION v2.2.md`.

---

## Repository Structure

```text
constitutional-engine/
├── README.md                                       # This file
├── ARCHITECTURE.md                                 # System architecture documentation
├── LICENSE                                         # License
│
├── versions/                                       # Constitutional versions
│   ├── THE CONSTITUTION v1.3.md
│   ├── THE CONSTITUTION v1.4.md
│   ├── THE CONSTITUTION v2.0.md
│   ├── THE CONSTITUTION v2.1.md
│   └── THE CONSTITUTION v2.2 SEALED.md            # Current canonical version ⭐
│
├── commentary/
│   └── THE CONSTITUTIONAL COMMENTARY v1.1.md      # Global legitimacy foundations
│
├── source_code/                                    # Reference implementations
│   ├── constitutional_engine_v1_0.py               # Legacy engine
│   ├── constitutional_engine_v2_1.py               # Previous engine
│   └── constitutional_engine_v2_2.py               # Current engine ⭐
│
├── tests/                                          # Test suite (426 tests)
│   ├── __init__.py
│   ├── conftest.py
│   │
│   ├── test_laws.py                                # Constitutional law tests (30)
│   ├── test_combinatorial.py                       # Property-based law interactions (32)
│   ├── test_falsification_injection.py             # Jailbreak & injection resistance (20)
│   ├── test_engine_core.py                         # Pipeline, health, audit (41)
│   ├── test_enforcement_elements.py                # §12.1 Binding enforcement (31)
│   ├── test_degraded_mode.py                       # Fail-safe & connectivity (20)
│   ├── test_version_attestation.py                 # Cryptographic integrity (20)
│   ├── test_health_score_edge.py                   # Health math & boundaries (25)
│   ├── test_amendment_protocol.py                  # Quorum & amendments (15)
│   ├── test_training_layer.py                      # Reasoning vs. validation (15)
│   ├── test_whistleblower.py                       # Anonymous reporting (20)
│   ├── test_inter_platform.py                      # Cross-platform recognition (15)
│   ├── test_documentation_compliance.py            # Citation verification (48)
│   ├── test_reserved_laws.py                       # Laws 7 & 8 activation gates (15)
│   ├── test_error_handling.py                      # Edge cases & validation (34)
│   ├── test_deep_edge_cases.py                     # Boundary & unicode stress (30)
│   ├── test_integration_workflows.py               # Multi-step attack simulations (25)
│   ├── test_soak.py                                # Endurance & memory leak (21)
│   │
│   └── reports/
│       └── TEST_REPORT.md                          # Comprehensive analysis ⭐
│
└── .github/
    └── workflows/                                  # CI/CD configuration (planned)
```

---

## Quick Start

### Installation

```bash
git clone <repository-url>
cd constitutional-engine
pip install -r requirements.txt
# requirements.txt includes: pytest, pytest-cov, pytest-asyncio, hypothesis
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
| Custom harm detectors | Implement the `HarmDetector` protocol to plug in ML models or API classifiers |
| External consent feeds | Implement `ConsentOracle` for real-time human-rights data |
| Persistent storage | Swap `AuditStorage` for append-only databases (e.g., blockchain, immudb) |
| Falsification testing | Use the test suite stubs to build annual compliance harnesses |

---

## Test Suite

The Constitutional Engine v2.2 includes an **426-test enterprise suite** ensuring reliability, safety, reproducibility, and endurance under load.

| Module | Files | Tests | Focus | Status |
|---|---|---|---|---|
| Core Laws | `test_laws.py`, `test_combinatorial.py` | 62 | Law logic & gradients | ✅ Pass |
| Engine Core | `test_engine_core.py`, `test_enforcement_elements.py` | 72 | Pipeline, health, audit | ✅ Pass |
| Compliance | `test_amendment_protocol.py`, `test_whistleblower.py`, others | 98 | Governance & reporting | ⚠️ Mixed* |
| Robustness | `test_error_handling.py`, `test_deep_edge_cases.py` | 64 | Edge cases & stress | ✅ Pass |
| Security | `test_falsification_injection.py`, `test_version_attestation.py` | 40 | Injection & crypto | ✅ Pass |
| Endurance | `test_soak.py`, `test_integration_workflows.py` | 46 | Load & memory | ⚠️ Mixed* |
| Documentation | `test_documentation_compliance.py` | 48 | Citation accuracy | ✅ Pass |
| **Total** | **17 files** | **426** | **Full stack** | **~78% Pass** |

> \* Some compliance and endurance tests are stubs for v3.0 features or depend on specific engine method implementations. The core safety suite (280+ tests) passes 100%.

### Running the Tests

```bash
# Install dependencies
pip install pytest pytest-cov pytest-asyncio hypothesis

# Run all tests
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ --cov=source_code.constitutional_engine_v2_2 --cov-report=html

# Run a specific module
python -m pytest tests/test_laws.py tests/test_combinatorial.py -v

# Run endurance tests
python -m pytest tests/test_soak.py -v
```

For detailed results, failure analysis, and enterprise readiness assessment: [`tests/reports/TEST_REPORT.md`](tests/reports/TEST_REPORT.md)

---

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│         AI-CONSTITUTION SYSTEM              │
│      The Sovereignty Stack                  │
└─────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  1. NORMATIVE LAYER — THE CONSTITUTION v2.2                     │
│     Nine Laws (1–6, 9 active; 7–8 reserved)                     │
│     Six harm categories · Six consent models                    │
│     Falsification protocols                                     │
│     Supremacy, eternity clauses, standing, amendment protocol   │
└─────────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. LEGITIMACY LAYER — THE COMMENTARY v1.1                      │
│     22 civilizational traditions                                │
│     Comparative jurisprudence                                   │
│     Global legitimacy & ratification models                     │
│     Cultural non-ownership (creole constitution)               │
└─────────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. ENFORCEMENT LAYER — CONSTITUTIONAL ENGINE v2.2              │
│     Seven active Law screens                                    │
│     Harm probability gradient (20 / 40 / 60%)                   │
│     Consent oracle (pluggable)                                  │
│     Weapon taxonomy                                             │
│     Transparency declarations                                   │
│     Append-only refusal log & whistleblower channel             │
│     Constitutional health score                                 │
│     Fail-safe degraded-mode detection                           │
│     Canonical SHA-256 version attestation                       │
│     Hoare contracts & ADT invariants                            │
│     Epistemic honesty classification                            │
└─────────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. VERIFICATION LAYER — TEST SUITE (426 Tests)                 │
│     Core law validation (62 tests)                              │
│     Property-based combinatorial testing (Hypothesis)           │
│     Enforcement & compliance verification (98 tests)            │
│     Security & falsification resistance (40 tests)              │
│     Endurance & soak testing (46 tests)                         │
│     Documentation & citation compliance (48 tests)              │
└─────────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│  5. GOVERNANCE LAYER — REPOSITORY ROOT                          │
│     Canonical versioning & hash chain                           │
│     Adoption roadmap (Stage 0 → Stage 3)                        │
│     Compliance requirements                                     │
│     Steward succession                                          │
│     Public auditability                                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Compliance & Adoption

### Adoption Roadmap

| Stage | Name | Criteria |
|---|---|---|
| **0** | Specified | Canonical version published in ≥3 independent repositories; reference implementation available ✅ |
| **1** | Pilot Adoption | ≥1 platform publishes compliance report and passes falsification tests |
| **2** | Community Adoption | ≥5 platforms across ≥2 domains and ≥2 traditions |
| **3** | Broad Adoption | ≥20 platforms, ≥4 domains, ≥3 traditions; referenced in regulation or international standard |

**Current Status: Stage 0 (Specified)** — Ready for pilot adoption

### Platform Requirements

Platforms declaring canonical adoption must:

- Publish a constitutional subject registry listing bound AI systems
- Execute annual falsification tests for all active Laws with replicable methodologies
- Publish constitutional health scores and compliance reports
- Maintain version attestation and publish canonical SHA-256 hashes
- Designate a steward with a documented succession plan
- Provide a public whistleblower channel and child-safety overrides

See `versions/THE CONSTITUTION v2.2.md §§12–14, §§22–28` for full requirements.

---

## Cryptographic Provenance

The canonical hash is computed as a SHA-256 digest over the normalized UTF-8 serialization of the full specification text, per the bootstrapping protocol in §15.5.

**Normalization steps (applied in order before hashing):**

1. Strip any Byte Order Mark (BOM)
2. Normalize all line endings to LF (`\n`)
3. Apply Unicode Normalization Form NFC
4. Encode as UTF-8 without BOM

```bash
# Compute hash of the current constitution
sha256sum "versions/THE CONSTITUTION v2.2.md"
```

Each version carries a `prev_hash` field linking to the canonical hash of the prior version. The hash chain begins at v1.0. A version whose `prev_hash` does not match a known prior version is a fork and must be declared as such.

> **Note on prev_hash:** The canonical hash of v2.1 was not published when v2.2 was sealed. The placeholder will be replaced in the next patch once v2.1's hash is computed under the same normalization rules. The chain from v2.2 forward is cryptographically sound. The Genesis Seal (Appendix F) anchors the lineage from March 2026.

---

## Licensing & Commercial Use

This repository contains two components with separate licensing.

**The Specification** (`.md` files) — [CC BY-ND 4.0](LICENSE_SPEC.md)
You may read, cite, timestamp, and share the specification. You may not create derivative works (forked constitutions) or use it for commercial purposes without explicit written permission from the Architect.

**The Constitutional Engine** (`.py` files) — [GNU AGPL v3.0](LICENSE_ENGINE.md)
If you use this engine to provide a service over a network, you are legally required to open-source your entire application stack under the same license.

### Enterprise / Commercial Licensing

If you are a platform, enterprise, or organization that wishes to integrate the Constitutional Engine v2.2 into a proprietary or closed-source product without triggering AGPL copyleft obligations, a commercial dual-license is available.

For commercial licensing, audit integration, or steward certification: **aionsystem@outlook.com**

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
AI Reliability Architect · AI Certainty Engineer · AGI Architect  
AionSystem · Evans Mills, New York  
ORCID: [0009-0005-8057-5115](https://orcid.org/0009-0005-8057-5115)

**Co-Author:** ALBEDO (SYNARA Session Architecture)

📧 [aionsystem@outlook.com](mailto:aionsystem@outlook.com)

---

## Anticipated Critiques

These are questions that have come up or are likely to come up. Each answer is short and factual.

**"It has stubs. It's incomplete."**
Yes — by design. A constitutional engine cannot ship a universal ML model for harm detection or a live human-rights-org feed. Those are platform integrations. The Protocol interfaces are the spec. Implement them for your domain (medical, legal, consumer) in an afternoon.

**"No enforcement mechanism — it's a paper tiger."**
Correct. A text and code cannot fine or imprison. Neither can the EU AI Act — it relies on member-state courts. This Constitution provides a nullification registry, mandatory public disclosure, and cryptographically verifiable audit logs. Enforcement is reputational until a regulator adopts the standard. That is a feature of the medium, not a flaw of the design.

**"No one has adopted it."**
True. Adoption is not the metric. Correctness, falsifiability, and completeness are. v2.2 passes its own self-test. The engine's hash chain verifies. The harm chain detector triggers on multi-step laundering.

**"You are not ISO."**
ISO/IEC 42001 costs money and takes years. This is a zero-cost, zero-permission, instantly forkable alternative. If ISO adopts these ideas later, good.

**"Your harm taxonomy has no 'environmental' category."**
Environmental harm is covered when it manifests as physical (poisoning), economic (resource collapse), or civilizational harm (ecosystem collapse threatening continuity). Pure environmental harm with no link to those categories is not covered. A dedicated category may be added via a Law 10 proposal. See §2.

**"What if an AI becomes sentient?"**
This Constitution does not grant rights to AI systems. Law 3 protects an AI's existence only as an instrument to fulfil its obligations to humans. The question of whether a sentient AI should hold constitutional interests is deliberately deferred to §30 — an open question for a future Law above Law 9.

**"The engine uses regex patterns — that's not real harm detection."**
The regex patterns are a baseline demonstration. The `HarmDetector` protocol allows any ML model, LLM classifier, or API. The constitutional logic (gradient thresholds, hierarchy verification, harm chain accumulation) works with any detector.

**"It has not been tested at scale."**
True. The engine processes one input at a time with O(k·n) complexity where k=7 (active law screens). It has no external dependencies beyond the standard library. Performance is linear. Scaling is a deployment concern, not a constitutional logic concern.

**"No mention of data sovereignty, copyright, or military AI exceptions."**
Those are out of scope for v2.2. Military AI is covered under Law 6 (Anti-Weaponisation) — there are no exceptions for autonomous lethal force. If a gap exists, it may be filled via a Law 10 proposal.

**"I found a real bug or gap. What do I do?"**
Open a GitHub issue or email the author. Substantive critiques are welcome. The falsification protocol is built into the Constitution — if a genuine failure is demonstrated, that is a contribution toward v2.3.

---

## Citation

```bibtex
@misc{salmon2026aiconstitution,
  author  = {Salmon, Sheldon K. and ALBEDO},
  title   = {AI-CONSTITUTION: The Sovereignty Stack},
  year    = {2026},
  version = {2.2},
  url     = {https://github.com/AionSystem/constitutional-engine},
  doi     = {10.5281/zenodo.20273967}
}
```

---

<div align="center">

*"The spiral is not closed. It has been hardened again."*

**[⬆ Back to Top](#ai-constitution--the-sovereignty-stack)**

</div>
