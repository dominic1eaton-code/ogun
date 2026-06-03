# ogun OS — Project Charter

**Document:** `ogun-charter.md`
**Version:** 0.1.0-beta
**Project:** Ogún · 2026
**Owner:** Dominic Eaton (`@eatondo`) · The Ogun Foundation
**Organization:** [The Ogun Foundation](https://gitlab.com/ogun-foundation)
**Repository:** [gitlab.com/ogun-foundation/ogun](https://gitlab.com/ogun-foundation/ogun)
**License:** GNU General Public License v3.0
**Status:** Active · Alpha → Beta Transition
**Last Updated:** June 2026

---

## Table of Contents

1. [Purpose](#1-purpose)
2. [Mission](#2-mission)
3. [Brief](#3-brief)
4. [Value Proposition](#4-value-proposition)
5. [Vision](#5-vision)
6. [Goals](#6-goals)
7. [Objectives](#7-objectives)
8. [Milestones](#8-milestones)
9. [Assumptions](#9-assumptions)
10. [Risks](#10-risks)
11. [Constraints](#11-constraints)
12. [Opportunities](#12-opportunities)
13. [Stakeholders](#13-stakeholders)
14. [Owners](#14-owners)
15. [Scope](#15-scope)
16. [Deliverables](#16-deliverables)
17. [Timeline](#17-timeline)
18. [Budget & Resources](#18-budget--resources)
19. [Roles & Responsibilities](#19-roles--responsibilities)
20. [Success Criteria](#20-success-criteria)

---

## 1. Purpose

ogun OS exists to give independent workers — freelancers, founders, creators, contractors, consultants, investors, and gig workers — a structured operating environment designed specifically for the way their professional lives actually work. Most independent workers are already running enterprises. Those enterprises have no structure, no persistent memory, no governance model, and no intelligence layer. The gap between what independent workers produce and what they could produce is not a motivation gap — it is a structural gap.

ogun OS closes the structural gap at the operating system level. Not at the application layer. Not with a SaaS subscription. At the kernel boundary, where identity, enterprise isolation, capability enforcement, and agent authority are enforced before any user-space application executes.

---

## 2. Mission

**Build and ship the world's first sovereign personal enterprise OS** — a Rust-native, locally-installed, cryptographically verified operating environment in which every independent worker can structure their enterprises, engagements, assets, workflows, agents, and value production as a first-class system concern, enforced at the kernel boundary, not at the policy document.

---

## 3. Brief

ogun OS is a hosted operating-system layer built in Rust and Tauri that runs on top of a host OS (Windows first; Linux, macOS, mobile, web, and server editions designed for subsequent releases) rather than replacing it. It presents a unified, capability-gated, workspace-oriented runtime with its own signed boot chain, virtual hardware emulation layer, kernel subsystems, SDKs, applications, and release artifacts.

Named after Ogun — the Yoruba orisha of iron, technology, and creation — the system embodies the principle of forging raw platform capabilities into a coherent, identity-consistent operating environment. The project is governed under The Ogun Foundation, is licensed GPL-3.0, and is developed and maintained by Dominic Eaton (`@eatondo`) as founder and primary steward.

The planned first public release is **`0.1.0-beta` — Windows x64 Desktop Edition — June 2026**. The current development state is `0.1.0-alpha`.

---

## 4. Value Proposition

### For Independent Workers

Every independent worker is already running an enterprise. Most just don't know it, because it has no structure, no memory, no rules, and no intelligence layer. ogun OS makes the enterprise explicit, structured, measurable, and compounding.

- **Freelancers / Operators:** Understand their real Effective Hourly Rate (EHR) across every client — including admin time and scope creep. Know which clients cost more than they produce.
- **Creators:** See which content formats earn the most per hour of production time. Know when to productize what's working into income that compounds.
- **Founders / Builders:** Track whether building produces more value per hour than consulting would. Manage MRR, runway, and equity-per-hour in one unified system.
- **Investors:** Unify portfolio view — stocks, real estate, crypto, angel positions — with passive income ratio and coverage ratios in a single runtime.
- **CNOs (Chief Navigation Officers):** Run a portfolio of enterprises as a single optimized system. See cross-enterprise synergies in real time.

### Technical Differentiators

- **Architectural depth no SaaS competitor can replicate:** virtual UEFI layer, three-stage bootloader verification (image signature → manifest integrity → host key re-derivation), 15 statically linked kernel subsystems, capability-gated IPC (Elegua Protocol), cross-enterprise data isolation (Ọpọn Protocol), software-defined execution scheduler (ogun-cpu), P2P network layer (OgunNet v2.0.0), and Rust-native embedded database (RustyDB).
- **Enterprise isolation at the kernel boundary:** The Ọpọn Protocol enforces cross-enterprise data isolation in the kernel Security subsystem — not at the application layer. This is the only credible isolation model in the independent-worker software market.
- **Agent governance model:** Sambara's four authority levels (OBSERVE → RECOMMEND → EXECUTE_BOUNDED → FULL_AUTONOMY), with escalation requiring explicit operator interaction, is a more auditable agent model than any current solopreneur platform.
- **Local-first, offline-capable, performance-native:** Rust + Tauri starts faster and uses less memory than Electron-based alternatives. No cloud dependency for core functionality.
- **Open source (GPL-3.0):** Architectural transparency as both philosophical commitment and community development strategy.

---

## 5. Vision

**The operating system for the independent worker's enterprise** — a sovereign runtime where every freelancer, creator, founder, and investor operates with the same structural clarity, measurement precision, intelligence governance, and data sovereignty that large enterprises have always had, but built specifically for how independent professionals actually work.

The long-term vision: ogun OS becomes the foundational platform for independent economic participation — the layer below every independent professional's tools — on Desktop, Web, Mobile, Server, and Device editions, across every major platform, in every market where independent work is the dominant mode of professional life.

---

## 6. Goals

### Goal 1 — Ship the Foundational Runtime (0.1.0-beta)
Deliver the complete foundational runtime for the Windows x64 Desktop Edition: virtual UEFI, bootloader, kernel core, all 15 subsystems, emulation and execution model, desktop host, drivers, OS apps, utility apps, Tier-4 personal enterprise suite, SDKs, signed images, and installer artifacts.

### Goal 2 — Establish the Personal Enterprise Model
Embed the personal enterprise paradigm — enterprises, lifecycle stages, engagement pipelines, EHR computation, Shock Insight, value dimensions — as a first-class kernel concern, enforced at the process boundary, not bolted on at the application layer.

### Goal 3 — Create and Own a New Product Category
Establish "sovereign personal enterprise OS" as a recognized, credible, and defensible product category that is clearly distinct from productivity apps, SaaS workspaces, cloud agent platforms, and bare-metal operating systems.

### Goal 4 — Build Technical Credibility Through Open Architecture
Use the open-source codebase, architecture documentation, and rigorous contribution standards to demonstrate that the architectural depth is real — not feature-list theater.

### Goal 5 — Seed the First Operator and Developer Communities
Build a first-tier community of technically sophisticated independent workers (developers, consultants, solo founders) and Rust/systems engineers who become the initial beta users, contributors, and advocates.

### Goal 6 — Establish the Platform for Subsequent Editions
Design the architecture to support Web, Mobile (Android/iOS), Server, and Device editions in subsequent releases, without requiring core runtime rework.

---

## 7. Objectives

### Runtime Objectives

- Complete the `0.1.0-beta` Windows x64 Desktop Edition artifact set: `ogun-setup-windows-0.1.0-beta.exe`, `ogun-desktop-windows-0.1.0-beta.exe`, `ogun-emulator-windows-0.1.0-beta.exe`, `ogun-windows-0.1.0-beta.img`, `ogun_image_tool-windows-0.1.0-beta.exe`, and all associated checksums and signature metadata.
- Restore the top-level Cargo workspace to a clean `cargo check --workspace` pass across all submodules — eliminating all P0 compile blockers identified in `TODO.md`.
- Implement the three-stage boot verification pipeline (image signature, manifest integrity, host key re-derivation) to production specification.
- Implement all 15 kernel subsystems to their canonical initialized state as documented in DESIGN.md and the architecture specification.
- Implement the Elegua Protocol IPC bus, Ọpọn Protocol enforcement, and Sambara agent authority system to their beta specifications.
- Implement the full RustyDB backend for session state, audit indexes, node identity, and module registry.

### Product Objectives

- Deliver the complete Tier-4 Personal Enterprise Suite (enzo, kogi, dongo, ume, heshima, shango, igi, akeel, moto, zamani, sambara, qala, shaba, kanna, zuri, ayo, mizeez, orun, apapo, didara, misimu) to beta functionality.
- Deliver the Tier-2 OS Apps (ogun-desktop, ogun-shell, ogun-command-center, ogun-settings, ogun-security-center, ogun-operator-center, ogun-file-explorer, ogun-messenger, ogun-search, ogun-assistant, ogun-app-store, ogun-package-manager) to functional state.
- Deliver the Tier-3 Utility Apps (ogun-notes, ogun-tasks, ogun-focus, ogun-calendar, ogun-contacts) to functional state.
- Implement onboarding, workspace management, operator profile, and enterprise lifecycle management.
- Implement five operator persona hypergrid templates (Freelancer/Operator, Creator, Builder/Founder, Investor, CNO).

### Security Objectives

- Enforce all production security invariants without exception: image signature validation mandatory, boot verification failure halts before runtime handoff, Ọpọn enforcement always active, capability audit before every grant/denial, CleanShutdownMarker as final act.
- System private key material never written to `~/.ogun/`; stored exclusively in host OS keychain.
- All production image signing keys held outside the repository and CI artifact set.

### Community & Ecosystem Objectives

- Publish the `0.1.0-beta` release on the GitLab repository with accurate, complete release documentation.
- Publish accurate download pages, architecture documentation, SDK reference, and CONTRIBUTING guide.
- Establish private security disclosure process per SECURITY.md before public release.
- Begin seeding the developer community through open-source release and documentation quality.

---

## 8. Milestones

| # | Milestone | Target |
|---|---|---|
| M0 | **P0 Cargo Workspace Restored** — all submodule workspaces pass `cargo check --workspace`; merge conflicts, stale paths, and duplicate names resolved | June 2026 (immediate) |
| M1 | **Boot Chain Functional** — `ogun-desktop.exe → ogun-emulator → virtual devices → ogun-uefi → ogun-bootloader → ogun-kernel-core` runs end-to-end with passing three-stage verification | June 2026 |
| M2 | **Session Manager Active** — `ogun-session-manager` handles lock screen, authentication, and session context binding; all 15 subsystems initialize in canonical order | June 2026 |
| M3 | **OS and Utility Apps Functional** — Tier-2 OS apps and Tier-3 utility apps are launchable; desktop environment is visible | June 2026 |
| M4 | **Personal Enterprise Suite (Tier 4) Beta-Ready** — core Tier-4 apps (enzo, kogi, dongo, qala, sambara) operational to beta quality | June 2026 |
| M5 | **Security Invariants Verified** — automated tests cover boot rejection, image kind rejection, ABI mismatch, manifest mismatch, and host-key mismatch | June 2026 |
| M6 | **`0.1.0-beta` Artifact Set Released** — signed Windows x64 platform image, installer, launcher, emulator, and image tool published with checksums and documentation | June 2026 |
| M7 | **`0.1.0-stable` Candidate** — post-beta patch releases addressing rough edges, performance improvements, and RustyDB backend stabilization | Post-June 2026 |
| M8 | **macOS Apple Silicon Desktop Edition** — second platform target | Post-beta |
| M9 | **Linux x86_64 Desktop Edition** — third platform target | Post-beta |
| M10 | **Mobile Editions (Android/iOS)** — `ogun-host-android`, `ogun-host-ios` complete | Post-beta |
| M11 | **Web Edition (WASM)** — `ogun-host-web` complete; browser-native runtime | Post-beta |
| M12 | **Server Edition** — multi-tenant `ogun-server-host` | Post-beta |

---

## 9. Assumptions

- **Host platform availability:** Windows x64 is the beta target. All development environments, CI, and release pipelines assume Windows x64 is the primary development host.
- **Rust toolchain stability:** Rust stable toolchain with Cargo is assumed available and stable. The project compiles against the Rust stable channel.
- **Tauri 2.0+ compatibility:** The Tauri 2.0+ framework is assumed to provide the WebviewWindow surface, IPC bridge, and Authenticode signing pipeline required by the beta release.
- **ed25519 signing infrastructure:** The release image signing pipeline (ed25519 private key) is assumed to be managed outside the repository and CI artifact set, per the security invariants.
- **GPL-3.0 legal adequacy:** The GPL-3.0 license is assumed appropriate for the project's open-source community strategy and compatible with all incorporated dependencies.
- **Yoruba cultural usage:** The use of Yoruba orisha names (Ogun, Elegua, Ọpọn, Sambara) is treated as a meaningful cultural attribution, not decorative naming. Documentation context and respectful use are assumed as ongoing obligations.
- **Solo founder development model:** Current development velocity is calibrated to a solo or very small team working against a concentrated sprint. Beta timeline assumes focused execution on the P0 priority list.
- **Market timing:** The independent worker market (72.9M US workers, projected >50% of workforce by 2027) continues to grow. The "sovereign personal enterprise OS" category position remains unoccupied by a direct competitor through the beta period.

---

## 10. Risks

### R1 — Implementation-to-Specification Gap (Critical)
The documentation and specification are substantially ahead of the code. Many crates are alpha scaffolding with placeholder implementations. The top-level `cargo check --workspace` currently fails to load. Closing this gap before the June 2026 beta target requires concentrated, focused engineering execution. **Probability: High. Impact: Critical. Mitigation: Execute P0 TODO list immediately; gate all feature work on clean workspace compile.**

### R2 — Beta Timeline Compression (High)
The June 2026 beta target is aggressive given the current P0 build blockers. Even after the workspace loads cleanly, core implementations (Elegua Protocol, RustyDB, Sambara, virtual devices, kernel subsystems) need substantial completion work. **Probability: Medium-High. Impact: High. Mitigation: Scope the beta to a working runtime first; Tier-4 app completeness is secondary to a bootable, installable, verifiable system.**

### R3 — Installation Friction as Adoption Barrier (Medium)
A full installer, signed images, and a boot chain are what make ogun OS architecturally credible — and exactly what will cause friction compared to zero-friction SaaS onboarding. The target user is accustomed to signing up with an email. **Probability: High. Impact: Medium. Mitigation: Invest heavily in the onboarding experience; make the first-boot moment high-signal and worth the setup cost.**

### R4 — Windows-Only Beta Limits Addressable Audience (Medium)
macOS-native creative and tech freelancers are a large, affluent segment. Mobile-first independent workers in international markets are entirely excluded by the Windows-only beta. **Probability: Confirmed. Impact: Medium. Mitigation: Explicitly non-block the beta on other platforms; design and document post-beta platform roadmap clearly.**

### R5 — SaaS Incumbents Accelerating (Medium)
Notion launched AI Agents in late 2025. The "solopreneur OS" framing is becoming mainstream SaaS marketing language. The window during which ogun OS's category position is genuinely differentiated may be narrowing. **Probability: Medium. Impact: Medium. Mitigation: Differentiate at the architecture and security layer — features incumbents cannot replicate by shipping a flag.**

### R6 — Supporting Library Immaturity (Medium)
`elegua`, `rustydb`, `bula`, `jaku`, and `oya` have extensive specification claims but minimal or placeholder code. If any of these are beta-critical, the sprint to completion is significant. **Probability: Medium. Impact: Medium-High. Mitigation: Explicitly classify each library as beta-critical or beta-optional; do not block Windows Desktop beta on non-critical libraries.**

### R7 — Single-Maintainer Bus Factor (Medium)
The project is currently founder-led by one primary maintainer. Governance, architecture decisions, security triage, and release authority all concentrate in one person. **Probability: Structural. Impact: Medium. Mitigation: Governance model in GOVERNANCE.md is well-documented; priority is shipping beta to attract contributors; maintainer expansion is a post-beta goal.**

### R8 — Security Vulnerability During Alpha (Low-Medium)
Alpha-stage code with placeholder implementations may have security gaps that don't align with the production invariants documented in SECURITY.md and DESIGN.md. **Probability: Low-Medium. Impact: High. Mitigation: Apply all production invariants from day one; never treat alpha artifacts as production-secure; do not distribute alpha builds publicly.**

---

## 11. Constraints

### Technical Constraints
- **Windows x64 only for 0.1.0-beta.** macOS, Linux, Web, Mobile, Server, and Device editions are designed but not shipping.
- **GPL-3.0 license.** All contributions are accepted under GPL-3.0. Subprojects may specify a different license for their own files explicitly.
- **Rust stable toolchain.** No nightly-only features in production crates.
- **Tauri 2.0+ as the desktop surface layer.** No direct framebuffer writes; virtual monitor renders via Tauri surfaces only.
- **Host OS API access only through approved boundaries.** `ogun-emulator-backend` is the sole component that calls host OS APIs; no component above it does so.
- **No raw packet injection.** Virtual network adapters use OS sockets only.
- **`opn_enforced = true` is non-negotiable.** No operator, app, or config file may disable Ọpọn enforcement.
- **Virtual host nesting depth ≤ 10.**
- **`CleanShutdownMarker` must be the last act of every shutdown.**
- **ABI version (`OGUN_ABI_VERSION`) must be honored at all component boundaries.**

### Resource Constraints
- Founder-led, solo or very small team. Contributor base is currently forming.
- No disclosed external funding or paid engineering headcount beyond the founder.
- Development environment is Windows x64 (`C:\dev\ogun`).

### Scope Constraints
- 0.1.0-beta does not include: macOS packaging, Linux packaging, Web Edition, Mobile Edition, Server Edition, Device Edition, post-beta storage backend migration, or full Bula/Jaku/Oya implementation.
- Beta release must not misrepresent the implementation state. All features described as shipping must be backed by artifacts and tests.

### Governance Constraints
- Security-sensitive decisions require steward approval. No public security disclosure before coordinated private triage.
- Architecture invariants may not be relaxed without an RFC and steward sign-off.
- Release scope and release dates are steward decisions.

---

## 12. Opportunities

### O1 — Unoccupied Category
No current product occupies the "sovereign personal enterprise OS" space. The architecture ogun OS is building — signed images, capability-gated kernel, workspace-bounded AI agents, enterprise isolation — is genuinely unoccupied. First-mover category definition is a rare and compounding advantage.

### O2 — Structural Market Tailwinds
The global gig economy is projected at $674.1B in 2026, growing at 15.79% CAGR. Full-time independent workers more than doubled from 13.6M (2020) to 27.7M (2024). Freelancers are projected to be >50% of the US workforce by 2027. The market is growing faster than the workforce itself.

### O3 — AI Governance as Differentiator
In a world of increasingly opaque cloud agents, Sambara's explicit authority model (OBSERVE → RECOMMEND → EXECUTE_BOUNDED → FULL_AUTONOMY) with operator-gated escalation is a defensible and auditable position. Compliance, professional liability, and client confidentiality are growing concerns for independent professionals.

### O4 — Local-First as Security and Performance Moat
As cloud dependency becomes a liability for independent professionals managing sensitive client data, local-first architecture with kernel-enforced enterprise isolation is a genuine differentiator. The Ọpọn Protocol's enforcement model is not achievable by cloud-native competitors without a full architectural rewrite.

### O5 — Open Source as Community Flywheel
GPL-3.0 combined with architecture documentation quality and rigorous contribution standards can attract serious Rust and systems engineers who are themselves independent workers or aligned with the mission. Contributors become advocates; advocates become users.

### O6 — Developer Ecosystem
An open SDK surface (ogun-app-sdk, ogun-service-sdk, ogun-kernel-sdk, ogun-driver-sdk, ogun-host-sdk), a documented IPC protocol (Elegua), and the `.ogun` package format create a platform on which other developers can build. Third-party integrations (28 categories, 100+ connectors planned) extend the network effect.

### O7 — Enterprise and Team Deployment Horizon
The Ọpọn Protocol's enterprise isolation, silent install mode, the Server Edition design, and OgunNet's P2P layer make multi-operator and enterprise deployment viable in a post-beta roadmap. The B2B surface is a natural expansion from the B2C operator foundation.

---

## 13. Stakeholders

| Stakeholder | Type | Interest |
|---|---|---|
| **Independent workers (freelancers, creators, founders, contractors, consultants, investors)** | Primary users (B2C) | A structured operating environment for their professional enterprise |
| **Developer / Rust engineering community** | Secondary audience | Open-source contribution, OS-layer systems work, SDK surface |
| **Enterprise / team operators** | Tertiary audience (post-beta) | Multi-operator deployment, compliance, and data isolation |
| **Dominic Eaton (`@eatondo`)** | Founder, steward, primary maintainer | Project direction, architecture integrity, release governance |
| **The Ogun Foundation** | Governing organization | Open-source stewardship, community hosting, release governance |
| **Contributors (current and future)** | Community | Code quality, documentation, ecosystem growth |
| **Host platform vendors (Microsoft, Apple, Linux distributions)** | Platform dependency | Host OS API stability, Tauri compatibility, signing infrastructure |
| **LLM providers (Anthropic, OpenAI, DeepSeek, Ollama)** | Integration dependency | Sambara agent driver availability and API stability |

---

## 14. Owners

| Area | Owner |
|---|---|
| **Project Steward** | Dominic Eaton (`@eatondo`) |
| **Architecture** | Dominic Eaton (`@eatondo`) |
| **Runtime (bootloader, kernel, session manager, subsystems)** | Dominic Eaton (`@eatondo`) |
| **Devices (emulator, virtual hardware)** | Dominic Eaton (`@eatondo`) |
| **SDK (ABI, component traits, manifests)** | Dominic Eaton (`@eatondo`) |
| **Applications (OS apps, utility apps, personal enterprise suite)** | Dominic Eaton (`@eatondo`) |
| **Tools (setup, image tool, packaging, release)** | Dominic Eaton (`@eatondo`) |
| **Documentation** | Dominic Eaton (`@eatondo`) |
| **Security** | Dominic Eaton (`@eatondo`) |
| **Marketing & Brand** | Dominic Eaton (`@eatondo`) |
| **Governance** | Dominic Eaton (`@eatondo`) |
| **Release Artifacts** | Dominic Eaton (`@eatondo`) |

*Note: Maintainer expansion by area is the post-beta governance goal. See GOVERNANCE.md for the maintainer role taxonomy.*

---

## 15. Scope

### In Scope — 0.1.0-beta (Windows x64 Desktop Edition)

**Runtime:**
- `ogun-desktop.exe` — user-facing launcher and autostart entry
- `ogun-emulator` — Tauri 2.0+ main entry point and top-level supervisor
- `ogun-emulator-backend` — sole host OS API boundary
- Four virtual hardware devices: `ogun-virtual-display-monitor`, `ogun-virtual-platform-host`, `ogun-virtual-cpu`, `ogun-virtual-network-adapter`
- `ogun-uefi` — virtual UEFI firmware (four phases: Pre-Init → Device Init → Boot Menu → Handoff)
- `ogun-bootloader` — three-stage verification pipeline and KernelBootBundle handoff
- `ogun-image-format` — shared image parsing, signing, and validation library
- `ogun-kernel-core` — 15 subsystem initialization, 17-step boot sequence
- `ogun-host-service` — persistent supervisor daemon
- `ogun-session-manager` — authentication, session context, workspace lifecycle, clean shutdown

**Kernel Subsystems (all 15):** Telemetry, Memory, Process, IPC, Storage, VFS, Security, Services, Host, Session, Display, State, Components, Network, Emulation

**SDK:** `ogun-types`, `ogun-image-format`, `ogun-app-sdk`, `ogun-service-sdk`, `ogun-kernel-sdk`, `ogun-driver-sdk`, `ogun-host-sdk`

**Protocols:** Elegua Protocol v0.3.0 (IPC), Ọpọn Protocol (enterprise isolation), OgunNet v2.0.0 (P2P network)

**Applications:**
- Tier-1: modules-manager, process-manager, ipc-broker
- Tier-2 OS Apps: ogun-desktop, ogun-shell, ogun-command-center, ogun-settings, ogun-security-center, ogun-operator-center, ogun-file-explorer, ogun-messenger, ogun-search, ogun-assistant, ogun-app-store, ogun-package-manager
- Tier-3 Utility Apps: ogun-notes, ogun-tasks, ogun-focus, ogun-calendar, ogun-contacts
- Tier-4 Personal Enterprise Suite: enzo, kogi, dongo, ume, heshima, shango, igi, akeel, moto, zamani, sambara, qala, shaba, kanna, zuri, ayo, mizeez, orun, apapo, didara, misimu

**Intelligence:** Sambara agent system with 14 platform-registered domain agents; LLM drivers for Anthropic Claude, OpenAI, DeepSeek, Ollama

**Storage:** RustyDB embedded database backend

**Tools:** `ogun-setup.exe` (installer), `ogun-image-builder` / `ogun-image-tool`

**Configuration:** `ogun.toml`, `display.toml`, `emulation.toml`, `uefi.toml`

**Operator Personas:** Freelancer/Operator, Creator, Builder/Founder, Investor, CNO — with Hypergrid Templates

### Out of Scope — 0.1.0-beta

- macOS Apple Silicon Desktop Edition
- Linux x86_64 Desktop Edition
- Web Edition (WASM / `ogun-host-web`)
- Mobile Edition (Android / iOS)
- Server Edition (`ogun-server-host`)
- Device Edition
- Fully implemented Bula (UI generation language), Jaku (release automation), or Oya (architecture generation) — unless explicitly beta-critical
- Post-beta storage backend migration (beyond RustyDB/beta storage scope)
- Third-party integrations (planned for post-beta releases)
- Public bug bounty program
- Multi-tenant or enterprise team deployment tooling

---

## 16. Deliverables

### Release Artifacts

| Artifact | Description |
|---|---|
| `ogun-setup-windows-0.1.0-beta.exe` | User-facing setup binary; includes `ogun-installer`; manages ogun OS installation; registers `ogun-desktop.exe` as autostart; silent install mode available |
| `ogun-desktop-windows-0.1.0-beta.exe` | User-facing launcher; starts ogun OS via `ogun-emulator`; manages image modifications, repairs, and updates |
| `ogun-emulator-windows-0.1.0-beta.exe` | Main entry point (Tauri application); initializes virtual hardware; supervises `ogun-host-service` for the full session lifetime |
| `ogun_desktop_windows-windows-0.1.0-beta.exe` | `ogun-host-service` for Windows; all subsystems statically linked; Authenticode-signed |
| `ogun-windows-0.1.0-beta.img` | Signed platform kernel image for Windows x64; ed25519 signed; zstd level-19 compressed; per-section SHA-256 checksums |
| `ogun_image_tool-windows-0.1.0-beta.exe` | Developer/operator image authoring tool |
| `SHA-256 checksums` | Checksums for all release artifacts |
| `Signature metadata` | Release signing metadata |

### Documentation Deliverables

| Document | Status |
|---|---|
| `README.md` | Umbrella repository map and quick-start commands |
| `DESIGN.md` | Architecture summary and invariants |
| `CHANGELOG.md` | Complete 0.1.0-beta component scope |
| `GUIDE.md` | Complete user guide |
| `CONTRIBUTING.md` | Contribution workflow |
| `SECURITY.md` | Vulnerability disclosure and supported versions |
| `GOVERNANCE.md` | Project roles and decision-making |
| `SUPPORT.md` | Where to get help |
| `ogun-architecture-0.1.0-beta.md` | Canonical system architecture document |
| `ogun-os-product-specification.md` | Canonical product specification |
| `ogun-execution-model.md` | Execution model specification |
| Operator user documentation | Install, onboard, operate, repair, update, uninstall |
| SDK reference documentation | App, service, kernel, driver, host SDK reference |
| Architecture documentation site | `ogun-docs.eatondo000.workers.dev` |
| Developer site | `ogun-developer.eatondo000.workers.dev` |
| Home site | `ogun.eatondo000.workers.dev` |

### Community Deliverables

- Open-source beta release on GitLab, mirrored to GitHub and Codeberg
- Beta waitlist and community seeding communications
- Architecture walkthrough content for technical community (X, LinkedIn, GitLab)

---

## 17. Timeline

| Phase | Period | Key Activities |
|---|---|---|
| **0.1.0-alpha (current)** | 2026 (internal) | Architecture design, scaffolding, type foundations, image format, bootloader structure, host service skeleton. Internal only; not publicly distributed. |
| **P0 Sprint — Workspace Restoration** | June 2026 (immediate) | Fix all Cargo compile blockers: merge conflict in `ogun-os/src/servers/ogun-host-server`, stale `ogun_types` path dependencies, duplicate crate names in `ogun-devices`, compile errors in `ogun-runtime` and `ogun-sdk`. Achieve clean `cargo check --workspace`. |
| **P0 Sprint — Architecture Alignment** | June 2026 | Normalize crate names to beta specification, resolve workspace structure decisions, ensure `ogun-types` is resolved from one canonical location. |
| **P1 Sprint — Core Implementation** | June 2026 | Implement boot chain end-to-end, session manager, 15 kernel subsystems, Elegua Protocol, Ọpọn Protocol, RustyDB backend, Sambara agent system. |
| **P1 Sprint — Application Completion** | June 2026 | OS apps, utility apps, core Tier-4 apps (enzo, kogi, dongo, qala) to beta functionality. |
| **P1 Sprint — Tests and Security** | June 2026 | Security invariant tests, image verification tests, boot integration tests, installer integration tests, end-to-end release smoke test. |
| **Beta Release Preparation** | June 2026 | Artifact build and signing, checksum generation, documentation finalization, known-limitations file, release notes, website updates. |
| **0.1.0-beta Public Release** | June 2026 | Windows x64 Desktop Edition public release on GitLab. |
| **0.1.0.x Patch Releases** | Post-June 2026 | Rough edge fixes, performance improvements, `enterprise_id` completeness in IPC messages, release candidate versioning. |
| **0.2.0 — Storage Backend Stabilization** | Post-beta | Migration to stable persistent backend; RustyDB graduation. |
| **macOS and Linux Desktop Editions** | Post-beta | Second and third platform targets. |
| **Mobile Editions** | Post-beta | Android arm64, iOS arm64. |
| **Web Edition** | Post-beta | WASM in-browser runtime. |
| **Server Edition** | Post-beta | Multi-tenant headless runtime. |

---

## 18. Budget & Resources

### Current Resource State

ogun OS is a founder-led open-source project at the alpha stage. The following resources are in place:

| Resource | Status |
|---|---|
| Founder engineering (Dominic Eaton) | Active |
| GitLab repository (primary) | Active — `gitlab.com/ogun-foundation/ogun` |
| GitHub mirror | Active — `github.com/dominic1eaton-code/ogun` |
| Codeberg mirror | Active — `codeberg.org/eatondo000/ogun` |
| Cloudflare Workers (sites hosting) | Active — home, docs, developer, prototype, tools sites |
| Development environment | Windows x64 — `C:\dev\ogun` |
| Rust stable toolchain | Active |
| Node.js / npm / Tauri 2.0+ | Active |

### Resource Needs (Beta Sprint)

- **Engineering time:** Concentrated founder sprint to close P0 blockers and P1 implementation items per the TODO.md priority list.
- **CI/CD pipeline:** Top-level CI gate once `cargo metadata` works cleanly. Requires GitLab CI configuration tied to the canonical workspace.
- **Code signing:** Windows Authenticode certificate for `ogun-host-service` and installer. ed25519 image signing key infrastructure for the release image pipeline.
- **Beta test users:** Small cohort of independent workers (freelancers, founders, creators) willing to install and run the beta on Windows x64 and provide structured feedback.

### Post-Beta Resource Considerations

- Community contributor pipeline (Rust engineers, app developers, systems programmers)
- Potential maintainer appointments by area (see GOVERNANCE.md role taxonomy)
- Platform SDK/signing credentials for macOS (Apple Developer Program) and Android (Google Play) for mobile and desktop editions
- Hosting and infrastructure for documentation, artifact distribution, and community channels

---

## 19. Roles & Responsibilities

| Role | Person / Entity | Responsibilities |
|---|---|---|
| **Project Steward** | Dominic Eaton (`@eatondo`) | Final authority on release scope, security decisions, architecture invariants, licensing, repository structure, and public project positioning. |
| **Runtime Maintainer** | Dominic Eaton (`@eatondo`) | Bootloader, image format, kernel, session manager, storage, and subsystem runtime. |
| **Device Maintainer** | Dominic Eaton (`@eatondo`) | Emulator, virtual UEFI, virtual CPU, virtual monitor, virtual host platform, network adapter. |
| **SDK Maintainer** | Dominic Eaton (`@eatondo`) | ABI contracts, component traits, manifests, and examples. |
| **Components Maintainer** | Dominic Eaton (`@eatondo`) | OS apps, utility apps, hosts, drivers, and services. |
| **Apps Maintainer** | Dominic Eaton (`@eatondo`) | Tier-4 personal enterprise suite applications. |
| **Tools Maintainer** | Dominic Eaton (`@eatondo`) | Setup, image tooling, packaging, repair, update, and release tooling. |
| **Docs Maintainer** | Dominic Eaton (`@eatondo`) | Product specs, architecture docs, release notes, user guide, and support docs. |
| **Security Maintainer** | Dominic Eaton (`@eatondo`) | Vulnerability triage, advisories, security review, and disclosure coordination. |
| **The Ogun Foundation** | Governing Organization | Open-source stewardship, community hosting, organizational identity. |
| **Contributors** | Open community | Bug fixes, tests, documentation improvements, feature prototypes in `ogun-test-features/`. Subject to `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`. |

### Contributor Responsibilities

Contributors are expected to:
- Read `README.md`, `DESIGN.md`, `SECURITY.md`, and `CHANGELOG.md` before contributing.
- Preserve all architecture invariants documented in `DESIGN.md` and `CONTRIBUTING.md`.
- Use private disclosure per `SECURITY.md` for any security-sensitive finding.
- Accept maintainer decisions on scope, architecture, and release timing.
- Follow `CODE_OF_CONDUCT.md` in all project spaces — including the Technical Disagreement standards that distinguish substantive critique from personal attacks.
- License contributions under GPL-3.0.

---

## 20. Success Criteria

### Beta Release Success Criteria

The `0.1.0-beta` release is considered successful when all of the following are true:

**Build and Compile:**
- [ ] `cargo check --workspace` passes cleanly across all submodule workspaces from the top-level umbrella
- [ ] `cargo fmt --all` passes cleanly across all supported workspaces
- [ ] All P0 compile blockers from the June 2026 TODO snapshot are resolved

**Boot Chain:**
- [ ] `ogun-desktop.exe → ogun-emulator → virtual devices → ogun-uefi → ogun-bootloader → ogun-kernel-core → ogun-host-service → ogun-session-manager` completes the full boot sequence without error
- [ ] Three-stage boot verification (image signature, manifest integrity, host key re-derivation) passes on a valid platform image
- [ ] Boot halts on invalid image signature, wrong image kind, ABI mismatch, manifest mismatch, and host key mismatch — verified by automated tests
- [ ] `CleanShutdownMarker` is written as the last act of a clean shutdown

**Installation:**
- [ ] `ogun-setup-windows-0.1.0-beta.exe` installs successfully on a clean Windows x64 machine
- [ ] Image signature is validated before any extraction
- [ ] `~/.ogun/` directory tree is scaffolded correctly with minimum 0o700 permissions
- [ ] `SystemKey` is generated and stored in Windows DPAPI; `HostKey` is derived and persisted correctly
- [ ] `ogun-desktop.exe` is registered as the sole autostart entry via Task Scheduler

**Security Invariants (all must pass automated verification):**
- [ ] `opn_enforced = true` cannot be disabled by config, operator, app, or IPC
- [ ] Every capability grant and denial is audited before returning
- [ ] System private key material is never written to `~/.ogun/`
- [ ] Image signing keys are not present in the repository or release artifacts

**Runtime:**
- [ ] All 15 kernel subsystems initialize in canonical order without error
- [ ] Elegua Protocol IPC bus routes messages correctly with workspace isolation
- [ ] Ọpọn Protocol enforces cross-enterprise data isolation
- [ ] Sambara agent system initializes with declared authority levels; escalation requires explicit operator action
- [ ] RustyDB backend persists and recovers session state across restarts

**Applications:**
- [ ] Tier-2 OS apps launch successfully and are usable in the desktop environment
- [ ] Tier-3 utility apps are functional
- [ ] Core Tier-4 apps (enzo, kogi, dongo, qala) are operational to beta quality

**Artifacts:**
- [ ] All six beta artifact binaries are built, signed, and published with checksums
- [ ] Platform image (`ogun-windows-0.1.0-beta.img`) validates ed25519 signature and per-section SHA-256 checksums
- [ ] Release smoke test passes: install → launch → authenticate/onboard → desktop visible → clean shutdown → relaunch → session restore

**Documentation:**
- [ ] `CHANGELOG.md` accurately reflects shipped beta scope — no undocumented omissions
- [ ] Known limitations for the beta release are documented before publication
- [ ] Release and download pages on the website are accurate and gated by the signed artifact manifest

### Long-Term Success Criteria

**Year 1 (post-beta):**
- macOS and Linux Desktop Editions shipped
- Mobile Edition (Android/iOS) in beta
- Active contributor community with at least one maintainer appointed per area
- Developer SDK documented with third-party app examples
- Initial operator community established with real EHR measurement and enterprise lifecycle feedback

**Year 2–3:**
- Web Edition shipped
- Server Edition for enterprise team deployment
- Third-party integration ecosystem active (connector marketplace)
- ogun OS recognized as the canonical "sovereign personal enterprise OS" category — referenced by name in discussions about independent worker tooling
- Sambara agent system operating at `FULL_AUTONOMY` for a significant subset of trusted operator workflows
- International market expansion via mobile and web editions reaching global gig economy participants

---

## Appendix A — Core Terminology

| Term | Definition |
|---|---|
| **ogun host** | A complete, running ogun OS runtime instance (virtual UEFI + bootloader + kernel + session manager) |
| **Personal enterprise** | The structured professional life of an independent worker — modeled as an enterprise with lifecycle stages, engagements, assets, revenue, and agents |
| **Operator** | The independent worker who runs ogun OS — the human principal of a personal enterprise |
| **EHR** | Effective Hourly Rate — the primary value metric for operator time |
| **EAV** | Effort-Adjusted Value — value accounting for actual effort invested |
| **EPV** | Expected Pipeline Value — forward-looking pipeline measurement |
| **Shock Insight** | A platform-named concept; a significant, threshold-crossing event detected by the Observatory (qala) that changes the operator's understanding of their enterprise state |
| **Elegua Protocol** | The typed IPC and namespace system for all component-to-component, process-to-process communication in ogun OS. Named after Èṣù-Ẹlẹ́gbára, Yoruba orisha of crossroads and communication. |
| **Ọpọn Protocol** | Cross-enterprise data isolation system enforced at the kernel Security boundary. Named after the Yoruba divination board — the space where decisions are made with full information. |
| **Sambara** | The AI agents operating system embedded within ogun OS |
| **OgunNet** | ogun OS's P2P network layer (Kademlia DHT, mDNS, gossip pub/sub) |
| **RustyDB** | Rust-native embedded database backend used by the Storage subsystem |
| **CleanShutdownMarker** | The absolute final act of every ogun OS shutdown — a crash-consistency primitive |
| **Hypergrid Template** | A preconfigured workspace layout for a specific operator persona |
| **CNO** | Chief Navigation Officer — the meta-persona for an operator running 3+ enterprises simultaneously |

---

## Appendix B — Canonical Architecture Invariants

All production code must preserve these invariants without exception:

1. Image signatures are always verified before boot.
2. Bootable runtime images must be `ImageKind::Platform` images with a compatible ABI version.
3. The bootloader must halt on verification failure without continuing into the runtime.
4. Ọpọn isolation remains enforced (`opn_enforced = true`) in all production builds — unconditionally reset after every `ogun.toml` load.
5. Every capability grant or denial is audited before returning to the caller.
6. IPC messages are typed Elegua messages with context metadata (`operator_id`, `enterprise_id`, `workspace_id`, `trace_id`).
7. Kernel, session, app, service, module, driver, device, and host boundaries stay explicit.
8. Lower layers do not depend on higher layers.
9. Host OS APIs are accessed only through `ogun-emulator-backend` — the sole approved host boundary.
10. `ogun-desktop.exe` is the only autostart entry — exactly one per machine.
11. System key private material is never written to `~/.ogun/`.
12. Private image signing keys are never committed or stored in release artifacts.
13. Virtual monitor renders via Tauri surfaces only — no direct framebuffer writes.
14. Virtual network adapters use OS sockets only — no raw packet injection.
15. `CleanShutdownMarker` is written as the absolute last act of every shutdown.
16. Every component tick is wrapped in `catch_unwind` — a panicking component never crashes the execution loop.
17. Virtual host nesting depth ≤ configured maximum (≤ 10).
18. `OGUN_ABI_VERSION` is the single source of truth for ABI compatibility checks at all component boundaries.

---

*ogun OS — Operating System for Independent Workers*
*Copyright (C) 2026 Dominic Eaton @ The Ogun Foundation*
*Licensed under the GNU General Public License v3.0*

*ogun-charter.md · Project Ogún · 2026*
*Owner: Dominic Eaton (@eatondo)*
*Repository: gitlab.com/ogun-foundation/ogun*
