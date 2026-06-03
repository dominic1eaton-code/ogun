# ogun OS — Product Brief
**Version 0.1.0-beta · Project Ogún · June 2026**
**Owner:** Dominic Eaton (@eatondo) · The Ogun Foundation
**License:** GNU General Public License v3.0

---

## What Is ogun OS?

ogun OS is a **Rust-native operating-system layer for independent workers**. It does not replace the operating system on your machine — it runs on top of it, presenting a second, structured runtime environment that is purpose-built for the way independent professionals actually work.

Named after Ogun, the Yoruba orisha of iron, technology, and creation — the force that forges raw material into tools and purpose — ogun OS takes the raw capabilities of your machine and forges them into a structured, intelligence-driven workspace for building an independent economic life.

The first public release, version **0.1.0-beta**, targets **Windows x64** and ships June 2026 with the complete foundational runtime: a three-stage verified bootloader, a 15-subsystem kernel, a full desktop environment, 21 personal enterprise applications, a P2P network layer (OgunNet), an AI agents operating system (Sambara), and a full SDK surface for third-party developers.

---

## The Core Idea

Every independent worker — freelancer, consultant, creator, founder, investor — is already running an enterprise. Most just don't know it, because it has no structure, no memory, no rules, and no intelligence layer.

ogun OS makes the enterprise **explicit, structured, measurable, and compounding**.

Unlike conventional operating systems that organize files, applications, and windows, ogun OS organizes **enterprises, engagements, assets, workflows, agents, intelligence systems, and value production**. Applications are not isolated utilities — they are runtime systems sharing a common process model, IPC bus, semantic filesystem, observability layer, and workspace context.

### The Core Reframe

| What you think it is | What ogun OS calls it |
|---|---|
| A piece of work | An **Engagement** — a state machine moving through a production pipeline |
| Output from that work | An **Artifact** — tracked, attributed, and registered |
| A collection of deliverables | An **Asset** — a portfolio item with a value and revenue attribution |
| All your assets together | A **Portfolio** — a graph of assets with aggregate valuation |
| Your whole career | An **Enterprise** — a configured value transformation system |
| Your whole working life | A **Portfolio of Enterprises** — governed by one system |

---

## What ogun OS Is — and Is Not

**ogun OS IS:**
- A hosted operating-system layer running on top of Windows (later macOS, Linux)
- A programmable operating environment for independent workers
- A full application runtime with verified boot, 15 kernel subsystems, and capability-gated processes
- An enterprise management system that makes personal businesses explicit and compounding
- An AI agents OS (Sambara) with kernel-level identity and authority governance
- A P2P network layer (OgunNet) for encrypted communication, file transfer, and distributed operations
- A semantic filesystem with 12 namespace schemes that organizes resources by meaning, not just path

**ogun OS IS NOT:**
- A replacement for Windows, macOS, or Linux
- A simple productivity app, project manager, or freelancer invoicing tool
- A cloud service requiring constant internet access to function
- A virtual machine or traditional containerization platform

---

## Platform Editions

| Edition | Platform | Status |
|---|---|---|
| **Desktop** | Windows x64 | **Available — 0.1.0-beta (June 2026)** |
| Desktop | macOS Apple Silicon, Linux x86_64 | Designed; post-beta |
| Mobile | Android arm64, iOS arm64 | In progress |
| Web | Browser WASM | Designed; post-beta |
| Server | Headless Linux | Designed; post-beta |
| Device | IoT / embedded | Designed; post-beta |

---

## Key Features

### The Personal Enterprise Suite (21 Tier-4 Apps)
The heart of ogun OS is a suite of composable enterprise management applications, each a software-defined operating system for a specific domain of independent work:

| App | Purpose |
|---|---|
| **enzo** | Personal enterprise management — makes your enterprises explicit, structured, and compounding |
| **kogi** | Software-defined office — pipeline management, engagement tracking, commitment control |
| **dongo** | Financial management — double-entry accounting, wallets, tax reserve, digital assets |
| **ume** | Organization OS — legal entities, contracts, cap tables, SOPs |
| **heshima** | Identity management — credentials, verification, reputation, linktree |
| **shango** | Solution factory — build environments, product lifecycle, QA, distribution |
| **igi** | Portfolio management — asset tracking, EVS computation, passive income trajectory |
| **akeel** | Knowledge management — documentation, decision log, institutional memory |
| **moto** | Project management — milestones, work packages, scope control |
| **zamani** | Estate management — wealth, physical assets, continuity planning |
| **sambara** | Agent management OS — AI agents with kernel-level identity and authority governance |
| **qala** | Observatory and analytics — metrics, insights, telemetry, scenario modeling |
| **shaba** | Strategic management — OKRs, vision, strategy execution |
| **kanna** | Governance management — policies, cooperative governance, hub management |
| **zuri** | Digital marketplace — stores, listings, commerce, exchange |
| **ayo** | Digital spaces — public portfolio, social platform, community |
| **mizeez** | Version and change control — artifact versioning, change management |
| **orun** | Semantic filesystem runtime — workspace bootstrapping, namespace paths |
| **apapo** | Hypergrid platform — domain OS development, distributed environments |
| **didara** | IP tracking — patents, trademarks, licensing, royalties |
| **misimu** | Schedule and event management — full-featured calendar, timeline, booking |

### The Desktop Environment
A complete graphical environment with Command Center, Command Palette, ogun Shell, File Explorer, Security Center, Profile Center, and Settings Center — all enterprise-aware and workspace-scoped.

### OgunNet v2.0.0 — Built-in P2P Networking
Every installation generates an ed25519-derived NodeId and becomes an addressable peer on a distributed network. Features include Kademlia DHT peer discovery, mDNS LAN discovery, encrypted messaging via named channels (AES-256-GCM), chunked encrypted file transfer, and a gossip pub/sub layer.

### Sambara — The AI Agents OS
A complete operating system for AI agents with kernel-level identity, workspace-bounded execution, and four authority tiers (Observe → Recommend → Execute Bounded → Full Autonomy). Model-agnostic with built-in drivers for Anthropic Claude, OpenAI, DeepSeek, and Ollama. Every agent action is logged before execution.

### The Shock Insight
The platform's defining onboarding moment: once you connect real data (calendar, financial accounts), the Observatory processes your history and delivers a personalized, data-backed revelation — the gap between what you think you earn per hour and what the data actually shows. For most users, this gap is 2–4× across clients.

---

## Architecture Summary

ogun OS runs a complete, verified runtime on top of your host OS through a layered architecture:

```
ogun-desktop.exe (launcher)
  → ogun-emulator (Tauri 2.0+ app)
      → 4 virtual devices (display, CPU scheduler, host platform, network)
      → ogun-uefi (virtual UEFI firmware)
      → ogun-bootloader (3-stage cryptographic verification)
      → ogun-kernel-core (15 subsystems, 17-step boot)
          → ogun-session-manager (auth, workspaces, lifecycle)
              → All applications (Tier 1–4)
```

**15 Kernel Subsystems** initialize in strict canonical order: Telemetry, Memory, Process/Scheduler, IPC/Elegua Bus, Storage/RustyDB, VFS/Namespaces, Security/Ọpọn, Services, Host/Drivers, Session/RBAC, Display/UI, State/Snapshots, Components/Modules, Network/OgunNet, Emulation/Virtual Devices.

**Three-Stage Boot Verification** runs on every boot:
1. Image authenticity — ed25519 signature over the platform image
2. Install integrity — SHA-256 manifest verification of all installed files
3. Host key re-derivation — HKDF-SHA256 binding the image key to this specific installation

Any stage failure calls `halt()` before any higher runtime code executes.

---

## Security Model

Security is non-negotiable in ogun OS. Several invariants are unconditional and cannot be disabled by any configuration, flag, or message.

**Three Cryptographic Keys:**
- **Image Key** — ed25519 keypair owned by CI; private key never leaves the build vault; verifies every image on every boot
- **System Key** — ed25519 keypair generated once on your machine; private key in Windows DPAPI only (never on disk); signs the system manifest
- **Host Key** — 32-byte key derived via HKDF-SHA256 from the image and system keys; unique per image+installation; stamped on every telemetry event and audit log entry

**The Ọpọn Protocol** — named after the Ọpọn Ifá divination tray, upon which no reading for one supplicant may be contaminated by the marks of another. Five immutable rules enforce cross-enterprise data isolation at the kernel level. `opn_enforced = true` is reset unconditionally after every config load and cannot be disabled.

**Capability System** — every process declares its capability set in its manifest; every system call is checked before execution; every grant and denial is written to an AES-256-GCM encrypted audit log before the operation completes.

---

## Supported Operator Personas

ogun OS ships Hypergrid Templates for five primary personas — pre-configured enterprise environments that initialize the full app suite with the right pipelines, policies, agents, wallets, and observatories:

| Persona | Who it's for | North Star Metric |
|---|---|---|
| **Freelancer/Operator** | Consultants, contractors, coaches, gig workers | Effective Hourly Rate (EHR) |
| **Creator** | Content creators, artists, writers, musicians, indie developers | Content EHR + Passive Income Ratio |
| **Founder/Builder** | Entrepreneurs, solopreneurs, startup founders | MRR + Runway |
| **Investor** | Retail investors, real estate, angels, crypto holders | Portfolio IRR |
| **CNO** (meta-persona) | Multi-enterprise portfolio operators | Total Portfolio Value + Passive Ratio |

---

## The Enterprise Lifecycle

Every enterprise created in ogun OS moves through eight canonical states as data flows in and intelligence accumulates:

`SEED → COLD → ACTIVATED → CALIBRATED → INTELLIGENT → OPTIMIZED → COMPOUNDING → ARCHIVED`

At the **Cold → Activated** transition, the Shock Insight fires — the first quantified, personalized revelation from real data.

By the **Compounding** state (365+ metric snapshots, passive income above 20%), the platform operates with full predictive intelligence and agents earn their highest authority levels.

---

## Key Metrics the Platform Tracks

| Metric | Formula |
|---|---|
| **EHR** (Effective Hourly Rate) | `total_income / total_hours` (including admin, meetings, non-billable) |
| **EPV** (Expected Pipeline Value) | `Σ(proposed_value × win_probability)` |
| **TPV** (Total Portfolio Value) | Aggregate of all enterprise asset valuations |
| **EVS** (Enterprise Value Score) | `base_value + (revenue_multiple × annual_revenue) + strategic_premium` |
| **PIR** (Passive Income Ratio) | `passive_income / total_income` |
| **τ** (Commitment Tension) | `Σ(committed_effort) − weekly_hours_max` |

---

## System Requirements (0.1.0-beta, Windows x64)

- Windows 10 x64 or Windows 11 x64
- 4 GB RAM (8 GB recommended)
- 2 GB available disk space
- Internet connection for initial installation and OgunNet peer discovery
- Administrator rights for initial installation

---

## Release Artifacts

| Artifact | Description |
|---|---|
| `ogun-setup-windows-0.1.0-beta.exe` | User-facing installer — 9-step installation pipeline; silent install mode available |
| `ogun-desktop-windows-0.1.0-beta.exe` | User-facing launcher — starts ogun OS; manages updates and repairs |
| `ogun-emulator-windows-0.1.0-beta.exe` | Main entry point (Tauri 2.0+); initializes virtual hardware |
| `ogun-windows-0.1.0-beta.img` | Signed platform kernel image — ed25519 signed; zstd compressed |
| `ogun_image_tool-windows-0.1.0-beta.exe` | Image builder for CI and local developer use |

---

## Known Limitations (0.1.0-beta)

- Windows x64 only — macOS and Linux editions are architected and scheduled post-beta
- Mobile, Web, Server, and Device editions are not included in this release
- `enterprise_id` in IPC messages is an identified open item to be resolved in a patch release
- Storage backend (RustyDB) is scheduled for migration to the stable persistent backend in 0.2.0
- Beta qualifier: all documented features are present; some performance rough edges expected

---

---

# Frequently Asked Questions

## Getting Started

**Q: What is ogun OS, in one sentence?**
ogun OS is a structured operating environment that runs on top of Windows (and later macOS and Linux) and organizes your independent work life around enterprises, engagements, and intelligence — not just files and applications.

**Q: Do I need to uninstall Windows to use ogun OS?**
No. ogun OS runs on top of your existing operating system. It installs like a desktop application, starts automatically when you log in, and runs alongside your existing software. Your normal Windows environment remains completely untouched.

**Q: Who is ogun OS for?**
ogun OS is built for independent workers — freelancers, consultants, contractors, coaches, creators, founders, and investors. If you run any kind of independent economic life (even part-time alongside a job), ogun OS is designed for you.

**Q: What's the difference between ogun OS and project management software like Notion or Asana?**
ogun OS is not a project management tool. It is a complete operating environment. Project management (via `moto`) is one of 21 composable enterprise applications. The key difference is that all applications share a common runtime, IPC bus, financial layer, security model, and intelligence layer. A task in `moto` is linked to a client engagement in `kogi`, which is linked to a contract in `ume`, which is linked to an invoice in `dongo`, which feeds your Observatory in `qala` — automatically, because they are running in the same enterprise context. No integrations required.

**Q: What's the difference between ogun OS and QuickBooks or FreshBooks?**
`dongo` (the financial management app) does what QuickBooks does, but it is one app in a system of 21 composable enterprise apps. The key advantage is that financial data in `dongo` is automatically linked to engagements in `kogi`, clients in `ogun-contacts`, and portfolio assets in `igi` — because they all share the same enterprise context and IPC bus. Your Effective Hourly Rate is computed across all clients, not just the ones you tagged correctly.

**Q: Is ogun OS free?**
ogun OS is licensed under the GNU General Public License v3.0 (GPL-3.0). The source code is open. Download the installer from the official release page to get started.

**Q: What does "beta" mean for this release?**
The 0.1.0-beta release is the first public release. All documented features are present and functional. "Beta" means there may be rough edges, some performance characteristics will improve, and the storage backend will be migrated in 0.2.0. It is not an incomplete or partially-built product — it is a fully featured first public release of a complex system.

---

## Core Concepts

**Q: What is an "enterprise" in ogun OS?**
An enterprise is a complete, configured value transformation system — not just a company name or a folder. When you create an enterprise, the system provisions a namespace root, a workspace, a default wallet, an observatory configuration, a pipeline, and a starter policy set. An enterprise has a lifecycle state (from `SEED` to `COMPOUNDING`) and a GoalWeightVector that declares how you weight income, asset growth, passive income, and network. Multiple enterprises can be managed simultaneously — the CNO meta-persona exists specifically for multi-enterprise portfolio operators.

**Q: What is a "workspace"?**
A workspace is an isolated, persistent, enterprise-aware runtime context that scopes all OS activity — processes, files, agents, telemetry, and layout — to a specific operational domain. Every process you run inside a workspace is tagged with that workspace's `workspace_id` and `enterprise_id`. Every file you create lands in the right namespace. Switching workspaces freezes your current context, saves its state, activates the new one, and restores its running apps — all in a few hundred milliseconds.

**Q: What is the Shock Insight?**
The Shock Insight is the platform's first quantified, personalized revelation — delivered automatically at the `Cold → Activated` enterprise lifecycle transition once you connect real data (calendar, financial accounts, invoicing). For a freelancer it might read: *"You earned $9,800 last month but spent 186 hours working — $52/hour effective rate. Your three retainer clients averaged $94/hour. Your two project clients averaged $31/hour."* This gap was invisible before. It becomes the foundation of all intelligence the platform generates from that point forward.

**Q: What is the Ọpọn Protocol?**
The Ọpọn Protocol is the cross-enterprise data isolation system built into the kernel. Named after the Ọpọn Ifá — the Yoruba divination tray upon which no reading for one supplicant may be contaminated by the marks of another — it enforces five immutable rules ensuring that data belonging to one enterprise cannot be read or written in the context of another without explicit, logged, operator-approved consent. This is unconditional; it cannot be disabled by any configuration setting or runtime flag.

**Q: What is the Elegua Protocol?**
The Elegua Protocol is ogun OS's unified IPC (inter-process communication) specification — named after Èṣù-Ẹlẹ́gbára, the Yoruba orisha of crossroads and communication. It is the typed message bus that all components, services, and applications use to communicate. Every message carries operator, enterprise, workspace, and trace context. No silent side channels are permitted between components.

**Q: What is OgunNet?**
OgunNet is the P2P network layer built into the kernel (Subsystem 14). Every ogun OS installation automatically generates an ed25519-derived NodeId and becomes an addressable peer. Features include Kademlia DHT for global peer discovery, mDNS for local area network discovery, encrypted messaging via named channels, chunked encrypted file transfer, a gossip pub/sub system, and relay-assisted NAT traversal. It enables encrypted communication and collaboration between ogun OS users without any central server.

**Q: What is Sambara?**
Sambara is the AI agents operating system built into ogun OS — not a prompt-chaining tool or LLM wrapper, but a complete OS for agents. Agents are first-class runtime entities with kernel-level identity (`agent_id`), workspace-bounded execution, and four authority tiers: `OBSERVE`, `RECOMMEND`, `EXECUTE_BOUNDED`, and `FULL_AUTONOMY`. Every agent action is written to an encrypted audit log before execution. Agents cannot escalate their own authority — escalation always requires explicit operator interaction. Sambara is model-agnostic and ships with built-in drivers for Anthropic Claude (Opus, Sonnet, Haiku), OpenAI (GPT-4o, o1, o3-mini), DeepSeek, and Ollama.

---

## Security

**Q: How does ogun OS verify that the software hasn't been tampered with?**
On every boot, ogun OS runs three sequential cryptographic verification stages before any user code executes. Stage 1 verifies the ed25519 signature of the platform image. Stage 2 re-hashes every security-critical installed file against a signed system manifest. Stage 3 re-derives the HostKey via HKDF-SHA256 and compares it against the stored value. Any failure in any stage calls `halt()` with zero side effects — nothing else runs. This three-stage verification is unconditional in all production builds.

**Q: Where are my private keys stored?**
The system key's private half is stored exclusively in Windows DPAPI (Windows Credential Manager). It never exists in the `~/.ogun/` directory. The image signing private key never leaves the CI build vault and is never present on any user machine.

**Q: Can I see what permissions an app has?**
Yes. The Security Center shows every active capability grant for every running process. You can revoke any grant instantly. Revocation is logged to the audit trail before it takes effect. Every app declares its capability set in its `ogun-component.toml` manifest, which is reviewed at install time and enforced at every system call.

**Q: Can agents access data from multiple enterprises?**
Agents are subject to the Ọpọn Protocol like all other processes. An agent with `enterprise_id = A` cannot access data tagged `enterprise_id = B` without an explicit, logged, operator-approved cross-enterprise grant. This is enforced at the kernel Security subsystem, IPC broker, and storage layer simultaneously.

---

## Technical

**Q: What technology is ogun OS built with?**
ogun OS is written in Rust. The desktop frontend uses Tauri 2.0+. The embedded database is RustyDB (a Rust-native WAL-backed key-value store). Cryptography uses `ring` v0.17 (ed25519, X25519, AES-256-GCM, HKDF-SHA256) and `sha2` v0.10 (SHA-256).

**Q: How does ogun OS use my CPU?**
ogun OS uses a software-defined execution scheduler called `ogun-cpu` — one of the four virtual devices initialized at boot. It runs at 100 Hz base (one tick every 10ms) and schedules all in-process components through a priority-respecting round-robin on a shared Tokio thread pool. At idle, the system uses 1 main thread (Tauri) plus 1–2 Tokio worker threads. The pool expands dynamically under load (up to `num_cpus - 1` maximum). A panicking component is always caught and isolated via `std::panic::catch_unwind` — it can never crash the execution loop or any other component.

**Q: Can I build apps for ogun OS?**
Yes. ogun OS ships a full SDK surface — six crates covering apps (`ogun-app-sdk`), services (`ogun-service-sdk`), kernel modules (`ogun-kernel-sdk`), drivers (`ogun-driver-sdk`), and host types (`ogun-host-sdk`). Apps are packaged as `.opkg` files and installed via `opm` (the ogun Package Manager). Shell extensions (shell packages) are the lightest-weight extensibility mechanism and require minimal ceremony. The repository is at `gitlab.com/ogun-foundation/ogun`.

**Q: What is the `.img` file?**
The `ogun-windows-0.1.0-beta.img` is a signed platform kernel image — a five-region binary containing `FileHeader`, `SectionTable`, `SectionData`, `ImageVerifyKey`, and `SignatureBlock`. Section blobs are zstd level-19 compressed with per-section SHA-256 checksums. The image is signed with an ed25519 key owned by the CI pipeline. The bootloader verifies this signature on every boot before extracting anything.

**Q: What is ABI version compatibility?**
`OGUN_ABI_VERSION: u32 = 1` (in 0.1.0-beta) is a single constant defined in `ogun-types` and imported by every subsystem, SDK, and component. Every app, module, driver, and extension declares which ABI version it was compiled against. The runtime checks this at every load boundary — a mismatch causes the component to be rejected and logged, not a silent failure.

---

## Business Use Cases

**Q: I'm a freelancer. How does ogun OS help me?**
The Freelancer Hypergrid template sets up your enterprise in minutes: a client pipeline in `kogi`, a double-entry accounting wallet in `dongo`, a contract library in `ume`, and an Observatory in `qala`. The platform immediately tracks your Effective Hourly Rate across all clients — including admin, revisions, and meetings. Most freelancers discover a 2–4× EHR gap between their highest and lowest-value clients they've never seen before. The platform then helps you act on it: rate floor policies, concentration cap alerts, and a productization signal when you've delivered the same deliverable type four or more times.

**Q: I'm a creator. What does ogun OS do that YouTube Studio or Spotify for Artists doesn't?**
Platform dashboards only show you one platform's metrics. ogun OS computes your **Content EHR** — revenue per production hour by content format (video, written, audio, visual) and by platform simultaneously. Most creators discover their highest-earning format produces 3–10× more per hour than their most time-intensive format. This is the Format Efficiency Gap — invisible when your data lives in five different platform dashboards.

**Q: I'm building a startup. What value does ogun OS add?**
The Founder Hypergrid template sets up MRR tracking, runway monitoring, and equity-per-hour-invested computation (compared against your consulting EHR baseline). The platform also helps structure your holding entity hierarchy (personal → HoldCo → Operating Entities → IP Entity), manage contracts and cap tables in `ume`, and automate bookkeeping in `dongo`. The Sambara agent suite includes a `LIFECYCLE_AGENT` that monitors when your enterprise is ready to graduate to the next maturity stage.

**Q: I manage multiple businesses. Is that supported?**
Yes — this is the CNO (Chief Navigation Officer) meta-persona. You can manage unlimited enterprises simultaneously, each with its own namespace, workspace, pipeline, wallet, observatory, and agent configuration. The Portfolio Control Center in `enzo` shows aggregate metrics (MRR, TPV, EPV, EHR) across all enterprises and computes cross-enterprise synergy value — identifying where shared audiences, referrals, or IP reuse are being left unrealized.

**Q: Can two people collaborate within ogun OS?**
Yes, via the Hub pattern in `kanna`. Two or more operators create a Hub for a specific engagement or time period, declare a `RevenueSplit`, and link their enterprise wallets. Each operator works in their own enterprise namespace (Ọpọn Protocol enforced — their data stays isolated). The Hub has its own shared namespace for joint work. Revenue is split and attributed to each enterprise's wallet automatically.

**Q: Does ogun OS work offline?**
Yes. The entire local runtime operates offline. OgunNet peer discovery and connectivity require network access, and initial installation requires internet access, but the complete desktop environment, all personal enterprise apps, and all AI agent features with locally-served models (Ollama) operate without internet.

---

---

# Use Cases & Business Cases

## For Independent Professionals

### The Freelancer EHR Problem
Most freelancers have no idea what their actual effective hourly rate is. They know their billing rate, but not the EHR — the rate that accounts for admin time, revision cycles, sales calls, unpaid scoping, and the 4-hour meeting for the 2-hour project. ogun OS computes EHR automatically by connecting your calendar (hours invested) and your financial accounts (income generated) across every client simultaneously. The typical first Shock Insight reveals a 2–4× gap in EHR between the operator's highest and lowest-value clients — a gap that directly drives the platform's pricing and client mix recommendations.

**Business case:** A consultant billing $150/hour discovers their EHR on their largest client is $67/hour (after admin and revisions) versus $118/hour on their smallest retainer client. ogun OS surfaces this gap, enforces a rate floor policy, and triggers an acquisition agent when the high-yield client share drops below threshold. Conservative projection: 15–20% improvement in effective income within 90 days of active use.

### The Creator Format Gap
Content creators spread across YouTube, Substack, Spotify, and Gumroad have no unified view of revenue per production hour. A creator spending 12 hours on a video earning $400 and 2 hours on a newsletter earning $180 is actually earning more per hour from the newsletter — but this is invisible until data is unified. ogun OS computes Content EHR by format and by platform simultaneously, revealing the Format Efficiency Gap. Platform-specific dashboards cannot surface this insight because the data lives in silos.

**Business case:** A creator reallocating 20% of production hours from their lowest-EHR format to their highest-EHR format realizes a 12–18% revenue increase with the same total time invested.

### The Founder Build Trap
Founders and solopreneurs often don't know if building equity is returning more than comparable consulting work would. ogun OS tracks time invested against enterprise value created and computes an equity-per-hour metric versus the operator's service EHR baseline. When the equity-per-hour calculation falls below the consulting EHR for an extended period, the Observatory surfaces an alert and the platform offers scenario modeling for rebalancing.

### Multi-Enterprise Portfolio Management
Senior independent workers — those who have been at it for five or more years — typically have multiple income streams: consulting, content, equity stakes, digital products, and physical assets. Managing these as separate, disconnected entities leaves cross-enterprise synergies invisible and creates coordination overhead that consumes more value than it creates. ogun OS's CNO meta-persona provides a unified view and computes the coordination cost explicitly, surfacing when portfolio complexity is costing more than it earns.

---

## For the Platform Ecosystem

### Third-Party App Development
ogun OS ships a complete SDK surface. Developers can build Tier-4 user apps distributed as `.opkg` packages with access to the full enterprise context, IPC bus, semantic filesystem, and agent infrastructure via declared capability grants. The `opm` package manager handles installation, versioning, and ABI compatibility enforcement. Shell packages offer the lowest-friction extensibility path — new shell commands in hours.

**Business case for developers:** access to an active installed base of independent workers with financial data, calendar data, client records, and project history — all normalized and enterprise-contextualized. Building on ogun OS means building on a platform where the hard integrations are already done and the user's data is already structured.

### Enterprise Deployment
The `ogun-setup.exe` installer ships with a silent install mode (`--silent --install-dir "..." --no-autostart`) for enterprise deployment scenarios. Multiple ogun OS instances on a team can be connected via OgunNet for encrypted peer communication, file sharing, and shared named channels. The Ọpọn Protocol ensures each team member's enterprise data remains isolated while shared work flows through the Hub namespace.

### AI / Agent Infrastructure
Sambara's model-agnostic architecture and kernel-level agent governance make it a platform for AI agent deployment in professional contexts where auditability, authority governance, and cross-enterprise isolation matter. Every agent action logged before execution. Every authority escalation requiring explicit operator consent. Every agent bounded to declared parameter ranges. This architecture is appropriate for deployments where AI actions have financial or legal consequences.

---

## Industry Context

ogun OS addresses a market segment that existing software categories serve poorly. Project management tools (Notion, Asana, Linear) provide task organization but no financial layer, no intelligence, and no enterprise structure. Financial tools (QuickBooks, FreshBooks) track money but have no operational context. Productivity suites (Microsoft 365, Google Workspace) are designed for employees within organizations, not operators running their own enterprises. CRMs are designed for sales teams, not individual practitioners managing their own pipelines.

ogun OS's thesis is that the independent worker market — estimated at 60+ million in the US alone — is underserved not because no individual tool is good enough, but because no tool treats the independent worker as an enterprise operator whose data, workflows, and intelligence belong together in one system.

---

---

# Marketing Overview

## Positioning

**Category:** Operating environment for independent workers
**Tagline:** *Your enterprise, explicit and compounding.*
**Segment:** Independent professionals — freelancers, consultants, creators, founders, investors
**Platform:** Windows (0.1.0-beta); macOS, Linux, Mobile (planned)
**Price:** Open source (GPL-3.0)

## The Pitch

You are already running an enterprise. You probably just don't know it — because it has no structure, no memory, no rules, and no intelligence layer.

ogun OS changes that. It is a structured operating environment that runs on top of your existing computer and transforms the way you work: organizing enterprises, not files. Tracking engagements, not tasks. Computing your real effective hourly rate, not the number on your invoice. Running AI agents that are governed, auditable, and bounded — not black boxes.

The first time you connect your calendar and your financial accounts, ogun OS delivers your Shock Insight — a personalized, data-backed revelation that most users say they can't believe they lived without. The gap between what you thought you earned per hour and what you actually earned per hour. The clients you undercharged for years. The format you should have doubled down on six months ago.

From that moment, the platform never stops working. Agents run. The observatory generates insights. The pipeline tracks. The finances reconcile. And every 60 seconds, the session snapshots itself — so nothing is ever lost.

## Key Messages

**For the independent worker:**
"You're already running an enterprise. ogun OS makes it explicit, structured, and compounding."

**For the creator:**
"You post on five platforms and earn on four. ogun OS shows you which hour of your work earns the most — and which platform is wasting your time."

**For the developer:**
"A fully verified, kernel-level runtime with a clean SDK surface. Build enterprise apps on top of a system that already handles the hard parts: financial data, identity, capability governance, and agent infrastructure."

**For the security-conscious:**
"Three-stage cryptographic boot verification. Unconditional cross-enterprise data isolation. Every capability grant and agent action logged before it completes. Security that can't be configured away."

## Differentiation

| What exists | What ogun OS adds |
|---|---|
| Project management tools | Enterprise context, financial attribution, intelligence |
| Financial software | Operational connection to engagements and clients |
| Productivity suites | Enterprise model, agents, and cross-app intelligence |
| AI productivity tools | Governed agents with kernel-level identity and audit |
| P2P messaging apps | Integrated with enterprise runtime and file system |

## Distribution Strategy

- **Direct download** from project release page (`gitlab.com/ogun-foundation/ogun`)
- **Open source community** via GitLab — contributions welcome under GPL-3.0
- **Developer ecosystem** via SDK and `opm` package registry — third-party apps extend the platform
- **Word of mouth** via Shock Insight — the personalized data revelation is designed to be shareable and compelling enough to generate organic growth
- **OgunNet virality** — each installed user becomes a network peer, creating social surface for discovery

## Launch Milestones

| Milestone | Timing |
|---|---|
| `0.1.0-beta` public release (Windows x64) | June 2026 |
| `0.1.0` stable release | Post-beta feedback cycle |
| `0.2.0` — storage backend migration + additional platforms | TBD |
| macOS Apple Silicon Desktop Edition | Planned post-0.1.0 |
| Linux x86_64 Desktop Edition | Planned post-0.1.0 |
| Android + iOS Mobile Editions | In progress |

---

## Resources

| Resource | URL |
|---|---|
| ogun OS prototype | https://ogun-prototype.eatondo000.workers.dev/ |
| Documentation | https://ogun-docs.eatondo000.workers.dev/ |
| ogun home site | https://ogun.eatondo000.workers.dev/ |
| Source repository | https://gitlab.com/ogun-foundation/ogun |

---

*ogun OS · v0.1.0-beta · Project Ogún · 2026*
*Owner: Dominic Eaton (@eatondo) · The Ogun Foundation*
*License: GNU General Public License v3.0*
