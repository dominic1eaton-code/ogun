# ogun OS — Complete User Guide
## Version 0.1.0-beta · Project Ogún · 2026

**Owner:** Dominic Eaton (@eatondo)  
**Organization:** The Ogun Foundation  
**License:** GNU General Public License v3.0  
**Platform:** Windows x64 (initial release)  
**Language:** Rust · Tauri 2.0+  
**Status:** First public beta release — June 2026

---

## Table of Contents

**Part I — What Is ogun OS**
1. [Introduction and Product Vision](#1-introduction-and-product-vision)
2. [What ogun OS Is — and Is Not](#2-what-ogun-os-is--and-is-not)
3. [The Personal Enterprise Model](#3-the-personal-enterprise-model)
4. [Platform Editions](#4-platform-editions)
5. [Release History and Versioning](#5-release-history-and-versioning)

**Part II — Getting Started**
6. [System Requirements](#6-system-requirements)
7. [Installation Walkthrough](#7-installation-walkthrough)
8. [First Boot and Onboarding](#8-first-boot-and-onboarding)
9. [Creating Your Operator Profile](#9-creating-your-operator-profile)
10. [Setting Up Your First Enterprise](#10-setting-up-your-first-enterprise)
11. [Understanding Workspaces](#11-understanding-workspaces)

**Part III — The Desktop Environment**
12. [The ogun Desktop Layout](#12-the-ogun-desktop-layout)
13. [The Command Center](#13-the-command-center)
14. [The Command Palette](#14-the-command-palette)
15. [The ogun Shell](#15-the-ogun-shell)
16. [The File Explorer (orun Namespaces)](#16-the-file-explorer-orun-namespaces)
17. [Settings Center](#17-settings-center)
18. [Security Center](#18-security-center)
19. [Profile Center](#19-profile-center)

**Part IV — The Personal Enterprise Suite (Tier 4 Apps)**
20. [enzo — Personal Enterprise Management System](#20-enzo--personal-enterprise-management-system)
21. [kogi — Software-Defined Office](#21-kogi--software-defined-office)
22. [dongo — Financial Management System](#22-dongo--financial-management-system)
23. [ume — Organization Operating System](#23-ume--organization-operating-system)
24. [heshima — Identity Management System](#24-heshima--identity-management-system)
25. [shango — Solution Factory](#25-shango--solution-factory)
26. [igi — Portfolio Management System](#26-igi--portfolio-management-system)
27. [akeel — Knowledge Management System](#27-akeel--knowledge-management-system)
28. [moto — Project Management System](#28-moto--project-management-system)
29. [zamani — Estate Management System](#29-zamani--estate-management-system)
30. [sambara — Agent Management System](#30-sambara--agent-management-system)
31. [qala — Observatory and Analytics](#31-qala--observatory-and-analytics)
32. [shaba — Strategic Management System](#32-shaba--strategic-management-system)
33. [kanna — Governance Management System](#33-kanna--governance-management-system)
34. [zuri — Digital Marketplace System](#34-zuri--digital-marketplace-system)
35. [ayo — Digital Spaces Management](#35-ayo--digital-spaces-management)
36. [mizeez — Version and Change Control](#36-mizeez--version-and-change-control)
37. [orun — Semantic Filesystem Runtime](#37-orun--semantic-filesystem-runtime)
38. [apapo — Hypergrid Platform](#38-apapo--hypergrid-platform)
39. [didara — IP Tracking and Management](#39-didara--ip-tracking-and-management)
40. [misimu — Schedule and Event Management](#40-misimu--schedule-and-event-management)

**Part V — Utility Apps (Tier 3)**
41. [ogun-notes](#41-ogun-notes)
42. [ogun-tasks](#42-ogun-tasks)
43. [ogun-focus](#43-ogun-focus)
44. [ogun-calendar (ogun-schedule)](#44-ogun-calendar-ogun-schedule)
45. [ogun-messenger](#45-ogun-messenger)
46. [ogun-search](#46-ogun-search)
47. [ogun-assistant (OBA)](#47-ogun-assistant-oba)
48. [ogun-contacts](#48-ogun-contacts)

**Part VI — Operator Personas and Hypergrid Templates**
49. [Understanding Operator Personas](#49-understanding-operator-personas)
50. [Freelancer / Operator Persona](#50-freelancer--operator-persona)
51. [Creator Persona](#51-creator-persona)
52. [Founder / Builder Persona](#52-founder--builder-persona)
53. [Investor Persona](#53-investor-persona)
54. [CNO — Chief Navigation Officer (Meta-Persona)](#54-cno--chief-navigation-officer-meta-persona)
55. [Hypergrid Templates Overview](#55-hypergrid-templates-overview)
56. [The eatondo Portfolio — Reference CNO Implementation](#56-the-eatondo-portfolio--reference-cno-implementation)

**Part VII — Core Platform Workflows**
57. [Workflow: Setting Up a New Enterprise from Scratch](#57-workflow-setting-up-a-new-enterprise-from-scratch)
58. [Workflow: Running Your Daily Production Loop](#58-workflow-running-your-daily-production-loop)
59. [Workflow: Managing a Client Engagement](#59-workflow-managing-a-client-engagement)
60. [Workflow: Productizing a Repeating Service](#60-workflow-productizing-a-repeating-service)
61. [Workflow: Deploying and Managing Agents (Sambara)](#61-workflow-deploying-and-managing-agents-sambara)
62. [Workflow: Multi-Enterprise Portfolio Operations](#62-workflow-multi-enterprise-portfolio-operations)
63. [Workflow: Publishing Your Identity and Portfolio (Heshima + Ayo)](#63-workflow-publishing-your-identity-and-portfolio-heshima--ayo)
64. [Workflow: Financial Tracking and Reporting](#64-workflow-financial-tracking-and-reporting)
65. [Workflow: Setting Governance Policies](#65-workflow-setting-governance-policies)
66. [Workflow: Launching a Digital Product (Shango + Zuri)](#66-workflow-launching-a-digital-product-shango--zuri)
67. [Workflow: Homesteader / Estate Tracking](#67-workflow-homesteader--estate-tracking)
68. [Workflow: Sambara Data Engineering](#68-workflow-sambara-data-engineering)
69. [Workflow: Shango Platform Administration and Security](#69-workflow-shango-platform-administration-and-security)

**Part VIII — OgunNet and Networking**
70. [OgunNet v2.0.0 Overview](#70-ogunnet-v200-overview)
71. [Connecting to Peers](#71-connecting-to-peers)
72. [Named Channels and Group Communication](#72-named-channels-and-group-communication)
73. [File Transfer over OgunNet](#73-file-transfer-over-ogunnet)
74. [Peer Reputation and Security](#74-peer-reputation-and-security)

**Part IX — Security, Keys, and the Ọpọn Protocol**
75. [Security Architecture Overview](#75-security-architecture-overview)
76. [The Three Keys Explained](#76-the-three-keys-explained)
77. [The Ọpọn Protocol — Cross-Enterprise Isolation](#77-the-opn-protocol--cross-enterprise-isolation)
78. [Capability System for Users](#78-capability-system-for-users)
79. [Authentication Methods by Platform](#79-authentication-methods-by-platform)
80. [Audit Log and Security Center](#80-audit-log-and-security-center)

**Part X — Configuration and Administration**
81. [Configuration Files Overview](#81-configuration-files-overview)
82. [ogun.toml Reference](#82-oguntoml-reference)
83. [display.toml Reference](#83-displaytoml-reference)
84. [emulation.toml Reference](#84-emulationtoml-reference)
85. [uefi.toml Reference](#85-uefitoml-reference)
86. [Namespace Reference](#86-namespace-reference)
87. [Virtual UEFI Boot Menu](#87-virtual-uefi-boot-menu)
88. [Session Management and Recovery](#88-session-management-and-recovery)
89. [Updating ogun OS](#89-updating-ogun-os)
90. [Uninstalling ogun OS](#90-uninstalling-ogun-os)

**Part XI — SDK and Developer Notes**
91. [SDK Surface Overview](#91-sdk-surface-overview)
92. [Building Your First App](#92-building-your-first-app)
93. [The OgunApp Trait](#93-the-ogunapp-trait)
94. [Writing a Kernel Module](#94-writing-a-kernel-module)
95. [Writing a Shell Package](#95-writing-a-shell-package)
96. [Writing a Plugin or Extension](#96-writing-a-plugin-or-extension)
97. [The .opkg Package Format and opm](#97-the-opkg-package-format-and-opm)
98. [App Manifest Reference (ogun-component.toml)](#98-app-manifest-reference-ogun-componenttoml)
99. [Development Quick Start](#99-development-quick-start)

**Part XII — System Architecture Reference**
100. [Runtime Architecture and Boot Chain](#100-runtime-architecture-and-boot-chain)
101. [The 15 Kernel Subsystems](#101-the-15-kernel-subsystems)
102. [The Execution Model (ogun-cpu)](#102-the-execution-model-ogun-cpu)
103. [The Elegua Protocol (IPC)](#103-the-elegua-protocol-ipc)
104. [The VFS and 12 Namespaces](#104-the-vfs-and-12-namespaces)
105. [Virtual Hardware Layer](#105-virtual-hardware-layer)
106. [Known Limitations in 0.1.0-beta](#106-known-limitations-in-010-beta)

---

# Part I — What Is ogun OS

---

## 1. Introduction and Product Vision

ogun OS is a Rust-native operating-system layer for independent workers. It does not replace the operating system already on your machine — it runs on top of it, presenting a second, structured runtime environment that is specifically engineered for the way independent professionals, freelancers, consultants, founders, creators, and investors actually work.

The name "ogun" comes from Ogun, the Yoruba orisha of iron, technology, and creation — the force that forges raw material into tools and purpose. ogun OS embodies that principle: it takes the raw capabilities of your machine and forges them into a structured, intelligence-driven workspace for building an independent economic life.

The first public release — version 0.1.0-beta, June 2026 — targets Windows x64. It ships the complete foundational runtime: virtual UEFI firmware, a three-stage verified bootloader, a 15-subsystem kernel, a session manager, full desktop environment, 13 OS-level apps, 8 utility apps, 21 Tier-4 personal enterprise applications, a P2P network layer (OgunNet), an AI agents OS (Sambara), and the full SDK surface for third-party developers.

**What makes ogun OS different from a productivity app suite:**

Every application in ogun OS is not just software you install — it is a managed runtime entity with a declared identity, capability set, workspace context, enterprise context, telemetry stream, and lifecycle. Applications share a common IPC bus (the Elegua Protocol), a common semantic filesystem (12 namespace schemes), and a common observability layer (Qala). They do not merely coexist on your desktop — they compose into a unified operating environment where every action is attributed, every output is tracked, and every pattern surfaces as intelligence.

The underlying philosophy: every independent worker is already running an enterprise. Most just don't know it, because it has no structure, no memory, no rules, and no intelligence layer. ogun OS makes the enterprise explicit, structured, measurable, and compounding.

---

## 2. What ogun OS Is — and Is Not

**ogun OS IS:**

- A hosted operating-system layer that runs on top of a host OS (Windows, later macOS and Linux)
- A programmable operating environment for independent workers
- A full application runtime with verified boot, 15 kernel subsystems, and capability-gated processes
- An enterprise management system that makes your personal businesses explicit and compounding
- An AI agents operating system (Sambara) with kernel-level identity and authority governance
- A P2P network layer (OgunNet) for secure communication, file transfer, and distributed operations
- A semantic filesystem with 12 namespace schemes that organizes resources by meaning, not just path

**ogun OS IS NOT:**

- A replacement for your existing operating system (Windows, macOS, Linux)
- A traditional desktop environment like GNOME, KDE, or Windows Explorer
- A simple productivity app, project manager, or freelancer invoicing tool
- A cloud service that requires internet access to function (though many features are enhanced by it)
- A virtual machine or containerization platform in the traditional sense

---

## 3. The Personal Enterprise Model

The core conceptual framework of ogun OS is the **personal enterprise** — not a company in the legal sense, but a **closed-loop value transformation system** that converts your inputs (time, skill, capital, attention, relationships) into outputs (revenue, assets, reputation, equity, knowledge) through repeatable, structured operations that compound over time.

**The core reframe ogun OS enforces:**

| What you think it is | What ogun OS calls it |
|---|---|
| A piece of work | An **Engagement** — a state machine moving through a production pipeline |
| Output from that work | An **Artifact** — tracked, attributed, and registered |
| A collection of deliverables | An **Asset** — a portfolio item with a value and revenue attribution |
| All your assets together | A **Portfolio** — a graph of assets with aggregate valuation |
| Your whole career | An **Enterprise** — a configured value transformation system |
| Your whole working life | A **Portfolio of Enterprises** — governed by one system |

This mapping is not metaphorical. It maps precisely to the ogun data model in enzo, kogi, dongo, igi, and the Observatory.

**The Seven Value Dimensions**

ogun OS tracks value across seven dimensions simultaneously:

- **money** — income, revenue, financial returns
- **impact** — measurable outcomes for clients, communities, causes
- **knowledge** — learning, validated insight, developed capability
- **assets** — IP, equity, tools, systems that work independently of your time
- **network** — relationships, reputation, referral flow, social trust
- **emotional** — autonomy, satisfaction, security, creative fulfillment
- **progress** — movement toward your declared life vision

The platform is designed so that any enterprise optimizing only the "money" dimension while degrading others is treated as a suboptimally configured enterprise, not a success.

**The Enterprise Lifecycle**

Every enterprise you create in ogun OS moves through eight canonical states:

```
SEED → COLD → ACTIVATED → CALIBRATED → INTELLIGENT → OPTIMIZED → COMPOUNDING
                                                                        ↓
                                                                    ARCHIVED
```

| State | What it means |
|---|---|
| Seed | Pre-platform concept; no data yet |
| Cold | Enterprise record created; no connected data |
| Activated | First real data and first transaction recorded; **Shock Insight** delivered |
| Calibrated | 30+ metric snapshots; 3+ completed transactions; behavioral baselines computing |
| Intelligent | 90+ snapshots; personalized scenario models active; insights generated |
| Optimized | 180+ snapshots; agents earn higher authority; recommendations are predictive |
| Compounding | 365+ snapshots; passive income above 20%; full personalized intelligence |
| Archived | Deactivated; read-only history preserved |

**The Shock Insight** — at the `Cold → Activated` transition, the platform delivers your first quantified, personalized revelation from real data. For a freelancer this might be: *"You earned $9,800 last month but spent 186 hours working — $52/hour effective rate. Your three retainer clients averaged $94/hour. Your two project clients averaged $31/hour."* This gap was invisible before. It becomes the foundation of all intelligence from that point forward.

---

## 4. Platform Editions

ogun OS ships in five editions targeting different platforms. All share the same core Rust codebase — only the host driver, display driver, and certain platform behaviors vary.

| Edition | Platform | Host Type | Status |
|---|---|---|---|
| **Desktop** | Windows x64, macOS Apple Silicon, Linux x86_64 | `Desktop` | **0.1.0-beta (Windows x64 only)** |
| Web | Chrome, Firefox, Safari (WASM) | `Web` | Designed; planned post-beta |
| Mobile | Android arm64, iOS arm64 | `Mobile` | In progress |
| Server | Headless Linux | `Server` | Designed; planned post-beta |
| Device | IoT / embedded / custom hardware | `Device` | Designed; planned post-beta |

**Desktop Edition** — Installed on a local machine. Full 15-subsystem kernel. Tauri 2.0+ display. Passkey + TOTP/2FA authentication. Complete desktop environment with all apps. Offline capable.

**Web Edition (planned)** — Runs entirely in a browser tab as a WASM module. No installation required. WebAuthn authentication. Automatic updates. Requires internet connection.

**Mobile Edition (in progress)** — Native app for Android and iOS. Biometric authentication (FaceID/TouchID or fingerprint). Touch-optimized display. Responds to platform lifecycle (foreground, background, terminating).

**Server Edition (planned)** — Headless Linux. Multi-tenant: one `ogun-host` instance per active user/tenant. Skips authentication, desktop, and UI steps. Extra server-tier services: `TenantRegistry`, `ClientGateway`, `SyncBus`, `ResourceCoordinator`, `AdminApi`.

**Device Edition (planned)** — IoT, embedded, and custom hardware. Kiosk mode. Factory-flashed or OTA provisioned. Hardware authentication (NFC, PIN pad, certificate).

---

## 5. Release History and Versioning

ogun OS uses semantic versioning: `MAJOR.MINOR.PATCH[-qualifier]`

- **alpha** — Internal development; not for public distribution
- **beta** — First public pre-release; feature-complete for scope; known issues documented
- No qualifier — Stable release; all documented features verified; no known blocking issues

| Version | Status | Date | Description |
|---|---|---|---|
| `0.1.0-alpha` | Released (internal) | 2026 | Architecture and scaffolding; foundational types, image format, bootloader structure |
| `0.1.0-beta` | **Upcoming** | June 2026 | First public release; complete foundational runtime; Windows x64 Desktop |

**Planned post-beta:**
- `0.1.0` stable — refinements from beta feedback; no new features
- `0.2.0` — Storage backend migration from RustyDB to stable backend; additional platform targets
- Future: macOS Apple Silicon, Linux x86_64 Desktop; Android and iOS Mobile; Browser WASM Web

---

# Part II — Getting Started

---

## 6. System Requirements

**Minimum requirements for 0.1.0-beta (Windows x64):**

- Windows 10 x64 or Windows 11 x64
- 4 GB RAM (8 GB recommended)
- 2 GB available disk space (for installation; more for user data)
- Internet connection for initial installation and OgunNet peer discovery
- Administrator rights for initial installation and Task Scheduler registration

**Development requirements (if building from source):**

- Rust stable toolchain with Cargo
- Node.js and npm (for Tauri tools and desktop surfaces)
- Tauri 2 prerequisites for Windows
- Git

---

## 7. Installation Walkthrough

Installation is performed by `ogun-setup-windows-0.1.0-beta.exe` — the user-facing setup binary. It contains the full `ogun-installer` engine and is the only file you need to start.

**Step-by-step:**

1. Download `ogun-setup-windows-0.1.0-beta.exe` from the official release page.
2. Run the installer. You may need to allow it through Windows Defender SmartScreen.
3. The installer performs nine steps automatically:

| Step | What happens |
|---|---|
| 1. Platform detection | Verifies Windows x64; rejects unsupported platforms |
| 2. Image verification | Reads and verifies the ed25519 signature on the `.img` file before extracting anything |
| 3. Directory scaffolding | Creates `~/.ogun/` with all subdirectories; permissions set to owner-only |
| 4. Initial configuration | Writes `ogun.toml`, `display.toml`, `emulation.toml`, `uefi.toml` with defaults |
| 5. Security policy seeding | Extracts `opn-policy.json` and `capability-defaults.json` (both read-only after this) |
| 6. Registry seeding | Seeds the 12 namespace registrations, service registry, and package registry |
| 7. Module extraction | Extracts pre-built kernel modules to `~/.ogun/modules/` |
| 8. Security key generation | Generates SystemKey (private in Windows DPAPI; public at `system.pub`); derives HostKey |
| 9. Startup registration | Registers `ogun-desktop.exe` as the sole autostart entry via Task Scheduler |

4. After installation completes, ogun OS will start automatically on next login. To start immediately, run `ogun-desktop.exe` from the install directory.

**Silent install mode** (for enterprise deployment):

```
ogun-setup-windows-0.1.0-beta.exe --silent --install-dir "C:\ogun" --no-autostart
```

Use `--help` for the full flag reference. Silent mode is fully supported for enterprise deployment scenarios.

**What gets installed where:**

```
~/.ogun/
├── kernel/           — kernel image and version manifest
├── security/keys/    — image-verify.pub (0o444), system.pub (0o444), host.key (0o400)
├── security/         — system manifest, Ọpọn policy, capability defaults, encrypted audit log
├── config/           — ogun.toml, display.toml, emulation.toml, uefi.toml
├── modules/          — pre-built kernel modules (.dll)
├── logs/             — boot.log, uefi-boot.log, agent-actions.log
├── session/          — session state and current session record
├── snapshots/        — periodic session snapshots for crash recovery
├── namespaces/       — VFS namespace roots
├── packages/         — installed .ogun shell packages
├── plugins/          — OS runtime plugins
└── extensions/       — OS extensions (require operator approval)
```

The system key private half is stored exclusively in Windows DPAPI (Windows Credential Manager). It never appears under `~/.ogun/`.

---

## 8. First Boot and Onboarding

When you first launch ogun OS, the system runs a 17-step boot sequence and then presents the first-boot onboarding wizard. This wizard has three steps:

**Step 1 — Operator Profile**

Create your identity within ogun OS:
- Display name
- Handle (your @username in the system)
- Avatar
- Primary contact details
- Declare your primary and secondary personas (see [Section 49](#49-understanding-operator-personas))

**Step 2 — Enterprise Intent**

Declare what you are building:
- Select your enterprise type (Service / Creator / Founder / Investor / Hybrid / Cooperative / Estate / Platform)
- Select a Hypergrid template as your starting configuration (see [Section 55](#55-hypergrid-templates-overview))
- Set your GoalWeightVector (income / asset growth / passive income ratio / network weight)
- Optionally name your first enterprise

**Step 3 — Workspace Provisioning**

Set up your initial work context:
- Create your first workspace (or accept the auto-generated default)
- Configure workspace type (Enterprise / Client / Project / Focus / Research / Admin)
- Optionally connect your first integration (calendar, email, financial account)

After completing onboarding, you land in the Command Center — the operational headquarters of ogun OS.

**The Shock Insight delivery** — once you connect your first real data source (calendar, bank account, invoicing system), the Observatory processes your history and delivers your Shock Insight within minutes. This is your first personalized, data-backed revelation: the gap between how much you think you earn per hour and what the data shows.

---

## 9. Creating Your Operator Profile

Your **operator profile** is your primary identity within ogun OS. It governs what you see, how the system is configured, and what enterprises are in scope.

**To access:** Settings Center → Profile Center, or open `ogun-profile-center` from the App Bar.

**What an operator profile contains:**
- Display name and handle
- Avatar and bio
- Contact details and communication channels
- Primary and secondary personas
- GoalWeightVector (how you weight income, asset growth, passive income, network)
- Linked identities (Heshima verification, Linktree, OgunNet node ID)
- Enterprise memberships and roles
- RBAC role assignments per workspace and enterprise

**Multi-profile support** — you can create multiple operator profiles, each with its own enterprise set, workspace configuration, capability grants, and filesystem namespace. Switching profiles requires re-authentication (passkey + TOTP or recovery code). This is useful for separating a personal portfolio from work done under a specific agency or employer context.

---

## 10. Setting Up Your First Enterprise

An enterprise in ogun OS is a full runtime environment, not just a folder or a label. When you create one, the system provisions:

1. A namespace root at `enterprise://[enterprise-id]/`
2. A workspace linked to the enterprise
3. A default wallet in dongo
4. An observatory configuration in qala
5. A pipeline in kogi
6. A starter policy set based on your enterprise type

**To create an enterprise:**

1. Open **enzo** (Personal Enterprise Management System)
2. Click "New Enterprise" in the enterprise panel
3. Select a template (Freelancer, Creator, Founder, Investor, etc.) or start blank
4. Complete the enterprise identity form:
   - Canonical name
   - Enterprise type and sub-type
   - Mission and primary domain
   - Initial GoalWeightVector
5. Complete the Minimal Viable Enterprise (MVE) checklist:
   - [ ] At least one offer defined (a service, product, or investment thesis)
   - [ ] GoalWeightVector declared (sums to 1.0)
   - [ ] At least one active wallet configured in dongo
   - [ ] At least one KPI or dashboard tile created in qala

Until all four MVE conditions are met, the enterprise is in `Seed` state. You can continue working in this state, but no intelligence layer activates until data flows in.

**Enterprise types and their north star metrics:**

| Type | North Star Metric | Primary Intelligence Focus |
|---|---|---|
| Service (Freelancer) | EHR (Effective Hourly Rate) | EHR gap across clients; scope creep |
| Creator | Content EHR + Passive Income Ratio | Format efficiency gap; IP monetization |
| Founder | MRR + Runway | Build ROI by feature; equity rate |
| Investor | Portfolio IRR + Passive Income Coverage | Capital deployment efficiency; concentration risk |
| Hybrid | Multi-mode balance | Cross-enterprise allocation efficiency |
| Cooperative | Shared revenue per contributed hour | Hub governance; distributed equity |
| Estate | Net estate value + passive income | Asset yield; continuity planning |
| Platform | GMV + Network effects | Transaction volume; platform health |

---

## 11. Understanding Workspaces

A **workspace** is an isolated, persistent, enterprise-aware runtime context that scopes all OS activity — processes, files, agents, telemetry, and layout — to a specific operational domain.

Unlike a virtual desktop (which is just a way to arrange windows), an ogun workspace carries full enterprise context. Every process you run inside a workspace is tagged with that workspace's `workspace_id` and `enterprise_id`. Every file you create is placed under `enterprise://[enterprise-id]/...`. Every telemetry event, every agent action, every capability grant — all stamped with workspace context.

**Creating a workspace:**
1. Open **ogun-workspaces** from the Command Center or App Bar
2. Click "New Workspace"
3. Complete the creation wizard: purpose, type, enterprise linkage, layout preference

**Workspace types:**

| Type | Best for |
|---|---|
| Enterprise | Dedicated to running a single personal enterprise |
| Client | Per-client engagement environment |
| Project | Scoped to a specific project or work package |
| Focus | Single-application deep-work context (activates ogun-focus) |
| Research | Knowledge work and investigation |
| Admin | OS system administration |
| Template | Reusable workspace blueprint |
| Shared | Multi-operator collaborative workspace (via OgunNet) |
| System | Reserved for OS infrastructure; not user-created |

**Switching workspaces** — use `Ctrl+Shift+Space` to open the quick switcher. The system freezes your current workspace apps, saves their records, activates the target workspace, and restores its running app states. All this happens within a few hundred milliseconds.

**Workspace health** — each workspace carries a `HealthSignal` (Healthy / Warning / Degraded / Critical) driven by agent monitoring, outstanding tasks, and KPI status. The desktop system tray shows health indicators for all active workspaces.

---

# Part III — The Desktop Environment

---

## 12. The ogun Desktop Layout

The ogun desktop is structured as six spatial zones:

```
┌──────────────────────────────────────────────────────────────┐
│ TOP BAR                                                       │
├──────────────────────────────────────────────────────────────┤
│ UTILITY BAR                                                   │
├──────────────┬───────────────────────────────────────────────┤
│              │                                               │
│ APP BAR      │ APP PANEL                                     │
│              │                                               │
├──────────────┴───────────────────────────────────────────────┤
│ DOCK BAR                                                      │
├──────────────────────────────────────────────────────────────┤
│ FOOTER BAR                                                    │
└──────────────────────────────────────────────────────────────┘
```

| Zone | What it contains |
|---|---|
| **Top Bar** | Workspace switcher dots, global search, system clock, system tray (network node, memory pressure, session state) |
| **Utility Bar** | Schedule strip, Tasks strip, Focus timer, Notes quick-capture, unread Notifications, OBA AI summary strip |
| **App Bar** | Per-workspace side navigation for the currently active application |
| **App Panel** | Primary content area — application surfaces render here |
| **Dock Bar** | Home, Command Palette, Search, More; pinned application launchers |
| **Footer Bar** | System health signals, active process count, telemetry indicators, OgunNet peer count |

**Theme customization** — edit `display.toml` or use Settings Center → Display to change color scheme (light / dark / system), accent color, font families, and window scaling. The lock screen always displays in Cinzel typeface.

---

## 13. The Command Center

The **Command Center** (`ogun-command-center`) is the operational headquarters of ogun OS — the first screen after login and the central hub for all enterprise activity. It is a Tier 2 OS app with elevated access to session context.

**Home Dashboard — four permanent headline metrics:**

| Metric | Definition |
|---|---|
| **MRR** (Monthly Revenue) | Total income this month across all enterprises |
| **TPV** (Total Portfolio Value) | Estimated aggregate value of all portfolio assets |
| **EPV** (Expected Pipeline Value) | Σ(proposal_value × win_probability) across all active pipelines |
| **EHR** (Effective Hourly Rate) | Total income ÷ total hours invested including non-billable time |

**Enterprise Panel** — lists all your enterprises with lifecycle states. Click any enterprise to open it in enzo. Use the panel to switch the active enterprise context.

**Observatory Panel** — the intelligence surface. Shows system-wide telemetry, KPI snapshots, active insights, scenario modeling, and the Shock Insight when it first triggers. The Observatory runs continuously in the background via qala.

**Agents Panel** — all active Sambara agents with authority levels, current task, task history, recent actions, and orchestration controls. You can pause, resume, or escalate any agent from here without opening the full sambara app.

---

## 14. The Command Palette

**Keyboard shortcut:** `Ctrl+Shift+P` (or `Ctrl+K` — configurable in Settings Center → Keyboard)

The Command Palette is the universal keyboard-first interface available from any surface in ogun OS. It is context-aware: the commands shown change based on your active workspace, app, and enterprise.

**What you can do:**
- Open any installed app
- Switch workspaces
- Switch enterprises
- Run shell commands inline
- Navigate VFS namespace paths
- Dispatch agent commands
- Open settings panels
- Search for any operator record, contact, or file

Commands are fuzzy-searched. Type a few letters of anything to find it. Third-party apps can register their own commands at launch time.

---

## 15. The ogun Shell

The ogun Shell (`ogun-shell`) is a dual-surface command environment:
- **GUI Shell Surface** — an integrated, styled panel within the Command Center for interactive commands
- **Terminal Shell Surface** — a full terminal emulator for scripting and power users; accessible from the Dock Bar or via `Ctrl+Alt+T`

**Shell command categories:**

| Category | Examples |
|---|---|
| System | `sys.processes`, `sys.memory`, `sys.health`, `sys.restart` |
| Enterprise | `enzo.list`, `enzo.create`, `enzo.switch`, `enzo.kpis` |
| Financial | `dongo.wallet`, `dongo.tx`, `dongo.report` |
| Observability | `qala.metrics`, `qala.trace`, `qala.insight`, `qala.scan` |
| Filesystem | `fs.ls`, `fs.find`, `fs.cp`, `fs.mv`, `fs.stat` |
| Agent orchestration | `sambara.list`, `sambara.run`, `sambara.status`, `sambara.stop` |
| Workspace management | `ws.list`, `ws.switch`, `ws.create`, `ws.archive` |
| Package management | `opm.install`, `opm.remove`, `opm.list`, `opm.update` |
| Namespace operations | `ns.resolve`, `ns.list`, `ns.stat` |

Shell commands follow the `<package-id>.<verb>` naming convention. Additional commands can be installed as Shell Packages via `opm install`.

---

## 16. The File Explorer (orun Namespaces)

The File Explorer (`ogun-explorer`) is the graphical interface for the ogun virtual filesystem. Unlike conventional file explorers that show raw paths, ogun Explorer navigates all 12 registered namespace schemes with semantic metadata.

**The 12 Namespace Schemes:**

| Prefix | Contains |
|---|---|
| `ogun://` | System-wide ogun OS resources |
| `system://` | OS runtime state and kernel metadata |
| `user://` | Operator-owned personal data |
| `security://` | Security keys, audit logs (read-only), policy files |
| `app://` | Application-specific data namespaces |
| `data://` | General structured data storage |
| `network://` | OgunNet peer and channel registrations |
| `agent://` | Agent state and execution records |
| `enterprise://` | Enterprise-scoped resources (primary working namespace) |
| `workspace://` | Workspace runtime context and layouts |
| `session://` | Current and historical session records |
| `telemetry://` | Telemetry and metric streams |

**Dual-panel mode** — the Explorer can show a traditional path view alongside a semantic view, allowing you to browse `enterprise://my-consulting/clients/` while seeing metadata like EVS scores, last modified dates, attribution, and engagement links.

**Integrity display** — right-click any file to see its SHA-256 hash for integrity verification.

**OgunNet file transfer** — right-click any file to send it directly to an OgunNet peer without leaving the Explorer.

---

## 17. Settings Center

Access via: App Bar → Settings, or `opm` settings command, or `sys.settings` in the shell.

**Configuration panels:**

| Panel | What you can configure |
|---|---|
| Display | Theme, density, accent color, font size, transparency, window animations |
| Workspace | Default layout, persistence behavior, switching behavior |
| Keyboard | Global shortcuts, command palette bindings, shell key mappings |
| Locale | Region, timezone, date/time formats, language |
| Privacy | Telemetry opt-in, data sharing preferences |
| Integrations | External calendar sync, third-party service connectors |
| Startup | Boot apps, session restore behavior, onboarding state reset |
| Modules | Installed kernel modules; enable/disable; load order |
| Plugins | Installed OS plugins; hook configuration; enable/disable |
| Extensions | Installed OS extensions; approval state; behavior overrides |
| Advanced | Kernel parameters, IPC buffer sizes, telemetry verbosity, virtual CPU tick rate |

**Editing configuration files directly** — all configuration lives under `~/.ogun/config/`. You can edit `ogun.toml`, `display.toml`, `emulation.toml`, and `uefi.toml` with any text editor while ogun OS is not running, and they will be picked up on next boot.

---

## 18. Security Center

Access via: App Bar → Security, or Command Palette → "Security Center"

The Security Center (`ogun-security-center`) is the operator-facing interface for the kernel's capability-based security system.

**Security posture dashboard** — shows the overall security health: audit log entries, active capability grants, Ọpọn policy status, extension approval states, and certificate validity.

**Capability grant review** — lists every capability grant currently active for every running process. You can revoke any grant instantly. Revocation is logged to the audit trail before it takes effect.

**Agent authority audit** — shows every Sambara agent, its current authority level, and all actions it has taken. You can revoke or escalate agent authority from here (escalation requires explicit confirmation; it cannot be done by agents themselves).

**Peer reputation and ban list** — manage the OgunNet peer reputation scores and ban list from this surface.

**Audit log** — the encrypted audit log (`~/.ogun/security/audit.log`, AES-256-GCM encrypted) is viewable through the Security Center. Every capability grant, denial, Ọpọn Protocol enforcement event, and agent action is recorded here before the operation completes.

---

## 19. Profile Center

Access via: Top Bar → Profile icon, or Settings Center → Profiles

The Profile Center (`ogun-profile-center`) manages your operator profiles, enterprise identities, and public-facing identity configurations.

**Multi-profile operations:**
- Create new profiles
- Switch between profiles (requires re-authentication)
- Configure per-profile enterprise sets, workspace layouts, and keyboard shortcuts
- Export and import profile configurations
- Set up guest mode (restricted access profile)

**Enterprise profile management** — each enterprise can have its own branding, contact details, and Heshima verification status, separate from your personal operator profile.

---

# Part IV — The Personal Enterprise Suite (Tier 4 Apps)

The Tier-4 personal enterprise apps are the heart of ogun OS. Each one is a software-defined operating system for a specific domain of independent work. They are fully composable — designed to work together through shared data, the Elegua IPC bus, and the common enterprise context.

---

## 20. enzo — Personal Enterprise Management System

**enzo** is the enterprise operating system — the system that makes personal enterprises explicit, structured, measurable, and compounding. It is the control plane for your entire independent economic life.

**Core surfaces:**

**The Portfolio Control Center (PCC)** — the master view of all enterprises, their lifecycle states, aggregate portfolio metrics, and the intelligence feed. Four headline metrics always visible: MRR, TPV, EPV, EHR.

**Enterprise Dashboard** — per-enterprise view with the enterprise's current lifecycle state, value state V(t), active pipeline, KPI rail, and Observatory intelligence feed.

**The three system loops** (all running in the background):
1. **Production Loop** (daily/weekly): Demand → Pipeline → Work → Delivery → Payment → Portfolio Attribution
2. **Intelligence Loop** (weekly/monthly): Data → Observatory → Insight → Decision → Action → Outcome → Observatory
3. **Compounding Loop** (monthly/yearly): Better execution → Better artifacts → More revenue → Better attribution → Better decisions

**Software-Defined Enterprises** — create, configure, clone, fork, and merge enterprises. Enterprise templates set up policies, pipelines, and observatories in one click. All enterprise configuration is versioned.

**Enterprise Portfolio Management** — strategic alignment mapping, prioritization frameworks, balancing across risk, time horizon, income type, and effort.

**Enterprise Programs** — coordinate related projects under a program umbrella. Program chartering, milestone management, cross-project resource coordination.

**Enterprise Master Data Management** — canonical entity registry for clients, vendors, partners, products, and services. Cross-app synchronization ensures consistency everywhere.

**Key Metrics computed by enzo:**

| Metric | Formula |
|---|---|
| EHR | `total_income / total_hours` (billable + non-billable) |
| EAV (Effort-Adjusted Value) | `revenue / (time × cognitive_load_factor)` |
| EPV | `Σ(proposed_value × win_probability)` |
| TPV | Aggregate of all enterprise asset valuations |
| Passive Income Ratio | `passive_income / total_income` |
| Commitment Tension τ | `Σ(committed_effort) − weekly_hours_max` |

---

## 21. kogi — Software-Defined Office

**kogi** is the operational office runtime — the environment where value is actually created. The desk, the pipeline, the production engine, and the effort management system.

**The Desk** — your primary engagement surface. Create multiple desks (Client Desk, Product Desk, Admin Desk, Research Desk, Creative Desk) and configure their layouts. Desks have profiles: deep work, client calls, admin, creative, learning.

**Pipeline Management** — every incoming request, opportunity, or project is a stateful Engagement moving through a Pipeline. Pipeline types: Acquisition, Delivery, Content, Build, Investment, Deal. Each pipeline stage has configurable stall thresholds and stall actions.

**Effort and Commitment Management** — the Commitment Register tracks all active promises, deliverables, and obligations. Commitment Tension (τ = Σ(effort_required) − weekly_hours_max) is displayed in real time. When τ > 0, the system blocks new engagements and notifies you.

**Filtering System** — unified inbox for all inbound requests from all channels. Priority filtering, routing rules, delegation routing, and Do-Not-Disturb policies.

**Automation and Orchestration** — workflow automation builder (if-this-then-that style). Meeting prep automation, recurring checklist automation, daily briefing generation.

**Productivity Analytics** — time tracking by project, client, and task type. Productive vs. reactive time ratio. Focus session duration and interruption tracking. Planned vs. actual effort comparison.

**Universal service pipeline stages:**
```
Lead → Qualifying → Proposed → Negotiating → Contracted
     → InProgress → Delivered → Accepted → Paid → Closed
```

---

## 22. dongo — Financial Management System

**dongo** is the financial operating system — the full double-entry accounting, wallet, and financial intelligence layer.

**Software-Defined Wallets** — create programmable wallet objects with defined purpose, rules, limits, currencies, and linked accounts. Wallet templates: Operating, Tax Reserve, Client Escrow, Project Budget, Emergency. Automation rules: auto-sweep, threshold alerts, auto-pay, waterfall funding.

**Double-Entry Accounting** — full chart of accounts, journal entry creation, bank reconciliation, accounts receivable (with aging and dunning), accounts payable (vendor bills, payment scheduling), and financial statements (P&L, Balance Sheet, Cash Flow).

**Income Management** — income stream tracking by client, project, contract, or product. Invoice generation and payment tracking. Recurring invoice and retainer management. Earned-but-not-invoiced tracker.

**Expense and Budget Management** — business expense tracking and categorization. Receipt capture. Budget creation by project, client, time period, or cost center. Budget variance monitoring. Spending anomaly detection.

**Personal Benefits Management** — health, dental, vision, disability, life, and liability insurance tracking. Gap analysis. Open enrollment calendar. HSA/FSA management. Retirement management: Solo 401(k), SEP-IRA, SIMPLE IRA, traditional and Roth IRA. Contribution optimization.

**Digital Financial Assets** — cryptocurrency portfolio management (multi-wallet, multi-chain). Cost basis and gain/loss calculation. Staking and yield tracking. NFT tracking. DeFi positions. Digital asset tax reporting. Digital asset estate planning integration with zamani.

**Tax and Compliance** — estimated quarterly tax calculation and reserve management. Self-employment tax tracking. Deduction identification. 1099-NEC and 1099-K tracking.

**Cash Flow and Forecasting** — rolling projections (30/60/90/180 days). Scenario modeling (best/worst/expected). Break-even and runway analysis.

---

## 23. ume — Organization Operating System

**ume** is the organization operating system — legal entities, contracts, governance, and all business functions.

**Legal Entity and Contract Management** — entity registration tracking (LLC, S-Corp, partnership, cooperative). Corporate record keeping (resolutions, minutes, bylaws). Contract lifecycle (draft → negotiate → execute → monitor → renew/expire). Contract templates: MSA, SOW, NDA, Retainer, IP Assignment. Contract obligation tracking. Counterparty management.

**Business Functions managed by ume:**
- Human Resources (contractor/collaborator records, compensation, roles)
- IT and Asset Management (hardware/software inventory, license management)
- Marketing and Sales (brand assets, campaign planning, CRM-lite)
- Accounting and Finance (integrated with dongo)
- Supply Chain and Logistics (vendor management, procurement, delivery tracking)
- Production and Manufacturing (build pipeline, quality management, work orders)
- Strategic Management (business development pipeline, partnership management)

**Operations Management** — cross-functional operations planning. Operational KPI tracking. Process documentation and SOP management. Business continuity planning.

---

## 24. heshima — Identity Management System

**heshima** is the identity operating system — credentials, verification, reputation, and identity orchestration.

**Software-Defined Identities** — create and manage multiple identity profiles (personal, professional, business entity, pseudonymous). Identity lifecycle: draft → verified → active → retired. Identity versioning and audit trail. Decentralized Identity (DID) and verifiable credential support.

**Linktree / Linkforest / Linknet Management** — link profile creation for multiple contexts. Link categorization (social, professional, portfolio, commercial, contact). Dynamic link routing (A/B, geo-targeted, audience-segmented). Link analytics. QR code generation.

**Verification and Trust** — credential verification workflows (ID, certifications, references). Trust score and reputation aggregation. Professional reference management. Endorsement and recommendation management. KYC/AML compliance support.

**Operators and Executors** — delegate actions to others with defined scope and time limits. RBAC and ABAC. Executor configuration for automated agents (Sambara integration). Emergency access and recovery.

**Privacy and Security** — data minimization and selective disclosure controls. Pseudonymous identity isolation. Consent management and data sharing audit. Identity breach detection and response playbook.

---

## 25. shango — Solution Factory

**shango** is the production operating system — solution management, build environments, QA, and distribution.

**Software-Defined Factories** — factory definition for a category of solutions (software, content, consulting deliverables). Factory templates by solution type: SaaS product, report, course, API, design system. Configuration versioning. Multi-factory management.

**Software-Defined Environments** — dev, staging, and production environment management. Environment configuration-as-code. Environment parity monitoring (drift detection). Secrets and credential management. Ephemeral environments for testing.

**Solution Lifecycle States:** `Concept → Prototype → Alpha → Beta → Active → Deprecated`

**Testing and QA** — test plan and test case library. Automated test execution. QA gate enforcement. Defect tracking. Acceptance criteria management. QA performance metrics.

**Solution Delivery** — delivery checklist and handoff workflow. Client acceptance tracking. Post-delivery support period management. Solution documentation package generation.

**Shango Persona Templates included:**
- **Software Architect** — blueprint design, ADR library, API contracts, pattern catalog, technology registry governance
- **Engineering Leader** — executive dashboard with portfolio-level KPIs (deployment frequency, change failure rate, SLO compliance, compliance score, tech debt)
- **Security Engineer** — cross-cutting security authority embedded in all lifecycle stages (SAST/DAST, SEM, secrets vault, compliance frameworks: SOC 2, ISO 27001, PCI-DSS, HIPAA, GDPR)

---

## 26. igi — Portfolio Management System

**igi** is the portfolio management runtime — asset tracking, valuation, artifact attribution, and ownership systems.

**Software-Defined Portfolios** — portfolio creation, strategic alignment mapping, sub-portfolio nesting. Portfolio types: Work, Investment, Project, IP. Portfolio lifecycle states: forming, active, optimizing, winding down.

**Portfolio Governance** — portfolio charter and investment thesis. Strategic alignment scoring. Prioritization frameworks (weighted scoring, strategic fit, ROI, risk). Portfolio review cadences. Governance board setup.

**Enterprise Value Score (EVS):**
```
EVS = base_value + (revenue_multiple × annual_revenue) + strategic_premium

Revenue multiples:
  Service retainer:  12× monthly_value
  Digital product:   24–36× monthly_revenue
  Software:          ARR × 3–10× (stage-dependent)
  Equity:            ownership_pct × entity_valuation
```

**Passive Income Trajectory targets:**

| Horizon | Target Passive Ratio |
|---|---|
| Year 1 | < 10% |
| Year 3 | > 25% |
| Year 5 | > 50% |
| Year 7+ | > 70% |

---

## 27. akeel — Knowledge Management System

**akeel** is the knowledge operating system — documentation, research, methodology, and institutional memory.

**Knowledge Management** — knowledge base creation, multi-space management, document authoring with rich text and code blocks. Document templates library. Document lifecycle (draft → review → published → deprecated → archived). Knowledge graph (link related articles, projects, decisions, and people).

**Wiki Management** — hierarchical wiki structure. Page ownership and review assignment. Freshness tracking (flag stale pages). Version history and rollback. Access control per section or page.

**Decision Log** — document every significant decision with context, options considered, rationale, and outcome. Link decisions to projects, strategies, and programs. Decision review and retrospective support.

**Information Management** — bookmarking and clipping from external sources. Inbox for unprocessed information items. Information decay (archive old or superseded items). Personal and enterprise knowledge separation.

---

## 28. moto — Project Management System

**moto** is the project management system — work packages, scope management, milestone tracking.

**Project Management** — project scoping, brief generation, timeline and scheduling (linked to misimu), dependency mapping and critical path analysis. Project status tracking (on track, at risk, delayed, completed). Project health dashboard.

**Work Packages** — define work packages with owner, effort estimate, and deliverable. Decompose into tasks and sub-tasks. Budget tracking (linked to dongo). Dependency management. Blocked work package alerting.

**Scope Management** — scope statement documentation and approval. Scope change request intake and evaluation. Change impact analysis (cost, time, quality). Scope baseline maintenance. Out-of-scope item log.

**Resource and Effort Management** — task assignment and ownership. Effort estimation and actuals tracking. Resource availability and capacity check (linked to kogi). Overallocation detection. Time entry and timesheet management.

---

## 29. zamani — Estate Management System

**zamani** is the estate management system — wealth, physical assets, personal records, and continuity.

**Software-Defined Estates** — estate definition and scope (assets, liabilities, dependents, beneficiaries). Estate plan documentation and versioning. Multi-estate management (personal, family trust, business). Estate scenario modeling (retirement, disability, death, sale of enterprise).

**Wealth and Asset Management** — net worth dashboard (assets minus liabilities). Asset registry (real estate, vehicles, equipment, collectibles, digital assets). Asset valuation tracking. Investment portfolio management. Liability register.

**Estate Continuity Services** — will and trust document management. Beneficiary designation tracking. Digital asset inheritance planning. Power of attorney and healthcare directive management. Estate settlement workflow.

**Personal Records and Documents** — government records, health records, financial records, benefits records. Secure document storage with access control and expiry reminders.

**The Homesteader Persona** (zamani-estate-homesteader template) — for operators whose primary residence is also a productive estate node. Tracks:
- True monthly cost of the estate (mortgage P&I, insurance, utilities, internet)
- Home office income attribution (income generated per hour in home studio)
- Short-term rental income and occupancy rate
- Net daily cost vs. net daily value generated
- Vehicle as a mobility asset node

Example Shock Insight: *"Your home costs $4,240/month to operate. Your home office generates $8,100/month in consulting income. Your estate produces $4,540/month NET positive value — but only because of your office. Without it, this asset loses $3,560/month. Your home office is your highest-yield investment."*

---

## 30. sambara — Agent Management System

**sambara** is the AI agents operating system — not a prompt-chaining tool or LLM wrapper, but a complete operating system for AI agents. Agents are first-class runtime entities with kernel-level identity (`agent_id`), workspace-bounded execution, operator-governed authority, and continuously improving intelligence models.

**Every agent action is written to `~/.ogun/logs/agent-actions.log` (encrypted at rest) before the action completes.** Agents cannot bypass or inspect their own governance block.

**Agent Authority Levels:**

| Level | Capability |
|---|---|
| `OBSERVE` | Read-only; monitors and contributes to MetricSnapshots; no actions |
| `RECOMMEND` | Generates `InsightRecord`s and drafts for operator review; no automated actions |
| `EXECUTE_BOUNDED` | Takes actions within explicitly declared parameter ranges; exceptions escalate |
| `FULL_AUTONOMY` | Operates within declared domain without per-action approval; requires `OPTIMIZED` lifecycle stage |

Authority escalation requires explicit operator interaction. It cannot be triggered by agent logic, policy rules, or Observatory recommendations.

**Platform-Registered Domain Agents:**

| Agent | Function |
|---|---|
| FOLLOWUP_AGENT | Sends proposal follow-ups; tracks stalls in pipeline |
| PRICING_AGENT | Adjusts rates within bounded ranges when EHR exceeds floor by threshold |
| EXECUTION_AGENT | Manages task scheduling and delivery reminders |
| ACQUISITION_AGENT | Executes outreach when pipeline below health floor |
| BOOKKEEPING_AGENT | Reconciles transactions; flags missing attribution |
| OBSERVATORY_AGENT | Generates metric snapshots; surfaces insights |
| PRODUCTIZATION_AGENT | Detects scaffold patterns; initiates packaging pipeline |
| QALA_PLANNER | Plans analytics queries and model builds |
| ESTATE_AGENT | Monitors estate assets and cost/yield ratios |
| ATTRIBUTION_AGENT | Ensures revenue events have valid attribution IDs |
| LIFECYCLE_AGENT | Monitors enterprise readiness for lifecycle stage transitions |
| ORCHESTRATION_AGENT | Coordinates multi-agent workflows |
| PRIVACY_AGENT | Enforces Ọpọn Protocol at all data boundary crossings |

**LLM Drivers** — Sambara is model-agnostic. Built-in drivers:
- `anthropic-claude` — `claude-opus-4-6`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`
- `openai-chatgpt` — `gpt-4o`, `o1`, `o3-mini`
- `deepseek` — `deepseek-chat`, `deepseek-reasoner`
- `ollama-local` — any locally served model

Custom LLM drivers can be registered on the `ENTERPRISE` governance tier.

**Sambara Persona Templates:**
- **Data Engineer** — data platform authority; pipeline engineering; feature store management; schema registry governance; data quality and lineage
- **Platform Administrator** — platform infrastructure reliability; SLA management across all 14 Sambara packages; security posture; upgrade ownership

---

## 31. qala — Observatory and Analytics

**qala** is the Observatory, analytics, metrics, insights, and telemetry management system — the intelligence layer of ogun OS.

**Data Collection and Telemetry** — event ingestion from all ecosystem apps. Real-time streaming pipelines. Batch data ingestion and historical backfill. External data connectors (financial APIs, market data, social platforms). Data catalog.

**Metrics Management** — metric definition library (KPIs, OKRs, custom indicators). Calculation engine with formula and aggregation support. Metric versioning and change history. Threshold and target management.

**Analytics and Insights** — pre-built dashboards (enterprise health, financial performance, project status, capacity). Custom dashboard builder. Anomaly detection and smart alerting. Cohort analysis and trend detection. Predictive analytics (revenue forecasting, capacity planning, churn risk).

**Observability Pipeline:**
```
Runtime Event → Telemetry Bus → Aggregation → Storage → Observatory Engine → Insights / Actions
```

**Insight Types Generated by qala:**

| Type | Trigger |
|---|---|
| ShockInsight | First data-backed revelation (onboarding — `Cold → Activated`) |
| PricingOpportunity | EHR consistently above floor by > 30%; market rate evidence |
| EfficiencyGap | EHR disparity across clients; time allocation inefficiency detected |
| PipelineRisk | EPV below 1.5× monthly target; stall detected; concentration risk |
| ProductizationSignal | Scaffold detected (4+ deliveries in 180 days of same pattern) |
| AllocationOptimization | Time or capital reallocation opportunity |
| LifecycleGraduation | Enterprise ready to advance to next maturity stage |
| ConcentrationRisk | Single client or platform over 40% of revenue |

---

## 32. shaba — Strategic Management System

**shaba** is the strategic management system — value proposition, OKR management, strategy execution, and capability development.

**Value Proposition and Business Model** — value proposition canvas and design tools. Business Model Canvas (BMC) creation. Customer segment definition. Value chain analysis. Competitive differentiation articulation.

**Charters, Vision, Mission, and Purpose** — enterprise charter documentation and versioning. Vision statement creation and periodic review. Long-term aspiration tracking (10-year, 3-year, 1-year horizons).

**OKR Management** — Objectives and Key Results with check-in cadences. Strategic goal hierarchy (enterprise → program → project). Goal alignment verification. Goal retrospective and learning capture.

**Strategy Audit and Monitoring** — strategy execution scorecard. Strategic assumption tracking. Environmental scanning. Strategic risk register. Quarterly and annual strategy review facilitation.

---

## 33. kanna — Governance Management System

**kanna** is the governance management system — standards, policies, cooperative governance, and hub management.

**Software-Defined Hubs** — define governance units: personal enterprise, community, cooperative, or DAO. Hub membership management (members, roles, voting rights). Hub configuration (decision rules, quorum thresholds, voting mechanisms).

**Decentralized Governance** — proposal creation, discussion, and voting workflows. Voting mechanism support: majority, supermajority, consent, quadratic, ranked choice. Governance token or reputation-weighted voting. Governance history and audit trail.

**Standards, Frameworks, and Policies** — standards library (create, publish, maintain standards). Framework management. Policy creation, versioning, and approval workflows. Policy exception management. Compliance monitoring.

**Hub Pattern for multi-enterprise collaboration** — two or more enterprises share execution infrastructure for a joint engagement without merging as legal entities. Revenue is immediately split per the declared RevenueSplit and attributed to each enterprise's separate Wallet. Raw data from each enterprise remains isolated (Ọpọn Protocol enforced).

---

## 34. zuri — Digital Marketplace System

**zuri** is the digital marketplace and exchange system — software-defined stores, marketplace operations, and commerce.

**Software-Defined Stores** — store creation, configuration, and branding. Product and service catalog management. Pricing models: one-time, subscription, tiered, usage-based, bundled, revenue share. Multi-store management.

**Product and Service Management** — digital product management (files, courses, templates, software, licenses). Service offering management (consulting packages, retainers, workshops). Digital delivery automation. Service delivery scheduling.

**Commerce Operations** — order management (processing, fulfillment, tracking, cancellation). Payment processing and reconciliation (linked to dongo). Refund and dispute management. Coupon, discount, and promotion management. Affiliate and referral program management.

**Exchange Features** — peer-to-peer exchange and trading facilitation. Asset listing, bidding, and auction management. Escrow and milestone-based payment release.

---

## 35. ayo — Digital Spaces Management

**ayo** is the digital spaces management system — software-defined spaces, personal enterprise social infrastructure, and community management.

**Software-Defined Spaces** — create, configure, and publish digital spaces (personal, professional, community, commercial). Space templates and theming with custom domain mapping. Access control and permission layers.

**Personal Enterprise Spaces** — personal enterprise home page and public profile. Portfolio showcase space. Service catalog space. Client portal spaces (secure, branded, per-engagement). Space analytics (visitor traffic, engagement, conversion metrics).

**Independent Worker Social Media Platform** — professional profile and personal brand publishing. Content creation (posts, articles, case studies, micro-updates). Follow/subscribe model for audience building. Opportunity board (post and discover gigs, collaborations, contracts). Direct messaging. Feed curation.

---

## 36. mizeez — Version and Change Control

**mizeez** manages versioning and change control for all artifact types — not just code, but documents, configurations, designs, and any produced deliverable.

Git-compatible version control. Branching strategies (trunk-based, feature branches, release branches). Merge and conflict resolution workflows. Changelog generation. Semantic versioning enforcement. Artifact repository for binaries, packages, and builds. Package registry management. Artifact signing and integrity verification. Change request intake and approval workflow. Emergency change fast-track process.

---

## 37. orun — Semantic Filesystem Runtime

**orun** is the semantic filesystem layer and workspace bootstrapper — the runtime that gives meaning to paths, manages namespace resolution, and orchestrates workspace and asset initialization.

**Workspace Bootstrapper** — one-click workspace initialization for new enterprises, projects, or programs. Guided setup wizard. Workspace templates by use case. Pre-configured workspace bundles. Bootstrap checklist with guided completion.

**Asset System** — reusable digital asset library (templates, configs, scripts, components, prompts). Asset tagging, search, and discovery. Asset versioning and update management.

**Semantic Filesystem Layer** — unified semantic file and artifact namespace across the enterprise. Smart search by meaning, not just name. File relationship mapping (related, derived, dependent). Semantic deduplication.

**Namespace Scheme Reference:**
```
enterprise://[enterprise-id]/[path]     — enterprise-scoped resources
asset://[portfolio-id]/[asset-id]       — portfolio-registered assets
artifact://[enterprise-id]/[artifact]   — produced deliverable objects
operator://[operator-id]/[path]         — operator-owned identity data
agent://[agent-id]/[path]               — agent state and execution records
workspace://[workspace-id]/[path]       — workspace runtime context
service://[service-id]/[path]           — system service registration
system://[subsystem]/[path]             — OS runtime and kernel state
ipc://[channel-id]/[path]               — IPC channels and message buses
telemetry://[scope-id]/[stream]         — telemetry and metric streams
config://[component-id]/[key]           — configuration values
temp://[process-id]/[path]              — transient scratch space
```

---

## 38. apapo — Hypergrid Platform

**apapo** is the domain operating system development platform — the runtime for building and deploying distributed ogun environments.

**Platform and Runtime** — hypergrid kernel management. Domain registration, routing, and namespace management. Multi-tenant domain isolation. Cross-domain service mesh and API gateway. Runtime environment provisioning.

**Developer Platform** — SDK and API surface for building software-defined apps. Developer console. App scaffolding and templating. Plugin and extension marketplace. Webhook and event bus management.

**Infrastructure and Operations** — compute resource allocation and autoscaling. Storage layer management. Network topology configuration. Load balancing. Disaster recovery. System health dashboards.

---

## 39. didara — IP Tracking and Management

**didara** manages intellectual property — patents, trademarks, copyrights, trade secrets, licenses, and equity arrangements.

Patent application tracking (provisional, non-provisional, PCT). Patent prosecution timeline and maintenance fee scheduling. Trademark application and registration tracking. Use evidence documentation. Renewal and maintenance scheduling.

**Rights, Ownership, and Licenses** — IP ownership assignment and transfer records. Licensing agreement tracking (exclusive, non-exclusive, field-of-use). Royalty rate management and payment tracking. Open source license compliance tracking.

**Equity Management** — IP-backed equity arrangements. IP contribution to joint ventures. IP valuation for fundraising. IP pledge and collateral management.

---

## 40. misimu — Schedule and Event Management

**misimu** is the full-featured schedule, calendar, timeline, and event management system (complementing the lightweight `ogun-schedule` utility app).

Multi-calendar management. Availability management and scheduling rules. Booking link management (public scheduling pages). Buffer time and recovery time settings. Calendar analytics (how time is actually being spent).

**Timeline Management** — project and program timeline visualization (Gantt-style). Milestone and phase management. What-if scenario modeling. Timeline export and client sharing.

**Event Management** — event creation (meetings, workshops, webinars, launches, reviews). Attendee management. Event material management. Post-event follow-up task generation. Event series management.

**Time Intelligence** — time blocking recommendations (linked to kogi). Scheduling conflict detection. Time zone management. Personal energy management integration (schedule deep work at peak hours). Annual planning calendar with strategic review dates.

---

# Part V — Utility Apps (Tier 3)

---

## 41. ogun-notes

Persistent, searchable, enterprise-linked notes. Markdown support with live preview. Enterprise and engagement linking. Tagging and categorization. Full-text search. Note templates. Embed links to semantic namespace paths. Export to `artifact://`. Utility Bar strip for quick capture without opening the full app.

---

## 42. ogun-tasks

Unified task and to-do management. Task creation with priority, due date, assignee, and enterprise linkage. Priority levels: low, medium, high, critical. Engagement and project linkage. Agent delegation (assign tasks to Sambara agents). Completion tracking with telemetry. Recurring tasks. Utility Bar strip showing today's priority tasks.

---

## 43. ogun-focus

Focus session and deep work mode management. Pomodoro and custom focus intervals. Distraction blocking during sessions (suppresses non-critical notifications). Session logging with actual vs. planned time. Session attribution to enterprise and engagement. Time blocking (coordinates with misimu). Utility Bar strip with current session timer.

---

## 44. ogun-calendar (ogun-schedule)

Lightweight schedule, calendar, and timeline management. Day, week, and month views. Event creation with enterprise linking. External calendar sync (Google, Outlook, CalDAV). Timeline visualization across workspace activity. Deadline tracking. Utility Bar strip with today's agenda.

For full-featured calendar management with booking links, public scheduling pages, and energy management integration, use **misimu** (Tier 4).

---

## 45. ogun-messenger

Unified notifications and messaging hub. Notification aggregation across all apps, agents, and system events. Policy engine alerts. Agent activity feed. Workspace-filtered notification views. Message threads. Priority levels: informational, warning, action required, critical. Utility Bar strip with unread count badge.

For secure P2P messaging over OgunNet, the underlying transport is the OgunNet named channel system. See [Section 72](#72-named-channels-and-group-communication).

---

## 46. ogun-search

Universal system-wide search across all 12 namespace schemes. Searches: files, notes, tasks, contacts, engagements, assets, agents, workspaces, and commands. Semantic search by attribute and meaning (not just filename). Enterprise-scoped filtering. Recent items history. Saved searches. Agent-powered index refresh. Keyboard-first interface.

---

## 47. ogun-assistant (OBA)

OBA — the ogun AI assistant. A bounded Sambara agent with a conversational interface running at `RECOMMEND` authority by default.

**Capabilities:**
- Observatory insight surfacing (translates telemetry into plain-language summaries)
- Draft generation (emails, proposals, notes, reports with enterprise context awareness)
- Task and engagement creation via natural language
- Command translation (describe what you want; OBA generates the shell command)
- Context-aware responses (knows active workspace, enterprise, current engagements, portfolio state)

All OBA actions are logged, attributable, and auditable. OBA can be granted `EXECUTE_BOUNDED` authority by the operator in the Security Center.

---

## 48. ogun-contacts

Contact and network management. Contact records linked to pipeline clients, engagement counterparties, and network nodes. Contact metadata (name, organization, role, channels, relationship history). Network metrics (referral count, engagement history, relationship strength signals). Integration with Heshima identity verification, Kogi pipeline, and Zuri marketplace. Network value tracking.

---

# Part VI — Operator Personas and Hypergrid Templates

---

## 49. Understanding Operator Personas

A persona is your primary lens for how you create value. ogun OS supports five primary personas and a meta-persona:

| Persona | Primary Resource | Primary Constraint | North Star Metric |
|---|---|---|---|
| **Creator** | Creative output + Audience | Production consistency | Revenue per production hour (Content EHR) |
| **Operator** (Freelancer) | Time + Skill | Capacity (hours/week) | EHR |
| **Builder** (Founder) | Build time + Capital | Product-market fit | MRR + Runway |
| **Investor** | Capital | Deployment judgment | Portfolio IRR |
| **CNO** (meta-persona) | Attention and decision quality | Multi-enterprise coordination | TPV + Portfolio passive ratio |

You can declare a primary and secondary persona. Many operators run multiple simultaneously (Builder + Operator, Creator + Investor, etc.).

**Persona Progression Paths:**
- Creator → Creator + Builder (when packaging knowledge into software tools)
- Operator → Operator + Investor (when taking equity stakes in collaborators' enterprises)
- Builder → Builder + Operator (when taking custom work alongside product sales)
- Any → Cooperative (when sharing enterprise ownership with another operator via Kanna Hub)
- Any 2+ → CNO (when the portfolio needs managing as a unified entity)

---

## 50. Freelancer / Operator Persona

**Template:** `hypergrid-freelancer.xml`

The Freelancer template is for consultants, contractors, coaches, gig workers, and all client-based service providers. The enterprise model is service-based: time for money, moving toward retainerization and then productization.

**Revenue progression path:**
1. Time for money (hourly/project billing)
2. Retainerization (monthly recurring clients)
3. Productization (Observatory trigger → Shango build → Zuri listing)
4. IP and system licensing

**North Star:** EHR per client, per service type

**Shock Insight:** The EHR gap across clients — which client pays the most per hour including admin time, revisions, and meetings. Most freelancers have a 2–4× gap they've never seen because the data was never unified.

**Starter Policy Set:**
- Rate/EHR Floor policy — alerts when any engagement drops below floor rate
- Concentration Cap — alerts when any single client exceeds 40% of revenue
- Pipeline Health Floor — triggers acquisition agent when pipeline EPV drops below 1.5× monthly target
- Burnout Protection — blocks new commitments when Commitment Tension τ > 0 for 2+ consecutive weeks

---

## 51. Creator Persona

**Template:** `hypergrid-creator.xml`

The Creator template is for content creators, artists, journalists, writers, musicians, media creators, indie developers, and anyone converting knowledge and creativity into IP and audiences.

**Sub-personas supported:** content-creator, visual-artist, musician, writer, media-creator, indie-developer, hobbyist

**Revenue progression path:**
1. Single platform, single income stream (AdSense, streaming)
2. Platform + audience monetization (Patreon, Substack)
3. Products + IP monetization (Shango courses/templates, licensing)
4. IP portfolio as primary asset (passive income dominant)

**North Star:** Content EHR — revenue per production hour by content type AND by platform

**Shock Insight:** Format efficiency gap — which creative work earns the most per production hour. Most creators discover their highest-earning format produces 3–10× more per hour than their most time-intensive format.

**Key metrics tracked:**
- Content EHR by format (video, written, audio, visual, software)
- Content EHR by platform
- Audience size and growth rate
- IP passive income ratio
- Productization readiness score (scaffold signal detection)

---

## 52. Founder / Builder Persona

**Template:** `hypergrid-founder.xml`

The Founder template is for entrepreneurs, solopreneurs, micropreneurs, intrapreneurs, startup founders, and studio operators.

**Sub-personas:** solopreneur, micropreneur, startup-founder, intrapreneur, serial-founder, studio-operator

**Typical structure:**
- Personal Office (ROOT)
- HoldCo (planned — centralizes equity ownership)
- Operating Entities (active ventures)
- IP Entity (optional — codebase, brand, methodology, data)

**North Star:** MRR + Runway + Equity-per-hour-invested

**Shock Insight:** Time-to-equity ratio — hours invested vs. enterprise value created vs. opportunity cost. Reveals whether building equity is returning more than comparable consulting work.

**Key metrics tracked:**
- MRR growth rate
- Runway in months
- Burn rate
- Equity-per-hour (vs. operator's service EHR)
- Product-market fit signals (user growth, churn, NPS)

---

## 53. Investor Persona

**Template:** `hypergrid-investor.xml`

The Investor template is for retail investors, real estate holders, angel investors, crypto holders, donors, patrons, and crowdfunding participants.

**Sub-personas:** retail-investor, real-estate, angel, crypto-holder, donor, patron, note-holder, crowdfunding

**Portfolio evolution:**
1. Single asset class (stocks or savings)
2. Multi-class portfolio (real estate, alternatives, crypto added)
3. Active deal deployment (angel investing via Zuri)
4. Managed portfolio (passive income dominant, estate integration)

**North Star:** Portfolio IRR + Passive Income Coverage Ratio (passive_income / monthly_expenses)

**Shock Insight:** Capital deployment efficiency — what your money is actually doing vs. what it could do. Includes the cost of idle capital and the impact of giving.

---

## 54. CNO — Chief Navigation Officer (Meta-Persona)

The CNO persona is for operators running multiple enterprises simultaneously. It is accessed from the **Portfolio Control Center** in enzo.

The CNO manages through the canonical portfolio optimization equation:
```
Π* = argmax Σᵢ wᵢ V(ℙᵢ) + V_cross(Π) − C_coord(Π)
```

Where:
- `V(ℙᵢ)` = value of each individual enterprise
- `V_cross(Π)` = cross-enterprise synergy value (shared audiences, referrals, IP reuse)
- `C_coord(Π)` = coordination cost (attention, time, overhead)

The CNO view surfaces insights that are only visible at the portfolio level: which enterprise is consuming the most cognitive load relative to its value, where cross-enterprise synergies are being left unrealized, and when the portfolio balance has drifted from the declared GoalWeightVector.

---

## 55. Hypergrid Templates Overview

Hypergrid templates are XML configuration files (`.xml`) that define a complete enterprise starting configuration: enterprises, pipelines, workspaces, policies, agents, wallets, offers, and system integrations. They are the fastest way to initialize a new enterprise or persona configuration.

**Available templates:**

| Template | Persona | Use case |
|---|---|---|
| `hypergrid-freelancer.xml` | Freelancer | Consultants, contractors, coaches, gig workers |
| `hypergrid-creator.xml` | Creator | Content creators, artists, writers, musicians, indie developers |
| `hypergrid-founder.xml` | Founder | Entrepreneurs, solopreneurs, micropreneurs, startup founders |
| `hypergrid-investor.xml` | Investor | Retail investors, real estate, angels, crypto, donors |
| `sambara-hypergrid-data-engineer.xml` | Data Engineer | Sambara data platform and pipeline engineering |
| `sambara-hypergrid-platform-admin.xml` | Platform Admin | Sambara platform infrastructure and SLA management |
| `shango-hypergrid-architect.xml` | Software Architect | Blueprint design, ADR library, technology registry governance |
| `shango-hypergrid-engineering-leader.xml` | Engineering Leader | Portfolio-level KPIs, executive dashboard, strategic decisions |
| `shango-hypergrid-security-engineer.xml` | Security Engineer | Cross-cutting security authority, compliance frameworks |
| `zamani-estate-homesteader-nadiachen.xml` | Homesteader | Primary residence as a productive estate node |
| `eatondo-portfolio.xml` | CNO | Reference CNO portfolio implementation across 40+ enterprises |

To apply a template: open **orun** → Workspace Bootstrapper → Import Template → select the XML file → configure required fields → launch.

---

## 56. The eatondo Portfolio — Reference CNO Implementation

The `eatondo-portfolio.xml` is the reference implementation of a full CNO portfolio, owned by Dominic Eaton (@eatondo) — the creator of ogun OS. It demonstrates the complete personal enterprise model across multiple enterprise types and sub-enterprises.

**Portfolio structure:**

| ID | Enterprise | Type |
|---|---|---|
| 000 | eatondo-root-portfolio | ROOT — meta portfolio |
| 001 | mungu-project-enterprise | Investment / Meta-Governance |
| 002 | ogun-project-enterprise | Holding / Platform Products |
| 002.1 | ogun-enterprise | Portfolio Operations |
| 002.2–002.10 | enzo, qala, kogi, shango, zamani, ume, apapo, zuri, ayo | Platform Products |
| 003 | eaton-estate-enterprise | Personal Office / Estate |
| 003.1.1–003.1.4 | Written works, Musical works, Art works, Games | Creator enterprises |
| 003.2 | de-software-solutions-enterprise | Builder / Consulting |
| 003.3 | de-assets-enterprise | Investment |
| 003.4 | eaton-family-office-enterprise | Estate / Family Office |
| 004 | obatala-studios-enterprise | Venture Studio / VC |
| 004.1–004.12 | Multiple ventures | Various (engineering, research, mobility, etc.) |

Primary persona: CNO. Secondary: Creator, Builder, Investor, Founder. Canonical equation: `Π* = argmax Σᵢ wᵢ V(ℙᵢ) + V_cross(Π) − C_coord(Π)`.

---

# Part VII — Core Platform Workflows

---

## 57. Workflow: Setting Up a New Enterprise from Scratch

This workflow covers creating an enterprise from zero to its first Shock Insight.

**Duration:** 30–60 minutes for setup; Shock Insight delivered within 30 minutes of first data connection.

**Steps:**

1. **Create the enterprise record** — Open enzo → New Enterprise. Select your enterprise type and a matching Hypergrid template. Fill in identity: canonical name, primary domain, mission statement.

2. **Complete the MVE Checklist** — Confirm all four MVE conditions before proceeding:
   - Production: define at least one offer (name, pricing model, base price, value proposition)
   - Allocation: set your GoalWeightVector (weights for income, asset growth, passive income, network) — must sum to 1.0
   - Exchange: create at least one active wallet in dongo
   - Feedback: create at least one KPI definition or dashboard tile in qala

3. **Set up your first offer** — Open kogi → Offers → New Offer. Use the three-tier model:
   - Entry tier (10–20% of core price — barrier reduction)
   - Core tier (market rate — primary revenue engine)
   - Premium tier (2–5× core price — maximum access)

4. **Configure your pipeline** — Open kogi → Pipelines → New Pipeline. Select the pipeline type for your enterprise (Acquisition, Delivery, Content, Build, Investment, Deal).

5. **Connect your first data source** — Settings Center → Integrations. Connect at minimum one calendar source and one financial account or invoicing system.

6. **Wait for Shock Insight** — The Observatory will process your connected history and deliver the Shock Insight at the Cold → Activated lifecycle transition. This appears in enzo's intelligence feed and the Command Center Observatory panel.

7. **Set your first policies** — In enzo → Policies, enable the starter policy set for your enterprise type. At minimum: EHR Floor and Pipeline Health Floor.

---

## 58. Workflow: Running Your Daily Production Loop

The Production Loop is the heartbeat of every enterprise. Here is a practical daily workflow:

**Morning (15–20 minutes):**

1. Check the **Utility Bar** strips — today's schedule, priority tasks, unread notifications, and OBA's morning briefing
2. Open **kogi** → Desk → Today's View — see all active engagements, today's commitments, and Commitment Tension τ
3. Review **ogun-tasks** priority list for the day — anything due today or at risk?
4. Check **dongo** for any outstanding invoices or flagged transactions
5. Review any new **Observatory insights** in enzo or the Command Center

**During the day:**

1. All work happens inside the relevant workspace — the right enterprise, client, or project workspace keeps everything contextualized
2. Use **ogun-focus** to protect deep work blocks — set a focus session, which suppresses non-critical notifications and tracks your time
3. When moving an engagement to a new stage (Proposed, Contracted, InProgress, etc.) — update it in kogi → Desk
4. Capture notes in **ogun-notes** with the Utility Bar quick-capture button (attributed to the active enterprise automatically)
5. When an agent takes an action or surfaces a recommendation — review it in the Agents Panel

**End of day (10 minutes):**

1. Update task completion in **ogun-tasks**
2. Close any focus sessions in **ogun-focus**
3. Review any new **insights or alerts** in qala
4. Check **dongo** for any invoices to send for work delivered today
5. Write any important decisions to **akeel** Decision Log

---

## 59. Workflow: Managing a Client Engagement

This covers the full lifecycle of a client engagement from lead to payment.

**Lead arrives:**

1. Create a new Contact in **ogun-contacts** for the prospect
2. Create a new Engagement in **kogi** → Pipeline → Lead
3. Fill in: estimated value, initial win probability, contact link, engagement type

**Discovery and qualification:**

1. Move engagement to `Qualifying` stage in kogi
2. Create a moto project brief if the scope warrants full project management
3. Research the prospect using **ogun-search** across your namespace

**Proposal:**

1. Move engagement to `Proposed` in kogi — this updates EPV calculation
2. Generate the proposal document using **akeel** (or your preferred tool) with enterprise context
3. Record the proposal value and win probability in the engagement record
4. **Important:** the Contract-Before-Work policy (opn-003 enforcement) means you cannot move to `Contracted` without an executed contract in ume

**Contract and kick-off:**

1. Create and execute the contract in **ume** → Contracts
2. Link the contract to the engagement in kogi
3. Move engagement to `Contracted` (now unlocked)
4. Create the project in **moto** if not already done, linked to this engagement
5. Create a dedicated workspace in **ogun-workspaces** for this client if they are significant enough to warrant one

**Execution:**

1. Work happens in the moto project — tasks, work packages, milestones
2. Track time against the engagement for EHR computation
3. Any scope change: use moto → Scope Management → Change Request

**Delivery and payment:**

1. Move engagement to `Delivered` in kogi
2. Generate invoice in **dongo** and send
3. Move to `Accepted` when client confirms
4. Move to `Paid` when payment clears — dongo records the transaction automatically
5. Create an Artifact record in **igi** for the deliverable — this attributes revenue to the specific work

**Post-engagement:**

1. Write a case study or retrospective in **akeel**
2. Tag the engagement in **orun** for searchability
3. Archive the workspace if it was client-specific
4. Review if the engagement type triggers a Scaffold Detection signal (4+ similar deliveries → productization recommendation)

---

## 60. Workflow: Productizing a Repeating Service

The Scaffold Detection system identifies when you've delivered the same type of work four or more times in 180 days. When triggered, qala surfaces a `ProductizationSignal` insight.

**When the signal fires:**

1. Review the insight in qala / Command Center Observatory panel
2. The insight includes: pattern name, average delivery hours, average delivery value, computed EHR, estimated build hours (1.5× avg delivery), expected monthly revenue, payback period, recommended price, and recommended format

**To act on it:**

1. Open **shango** → New Factory → select "Product" or "Template" type
2. Pre-populate with artifacts from the identified engagements (shango can import from your artifact registry via igi)
3. Build the productized version — define it as a self-contained deliverable
4. Set up QA gates appropriate for the format
5. Price using shango's pricing suggestion (average delivery value × 0.6 is the default starting point)
6. Create a listing in **zuri** for distribution
7. Optionally create an ayo space page for discoverability

**Revenue attribution:** once the first sale occurs, dongo records it and igi creates a `DigitalProduct` portfolio item, automatically starting EVS computation.

---

## 61. Workflow: Deploying and Managing Agents (Sambara)

**Creating a new agent:**

1. Open **sambara** → Agents → New Agent
2. Define: agent name, purpose, persona, capabilities, and constraints
3. Select or write a system prompt
4. Set initial authority level (start at `OBSERVE` for new agents — always)
5. Configure the LLM driver (select your preferred model)
6. Define action bounds (what parameters the agent is allowed to touch)
7. Link the agent to relevant enterprise, workspace, or data scope

**Agent lifecycle progression:**

```
Draft → Testing → Deployed → Paused → Retired
```

During `Testing`: run the agent on historical scenarios before giving it access to live data. Review all proposed actions in the recommendation log.

**Authority escalation protocol:**

Agents start at `OBSERVE`. Escalation to `RECOMMEND` requires: completing the testing phase, zero critical policy violations. Escalation to `EXECUTE_BOUNDED` requires: operator explicitly granting it in the Security Center, with a defined action parameter set. Escalation to `FULL_AUTONOMY` requires: `OPTIMIZED` enterprise lifecycle stage (180+ metric snapshots, avg policy effectiveness > 75%), plus explicit operator grant.

**Monitoring agents in production:**

1. Review the Agent activity log in sambara → Monitoring
2. Check all bounded actions in the Security Center → Agent Authority Audit
3. Review performance metrics: tasks completed, success rate, error rate, cost per agent (tokens consumed)
4. Receive anomaly alerts via ogun-messenger when agent behavior deviates from baseline

---

## 62. Workflow: Multi-Enterprise Portfolio Operations

**Viewing the full portfolio:**

1. Open **enzo** → Portfolio Control Center (PCC) — headline metrics: MRR (aggregate), TPV, EPV, EHR
2. Each enterprise card shows lifecycle state, last-30-day revenue, and health signal

**Portfolio optimization:**

1. Open qala → Portfolio Analytics for the cross-enterprise view
2. Review: income stream diversification, passive income ratio by enterprise, concentration risk, allocation efficiency
3. The CNO meta-persona view shows `V_cross(Π)` — cross-enterprise synergy value (shared audience, referrals, IP reuse)
4. Use shaba → Portfolio Management → Rebalancing to record and act on rebalancing decisions

**Hub pattern for collaboration:**

1. You and another operator each need active enterprises with `hub_enabled = true`
2. Create a Hub in **kanna** → Hubs → New Hub
3. Define hub scope (specific engagement or time period)
4. Define `RevenueSplit` — percentages, linked wallet IDs for each participant
5. Hub has its own namespace — all shared work goes there; each operator's data stays in their own enterprise namespace (Ọpọn Protocol enforced)

---

## 63. Workflow: Publishing Your Identity and Portfolio (Heshima + Ayo)

1. Open **heshima** → Identities → your primary professional identity
2. Complete your skill declarations with market rate estimates
3. Add your delivery history count and review score (initially estimated; fills in from dongo/kogi data over time)
4. Enable DID (Decentralized Identity) if you want a portable, verifiable credential

**Publishing your linktree:**

1. heshima → Linktree → New Link Profile
2. Add links: portfolio, social, contact, commercial, professional
3. Enable dynamic routing if you want different links for different audiences
4. The linktree is published via your ayo Space

**Creating your public portfolio space:**

1. Open **ayo** → Spaces → New Space → type "Portfolio"
2. Theme the space with your brand colors and logo
3. Embed live metrics from qala (optional — shows aggregate numbers without exposing sensitive data)
4. Add portfolio items from **igi** as project showcases
5. Link your Zuri store for any productized services or digital products
6. Connect your Heshima linktree for the contact/social layer
7. Publish and configure your custom domain (if you have one)

---

## 64. Workflow: Financial Tracking and Reporting

**Daily financial hygiene:**

1. dongo → Dashboard — check cash position, outstanding receivables, recent transactions
2. Review any flagged transactions (the Attribution Agent flags transactions without engagement or artifact attribution)
3. Send any outstanding invoices from dongo → Invoices

**Monthly close:**

1. dongo → Accounting → Bank Reconciliation — reconcile all accounts
2. Review P&L, Balance Sheet, Cash Flow statement
3. dongo → Tax → Quarterly Estimate — review estimated tax payment (based on income to date)
4. Review income concentration: dongo → Reports → Income by Client/Source

**Annual tax preparation:**

1. dongo → Tax → Annual Summary — generates a summary of all 1099-trackable income
2. Review deduction identification suggestions
3. Export to your accountant via the dongo reports export function

---

## 65. Workflow: Setting Governance Policies

**Starter policy configuration:**

1. Open **enzo** → Policies → Enterprise Policies
2. Enable the universal starter policy set for your enterprise type:

| Policy | Threshold to set | Trigger action |
|---|---|---|
| Rate/EHR Floor | Your minimum acceptable hourly rate | Alert + block engagement entry |
| Concentration Cap | Maximum single-client revenue share (default: 40%) | Alert + diversification prompt |
| Pipeline Health Floor | Minimum EPV as multiple of monthly target (default: 1.5×) | Alert + dispatch acquisition agent |
| Commitment Tension Alert | τ > 0 for N days (default: 7) | Alert + block new commitments |

**Creating a custom policy:**

1. enzo → Policies → New Policy
2. Select domain: Allocation, Pricing, Pipeline, Financial, Risk, Governance, Agent, or Lifecycle
3. Set condition: metric name, comparison operator, threshold, sustain days (optional)
4. Set action: AlertOperator, BlockEngagementCreate, DispatchAgent, GenerateInsight, FlagForReview, or AutoExecute
5. Set requires_approval if the action is consequential
6. Save and activate

**Policy evaluation order:** System policies evaluate first (always; cannot be overridden). Then User policies, sorted by priority. Then Agent policies (always bounded by user policies).

---

## 66. Workflow: Launching a Digital Product (Shango + Zuri)

1. **Define the product** in shango → Factory → New Solution. Type: `Product`. Fill in: name, value proposition, features, pricing, target audience.

2. **Build the product** using the shango Build Pipeline. Set up dev, staging, and production environments. Use shango's Software-Defined Environment management for configuration-as-code.

3. **QA and release gating** — configure QA gates in shango → QA. Minimum: automated test pass, vulnerability attestation (if software), acceptance criteria review.

4. **Create the listing** in zuri → Products → New Product. Link to the shango solution record. Set pricing model (one-time, subscription, tiered), pricing tiers, and delivery method.

5. **Publish your store** in ayo → Spaces → Service Catalog Space. Embed the Zuri store widget. Configure custom domain if available.

6. **Set up revenue attribution** in dongo — when a sale occurs, dongo records it and the Attribution Agent links it to the Zuri product and shango solution as a portfolio item in igi.

7. **Monitor performance** in qala → Analytics → Product Performance. Track MRR, conversion rate, churn rate, revenue per user.

---

## 67. Workflow: Homesteader / Estate Tracking

Based on the Nadia Chen `zamani-estate-homesteader-nadiachen.xml` template — for operators whose home is a productive estate node.

1. **Open zamani** → Estate Setup Wizard
2. Define estate identity: address, property type (`residential-primary-with-studio-and-rental` or similar)
3. Configure estate nodes:
   - Primary residence (entire property as asset)
   - Home studio / office (income-generating space)
   - Guest room / rental space (income-generating space)
   - Vehicle (mobility asset node)
4. Define cost inputs: mortgage P&I, property tax (monthly), insurance, utilities, internet, maintenance reserve
5. Connect income sources: consulting income attributed to office space, short-term rental income from guest room
6. The Observatory computes:
   - Net estate position (total income − total operating cost)
   - Income per square foot of productive space
   - Home office yield (income / hours × active space utilization)
   - Rental occupancy rate and income per night

**The Shock Insight format for homesteaders:** Shows the net estate position — whether the home is costing money, breaking even, or generating positive returns — and which space is the highest-yield investment per square foot.

---

## 68. Workflow: Sambara Data Engineering

For operators using sambara in a data engineering capacity (`sambara-hypergrid-data-engineer.xml`).

1. **Configure data sources** — sambara → Data → Sources → Register Source. For each source (kogi enterprise events, qala build events, zamani IoT, external APIs), define: schema, ingestion type (real-time stream or batch), refresh interval, and quality expectations.

2. **Define transformation pipelines** — sambara → Transformer → New Pipeline. Map input schemas to output schemas. Configure normalization rules.

3. **Set up the feature store** — sambara → Learning → Feature Store. Define features for model training (offline) and real-time serving (online). Set feature freshness SLOs.

4. **Configure data governance** — sambara → Governance → Data Boundaries. Define which data crosses enterprise boundaries (Ọpọn Protocol enforced). Set data classification labels (public, internal, confidential, restricted).

5. **Monitor data quality** — sambara → Data → Quality Dashboard. Track freshness scores, completeness, and accuracy by source. Set alerts for pipeline staleness.

6. **Maintain data lineage** — sambara → Data → Lineage Graph. Review the lineage of any metric or feature to understand exactly which raw events contributed to it.

---

## 69. Workflow: Shango Platform Administration and Security

For operators with platform administration or security engineering responsibilities.

**Platform Admin:**

1. Monitor platform health — shango → Plant → SLO Dashboard. Check availability against targets: Gateway 99.95%, Governance engine 99.99%, Kernel 99.9%, Model serving 99.95%, Event bus 99.99%.

2. Check performance targets:
   - Agent activation latency p99: < 500ms
   - Governance check p99: < 20ms
   - Model inference p99: < 50ms
   - Feature serving p99: < 10ms

3. Manage upgrades — shango → Platform → Upgrade Pipeline. Plan, stage, and deploy package upgrades across all 14 sambara packages with rollback capability.

**Security Engineer:**

1. SAST review — shango → Security → SAST Reports. Review static analysis results for all active components. Use the SecurityAgent for automated triage and CVE prioritization.

2. Compliance posture — shango → Governance → Compliance Dashboard. Track coverage against active frameworks (OWASP Top 10 is always active; SOC 2, ISO 27001, PCI-DSS, HIPAA, GDPR configurable).

3. Release security clearance — shango → Foundry → Release Approval. Review vulnerability attestation, SBOM, and security scan results before any production release.

4. Secrets management — shango → Security → Secrets Vault. Rotate secrets on schedule. Audit secret access. Review any secrets-in-code alerts from the SecurityAgent.

---

# Part VIII — OgunNet and Networking

---

## 70. OgunNet v2.0.0 Overview

OgunNet is the P2P network layer built into ogun OS at the kernel level (Subsystem 14). It gives every ogun OS instance an encrypted, addressable node on a distributed network.

**Node Identity:**
- Every ogun OS installation generates an Ed25519 signing key (stored via the storage subsystem)
- Your NodeId is computed as: `SHA-256(verifying_key ‖ "ogunnet-node-id-v1")`
- Your node also has a human-readable alias: `adjective-noun-NNN` (e.g., `swift-harbor-042`)
- Your NodeId is stable across restarts and machine reboots

**Transport:**
- TCP with 4-byte big-endian length-prefix framing
- Maximum message size: 4 MiB per message

**Encryption:**
- X25519 ECDH key exchange with Ed25519-signed DH public keys → per-session AES-256-GCM
- All `Data`, `Chat`, `ChannelMsg`, and `FileChunk` payloads encrypted
- Each connection has its own session key

**Discovery mechanisms:**
- **Kademlia DHT** — 256-bucket XOR-metric routing table, k=20, α=3; global discovery via bootstrap nodes; 1-hour TTL for stored values
- **mDNS** — UDP multicast on `239.255.17.170:17171`; sends `LocalAnnounce` every 30 seconds; discovers peers on your local area network without any bootstrap configuration
- **PEX (Peer Exchange)** — every connected peer receives your routing table every 60 seconds; WAN-scale discovery without central servers

**Configuring OgunNet** in `ogun.toml [network]`:
```toml
port = 17170          # listening port
mdns_enabled = true   # LAN discovery
pex_enabled = true    # WAN peer exchange
max_peers = 50        # maximum simultaneous connections
```

---

## 71. Connecting to Peers

**Automatic discovery** — if mDNS is enabled, ogun OS will discover peers on your local network automatically. They appear in the Contacts app (ogun-contacts) and the Security Center → OgunNet Peers list.

**Manual connection via Shell:**
```
ns.connect <NodeId>
ns.connect swift-harbor-042
```

**Peer status:** the Footer Bar shows your current OgunNet peer count. Click it to open the OgunNet Peers panel in the Command Center.

**Rate limiting:** the network subsystem enforces a maximum of 5 new inbound connections per IP address per 60 seconds. Handshakes must complete within 10 seconds. These limits protect against connection flooding.

---

## 72. Named Channels and Group Communication

OgunNet supports IRC-style named channels for group communication.

**Creating or joining a channel via Shell:**
```
channel.join #project-alpha
channel.join #team-collab
channel.list
channel.send #project-alpha "Hello team"
```

**Channel encryption:** each named channel derives an AES-256-GCM key from the channel name. All `ChannelMsg` payloads are encrypted. Anyone who knows the channel name can join — share channel names only with intended participants.

**ogun-messenger integration** — named channels surface in the ogun-messenger app as group conversations. Messages, notifications, and file shares from named channels appear in the unified inbox.

---

## 73. File Transfer over OgunNet

File transfer uses a chunked encrypted protocol.

**From the File Explorer:**
1. Right-click any file in ogun-explorer
2. Select "Send to OgunNet Peer"
3. Select the peer from the connected peers list
4. The file is chunked into 64 KiB blocks, encrypted per-session, and transferred with SHA-256 integrity verification

**Via Shell:**
```
files.send <peer-NodeId> /path/to/file
files.receive                          # list pending incoming transfers
files.accept <transfer-id>             # accept an incoming transfer
```

**File transfer protocol stages:** `FileOffer → FileOfferReply → FileChunk × N → FileChunkAck × N → FileComplete`

Each chunk is acknowledged before the next is sent. If a chunk fails integrity verification, it is re-requested automatically.

---

## 74. Peer Reputation and Security

OgunNet maintains a per-peer reputation score (integer). Reputation is updated based on behavior (protocol compliance, message validity, etc.).

- Auto-ban threshold: score ≤ −10 (the peer is automatically banned)
- Manual ban: Security Center → OgunNet → Ban Peer
- Manual unban: Security Center → OgunNet → Unban Peer
- Peer reports propagate to other peers via a `PeerReport` gossip message

**Rate limiting protections:**
- Maximum 5 new inbound connections per IP per 60 seconds
- Handshakes must complete within 10 seconds or the connection is dropped

---

# Part IX — Security, Keys, and the Ọpọn Protocol

---

## 75. Security Architecture Overview

ogun OS implements a three-tier security architecture:

1. **Boot-time verification** — three sequential cryptographic stages verify the platform image, system manifest, and host key derivation on every boot. Any failure calls `halt()` with zero side effects.

2. **Runtime capability enforcement** — every process has a declared capability set; every system call is checked against it by Subsystem 7 (Security) before the operation completes.

3. **Cross-enterprise data isolation** — the Ọpọn Protocol enforces strict data partitioning between enterprises at the kernel Security subsystem, IPC broker, storage layer, VFS, and agent runtime.

**Security is non-negotiable** — several invariants are unconditional and cannot be disabled by any configuration, operator setting, runtime flag, or IPC message. These are marked as design invariants I-10 through I-35 in the architecture specification.

---

## 76. The Three Keys Explained

ogun OS is anchored by three cryptographic keys, each serving a distinct purpose:

**Image Key (ImageSigningKey)**
- An ed25519 keypair owned exclusively by the CI build pipeline
- Private key: stored in the CI secrets vault; never on any user machine; never in source
- Public key: embedded in every `.img` file, extracted to `~/.ogun/security/keys/image-verify.pub` (0o444)
- Purpose: proves a binary image was produced by the official build pipeline
- Changes: when a new release is issued

**System Key (SystemKey)**
- An ed25519 keypair generated by the installer exactly once on your machine
- Private key: stored in Windows DPAPI (Credential Manager); **never** in `~/.ogun/`
- Public key: `~/.ogun/security/keys/system.pub` (0o444)
- Purpose: signs the system manifest (SHA-256 hash table of all security-critical files). Bootloader Stage 2 verifies this on every boot to prove installed binaries have not been tampered with.
- Changes: only on full reinstall; persists across image updates

**Host Key (HostKey)**
- A 32-byte derived key (not a keypair) — an identity token, not a signing key
- Derived via: `HKDF-SHA256(ikm: image_pubkey ‖ system_pubkey, salt: install_id, info: "ogun-host-key-v1", len: 32)`
- Stored at: `~/.ogun/security/keys/host.key` (0o400)
- Purpose: unique fingerprint for this specific image running on this specific installation. Stamped on every telemetry event, audit log entry, IPC message, and capability grant. Verified by Stage 3 of the bootloader on every boot.
- Changes: when the image is updated (new image_pubkey changes the derivation input)

---

## 77. The Ọpọn Protocol — Cross-Enterprise Isolation

Named after the Ọpọn Ifá — the Yoruba divination tray upon which no reading for one supplicant may be contaminated by the marks of another — the Ọpọn Protocol is the cross-enterprise data isolation system.

**Core invariant:** data belonging to Enterprise A cannot be read or written in the context of Enterprise B without explicit, logged, operator-approved consent. This applies even when both enterprises are owned by the same operator.

**`opn_enforced = true` is unconditional.** No configuration setting, app, or IPC message can disable it. The setting is reset to `true` after every load of `ogun.toml`.

**Five immutable rules:**

| Rule | What it enforces |
|---|---|
| `opn-001` | Enterprise namespace isolation — processes with `enterprise_id = A` cannot access `enterprise_id = B` namespaces without an explicit cross-enterprise grant |
| `opn-002` | Agent authority bounds — agents cannot execute actions outside their declared authority level without operator approval |
| `opn-003` | Contract-before-active — enterprise workflows in active/billable states require an associated contract record in ume |
| `opn-004` | Revenue attribution integrity — every revenue event must carry a valid `attribution_id` traceable to an operator-verified source |
| `opn-005` | Extension approval gate — extensions require `operator_approved_at` in their manifest before `dlopen` is called |

**What is and is not permitted:**

| Operation | Status |
|---|---|
| Raw client record from Enterprise A accessed in Enterprise B | **BLOCKED** |
| Financial transaction from Enterprise A referenced in Enterprise B | **BLOCKED** |
| Agent acting on Enterprise A data from Enterprise B context | **BLOCKED** |
| Aggregate portfolio metric (e.g., "portfolio average EHR") | **PERMITTED** — aggregate, not raw |
| Hub-pattern shared execution context | **PERMITTED** — Hub has its own namespace; each enterprise's data stays isolated |
| Operator explicitly consenting to cross-enterprise reference | **PERMITTED** — with logged consent record; scoped and time-bounded |

---

## 78. Capability System for Users

Every application in ogun OS declares a capability set in its `ogun-component.toml` manifest. The Security subsystem checks these at every system call boundary.

**Capability classes:**

| Class | Controls |
|---|---|
| `filesystem.*` | Read, write, create, delete per namespace prefix |
| `network.*` | Outbound/inbound connections |
| `ipc.*` | IPC channels the app can publish to or subscribe to |
| `financial.*` | Read and write access to dongo wallets and transactions |
| `agent.*` | Agent registration and execution authority |
| `runtime.*` | Process spawning and module loading authority |

**As a user, you can:**
- Review all active capability grants in Security Center → Active Grants
- Revoke any grant instantly — the revocation is logged to the audit trail before it takes effect
- Review per-app capability declarations in App Manager → select app → Capabilities tab
- Configure the operator-level capability ceiling via `capability-defaults.json` (read-only after install; contact system administrator to modify)

---

## 79. Authentication Methods by Platform

| Platform | Primary Method | Secondary Method |
|---|---|---|
| Desktop (0.1.0-beta) | Passkey (FIDO2) | TOTP/2FA |
| Web (planned) | WebAuthn (`navigator.credentials`) | — |
| Mobile iOS (planned) | FaceID / TouchID | PIN |
| Mobile Android (planned) | Fingerprint | PIN |
| Device (planned) | Hardware (NFC / PIN pad / certificate) | Device-specific |
| Server (planned) | Skipped | Skipped |

**Setting up passkey on Desktop:**
1. Profile Center → Security → Authentication → Register Passkey
2. Follow the FIDO2 flow (Windows Hello, security key, or platform authenticator)
3. Optionally enroll a TOTP authenticator app as backup
4. Generate recovery codes and store them securely (not in ogun OS itself)

**Lockout policy** — configurable in `ogun.toml [session]`:
- `lockout_threshold` — consecutive failures before lockout (default: 5)
- `lockout_duration_ms` — lockout duration (default: 300,000ms / 5 minutes)

---

## 80. Audit Log and Security Center

Every security-relevant event is written to `~/.ogun/security/audit.log` (AES-256-GCM encrypted) **before** the operation completes. If the log write fails, the operation is aborted. This is unconditional.

**Events logged:**
- Every capability grant or denial
- Every Ọpọn Protocol enforcement event (blocked access attempts)
- Every cross-enterprise access attempt (permitted or blocked)
- Every agent action
- Every extension `dlopen` attempt (with approval status)
- Every host key derivation at boot

**Viewing the audit log:**
1. Security Center → Audit Log
2. Filter by date, event type, enterprise, or agent
3. Export to CSV or JSON for external review

The audit log is encrypted at rest and requires authentication to view. The log entries are append-only and include the `host_key` stamp for tamper detection.

---

# Part X — Configuration and Administration

---

## 81. Configuration Files Overview

All configuration files live under `~/.ogun/config/`:

| File | Purpose | When loaded |
|---|---|---|
| `ogun.toml` | Primary runtime configuration | Every boot, by the bootloader |
| `display.toml` | Display and theming | At subsystem 11 initialization |
| `emulation.toml` | Virtual device configuration | At subsystem 15 initialization |
| `uefi.toml` | Virtual UEFI firmware settings | At UEFI Pre-Init phase |

**Security policy files** (read-only after install):
- `~/.ogun/security/opn-policy.json` — Ọpọn Protocol rules (0o444; never modified after install)
- `~/.ogun/security/capability-defaults.json` — capability tier ceilings (0o444)

**Editing configuration:** You can edit TOML files with any text editor while ogun OS is not running. The Settings Center GUI provides a safe editing surface for all user-accessible settings. Settings that would be unsafe to change via the GUI (kernel internals, security policies) require direct file editing.

---

## 82. ogun.toml Reference

```toml
[kernel]
abi_version               = 1
validate_image_signature  = true     # ALWAYS true in production; cannot be set false
max_restart_attempts      = 3        # max host instance restart attempts on crash

[kernel.cpu]
tick_rate_hz              = 100      # base tick rate (Hz); 1 tick = 10ms at 100Hz
min_worker_threads        = 1        # pool never shrinks below this
max_worker_threads        = 0        # 0 = auto (num_cpus - 1)
scale_up_queue_depth      = 8        # pending ticks that trigger scale-up
scale_up_utilization_pct  = 0.80     # utilization fraction that triggers scale-up
scale_down_utilization_pct= 0.30     # utilization fraction threshold for scale-down
scale_down_cooldown_ms    = 5000     # duration below threshold before worker removed
starvation_threshold      = 200      # ticks skipped before starvation promotion to P0
timeslice_ns              = 10000000 # nominal time budget per component per tick (10ms)

[network]
port                      = 17170    # OgunNet listening port
mdns_enabled              = true     # LAN peer discovery
pex_enabled               = true     # WAN peer exchange
max_peers                 = 50       # maximum simultaneous peer connections
advertise_address         = ""       # optional: public IP/hostname for WAN bootstrap

[session]
snapshot_interval_ms      = 60000    # session snapshot interval (60s default)
lockout_threshold         = 5        # consecutive auth failures before lockout
lockout_duration_ms       = 300000   # lockout duration (5 minutes default)
auto_lock_timeout_ms      = 0        # 0 = never auto-lock; set to lock on idle

[storage]
database_path             = "~/.ogun/data/rustydb"
wal_enabled               = true

[telemetry]
log_level                 = "Info"   # Trace | Debug | Info | Warn | Error | Fatal
log_sinks                 = ["file"] # file | memory | ipc
buffer_size               = 1024

[security]
opn_enforced              = true     # ALWAYS reset to true; cannot be disabled
audit_log_encrypted       = true     # AES-256-GCM encryption on audit.log
audit_log_path            = "~/.ogun/security/audit.log"
opn_policy_path           = "~/.ogun/security/opn-policy.json"
```

---

## 83. display.toml Reference

```toml
[theme]
active_theme     = "default"  # theme name
color_scheme     = "dark"     # dark | light | system
accent_color     = "#7C3AED"  # royal purple default

[window]
default_width    = 1440
default_height   = 900
scaling_factor   = 1.0        # display scaling; 2.0 for HiDPI
animations_enabled = true

[fonts]
primary_font     = "Inter"          # system sans-serif fallback if unavailable
monospace_font   = "JetBrains Mono" # monospace fallback available
lock_screen_font = "Cinzel"         # display typeface for lock screen
base_font_size   = 14               # base size in points

[surfaces]
refresh_rate     = 60               # target refresh rate (Hz)
vsync_enabled    = true
```

---

## 84. emulation.toml Reference

```toml
[virtual_monitor]
resolution       = [1920, 1080]
scale_factor     = 1.0
refresh_rate     = 60

[virtual_network]
identity_persistence_key = "ogunnet.identity.signing_key"
connection_rate_limit    = 5    # max new inbound connections per IP per 60s
handshake_timeout_ms     = 10000 # 10 seconds

[virtual_host]
max_nesting_depth = 10           # maximum virtual host nesting depth; 0 treated as 1
default_host_type = "Desktop"    # default HostType for auto-provisioned virtual hosts

[devices.auto_provision]
# Array of virtual device definitions to initialize at boot
# Example:
# [[devices.auto_provision]]
# kind = "monitor"
# id   = "default-monitor"
```

---

## 85. uefi.toml Reference

```toml
[boot]
boot_menu_timeout_ms = 3000  # interrupt window duration (1000–10000ms; 0 = 3000ms)
uefi_boot_log_path   = "~/.ogun/logs/uefi-boot.log"

[secure_boot]
policy               = "require_platform"  # only ImageKind::Platform images bootable
```

---

## 86. Namespace Reference

The 12 canonical VFS namespaces and their typical contents:

| Namespace | Typical contents | Access |
|---|---|---|
| `ogun://` | System-wide ogun OS resources, configuration references | Read; kernel write |
| `system://` | Runtime state: `system://host/phase.json`, `system://boot/config.json` | Read; kernel write |
| `user://` | Operator-owned personal files and data | Read-write (operator) |
| `security://` | Keys (`security://keys/`), audit logs (read-only view), policies | Read-only (apps); kernel read-write |
| `app://` | Per-application data namespaces | App-scoped read-write |
| `data://` | General structured data storage | Read-write per capability |
| `network://` | OgunNet peer registry, channel registrations | Network subsystem |
| `agent://` | Agent state files, execution logs, memory stores | Agent-scoped; operator read |
| `enterprise://` | Enterprise-scoped resources — primary working namespace | Enterprise-scoped read-write |
| `workspace://` | Workspace layout states, running app records | Session manager; operator read |
| `session://` | Current and historical session records, snapshots | Session manager; operator read |
| `telemetry://` | Live and archived telemetry streams | Qala; read-only for most apps |

**Virtual device paths** (Subsystem 15):
- `device://vdev/monitor/<id>` — virtual display monitors
- `device://vdev/network/<id>` — virtual network adapters
- `device://vdev/host/<id>` — virtual host instances

---

## 87. Virtual UEFI Boot Menu

The UEFI boot menu is accessible during the boot interrupt window (default: 3 seconds, configurable 1–10 seconds in `uefi.toml`). Interrupt by pressing any key during the splash screen.

**Boot menu options:**
- Boot settings (boot order, image path)
- Secure Boot policy settings (configurable only between boot cycles)
- Emulation settings (virtual monitor resolution, network adapter configuration)
- Diagnostics (verify current image signature, display host key fingerprint, show installation identity)
- Advanced settings (UEFI variable store inspection)

**UEFI invariants you cannot change:**
- `set_variable` is locked unconditionally after `ExitBootServices()` — UEFI variables are immutable for the duration of every boot
- Boot does not halt on a missing or corrupt variable store (a fresh default is written; you are notified)
- Boot **does** halt on a Secure Boot policy violation
- Every phase transition and every error is written to `~/.ogun/logs/uefi-boot.log`

---

## 88. Session Management and Recovery

**Session snapshot** — ogun OS periodically writes a `SessionSnapshotState` record (default: every 60 seconds). The snapshot contains: `ActiveSessionContext`, workspace session records (running apps, window layouts, active tabs), and operator preferences. Snapshots are stored at `~/.ogun/snapshots/<timestamp>.snap` as MessagePack-serialized, zstd-compressed files.

**Clean shutdown** — the last act of every clean shutdown is writing the `CleanShutdownMarker`. This is unconditional and absolute.

**Crash recovery** — if ogun OS starts and the `CleanShutdownMarker` is absent (indicating the previous session did not shut down cleanly), crash recovery mode activates automatically:
1. The most recent valid snapshot is loaded
2. Workspace layouts and running app states are restored from the snapshot
3. A crash report is generated and queued to `ogun-system-manager`
4. The crash report is presented in the system dashboard after the desktop is live

**Managing snapshots manually:**
```
sys.snapshots.list              # list all snapshots with timestamps
sys.snapshots.restore <id>      # restore to a specific snapshot
sys.snapshots.clean             # remove all but the N most recent (default: 10)
```

**Session persistence triggers:**
1. Snapshot interval elapsed (configurable in `ogun.toml [session]`)
2. Clean shutdown initiated
3. Workspace or profile switch (saves previous workspace/profile record)

---

## 89. Updating ogun OS

Updates are managed by `ogun-desktop.exe` (the user-facing launcher) and `ogun-system-manager`.

**When an update is available:**
1. `ogun-system-manager` detects the new image file (via network or manual download)
2. The new `.img` file's signature is verified before any extraction
3. The update is staged — prepared without replacing the running installation
4. You are notified via the system tray and ogun-messenger
5. The update is applied on the next boot (not while running)

**Manual update via Shell:**
```
sys.update.check                # check for available updates
sys.update.download             # download pending update
sys.update.apply                # stage the update for next boot
sys.update.status               # show current update state
```

**What happens during update application (at next boot):**
1. The new image signature is re-verified
2. New binaries are extracted to `~/.ogun/`
3. The system manifest is recomputed and re-signed with the existing SystemKey
4. The HostKey is re-derived (image key changes → HostKey changes)
5. Configuration migrations are applied if required

**Rolling back** — if the updated version fails to boot, the host service's crash recovery will attempt to start with the previous configuration. Manual rollback:
```
ogun-setup.exe --rollback
```

---

## 90. Uninstalling ogun OS

To completely remove ogun OS from your Windows machine:

1. Run `ogun-setup-windows-0.1.0-beta.exe --uninstall`
2. The uninstaller will:
   - Stop and remove the autostart Task Scheduler entry
   - Offer to delete `~/.ogun/` (user data) — you can decline to keep your data
   - Remove the ogun binaries from the installation directory
3. The SystemKey private half in Windows DPAPI is automatically removed when `~/.ogun/` is deleted

If you want to preserve your data for a future reinstallation: choose "Keep user data" during uninstallation. Your enterprises, financial records, notes, and all application data remain at `~/.ogun/` and will be picked up on reinstall.

---

# Part XI — SDK and Developer Notes

---

## 91. SDK Surface Overview

ogun OS provides six SDK crates for third-party developers:

| Crate | Who uses it | What it provides |
|---|---|---|
| `ogun-types` | Everyone | Zero-dependency foundational types, `OGUN_ABI_VERSION`, binary format constants |
| `ogun-app-sdk` | App developers (Tier 1–4) | `OgunApp` trait, `AppMetadata`, capability declaration types, `OGUN_ABI_VERSION` re-export |
| `ogun-service-sdk` | Service developers | `OgunService` trait for OS-tier services |
| `ogun-kernel-sdk` | Module authors | `OgunModule` trait, `ModuleContext`, capability-gated subsystem handle access |
| `ogun-driver-sdk` | Driver authors | `OgunHostDriver`, `OgunDisplayDriver`, `OgunVirtualDriver` traits |
| `ogun-host-sdk` | Host type implementors | `OgunHost` trait, `HostType`, `HostStatus`, `HostResult`, `CrashReport` |

**ABI Version** — `OGUN_ABI_VERSION: u32 = 1` (in 0.1.0-beta) is the single source of truth. Every app, module, plugin, extension, driver, and host type declares its ABI version. Any mismatch at a load boundary causes the component to be rejected with a logged error. This is unconditional.

---

## 92. Building Your First App

1. Create a new Rust crate:
```bash
cargo new --lib my-ogun-app
cd my-ogun-app
```

2. Add to `Cargo.toml`:
```toml
[lib]
crate-type = ["cdylib", "rlib"]  # cdylib for runtime loading, rlib for testing

[dependencies]
ogun-app-sdk = { path = "/path/to/ogun-sdk/ogun-app-sdk" }
```

3. Create your app struct and implement `OgunApp`:
```rust
use ogun_app_sdk::{OgunApp, AppContext, AppMetadata, ogun_app};

pub struct MyApp {
    tick_count: u64,
}

impl OgunApp for MyApp {
    fn on_init(&mut self, _ctx: AppContext) -> AppResult<()> {
        // Initialize state; no side effects
        Ok(())
    }
    
    fn on_configure(&mut self, _ctx: AppContext, _config: AppConfig) -> AppResult<()> {
        // Apply configuration
        Ok(())
    }
    
    fn on_start(&mut self, _ctx: AppContext) -> AppResult<()> {
        // Open connections, register IPC channels
        Ok(())
    }
    
    fn on_tick(&mut self, ctx: AppContext, _dt: Duration) -> AppResult<TickOutcome> {
        self.tick_count += 1;
        // Process inbox messages
        for msg in ctx.drain_inbox() {
            // handle message
        }
        Ok(TickOutcome::Continue)
    }
    
    fn on_shutdown(&mut self, _ctx: AppContext) -> AppResult<()> {
        // Flush state, close connections
        Ok(())
    }
    
    fn app_name(&self) -> &'static str { "my-app" }
    
    fn metadata(&self) -> AppMetadata {
        AppMetadata {
            app_id: "my-app",
            display_name: "My Application",
            version: "0.1.0",
            requested_caps: &["filesystem.enterprise://read"],
            description: "My first ogun OS app",
        }
    }
}

// Export the factory function
ogun_app!(MyApp);
```

4. Create `ogun-component.toml` in your crate root:
```toml
[component]
kind = "app"
id   = "my-app"
name = "My Application"
version = "0.1.0"

[app]
entry = "my_ogun_app"  # matches your crate name

[app.capabilities]
filesystem = ["enterprise://read"]
```

5. Build and install:
```bash
cargo build --release
opm pack --manifest ogun-component.toml --lib target/release/libmy_ogun_app.so
opm install my-app.opkg
```

---

## 93. The OgunApp Trait

The full `OgunApp` trait interface (0.1.0-beta):

```rust
pub trait OgunApp: Send + Sync {
    fn on_init(&mut self, ctx: AppContext) -> AppResult<()>;
    fn on_configure(&mut self, ctx: AppContext, config: AppConfig) -> AppResult<()>;
    fn on_start(&mut self, ctx: AppContext) -> AppResult<()>;
    fn on_tick(&mut self, ctx: AppContext, dt: Duration) -> AppResult<TickOutcome>;
    fn on_message(&mut self, ctx: AppContext, msg: Message) -> AppResult<()>;
    fn on_pause(&mut self, ctx: AppContext) -> AppResult<()>;
    fn on_freeze(&mut self, ctx: AppContext) -> AppResult<()>;
    fn on_reset(&mut self, ctx: AppContext) -> AppResult<()>;
    fn on_shutdown(&mut self, ctx: AppContext) -> AppResult<()>;
    fn app_name(&self) -> &'static str;
    fn metadata(&self) -> AppMetadata;
}
```

**Lifecycle contract:**
- `on_init` — called once at load; allocate state; **no external calls or side effects**
- `on_configure` — receive configuration; reads `config://` namespace; **no I/O side effects**
- `on_start` — heavy initialization: open handles, register IPC channels, subscribe to events
- `on_tick` — called every CPU cycle at the component's declared tick rate; must complete within the timeslice (10ms at 100Hz base)
- `on_message` — called for each message in inbox; drain inbox in `on_tick` for better throughput
- `on_pause` — suspend active behavior; preserve all state in memory; tick calls cease
- `on_freeze` — serialize full state via `on_snapshot()`; release expensive resources (connections, large memory buffers)
- `on_reset` — tear down and re-run `init → configure → start`; used for crash recovery
- `on_shutdown` — flush state, close connections, release all resources; removed from registry

**The `AppContext`** injected into every call carries: `operator_id`, `enterprise_id`, `workspace_id`, `session_id`, `host_key`, `trace_id`, a `KernelHandle` for system calls, and methods `drain_inbox()` and `send_message(target_pid, msg)`.

---

## 94. Writing a Kernel Module

Kernel modules are `cdylib` crates dynamically loaded by the Kernel Modules Manager at boot. They have access to kernel subsystem handles via `ModuleContext`.

```rust
use ogun_kernel_sdk::{OgunModule, ModuleContext, ogun_export_module};

pub struct MyModule;

impl OgunModule for MyModule {
    fn module_name(&self) -> &'static str { "my-module" }
    fn abi_version(&self) -> u32 { ogun_kernel_sdk::OGUN_ABI_VERSION }
    
    fn on_load(&mut self, ctx: &ModuleContext) -> Result<(), String> {
        // ctx.ipc() — access IPC subsystem
        // ctx.vfs() — access VFS subsystem
        // ctx.telemetry() — access telemetry subsystem
        Ok(())
    }
    
    fn on_tick(&mut self, ctx: &ModuleContext) {
        // Called every CPU tick
    }
    
    fn on_unload(&mut self, ctx: &ModuleContext) {
        // Cleanup
    }
}

ogun_export_module!(MyModule);
```

Modules are installed to `~/.ogun/modules/` and configured in `ogun.toml [kernel] auto_load` to load at boot.

---

## 95. Writing a Shell Package

Shell packages add commands to the `ogun-shell` REPL. They are the lightest-weight extensibility mechanism.

```rust
use ogun_pkg_sdk::{OgunPackage, CommandContext, CommandResult, ogun_export_package};

pub struct MyPackage {
    state: MyState,
}

impl OgunPackage for MyPackage {
    fn package_id(&self) -> &'static str { "my-pkg" }
    
    fn commands(&self) -> Vec<&'static str> {
        vec!["hello", "status", "run"]
    }
    
    fn execute(&mut self, cmd: &str, args: &[&str], ctx: &CommandContext) -> CommandResult {
        match cmd {
            "hello" => CommandResult::output("Hello from my-pkg!"),
            "status" => CommandResult::output(format!("State: {:?}", self.state)),
            _ => CommandResult::unknown_command(cmd),
        }
    }
}

ogun_export_package!(MyPackage);
```

Shell commands follow the `<package-id>.<verb>` format: `my-pkg.hello`, `my-pkg.status`, `my-pkg.run`.

Build and install:
```bash
opm-build pack
opm install my-pkg.ogun
```

---

## 96. Writing a Plugin or Extension

**Plugin** — adds a new feature without modifying existing OS behavior:

```rust
impl OgunPlugin for MyPlugin {
    fn hooks(&self) -> Vec<PluginHook> {
        vec![PluginHook::WorkspaceOnSwitch, PluginHook::FsOnWrite]
    }
    fn on_hook(&mut self, hook: &PluginHook, ctx: &PluginContext) { ... }
}
```

**Extension** — modifies or replaces existing OS behavior. Extensions require explicit operator approval before loading (`opn-005`). The manifest must include `requires_approval = true`.

```rust
impl OgunExtension for MyExtension {
    fn modifies(&self) -> Vec<CoreBehavior> {
        vec![CoreBehavior::Compositor]
    }
    fn on_install(&mut self, ctx: &ExtensionContext) { ... }
    fn on_shutdown(&mut self) {
        // MUST restore all modified defaults
    }
}
```

Extensions must restore all modified defaults in `on_shutdown()` — this is enforced by the trait contract.

---

## 97. The .opkg Package Format and opm

All components are distributed as `.opkg` files — zstd-compressed archives:

```
my-package.opkg
├── ogun-component.toml     # signed package manifest
├── lib/
│   └── libmy_package.dll   # compiled shared library
└── assets/                 # optional: icons, docs, static files
```

**Build workflow:**
```bash
opm-build new <package-name>   # scaffold a new package
opm-build check                # lint and validate
opm-build pack                 # build and bundle into .opkg
opm install my-package.opkg    # install locally
```

**opm commands:**

| Command | Action |
|---|---|
| `opm install <path-or-name>` | Install a `.opkg` package |
| `opm remove <package-id>` | Uninstall a package |
| `opm list` | List all installed packages |
| `opm update [package-id]` | Update one or all packages |
| `opm info <package-id>` | Show package metadata and capabilities |
| `opm search <query>` | Search the package store |

**Installation paths:**
- Shell packages: `~/.ogun/packages/<package-id>/`
- Kernel modules: `~/.ogun/modules/`
- OS plugins: `~/.ogun/plugins/`
- OS extensions: `~/.ogun/extensions/`

---

## 98. App Manifest Reference (ogun-component.toml)

```toml
[component]
kind = "app"              # app | module | plugin | extension | driver
id   = "my-app"
name = "My Application"
version = "0.1.0"
tier = 4                  # 1 | 2 | 3 | 4 (apps only)
description = "Description of what this app does."
author = "Your Name"

[app]
entry = "my_app"          # Rust crate name (used to locate the compiled library)
icon  = "assets/icon.png"
auto_start = false        # launch automatically when ogun OS starts

[app.capabilities]
filesystem  = ["enterprise://read", "enterprise://write"]
network     = ["outbound"]
ipc         = ["my-app.*", "enzo.*"]
financial   = []          # empty = no financial access
agent       = []
runtime     = []

# For extensions only:
# [extension]
# requires_approval = true
# restore_on_shutdown = true
# modifies = ["compositor", "theme_engine"]
```

---

## 99. Development Quick Start

Clone the umbrella workspace:
```powershell
cd C:\dev
git clone https://gitlab.com/ogun-foundation/ogun.git ogun
cd C:\dev\ogun
```

Run focused Rust checks from the workspace you are changing:
```powershell
cd C:\dev\ogun\ogun-runtime
cargo check --workspace

cd C:\dev\ogun\ogun-sdk
cargo check --workspace

cd C:\dev\ogun\ogun-devices
cargo check --workspace

cd C:\dev\ogun\ogun-apps
cargo check --workspace
```

Run a Tauri tool in development mode:
```powershell
cd C:\dev\ogun\ogun-tools\src\ogun-image-tool
npm install
npm run tauri dev
```

**Before submitting a merge request:**
- All workspaces relevant to your change must pass `cargo check --workspace`
- All workspaces must pass `cargo fmt --all`
- The beta CI gate requires clean passes on all workspaces

**Repository layout:**

| Path | Purpose |
|---|---|
| `ogun-os/` | Main OS workspace, clients, host server scaffold, and beta tracking |
| `ogun-runtime/` | Runtime crates — types, image format, bootloader, kernel, session manager |
| `ogun-devices/` | Emulator, virtual UEFI, virtual CPU, display, host platform, network adapter |
| `ogun-components/` | Tier-2 and Tier-3 apps, hosts, drivers, services |
| `ogun-apps/` | Tier-4 personal enterprise application suite |
| `ogun-sdk/` | Public SDK traits, ABI constants, component contracts |
| `ogun-tools/` | Setup and image tooling |
| `ogun-config/` | Seed configuration templates |
| `ogun-artifacts/` | Staging area for built images, installers, checksums |
| `ogun-docs/` | Canonical product, architecture, and release documents |
| `elegua/` | Elegua Protocol typed IPC library |
| `rustydb/` | Embedded database backend |

---

# Part XII — System Architecture Reference

---

## 100. Runtime Architecture and Boot Chain

The full runtime hierarchy:

```
ogun-desktop.exe            ← user-facing launcher; registered autostart entry
  └── ogun-emulator         ← MAIN ENTRY POINT (Tauri 2.0+ application)
        ├── ogun-virtual-display-monitor   (Tauri WebviewWindow surface)
        ├── ogun-virtual-platform-host     (filesystem, entropy, timers, process)
        ├── ogun-virtual-cpu               (software-defined execution scheduler)
        ├── ogun-virtual-network-adapter   (software-emulated NIC; NodeId via ed25519)
        ├── ogun-uefi              (virtual UEFI: splash → boot menu → ExitBootServices)
        └── ogun-host-service      (persistent daemon; supervises host instances)
              ├── ogun-bootloader    (three-stage boot verification; KernelBootBundle)
              ├── ogun-kernel-core   (15 subsystems in canonical order; supervisor loop)
              ├── ogun-session-manager (auth; session context; workspace lifecycle)
              ├── Tier-1 kernel services (modules-manager, process-manager, ipc-broker)
              ├── Tier-2 OS apps         (desktop, shell, command-center, explorer, ...)
              ├── Tier-3 utility apps    (notes, tasks, focus, assistant, ...)
              └── Tier-4 user apps       (enzo, kogi, dongo, ume, shango, ...)
```

**The 17-step boot sequence:**

| Step | Phase | What happens |
|---|---|---|
| 1 | Emulator init | ogun-desktop.exe → ogun-emulator; emulator initializes 4 virtual devices |
| 2 | UEFI | ogun-uefi: Pre-Init → Device Init → Boot Menu → Handoff (ExitBootServices) |
| 3–6 | Bootloader | Platform detection; driver init; three-stage verification; KernelBootBundle assembly |
| 7 | Subsystem init | All 15 kernel subsystems initialize in strict canonical order (failure = crash) |
| 8 | Module loading | auto_load kernel modules loaded; ABI version verified; `on_load` called |
| 9 | Kernel services | Three Tier-1 services start: modules-manager, process-manager, ipc-broker |
| 10 | Lock screen | IPC channels registered; lock screen displayed; SessionStartBundle constructed |
| 11 | Authentication | Operator credential validated; lockout policy enforced |
| 12 | Session context | `ActiveSessionContext` constructed; all processes stamped from this point |
| 13 | OS services | security-manager (100), system-manager (101), app-manager (102) start |
| 14 | Session restore | Restore workspace sessions from snapshot, or crash recovery if marker absent |
| 15 | Desktop launch | ogun-desktop, ogun-shell, ogun-command-center, all auto_start Tier 2 apps |
| 16 | Extensions | OS Runtime Loader scans extensions; operator-approved ones loaded via dlopen |
| 17 | User apps | auto_start Tier 4 apps launch; `lifecycle.boot_completed` broadcast; RUNNING state |

---

## 101. The 15 Kernel Subsystems

All 15 subsystems are `rlib` crates statically linked into `ogun-host-service`. They initialize in this canonical order — failure at any step calls `crash()`:

| # | Subsystem | Why this order |
|---|---|---|
| 1 | `ogun-subsystem-telemetry` | Must be first; all other subsystems emit through it |
| 2 | `ogun-subsystem-memory` | Required before any allocation; OOM detection |
| 3 | `ogun-subsystem-process` | Required before concurrent activity; owns ogun-cpu virtual device |
| 4 | `ogun-subsystem-ipc` | Required before inter-subsystem messages; Elegua Protocol v0.3.0 |
| 5 | `ogun-subsystem-storage` | Required before VFS needs to persist; RustyDB WAL backend |
| 6 | `ogun-subsystem-vfs` | Registers 12 canonical namespaces from `NamespaceSeed` |
| 7 | `ogun-subsystem-security` | Ọpọn Protocol enforcement begins; all subsequent operations governed |
| 8 | `ogun-subsystem-services` | Service registry and baseline kernel service lifecycle records |
| 9 | `ogun-subsystem-host` | Host driver event channels; driver lifecycle; platform capability detection |
| 10 | `ogun-subsystem-session` | Session context, RBAC, operator records, workspace contexts |
| 11 | `ogun-subsystem-display` | Display surfaces, themes, input routing, window management |
| 12 | `ogun-subsystem-state` | Session snapshots, `CleanShutdownMarker`, crash scan |
| 13 | `ogun-subsystem-components` | Module and extension loading; ABI verification; `dlopen` gating |
| 14 | `ogun-subsystem-network` | OgunNet v2.0.0: Kademlia DHT, mDNS, gossip pub/sub, file transfer |
| 15 | `ogun-subsystem-emulation` | `VirtualDeviceRegistry`; all virtual device lifecycle; initialized last |

---

## 102. The Execution Model (ogun-cpu)

`ogun-cpu` is one of the four virtual devices managed by `ogun-emulator`. It is a **software-defined execution scheduler** — not a hardware emulator — that acts as the unified execution clock for every in-process component.

**Key properties:**
- All components tick through a shared priority-respecting round-robin on a shared Tokio thread pool
- Default tick rate: **100 Hz** (one tick = 10ms); configurable in `ogun.toml [kernel.cpu]`
- Minimum thread count at idle: 1 main thread (Tauri) + 1–2 Tokio worker threads
- Thread pool expands dynamically when work demands it

**Component Rate Divisors** (effective tick frequency relative to base 100 Hz):

| Divisor | Effective Rate |
|---|---|
| `Double(2)` | 200 Hz (burst) |
| `Full(1)` | 100 Hz (default) |
| `Half(2)` | 50 Hz |
| `Quarter(4)` | 25 Hz |
| `Eighth(8)` | 12.5 Hz |
| `Custom(n)` | (100/n) Hz |

**Priority Bands:**

| Band | Label | Execution |
|---|---|---|
| P0 | Critical kernel | Synchronous on CPU's own Tokio task; never deferred |
| P1–P4 | Normal | Dynamic Tokio thread pool |
| P5–P7 | Background | Pool workers with BackgroundYieldGate; lower effective rate |

**Starvation guard** — any component skipped for more than `starvation_threshold` ticks (default: 200) is temporarily promoted to P0 for one tick, then returns to its original priority.

**Panic isolation** — every component tick is wrapped in `std::panic::catch_unwind(AssertUnwindSafe(...))`. A panicking component never crashes the execution loop or any other component.

---

## 103. The Elegua Protocol (IPC)

Named after Èṣù-Ẹlẹ́gbára — the Yoruba orisha of crossroads and communication — the Elegua Protocol (v0.3.0) is the unified IPC and communication specification.

**Five communication patterns:** Request/Response, Publish/Subscribe, Fire-and-Forget, Stream, Broadcast

**Core IPC channels (session-lived, registered at boot):**

| Channel | Key messages |
|---|---|
| `ogun.host` | `phase.changed`, `status.changed`, `ready`, `crashed`, `shutdown_completed` |
| `ogun.session` | `session.started`, `operator.login`, `workspace.switched`, `context.updated` |
| `ogun.system` | `snapshot.written`, `crash.report`, `update.available`, `config.updated` |
| `ogun.security` | `capability.granted`, `capability.denied`, `opn.violation` |
| `ogun.apps` | `app.launched`, `app.terminated`, `app.crashed`, `app.installed` |
| `ogun.network` | `peer.connected`, `peer.disconnected`, `channel.opened` |
| `ogun.emulation` | `device.provisioned`, `device.terminated`, `registry.updated` |

**Every Elegua message carries:**
`protocol_version`, `message_id` (UUID v7), `correlation_id`, `timestamp` (Unix ms), `from` (namespace URI), `to` (namespace URI), `operator_id`, `enterprise_id`, `workspace_id`, `sender_pid`, `kind`, `payload` (MessagePack), `priority`, `trace_id`, `span_id`

**IPC rules:**
- Do not introduce silent side channels between runtime components
- Do not pass raw untyped bytes across layer boundaries when an Elegua type exists
- Always preserve workspace and enterprise context when forwarding messages
- `enterprise_id` must be present in all messages after session context bind (Step 12)

---

## 104. The VFS and 12 Namespaces

The VFS (Virtual Filesystem) is `ogun-subsystem-vfs` — initialized at step 6 with 12 canonical namespace schemes seeded from the image's `NamespaceSeed` section.

`OgunPath` resolution translates namespace URIs (e.g., `enterprise://my-consulting/clients/acme/`) to physical host filesystem paths via the `CallContext`. This translation happens at the VFS level — apps never see raw `~/.ogun/` paths.

**Workspace-scoped views** — each `workspace_id` gets its own namespace root. The VFS enforces this scoping, ensuring processes in workspace A cannot inadvertently access workspace B's files (subject to Ọpọn Protocol enforcement by the Security subsystem).

---

## 105. Virtual Hardware Layer

Four virtual devices are initialized and managed by `ogun-emulator` before the UEFI handoff:

| Device | Role | Implementation |
|---|---|---|
| `ogun-virtual-display-monitor` | Virtual display surface | Backed by Tauri 2.0+ `WebviewWindow`; no direct framebuffer writes; no GPU dependency |
| `ogun-virtual-platform-host` | Host platform services | Virtual filesystem, entropy, timers, shell execution, process management; platform-specific implementations |
| `ogun-virtual-cpu` | Execution scheduler | Software-defined clock; 100 Hz base; 8 priority bands; dynamic Tokio pool |
| `ogun-virtual-network-adapter` | Software-emulated NIC | NodeId via ed25519; X25519 session keys; AES-256-GCM; TCP/UDP only — no raw sockets |

**Subsystem 15 (`ogun-subsystem-emulation`)** owns the `VirtualDeviceRegistry` and manages the full lifecycle of all virtual devices, including virtual host instances (nested ogun OS instances). Maximum nesting depth is configurable (≤ 10; default 10).

**`ogun-emulator-backend`** is the only component in the entire stack that calls host OS APIs directly (WinAPI, POSIX, Bionic, web-sys). No component above it — including ogun-uefi, ogun-bootloader, drivers, kernel, session manager, or apps — calls host OS APIs directly. This is an unconditional design invariant.

---

## 106. Known Limitations in 0.1.0-beta

The following are documented limitations of the 0.1.0-beta release:

**Platform:**
- **Windows x64 only.** macOS Apple Silicon and Linux x86_64 Desktop Edition are designed and architected; packaging and testing are scheduled for subsequent releases.
- **Mobile Edition not included.** `ogun-host-android` and `ogun-host-ios` are in progress.
- **Web Edition not included.** `ogun-host-web` (WASM) is fully designed; not shipping in 0.1.0-beta.
- **Server Edition not included.** Multi-tenant `ogun-server-host` is designed; not shipping.
- **Device Edition not included.** Designed; not shipping.

**Technical:**
- **`enterprise_id` in IPC messages.** `enterprise_id` is defined in the session context and Elegua Protocol schema. Some messages may not yet include it explicitly. This is an open issue to be resolved in a patch release.
- **RustyDB backend.** The Storage subsystem uses RustyDB in 0.1.0-beta. Migration to the stable persistent backend is scheduled for 0.2.0.

**Beta qualifier:** All documented features are present in 0.1.0-beta. Some rough edges and performance characteristics are expected to improve in the stable 0.1.0 release. Report issues at [gitlab.com/ogun-foundation/ogun/-/issues](https://gitlab.com/ogun-foundation/ogun/-/issues).

---

## Appendix A — Release Artifacts (0.1.0-beta, Windows x64)

| Artifact | Description |
|---|---|
| `ogun-setup-windows-0.1.0-beta.exe` | User-facing setup binary; includes the full installer engine; manages ogun OS images and OS installation; silent install mode available |
| `ogun-desktop-windows-0.1.0-beta.exe` | User-facing launcher; starts ogun OS by launching the emulator; manages image modifications, repairs, and updates; registered as the sole autostart entry |
| `ogun-emulator-windows-0.1.0-beta.exe` | Main entry point (Tauri 2.0+ application); initializes virtual hardware; supervises ogun-host-service for the full session lifetime |
| `ogun_desktop_windows-windows-0.1.0-beta.exe` | `ogun-host-service` for Windows; all 15 subsystems statically linked; Authenticode-signed |
| `ogun-windows-0.1.0-beta.img` | Signed platform kernel image for Windows x64; sections: `KernelCore`, `SessionManager`, `BootConfig`, `SystemManifest`, `Modules`, `Assets`; signed with 0.1.0-beta ed25519 image signing key |
| `ogun_image_tool-windows-0.1.0-beta.exe` | `ogun-image-builder` Windows binary; produces signed `.img` files; for CI and local developer/operator use |

---

## Appendix B — Key Metrics Glossary

| Metric | Full Name | Formula |
|---|---|---|
| **EHR** | Effective Hourly Rate | `total_income / total_hours` (including admin, meetings, non-billable) |
| **EAV** | Effort-Adjusted Value | `revenue / (time × cognitive_load_factor)` |
| **EPV** | Expected Pipeline Value | `Σ(proposed_value × win_probability)` |
| **TPV** | Total Portfolio Value | Aggregate of all enterprise asset valuations |
| **MRR** | Monthly Recurring Revenue | Total recurring income base |
| **ARR** | Annual Recurring Revenue | MRR × 12 |
| **EVS** | Enterprise Value Score | `base_value + (revenue_multiple × annual_revenue) + strategic_premium` |
| **PIR** | Passive Income Ratio | `passive_income / total_income` |
| **PICC** | Passive Income Coverage | `passive_income / monthly_expenses` |
| **τ** | Commitment Tension | `Σ(committed_effort) − weekly_hours_max` |
| **IRR** | Internal Rate of Return | Standard IRR formula applied to portfolio investments |

---

## Appendix C — Prototype and Documentation Sites

| Site | URL |
|---|---|
| ogun OS prototype | https://ogun-prototype.eatondo000.workers.dev/ |
| ogun OS documentation | https://ogun-docs.eatondo000.workers.dev/ |
| ogun home site | https://ogun.eatondo000.workers.dev/ |
| jaku devops platform | https://jaku.eatondo000.workers.dev/ |
| oya system development platform | https://oya.eatondo000.workers.dev/ |
| bula UIUX development platform | https://bula.eatondo000.workers.dev/ |
| Source repository | https://gitlab.com/ogun-foundation/ogun |

---

## Appendix D — Cryptographic Primitives Reference

| Primitive | Library | Usage |
|---|---|---|
| ed25519 | `ring` v0.17 | Image and manifest signing/verification; OgunNet node identity |
| SHA-256 | `sha2` v0.10 | Per-section checksums, NodeId derivation, self-hashes |
| HKDF-SHA256 | `ring` v0.17 | HostKey derivation from image pubkey + system pubkey + install_id |
| zstd level 19 | `zstd` | Section compression in `.img` files |
| AES-256-GCM | `ring` v0.17 | Audit log encryption at rest; OgunNet per-session payload encryption |
| X25519 ECDH | `ring` v0.17 | OgunNet session key exchange |

---

*ogun OS · 0.1.0-beta · Project Ogún · 2026*  
*Owner: Dominic Eaton (@eatondo)*  
*Organization: The Ogun Foundation*  
*License: GNU General Public License v3.0*  
*Repository: [gitlab.com/ogun-foundation/ogun](https://gitlab.com/ogun-foundation/ogun)*
