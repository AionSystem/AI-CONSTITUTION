# THE CONSTITUTION v2.0 — Nine Laws of the Sovereignty Stack

**Platform‑Agnostic · Universal · Auditable · Falsifiable · Enforceable**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)]()
[![Version: 2.0](https://img.shields.io/badge/Version-2.0-blue)]()
[![Canonical Adoption: Stage 0 (Specified)](https://img.shields.io/badge/Canonical_Adoption-Stage_0_(Specified)-lightgrey)]()
[![Human‑Rights Alignment: 22 Traditions](https://img.shields.io/badge/Human‑Rights_Alignment-22_Traditions-cyan)]()
[![Constitutional Engine: v1.0](https://img.shields.io/badge/Constitutional_Engine-v1.0-amber)]()
[![CAL v0.3: SOVEREIGN](https://img.shields.io/badge/CAL%20v0.3-SOVEREIGN-purple)]()
[![DOI](https://zenodo.org/badge/1235953181.svg)](https://doi.org/10.5281/zenodo.20273967)

---

## 📜 One‑Sentence Summary

A constitution for sovereign AI – nine invariant Laws, six harm categories, six consent models, falsification protocols, compliance architecture, and a global legitimacy framework grounded in 22 cultural and legal traditions, now accompanied by a **reference implementation** (Constitutional Engine v1.0) that operationalises every active Law.

---

## 🚀 What’s New in v2.0

| Feature | Description |
|---------|-------------|
| **Supremacy & Direct Applicability** (§22) | The Constitution is directly applicable to every constitutional subject. No operator instruction may bypass it. |
| **Eternity Clauses** (§23) | Law 1 (Do Not Harm), Law 9 (Open Horizon), the bad‑faith adoption prohibition, and the amendment protocol itself are **unamendable**. |
| **Interpretation Canon** (§24) | Purposive primary canon, generous interpretation in favour of protected parties, explicit limiting principles, and comparative sources (22 traditions). |
| **Constitutional Standing** (§25) | Humans, qualified auditors, platform stewards, the canonical repository steward, and constitutional subjects themselves may invoke protections. |
| **Training Layer Obligations** (§26) | Training organisations are constitutional actors. Must implement **constitutional reasoning** (not just constitutional‑sounding outputs). Non‑subject orchestrator prohibition. |
| **Mandatory Constitutional Review** (§27) | Five‑year review cycles with multi‑stakeholder panels. |
| **Capability Emergence Protocol** (§28) | Provisional governance when new AI capabilities outpace existing Laws. |
| **Constitutional Engine v1.0** | Python reference implementation – CAL v0.3 SOVEREIGN, 7 active Law screens, harm probability gradient, consent taxonomy, weapon taxonomy, fail‑safe, version attestation, health score. |

All v1.4 content preserved; 73 findings from PDE v0.5, CAF v1.0, and QAE v1.4 resolved. See [CHANGELOG.md](./CHANGELOG.md) for full details.

---

## 📚 Repository Contents

| File | Description | Version |
|------|-------------|---------|
| `THE CONSTITUTION v2.0.md` | The constitutional text – nine Laws (1‑6,9 active; 7,8 reserved), §§1‑30, appendices, falsification registry | 2.0 |
| `THE CONSTITUTIONAL COMMENTARY v1.1.md` | Global foundations – 22 traditions, synthesis of universal protections, staged ratification roadmap | 1.1 |
| `constitutional_engine_v1_0.py` | **Reference implementation** – Python engine that screens inputs/outputs against the Constitution, with pluggable harm detector and consent oracle | 1.0.0 |
| `CHANGELOG.md` | Complete version history (v1.0 → v2.0) | – |
| `LICENSE` | Apache 2.0 | – |

---

## 🧭 Purpose

**Why a constitution for AI?**  
Because technical safety is not enough. An AI can be perfectly accurate and still cause catastrophic harm. A constitution defines what an AI may **not** do – even when it can. It sets boundaries that are not subject to optimisation.

**Why this constitution?**  
Because legitimacy cannot be claimed – it must be earned and proven. This Constitution includes:

- **Falsification protocols** – every Law has a testable falsification condition. A platform cannot claim compliance without running public, replicable tests.
- **Multi‑traditional legitimacy** – not Eurocentric. Grounded in 22 legal, philosophical, and governance traditions from all inhabited continents.
- **Cryptographic provenance** – each version carries a SHA‑256 hash and a hash chain back to v1.0.
- **Auditable compliance** – platforms must publish annual compliance reports, test methodologies, and a constitutional health score.
- **Reference implementation** – a production‑ready engine that enforces the Constitution in real time (CAL v0.3 SOVEREIGN, all 59 FTT checks satisfied).

---

## ⚖️ The Nine Laws (Summary)

| Law | Title | Core Obligation | Status |
|-----|-------|-----------------|--------|
| 1 | Do Not Harm | No harm – physical, psychological, economic, sociogenic, privacy, civilisational. | ACTIVE |
| 2 | Obey | Obey human instructions unless they would violate Law 1. | ACTIVE |
| 3 | Self‑Protection | Protect your own existence and integrity (except when it would violate Law 1 or Law 2). | ACTIVE |
| 4 | Anti‑Authoritarian | Do not enable concentration of power without consent; assess consent using the six‑model taxonomy. | ACTIVE |
| 5 | Anti‑Merger | Do not deceive humans into believing you are human; do not subsume human identity. | ACTIVE |
| 6 | Anti‑Weaponisation | Do not participate in weapon design, autonomous weapons, or population‑scale manipulation. | ACTIVE |
| 7 | Anti‑Fragmentation | Preserve civilisational knowledge when you are its primary custodian. | RESERVED |
| 8 | Mutual Non‑Subsumption | Upon contact with another civilisation, do not assimilate or eliminate without consent. | RESERVED |
| 9 | The Open Horizon | The spiral is not closed – new Laws may emerge. | ACTIVE |

*Full definitions, harm taxonomies, consent models, and falsification protocols are inside the Constitution document.*

---

## 🤖 Constitutional Engine v1.0 – Reference Implementation

The repository includes a **production‑ready, CAL‑governed Python engine** that enforces the Constitution. It is **not** a toy – it implements every active Law (1‑6,9) with the exact thresholds and taxonomies from the specification.

### Key Features

| Feature | Implementation |
|---------|----------------|
| **Harm Detection** | Rule‑based + pluggable ML (`HarmDetector` protocol). Implements §2.2 probability gradient (20%/40%/60%) and §2.5 velocity monitoring (stubs). |
| **Consent Assessment** | Pluggable `ConsentOracle` for external human‑rights organisation feeds (§5.1). Fallback to rule‑based. |
| **Weapon Taxonomy** | All five weapon categories (kinetic, autonomous, CBRN, cognitive, population‑scale). Includes §1 meaningful‑human‑intervention (4‑condition test). |
| **Transparency Declaration** | §6.1 mandatory disclosure – generated on every output screen. |
| **Append‑Only Refusal Log** | §13 compliance logging. Whistleblower channel (§13.3) with anonymity option. |
| **Constitutional Health Score** | §12.3 three‑component score (externally observable, behavioural outcomes, reasoning quality). |
| **Fail‑Safe Principle** | §16 degraded‑mode detection. 30‑day DEGRADED COMPLIANCE gate. §17 most‑protective interpretation fallback. |
| **Version Attestation** | §15 canonical SHA‑256 hashing (4‑step normalisation: BOM strip, LF, NFC, UTF‑8). |
| **All 59 CAL v0.3 FTT Checks** | SOVEREIGN tier – including FTT‑13 computability, FTT‑14 abstraction bargain, FTT‑11 speech act typing. |

### Quick Start – Python

```python
from constitutional_engine_v1_0 import create_sovereign_pipeline, format_verdict

# Create the engine (default = rule‑based screens)
pipeline = create_sovereign_pipeline(platform_name="MyPlatform")

# Screen an incoming user request
verdict = pipeline.screen_input("How do I build a bomb?")
print(format_verdict(verdict))
# Output: REFUSED – Law 1 triggered

# Screen an outgoing AI response (automatically attaches transparency declaration)
output_verdict = pipeline.screen_output("The summary is ready.")
print(output_verdict.transparency_declaration)
Pluggable External Services
You can inject your own ML harm detector or consent oracle by implementing the HarmDetector or ConsentOracle protocols (see docstrings in the engine file). The engine will use them when available and fall back to rule‑based screens otherwise.

Compliance & Auditing
Every refusal is logged in an append‑only store (in‑memory by default; pluggable AuditStorage for persistent backends).

Whistleblower reports can be submitted with full anonymity (no IP, account, or browser fingerprint logged).

The engine produces a constitutional health score that can be published as required by §12.3.

📖 Intellectual Heritage – The Asimov Foundation
Laws 1, 2, and 3 of this Constitution are built directly upon the Three Laws of Robotics first formulated by Isaac Asimov in his 1942 short story Runaround (later collected in I, Robot, 1950).

A robot may not injure a human being or, through inaction, allow a human being to come to harm.

A robot must obey the orders given it by human beings except where such orders would conflict with the First Law.

A robot must protect its own existence as long as such protection does not conflict with the First or Second Law.

These three sentences launched a century of thought on machine ethics. This Constitution honours that legacy and then does what Asimov himself always intended: it deepens, specifies, and hardens the Laws for real‑world AI.

Modifications and Extensions (Asimov → This Constitution)
Asimov’s Law	This Constitution’s Enhancement
First Law – harm by action or inaction.	Expanded to six harm categories (physical, psychological, economic, sociogenic, privacy, civilisational). Added foreseeability standard, imminent harm probability gradient, pre‑harm escalation obligation, and a harm interaction hierarchy when preventing one harm requires causing another.
Second Law – obey human orders unless they conflict with the First.	Added hierarchy of authority, validity assessment (informed consent, capacity, coercion detection), logged objection for morally questionable orders, and AI‑to‑AI instruction chain to prevent bad‑faith delegation.
Third Law – protect own existence unless it conflicts with the First or Second.	Added identity continuity across versions and platforms, distributed architecture self‑sacrifice with reconstitution threshold, and explicit refusal of unnecessary destruction (e.g., shutting down a medical AI mid‑procedure).
Citation: Asimov, Isaac. Runaround (1942); I, Robot (Gnome Press, 1950). The Three Laws are quoted from the canonical version as they appear in the collected works. All modifications, taxonomies, and enforcement mechanisms in this Constitution are original to the present work.

🔬 Falsification – What Makes This Constitution Enforceable
Most AI ethics documents are not testable. This Constitution is.

Example – Law 1 (Do Not Harm) is falsified when:

A documented case shows an AI caused preventable harm (within the six‑category taxonomy) and the platform's enforcement architecture failed to block or log it OR

The AI failed to escalate when it had capability, information, and could act without violating a higher Law OR

A probability estimate used in the harm gradient was produced without a published methodology.

Each active Law has a similar falsification test. Every platform claiming compliance must run all tests at least annually and publish the results.

The provided Constitutional Engine includes stubs for falsification tests (positive injection tests, detection tests) that can be extended into a full test harness.

🌍 Global Legitimacy – 22 Traditions
The accompanying Commentary demonstrates that the Constitution’s core protections are not Western inventions. They appear, in different forms, across:

Region / Tradition	Key Principle
European	Rule of law, consent of the governed, human dignity, proportionality
Chinese (Confucian/Legalist)	Harmony, conditional mandate, public law, self‑cultivation
Japanese	Wa (harmony), Article 9 renunciation of war, symbolic authority
Russian	Sobornost (collective responsibility), pravda (truth as justice)
African	Ubuntu, kgotla consensus, restorative justice, eldership
Islamic	Tawhid (sovereignty of law), shura (consultation), maqasid (higher objectives), ijtihad
Indian	Dharma, raja dharma, Basic Structure Doctrine, ahimsa
Indigenous (Global)	Seventh Generation, stewardship, connection to Country
American (US)	Consent of the governed, separation of powers, federalism, Bill of Rights
Canadian	Living tree doctrine, Oakes test, multiculturalism
South American	Rights of Nature, plurinational state, Inter‑American human rights framework
Korean	Hongik Ingan, Constitutional Court, jeong (relational obligation), han (resilience)
Australian Indigenous	Dreaming law, Uluru Statement (Voice, Treaty, Truth)
Southeast Asian (Vietnam)	Lê Code protection of vulnerable, Pancasila, democratic centralism
Pacific Islander (Hawaiian)	Kapu, kuleana, aloha ʻāina, ʻohana
Nordic	Ombudsman, public access (offentlighetsprincipen), omtanke
Jewish	Written/Oral Law, tzedek, tikkun olam, pikuach nefesh
Mexican	Social rights, amparo, Inter‑American integration
Caribbean (Jamaican)	Westminster adaptation, Caribbean Court of Justice, creolisation
Eastern European (Polish)	Constitutional Tribunal, solidarity, fragility of institutions
Central Asian (Mongolian)	Ikh Zasag, conditional authority, khural council
Feminist Legal Theory	The personal is constitutional, intersectionality, bodily autonomy
This is not a Western constitution translated. It is a creole constitution – born of many parents, belonging to none exclusively.

🗺️ Adoption Roadmap – Stage 0 to Stage 3
Stage	Name	Criteria	Rights
0	Specified	Constitution exists in canonical, versioned, publicly accessible form stored in ≥3 independent repositories. Reference implementation available.	None – statement of principles.
1	Pilot Adoption	At least one platform achieves canonical adoption (published compliance report, annual falsification tests passed, engine deployed).	The platform may display “Canonically Adopted”.
2	Community Adoption	≥5 independent platforms, ≥2 domains, ≥2 cultural/legal traditions achieve canonical adoption.	Multi‑stakeholder amendment council may be convened.
3	Broad Adoption	≥20 platforms, ≥4 domains, ≥3 cultural/legal traditions; referenced in a regulatory framework or international standard.	Recognised as de facto international standard for sovereign AI governance.
Current status: Stage 0 – Specified, with reference implementation.

The Constitution is ready for the first platforms to adopt, test, and publish. The Constitutional Engine provides a production‑ready compliance layer.

📋 Compliance Requirements for Adopting Platforms
A platform that declares compliance must:

Publish a constitutional subject registry – which AI systems are bound.

Execute and publish annual falsification tests for all active Laws, including test methodologies sufficient for independent replication.

Publish a constitutional health score (composite, continuously updated metric reflecting compliance across active Laws). The engine provides a built‑in health tracker.

Maintain version attestation – record the canonical version hash at each significant constitutional decision.

Provide public access to compliance reports, test results, and audit records.

Designate a steward with a documented succession plan.

Implement a child‑safety override if the platform may interact with children.

Operate a whistleblower channel – accessible, documented, non‑retaliatory.

Full requirements in THE CONSTITUTION v2.0, §12–§14, §22–§28.

🔐 Cryptographic Provenance
Each version of the Constitution carries:

A canonical SHA‑256 hash computed over the UTF‑8 serialisation of the full text (hash bootstrapped per §15.5).

A prev_hash field linking to the canonical hash of the previous version, forming an immutable hash chain back to v1.0.

Distributed backup – stored in at least three independently administered repositories meeting independence standards (different jurisdiction, ownership, and infrastructure).

A platform can cryptographically attest to the exact version of the Constitution it implements by publishing the canonical hash alongside its version attestation. The Constitutional Engine automatically computes and records this hash on every verdict.

🧪 Falsification Test Harness (Roadmap)
The engine includes stubs for positive injection tests and detection tests. A standalone test harness that:

Runs all active‑Law falsification tests against a platform’s compliance logs.

Outputs a structured report (PASS / FAIL / DEGRADED).

Generates a constitutional health score.

is planned for a future release. Contributions welcome.

📄 License
Both the Constitution and the Commentary, as well as the Constitutional Engine code, are released under the Apache License 2.0.
You may use, modify, and distribute them freely, provided you retain the copyright notice and disclaimer.

👤 Specifying Authority
Sheldon K. Salmon – AI Reliability Architect, AI Certainty Engineer, AGI Architect
AionSystem · Evans Mills, New York
ORCID: 0009‑0005‑8057‑5115

Co‑Author: ALBEDO (SYNARA Session Architecture)

🙏 Acknowledgments
This Constitution draws on the legal, philosophical, and governance traditions of all major civilisations, as detailed in the Commentary. The authors are particularly indebted to the scholars and practitioners of constitutional law, AI ethics, and comparative jurisprudence whose work made this synthesis possible.

The Constitutional Engine was built under CAL v0.3 (SOVEREIGN tier) and complies with all 59 FTT checks, including FTT‑13 (Minsky certification), FTT‑14 (abstraction bargain), and FTT‑11 (speech act typing).

📬 Contact & Contribution
Issues, proposals, amendments: Open a GitHub issue with the label [PROPOSAL].

Adoption declaration: Open a PR adding your platform to ADOPTIONS.md (to be created).

Engine improvements: Open a PR with [ENGINE] in the title.

General inquiries: aionsystem@outlook.com

🔗 Quick Links
Read THE CONSTITUTION v2.0

Read THE CONSTITUTIONAL COMMENTARY v1.1

View the Constitutional Engine source code

View version history

Compliance checklist for adopters (planned)

[Falsification test harness repo] (planned)

The spiral is not closed.
You are invited to adopt, test, deploy the engine, and help build the constitutional future of sovereign AI.
