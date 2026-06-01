# Ogun Operating System for Independent Workers

[![Version](https://img.shields.io/badge/version-0.1.0--beta-orange?style=flat-square)](https://gitlab.com/ogun-foundation/ogun/-/releases)
[![Status](https://img.shields.io/badge/status-beta--upcoming-yellow?style=flat-square)](https://gitlab.com/ogun-foundation/ogun/-/blob/main/CHANGELOG.md)
[![License](https://img.shields.io/badge/license-GPL--3.0-blue?style=flat-square)](https://gitlab.com/ogun-foundation/ogun/-/blob/main/LICENSE.md)
[![Platform](https://img.shields.io/badge/platform-Windows%20x64-informational?style=flat-square)](https://gitlab.com/ogun-foundation/ogun)
[![Language](https://img.shields.io/badge/language-Rust-orange?style=flat-square&logo=rust)](https://www.rust-lang.org/)
[![Framework](https://img.shields.io/badge/frontend-Tauri%202.0-blueviolet?style=flat-square)](https://tauri.app/)
[![Build](https://img.shields.io/gitlab/pipeline-status/ogun-foundation/ogun?branch=main&style=flat-square&logo=gitlab)](https://gitlab.com/ogun-foundation/ogun/-/pipelines)
[![Issues](https://img.shields.io/gitlab/issues/open/ogun-foundation/ogun?style=flat-square&logo=gitlab)](https://gitlab.com/ogun-foundation/ogun/-/issues)
[![Maintainer](https://img.shields.io/badge/maintainer-%40eatondo-lightgrey?style=flat-square)](https://gitlab.com/eatondo)

---

**ogun OS** is a Rust-native operating-system layer for independent workers. It runs on top of an existing host operating system rather than replacing it, then presents a signed, capability-gated, workspace-oriented runtime with its own boot chain, virtual devices, kernel subsystems, SDKs, applications, tools, and release artifacts.

This umbrella repository collects the implementation workspaces, product documentation, configuration templates, release artifacts, protocol libraries, and supporting crates used to build the planned `0.1.0-beta` Windows x64 Desktop Edition.

---

## Contents

- [Ogun Operating System for Independent Workers](#ogun-operating-system-for-independent-workers)
  - [Contents](#contents)
  - [Status](#status)
  - [What ogun OS Is](#what-ogun-os-is)
  - [Key Features](#key-features)
  - [Runtime Shape](#runtime-shape)
  - [Repository Map](#repository-map)
  - [Kernel Subsystems](#kernel-subsystems)
    - [VFS Namespaces (12)](#vfs-namespaces-12)
  - [Application Stack](#application-stack)
    - [Tier 1 — Kernel Apps](#tier-1--kernel-apps)
    - [Tier 2 — OS Apps](#tier-2--os-apps)
    - [Tier 3 — Utility Apps](#tier-3--utility-apps)
    - [Tier 4 — Personal Enterprise Suite](#tier-4--personal-enterprise-suite)
  - [Virtual Hardware](#virtual-hardware)
  - [Protocols](#protocols)
    - [Elegua Protocol](#elegua-protocol)
    - [Ọpọn Protocol](#ọpọn-protocol)
    - [OgunNet v2.0.0](#ogunnet-v200)
  - [SDK Surface](#sdk-surface)
  - [Configuration](#configuration)
  - [Release Artifacts](#release-artifacts)
  - [Personal Enterprise Model](#personal-enterprise-model)
    - [Enterprise Lifecycle](#enterprise-lifecycle)
    - [Enterprise Types](#enterprise-types)
    - [Operator Personas](#operator-personas)
    - [Hypergrid Templates](#hypergrid-templates)
    - [Key Metrics](#key-metrics)
  - [Agent System (Sambara)](#agent-system-sambara)
    - [Agent Authority Levels](#agent-authority-levels)
    - [Platform-Registered Domain Agents](#platform-registered-domain-agents)
    - [LLM Drivers](#llm-drivers)
  - [Platform Support](#platform-support)
  - [Development Requirements](#development-requirements)
  - [Quick Start](#quick-start)
  - [Documentation](#documentation)
  - [Contributing](#contributing)
  - [License](#license)
- [Ogun Prototype and tooling sites](#ogun-prototype-and-tooling-sites)
  - [ogun os prototype](#ogun-os-prototype)
  - [ogun os documentation](#ogun-os-documentation)
  - [ogun home site](#ogun-home-site)
  - [jaku devops platform](#jaku-devops-platform)
  - [oya system development platform](#oya-system-development-platform)
  - [bula UIUX development platform](#bula-uiux-development-platform)

---

## Status

| | |
|---|---|
| **Current development state** | `0.1.0-alpha` (internal) |
| **Planned first public beta** | `0.1.0-beta` — Windows x64 Desktop Edition — June 2026 |
| **Owner** | Dominic Eaton ([@eatondo](https://gitlab.com/eatondo)), dominic1.eaton@gmail.com |
| **Organization** | [The Ogun Foundation](https://gitlab.com/ogun-foundation) |

The `0.1.0-beta` release establishes the complete foundational runtime: virtual UEFI layer, bootloader, kernel core, session manager, 15 kernel subsystems, emulator, virtual devices, desktop host, drivers, OS apps, user apps, tools, SDKs, signed images, and installer artifacts.

Current alpha state: architecture and scaffolding are in place across all workspaces. Many crates are still implementing the documented specifications. See [`TODO.md`](TODO.md) for the full tracked work-to-beta list and [`CHANGELOG.md`](CHANGELOG.md) for the complete beta scope.

---

## What ogun OS Is

ogun OS is a **programmable operating environment for independent workers**. Unlike conventional operating systems that organize files, applications, and windows, ogun OS organizes **enterprises, engagements, assets, workflows, agents, intelligence systems, and value production**.

Every independent worker — freelancer, creator, founder, investor — is already running an enterprise. Most just don't know it, because it has no structure, no memory, no rules, and no intelligence layer. ogun OS makes the enterprise explicit, structured, measurable, and compounding.

Applications in ogun OS are not isolated utilities. They are **runtime systems** — composable operational environments that share a common process model, IPC bus, semantic filesystem, observability layer, and workspace context. Every application is a managed runtime entity with a declared identity, capability set, workspace context, telemetry stream, and lifecycle.

---

## Key Features

- **Hosted OS layer** — runs on Windows first; Linux, macOS, web, mobile, server, and device editions are designed for later targets.
- **Signed `.img` platform images** — ed25519 signature over SHA-256, per-section integrity checks, zstd level-19 compression.
- **Full boot chain** — `ogun-desktop.exe` → `ogun-emulator` → virtual hardware → `ogun-uefi` → `ogun-bootloader` → `ogun-kernel-core` → `ogun-session-manager`.
- **Elegua Protocol** — capability-gated typed IPC and namespace system for all inter-component communication.
- **Ọpọn Protocol** — cross-enterprise data isolation enforced at the kernel security boundary, not the application layer.
- **15 statically linked kernel subsystems** — telemetry, memory, process, IPC, storage, VFS, security, services, host, session, display, state, components, network, emulation.
- **Four application tiers** — Tier-1 kernel services, Tier-2 OS apps, Tier-3 utility apps, Tier-4 personal enterprise applications.
- **SDK crates** — for apps, services, modules, packages, plugins, drivers, hosts, devices, and components.
- **Sambara** — AI agents operating system embedded within ogun OS; kernel-level identity, workspace-bounded execution, and continuously improving intelligence models.
- **RustyDB** — Rust-native embedded database backend for session state, registries, audit indexes, and node identity.
- **OgunNet v2.0.0** — P2P network layer with Kademlia DHT, mDNS discovery, gossip pub/sub, named channels, and file transfer.

---

## Runtime Shape

```
ogun-desktop.exe
  └── ogun-emulator  (Tauri 2.0+ application — main entry point)
        ├── ogun-virtual-display-monitor
        ├── ogun-virtual-native-host-platform
        ├── ogun-virtual-cpu
        ├── ogun-virtual-network-adapter
        ├── ogun-uefi  (virtual UEFI firmware — four phases)
        └── ogun-host-service
              ├── ogun-bootloader        (three-stage image + manifest + key verification)
              ├── ogun-kernel-core       (15 subsystems in canonical init order)
              ├── ogun-session-manager   (lock screen → auth → session → desktop)
              └── services, apps, drivers, modules, and packages
```

`ogun-emulator-backend` is the sole component that calls host OS APIs directly (WinAPI, POSIX, Bionic, web-sys). No component above it calls host OS APIs.

---

## Repository Map

| Path | Purpose |
|---|---|
| `ogun-os/` | Main OS workspace, clients, host server scaffold, and beta tracking. |
| `ogun-runtime/` | Runtime crates — types, image format, bootloader, kernel, and session manager. |
| `ogun-devices/` | Emulator, virtual UEFI, virtual CPU, virtual display, virtual host platform, and virtual network adapter. |
| `ogun-components/` | Tier-2 and Tier-3 apps, hosts, drivers, and services. |
| `ogun-apps/` | Tier-4 personal enterprise application suite. |
| `ogun-sdk/` | Public SDK traits, ABI constants, and component contracts. |
| `ogun-tools/` | Setup and image tooling, including Tauri-based installer and image tool workspaces. |
| `ogun-config/` | Seed configuration templates for `ogun.toml`, `display.toml`, `emulation.toml`, `uefi.toml`. |
| `ogun-artifacts/` | Staging area for built images, installers, checksums, and release metadata. |
| `ogun-docs/` | Canonical product, architecture, release, and execution-model documents. |
| `ogun-sites/` | Public site and documentation site sources. |
| `elegua/` | Ogun's typed communication and IPC protocol. |
| `rustydb/` | Embedded database backend used by the storage subsystem. |
| `bula/`, `jaku/`, `oya/` | Supporting libraries and experiments used by the wider ecosystem. |
| `ogun-test-features/` | Test feature sandboxes and prototypes. |

---

## Kernel Subsystems

All 15 subsystems are implemented as separate `ogun-subsystem-*` `rlib` crates statically linked into `ogun-host-service`. They initialize in strict canonical order — failure at any step calls `crash()`.

| # | Crate | Responsibility |
|---|---|---|
| 1 | `ogun-subsystem-telemetry` | Structured telemetry bus — initialized first; all other subsystems emit through it. |
| 2 | `ogun-subsystem-memory` | Memory budget tracking, OOM detection, pressure-level reporting. |
| 3 | `ogun-subsystem-process` | Process table, PCB tracking, `operator_id`/`enterprise_id`/`workspace_id` stamping. |
| 4 | `ogun-subsystem-ipc` | Elegua Protocol v0.3.0 — unicast, multicast, broadcast, request/reply, workspace isolation. |
| 5 | `ogun-subsystem-storage` | RustyDB-backed WAL key-value storage for session state, node identity, and registries. |
| 6 | `ogun-subsystem-vfs` | Virtual filesystem — 12 namespace schemes, `OgunPath` resolution, workspace-scoped views. |
| 7 | `ogun-subsystem-security` | Ọpọn Protocol enforcement, capability system, AES-256-GCM audit log, ed25519 verification. |
| 8 | `ogun-subsystem-services` | Service registry and baseline kernel service lifecycle records. |
| 9 | `ogun-subsystem-host` | Host driver event channel lifecycle, `OgunHostDriver`/`OgunDisplayDriver` handle registration. |
| 10 | `ogun-subsystem-session` | Session context lifecycle, RBAC, authentication pipeline, multi-profile support. |
| 11 | `ogun-subsystem-display` | Display surface registry, theme/appearance state, input routing, window management. |
| 12 | `ogun-subsystem-state` | Session snapshots, checkpoint system, `CleanShutdownMarker`, crash recovery. |
| 13 | `ogun-subsystem-components` | `OgunModule` lifecycle, dynamic `cdylib` loading, ABI version verification. |
| 14 | `ogun-subsystem-network` | OgunNet v2.0.0 — Kademlia DHT, mDNS, gossip pub/sub, named channels, file transfer. |
| 15 | `ogun-subsystem-emulation` | `VirtualDeviceRegistry` and full lifecycle for all virtual devices. |

### VFS Namespaces (12)

`ogun://` · `system://` · `user://` · `security://` · `app://` · `data://` · `network://` · `agent://` · `enterprise://` · `workspace://` · `session://` · `telemetry://`

---

## Application Stack

### Tier 1 — Kernel Apps

| Component | Role |
|---|---|
| `ogun-modules-manager` | Kernel module lifecycle: load, initialize, tick, unload. |
| `ogun-process-manager` | Process table management, PCB tracking, scheduling coordination. |
| `ogun-ipc-broker` | Elegua Protocol message routing; workspace and enterprise isolation enforcement. |

### Tier 2 — OS Apps

`ogun-app-manager` · `ogun-command-center` · `ogun-command-palette` · `ogun-desktop` · `ogun-explorer` · `ogun-operator-center` · `ogun-profile-center` · `ogun-security-center` · `ogun-settings-center` · `ogun-shell` · `ogun-system-manager` · `ogun-ui` · `ogun-workspaces`

### Tier 3 — Utility Apps

`ogun-assistant` · `ogun-calendar` · `ogun-contactbook` · `ogun-focus` · `ogun-messenger` · `ogun-notes` · `ogun-search-engine` · `ogun-tasks`

### Tier 4 — Personal Enterprise Suite

Each Tier-4 app is a software-defined operating system for a specific domain of independent work.

| App | Role |
|---|---|
| **enzo** | Personal Enterprise Management — enterprise creation, KPI dashboards, portfolio tracking, Portfolio Control Center, Observatory integration. |
| **kogi** | Software-Defined Office — pipeline management, engagement tracking, desk, EHR intelligence, observatory runtime. |
| **dongo** | Financial Management — software-defined wallets, double-entry accounting, tax reserve, multi-currency, reporting. |
| **ume** | Organization Operating System — legal entities, contracts, cap tables, revenue splits, SOPs. |
| **heshima** | Identity Management — credentials, verification, reputation, operator roles, linktree, OgunNet identity. |
| **shango** | Solution Factory — build environments, solution lifecycle, CI/CD pipelines, distribution, productization. |
| **igi** | Portfolio Management — asset tracking, EVS computation, portfolio balancing, passive income trajectory. |
| **moto** | Project and Program Management — milestones, deliverables, tasks integrated with `ogun-tasks`. |
| **akeel** | Knowledge Management — documentation, research, institutional memory. |
| **zamani** | Estate Management — physical asset management, wealth systems, estate planning, home office intelligence. |
| **orun** | Semantic Filesystem Runtime — enterprise-linked namespace paths, VFS. |
| **mizeez** | Version and Change Control — artifact versioning, change management. |
| **shaba** | Strategic Management — OKRs, roadmap, strategic intent tracking. |
| **kanna** | Governance Management — hubs, policies, standards, cooperative governance. |
| **qala** | Observatory and Analytics — metrics, insights, telemetry, scenario modeling. |
| **sambara** | Agent Management System — autonomous agents, authority levels, orchestration (see [Agent System](#agent-system-sambara)). |
| **zuri** | Digital Marketplace — store management, listing distribution, buyer discovery. |
| **didara** | IP Tracking and Management — patents, trademarks, licensing, royalties. |
| **apapo** | Hypergrid Domain Operating System Dev Platform — SDK, API surface, multi-tenant domain isolation. |
| **ayo** | Digital Spaces Management — independent worker social platform, community tools, digital presence. |

---

## Virtual Hardware

Four virtual devices are initialized by `ogun-emulator` before the UEFI handoff:

| Device | Crate | Description |
|---|---|---|
| Virtual Display Monitor | `ogun-virtual-display-monitor` | Tauri 2.0+ `WebviewWindow` surface; presents `OgunDisplayDriver` interface. |
| Virtual Platform Host | `ogun-virtual-platform-host` | Virtual filesystem, entropy, timers, shell execution, and process management. |
| Virtual CPU | `ogun-virtual-cpu` | Software-defined execution scheduler; 100 Hz tick rate; 8 priority bands (P0–P7); dynamic Tokio thread pool. |
| Virtual Network Adapter | `ogun-virtual-network-adapter` | Software-emulated NIC; `NodeId` via ed25519; X25519 session key derivation; AES-256-GCM encryption; TCP/UDP only. |

---

## Protocols

### Elegua Protocol

The typed IPC and communication protocol for all inter-component communication in ogun OS. Every message carries `operator_id`, `workspace_id`, `enterprise_id`, `trace_id`, `span_id`, `protocol_version`, `timestamp`, `from`, `to`, `correlation_id`, `sender_pid`, `kind`, `payload`, and `priority`.

Patterns: unicast · multicast · broadcast · request/reply · pub/sub

### Ọpọn Protocol

Cross-enterprise data isolation enforced at the kernel security boundary. Named after the Ọpọn Ifá — the Yoruba divination tray, upon which no reading for one supplicant may be contaminated by the marks of another.

Five immutable rules: `opn-001` enterprise namespace isolation · `opn-002` agent authority bounds · `opn-003` contract-before-active enforcement · `opn-004` audit-before-execute · `opn-005` extension approval gate.

`opn_enforced = true` is unconditional in all production builds and cannot be configured away.

### OgunNet v2.0.0

P2P network layer implemented in `ogun-subsystem-network`:

- **Transport** — TCP with 4-byte big-endian length-prefix framing; max message 4 MiB.
- **Encryption** — X25519 ECDH → per-session AES-256-GCM.
- **Discovery** — Kademlia DHT (256-bucket, k=20, α=3); mDNS on `239.255.17.170:17171`; Peer Exchange (PEX).
- **Pub/sub** — Gossip with TTL decrement, 2048-entry seen-cache deduplication.
- **Channels** — IRC-style named channels with AES-256-GCM key derivation.
- **File transfer** — 64 KiB chunks, SHA-256 integrity, encrypted.
- **NAT punch** — relay-assisted UDP hole-punch.

---

## SDK Surface

| Crate | Purpose |
|---|---|
| `ogun-types` | Zero-dependency foundational types — `ProcessId`, `OperatorId`, `WorkspaceId`, `EnterpriseId`, `TraceId`, `OGUN_ABI_VERSION`, binary format constants. |
| `ogun-app-sdk` | `OgunApp` trait — `on_init`, `on_configure`, `on_start`, `on_tick`, `on_message`, `on_pause`, `on_freeze`, `on_reset`, `on_shutdown`. |
| `ogun-service-sdk` | `OgunService` trait for OS-tier services. |
| `ogun-kernel-sdk` | `OgunModule` trait and `ModuleContext` for kernel-level modules. |
| `ogun-driver-sdk` | `OgunHostDriver`, `OgunDisplayDriver`, `OgunVirtualDriver` traits. |
| `ogun-host-sdk` | `OgunHost` trait — `HostType`, `HostStatus`, `HostResult`, `CrashReport`. |

---

## Configuration

| File | Description |
|---|---|
| `ogun.toml` | Primary runtime configuration — boot, kernel, CPU scheduler, network, session, storage, telemetry, security. |
| `display.toml` | Display and theming — theme, window dimensions, fonts, surfaces. |
| `emulation.toml` | Emulation layer — virtual device auto-provisioning, virtual host nesting depth, virtual monitor and network settings. |
| `uefi.toml` | Virtual UEFI — boot menu interrupt window, Secure Boot policy, UEFI boot log path. |

`validate_image_signature` is treated as `true` unconditionally in all production builds. `opn_enforced` in `security/opn-policy.json` is reset to `true` unconditionally after every `ogun.toml` load.

---

## Release Artifacts

Planned `0.1.0-beta` artifacts for Windows x64:

| Artifact | Description |
|---|---|
| `ogun-setup-windows-0.1.0-beta.exe` | Installer — manages ogun OS images and OS installation; nine-step install pipeline; silent mode available. |
| `ogun-desktop-windows-0.1.0-beta.exe` | User-facing launcher — starts ogun OS; manages image modification, repair, and update. |
| `ogun-emulator-windows-0.1.0-beta.exe` | Main entry point (Tauri application) — initializes virtual hardware; supervises `ogun-host-service`. |
| `ogun_desktop_windows-windows-0.1.0-beta.exe` | `ogun-host-service` for Windows — all subsystems statically linked; Authenticode-signed. |
| `ogun-windows-0.1.0-beta.img` | Signed platform kernel image — sections: `KernelCore`, `SessionManager`, `BootConfig`, `SystemManifest`, `Modules`, `Assets`. |
| `ogun_image_tool-windows-0.1.0-beta.exe` | Image builder tool — produces signed `.img` files for CI and local developer use. |

The `.img` format uses a five-region layout: `FileHeader` · `SectionTable` · `SectionData` · `ImageVerifyKey` · `SignatureBlock`. Images are ed25519-signed with per-section SHA-256 checksums and zstd level-19 compression.

---

## Personal Enterprise Model

The personal enterprise model is the core conceptual framework baked into ogun OS. A **personal enterprise** is not a company or dashboard — it is a **closed-loop value transformation system** that converts inputs (time, skill, capital, attention, relationships) into outputs (revenue, assets, reputation, equity) through repeatable, structured operations that compound over time.

ogun OS makes the enterprise explicit at the kernel level. Every process carries `enterprise_context` as a first-class metadata field. Every filesystem path is enterprise-aware. Every transaction is enterprise-attributed. The Ọpọn Protocol enforces isolation at the Security Manager boundary.

### Enterprise Lifecycle

```
SEED → COLD → ACTIVATED → CALIBRATED → INTELLIGENT → OPTIMIZED → COMPOUNDING
                                                                      ↓
                                                                  ARCHIVED
```

### Enterprise Types

`Service` · `Creator` · `Founder` · `Investment` · `Hybrid` · `Cooperative` · `Estate` · `Platform`

### Operator Personas

`Creator` · `Operator` (Freelancer) · `Builder` (Founder) · `Investor` · `CNO` (Chief Navigation Officer — meta-persona running multiple enterprises)

### Hypergrid Templates

The Enzo Hypergrid provides persona-specific XML templates for bootstrapping enterprise configurations:

| Template | Persona |
|---|---|
| `hypergrid-freelancer.xml` | Freelancer — consultants, contractors, coaches, gig workers |
| `hypergrid-creator.xml` | Creator — content creators, artists, writers, musicians, indie developers |
| `hypergrid-founder.xml` | Founder — entrepreneurs, solopreneurs, micropreneurs, startup founders |
| `hypergrid-investor.xml` | Investor — retail investors, real estate, angels, crypto, donors |
| `sambara-hypergrid-enterprise-operator.xml` | Enterprise Operator — production AI fleet governance |
| `shango-hypergrid-indie-builder.xml` | Indie Builder — solo developer running the full build chain |
| `shango-hypergrid-sre-operator.xml` | SRE Operator — production reliability and operations |
| `zamani-estate-homesteader-nadiachen.xml` | Homesteader — primary residence as a productive estate node |
| `eatondo-portfolio.xml` | Complete CNO portfolio — reference implementation across 40+ enterprises |

### Key Metrics

| Metric | Definition |
|---|---|
| **EHR** | Effective Hourly Rate = `total_income / total_hours` (including admin, meetings, non-billable) |
| **EAV** | Effort-Adjusted Value = `revenue / (time × cognitive_load_factor)` |
| **EPV** | Expected Pipeline Value = `Σ(proposed_value × win_probability)` |
| **TPV** | Total Portfolio Value — aggregate of all enterprise asset valuations |
| **MRR** | Monthly Recurring Revenue baseline |
| **Passive Income Ratio** | Passive income ÷ total income |

---

## Agent System (Sambara)

**Sambara** is the AI agents operating system embedded within ogun OS. It is not a prompt-chaining tool or LLM wrapper — it is a complete **operating system for AI agents**.

Agents are first-class runtime entities with kernel-level identity (`agent_id`), workspace-bounded execution, operator-governed authority, and a continuously improving intelligence model. Every agent action is written to `~/.ogun/logs/agent-actions.log` (encrypted at rest) before the action completes. Agents cannot bypass or inspect their own governance block.

### Agent Authority Levels

| Level | Capability |
|---|---|
| `OBSERVE` | Read-only; monitors and contributes to MetricSnapshots; no actions. |
| `RECOMMEND` | Generates `InsightRecord`s and drafts for operator review; no automated actions. |
| `EXECUTE_BOUNDED` | Takes actions within explicitly declared parameter ranges; exceptions escalate. |
| `FULL_AUTONOMY` | Operates within declared domain without per-action approval; requires `OPTIMIZED` lifecycle stage. |

Authority escalation cannot be triggered by agent logic, policy rules, or Observatory recommendations — it requires explicit operator interaction.

### Platform-Registered Domain Agents

`FOLLOWUP_AGENT` · `PRICING_AGENT` · `EXECUTION_AGENT` · `ACQUISITION_AGENT` · `BOOKKEEPING_AGENT` · `OBSERVATORY_AGENT` · `PRODUCTIZATION_AGENT` · `QALA_PLANNER` · `QALA_EXECUTOR` · `ESTATE_AGENT` · `ATTRIBUTION_AGENT` · `LIFECYCLE_AGENT` · `ORCHESTRATION_AGENT` · `PRIVACY_AGENT`

### LLM Drivers

Sambara is model-agnostic. Built-in drivers: `anthropic-claude` (`claude-opus-4-6`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`) · `openai-chatgpt` (`gpt-4o`, `o1`, `o3-mini`) · `deepseek` (`deepseek-chat`, `deepseek-reasoner`) · `ollama-local` (any locally served model).

Custom drivers can be registered by operators on the `ENTERPRISE` governance tier.

---

## Platform Support

| Platform | Host Driver | Display Driver | Status |
|---|---|---|---|
| **Windows x64** | `ogun-host-windows` | `ogun-display-tauri` | **Beta target — June 2026** |
| Linux x86_64 | `ogun-host-linux` | `ogun-display-tauri` | Designed; post-beta |
| Linux ARM64 | `ogun-host-linux` | `ogun-display-tauri` | Designed; post-beta |
| macOS Apple Silicon | `ogun-host-macos` | `ogun-display-tauri` | Designed; post-beta |
| macOS Intel | `ogun-host-macos` | `ogun-display-tauri` | Designed; post-beta |
| Browser (WASM) | `ogun-host-web` | `ogun-display-web` | Designed; post-beta |
| Android | `ogun-host-android` | `ogun-display-android` | In progress |
| iOS | `ogun-host-ios` | `ogun-display-ios` | In progress |

---

## Development Requirements

**Required for all workspaces:**

- Rust stable toolchain with Cargo
- Git
- Windows x64 (for the current beta target)

**Required for Tauri tools and desktop surfaces:**

- Node.js and npm
- Tauri 2 prerequisites for the target platform
- Platform SDKs as required by the specific host or driver crate

**Optional depending on workspace:**

- WASM target support (`wasm32-unknown-unknown`) for browser-facing work
- Android NDK or Xcode for future mobile hosts

---

## Quick Start

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

Run a Tauri tool during development:

```powershell
cd C:\dev\ogun\ogun-tools\src\ogun-image-tool
npm install
npm run tauri dev
```

> **Note:** The top-level `Cargo-temp.toml` captures the intended combined workspace membership. The repo currently favors focused checks inside each project workspace until the umbrella workspace is promoted to a canonical top-level `Cargo.toml`. See [`TODO.md`](TODO.md) — P0 section — for the tracked build fix items.

---

## Documentation

| Document | Description |
|---|---|
| [`CHANGELOG.md`](CHANGELOG.md) | Release-facing changes and complete 0.1.0-beta component scope. |
| [`TODO.md`](TODO.md) | Full tracked work-to-beta list, organized by priority (P0/P1/P2). |
| [`DESIGN.md`](DESIGN.md) | Architecture summary and development boundaries. |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Contribution workflow and review expectations. |
| [`SECURITY.md`](SECURITY.md) | Vulnerability disclosure and supported versions. |
| [`GOVERNANCE.md`](GOVERNANCE.md) | Project roles and decision making. |
| [`SUPPORT.md`](SUPPORT.md) | Where to get help. |
| `ogun-docs/0.1.0-beta-release/` | Canonical beta product, architecture, and execution-model specifications. |

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full contribution workflow, branch conventions, and review expectations.

Before submitting a merge request, confirm that all workspaces relevant to your change pass `cargo check --workspace` and `cargo fmt --all`. The beta CI gate requires all workspaces to pass clean.

---

## License

ogun OS is licensed under the **GNU General Public License v3.0**.

```
ogun OS — Operating System for Independent Workers
Copyright (C) 2026 Dominic Eaton @ The Ogun Foundation

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
```

See [`LICENSE.md`](LICENSE.md) for the full license text.

---

# Ogun Prototype and tooling sites

## ogun os prototype
https://ogun-prototype.eatondo000.workers.dev/

## ogun os documentation
https://ogun-docs.eatondo000.workers.dev/

## ogun home site
https://ogun.eatondo000.workers.dev/

## jaku devops platform
https://jaku.eatondo000.workers.dev/

## oya system development platform
https://oya.eatondo000.workers.dev/

https://jaku.eatondo000.workers.dev/

## bula UIUX development platform
https://bula.eatondo000.workers.dev/

---

*ogun OS · Project Ogún · 2026 · [gitlab.com/ogun-foundation/ogun](https://gitlab.com/ogun-foundation/ogun)*
