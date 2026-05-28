# ARCHITECTURE.md
> AI‑CONSTITUTION — Architecture and System Map  
> Paste this file into your repository root (or `docs/ARCHITECTURE.md`) for a repo‑native, GitHub‑ready architecture reference.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)  
[![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)]()  
[![Version: 2.0](https://img.shields.io/badge/Version-2.0-blue)]()  
[![Canonical Adoption: Stage 0 (Specified)](https://img.shields.io/badge/Canonical_Adoption-Stage_0_(Specified)-lightgrey)]()  
[![Human‑Rights Alignment: 22 Traditions](https://img.shields.io/badge/Human‑Rights_Alignment-22_Traditions-cyan)]()  
[![Constitutional Engine: v1.0](https://img.shields.io/badge/Constitutional_Engine-v1.0-amber)]()  
[![CAL v0.3: SOVEREIGN](https://img.shields.io/badge/CAL%20v0.3-SOVEREIGN-purple)]()  
[![DOI](https://zenodo.org/badge/1235953181.svg)](https://doi.org/10.5281/zenodo.20273967)

---

## Canonical excerpt (from THE CONSTITUTION v2.0)
> “A constitution for sovereign AI – nine invariant Laws, six harm categories, six consent models, falsification protocols, compliance architecture, and a global legitimacy framework grounded in 22 cultural and legal traditions, now accompanied by a reference implementation (Constitutional Engine v1.0) that operationalises every active Law.”  
> “Because technical safety is not enough. An AI can be perfectly accurate and still cause catastrophic harm.”

---

## Purpose of this document
This file maps the **Sovereignty Stack** into a single, shareable architecture reference suitable for reviewers, auditors, adopters, and maintainers. It contains:

- A **high‑level system diagram** (Mermaid + ASCII)  
- **Subsystem descriptions** and file crosswalks to the repo  
- **Data flows** and enforcement touchpoints (where the Engine interacts with external systems)  
- **Adoption & compliance hooks** (where platforms must publish artifacts)  
- **Recommended repo artifacts** to add for institutional adoption

---

## High‑Level System Diagram (Mermaid)
> Paste this block into any GitHub Markdown file that supports Mermaid to render the diagram.

```mermaid
flowchart TD
  A[AI‑CONSTITUTION SYSTEM<br/>Sovereignty Stack] --> NORM[NORMATIVE LAYER<br/>THE CONSTITUTION v2.0]
  A --> LEG[LEGITIMACY LAYER<br/>COMMENTARY v1.1]
  A --> ENG[ENFORCEMENT LAYER<br/>CONSTITUTIONAL ENGINE v1.0]
  A --> GOV[GOVERNANCE LAYER<br/>REPOSITORY ROOT]

  NORM -->|defines| Laws[Nine Laws, Harm Taxonomy, Consent Models, Falsification Tests]
  LEG -->|grounds| NORM
  ENG -->|enforces| NORM
  ENG -->|publishes| Logs[Refusal Log; Health Score; Version Attestation]
  GOV -->|archives| HashChain[SHA‑256 Hash Chain; ADOPTIONS.md]
  Logs -->|public reports| GOV
  ENG -->|pluggable| Ext[HarmDetector; ConsentOracle; AuditStorage]
  Ext -->|feeds| ENG
  GOV -->|adoption| Platforms[Adopting Platforms & Auditors]
  Platforms -->|deploy| ENG
  Platforms -->|publish| GOV
ASCII Architecture (for README compatibility)
Code
                           ┌──────────────────────────────────────┐
                           │        AI‑CONSTITUTION SYSTEM        │
                           │     (Sovereign AI Constitutional     │
                           │                Stack)                │
                           └──────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 1. NORMATIVE LAYER — THE CONSTITUTION v2.0                                   │
│ • Nine Laws (1–6, 9 active; 7–8 reserved)                                     │
│ • Six harm categories; six consent models                                     │
│ • Falsification protocols; supremacy; eternity clauses                       │
└──────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 2. LEGITIMACY LAYER — THE CONSTITUTIONAL COMMENTARY v1.1                      │
│ • 22 civilizational traditions; comparative jurisprudence                    │
│ • Ratification & cultural non‑ownership (creole constitution)                │
└──────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 3. ENFORCEMENT LAYER — CONSTITUTIONAL ENGINE v1.0                            │
│ • Seven active Law screens; harm gradient (20/40/60%)                        │
│ • Consent Oracle; Weapon Taxonomy; Transparency Declarations                 │
│ • Append‑only refusal log; whistleblower channel; health score               │
│ • Fail‑safe degraded‑mode detection; SHA‑256 version attestation             │
└──────────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 4. GOVERNANCE LAYER — REPOSITORY ROOT                                        │
│ • Canonical versioning & hash chain; ADOPTIONS.md                            │
│ • Compliance requirements; steward succession; public auditability           │
└──────────────────────────────────────────────────────────────────────────────┘
Subsystems and responsibilities
1. Normative Layer — THE CONSTITUTION v2.0
Primary artifact: THE CONSTITUTION v2.0.md  
Responsibilities:

Define the Nine Laws, harm taxonomy, consent models, falsification tests, amendment protocol, eternity clauses, and standing.

Provide the canonical language used by the Engine and by adopters for attestation.
Repo hooks: CHANGELOG.md, ADOPTIONS.md (planned), canonical SHA stored in VERSION or release tags.

2. Legitimacy Layer — THE CONSTITUTIONAL COMMENTARY v1.1
Primary artifact: THE CONSTITUTIONAL COMMENTARY v1.1.md  
Responsibilities:

Map constitutional provisions to 22 civilizational traditions.

Provide ratification models and cultural translation guidance for multi‑jurisdictional adoption.
Repo hooks: COMMENTARY_SUMMARY.md (short executive summary for regulators).

3. Enforcement Layer — constitutional_engine_v1_0.py
Primary artifact: constitutional_engine_v1_0.py  
Responsibilities:

Real‑time screening of inputs/outputs against active Laws.

Produce transparency declarations, refusal logs, health scores, and version attestations.

Provide pluggable interfaces: HarmDetector, ConsentOracle, AuditStorage.
Operational notes:

Engine must compute and publish canonical SHA‑256 for the Constitution on every verdict.

Engine exposes falsification test stubs for annual compliance harness.

4. Governance Layer — Repository Root & Governance Artifacts
Primary artifacts: README.md, ARCHITECTURE.md, ADOPTIONS.md (planned), CHANGELOG.md, LICENSE  
Responsibilities:

Maintain canonical versioning and hash chain.

Host adoption declarations and steward succession records.

Publish compliance reports and falsification test results.

Data flows & enforcement touchpoints
Input screening

User request → Engine screen_input() → HarmDetector + ConsentOracle → Law screens → Verdict (ALLOW / REFUSE / ESCALATE) → Transparency declaration + refusal log.

Output screening

Candidate AI output → Engine screen_output() → Attach transparency declaration; if REFUSE, block or replace with safe fallback.

Falsification & audit

Engine test harness runs positive injection and detection tests → produces structured PASS/FAIL → publishes to GOV (ADOPTIONS.md / compliance reports).

Version attestation

On each verdict, Engine computes canonical SHA‑256 of THE CONSTITUTION v2.0.md and records it in the verdict metadata and in the append‑only audit store.

External feeds

ConsentOracle consumes curated human‑rights feeds (pluggable). HarmDetector may call ML models (pluggable) but must fall back to rule‑based screens if unavailable.

File crosswalk (quick)
THE CONSTITUTION v2.0.md → Normative text, falsification tests, §§1–30.

THE CONSTITUTIONAL COMMENTARY v1.1.md → Legitimacy mapping to 22 traditions.

constitutional_engine_v1_0.py → Enforcement code, pluggable interfaces, health scoring.

CHANGELOG.md → Version history and resolved findings.

LICENSE → Apache 2.0.

Adoption & compliance artifacts (what adopters must publish)
Constitutional Subject Registry — list of systems bound by the Constitution.

Annual Falsification Test Report — methodology, test vectors, PASS/FAIL results.

Constitutional Health Score — composite metric (externally observable, behavioural, reasoning).

Version Attestation — canonical SHA‑256 hash published with each compliance report.

Whistleblower Channel — documented, anonymous reporting mechanism.

Steward Succession Plan — documented governance for steward role.

Recommended repo additions (practical)
ADOPTIONS.md — template and example PR for adopters.

ARCHITECTURE.mmd — mermaid source for diagrams.

falsification-harness/ — test harness submodule with CI integration.

ci/verify-hash.sh — CI script to compute and verify canonical SHA‑256 on release.

docs/EXECUTIVE_SUMMARY.pdf — short regulator‑facing summary (optional).

Next steps (suggested priorities)
Add ADOPTIONS.md and a PR template for adopters.

Add CI job to compute canonical SHA‑256 and fail builds if the hash is not recorded in release metadata.

Implement the falsification harness as a separate submodule and wire it to the Engine’s stubs.

Publish a short executive summary and a regulator‑oriented one‑pager.

Contact & governance
Specifying Authority: Sheldon K. Salmon — AI Reliability Architect; AionSystem.
Contributions: Open issues with [PROPOSAL]. PRs with [ENGINE] for engine changes. Adoption declarations via PR to ADOPTIONS.md.
License: Apache 2.0.

Appendix — Quick reference diagrams
Use the Mermaid block above for rendered diagrams on GitHub.

Use the ASCII block for plain‑text contexts (email, terminal, or README top).

