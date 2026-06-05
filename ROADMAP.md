# ogun OS — Development Roadmap

**Version:** 0.1.0-beta  
**Project:** Ogún · 2026  
**Owner:** Dominic Eaton (@eatondo)  
**Target Platform:** Windows x64  
**Language:** Rust · Desktop Runtime: Tauri 2.0+  
**Status:** In Development  

---

## Overview

This roadmap covers the full development scope required to reach the `0.1.0-beta` release of ogun OS Desktop Edition. Development is organized into five sequential tracks: **Tools**, **SDK**, **OS Runtime**, **User Applications**, and **Artifacts**. The runtime track is ordered strictly by boot-chain dependency; the SDK track is a prerequisite for all application development. The final deliverable — user app `dongo` — marks the completion of all Rust package development for `0.1.0-beta`. Following a testing phase, the project advances to `0.1.0-rc`.

---

## Track 1 — ogun-image-tool

The build pipeline tool that produces signed `.img` kernel image files for each target platform. CI-only; does not ship to end users as a runtime component.

| Package | Description | Status |
|---|---|---|
| `ogun-types` | Shared type library — canonical types, `OgunPath`, ABI version constants | — |
| `ogun-image-format` | Image format spec — `OGUNIMG` header, section kinds, `ImageFlags`, `OGUNEND` sentinel | — |
| `ogun-image-builder` | Build-time image builder and ed25519 image signer; produces `ogun_image_tool.exe` | — |

**Milestone:** `ogun_image_tool.exe` 0.1.0-beta runtime executable — runnable, signing-verified kernel image output for Windows x64 target.

---

## Track 2 — ogun-setup / Installer

The installation pipeline that verifies the image, scaffolds the filesystem, generates cryptographic keys, and registers `ogun-desktop.exe` as the system autostart entry.

| Package | Description | Status |
|---|---|---|
| `ogun-installer` | Core installation logic — image verification, filesystem scaffolding, key generation (SystemKey, HostKey), `opn-policy.json` and `capability-defaults.json` write-once setup | — |
| `ogun-setup` | User-facing installer binary (`ogun-setup.exe`) — wraps `ogun-installer`; registers `ogun-desktop.exe` as the single autostart entry via Task Scheduler | — |

**Milestone:** `ogun-setup.exe` — ogun Desktop Edition 2026 0.1.0-beta installer artifact.

---

## Track 3 — ogun-sdk

The SDK layer provides all public ABI interfaces for application, driver, kernel module, service, plugin, extension, component, host, device, and package development. All Tier 2–4 apps and all drivers depend exclusively on SDK crates — zero visibility into kernel internals, driver handles, or UEFI variable store.

| Package | Description | Status |
|---|---|---|
| **`ogun-app-sdk`** | Public app development interface — `OgunApp` trait, `AppContext`, `KernelHandle`, `SyscallRequest`; used by all Tier 2, Tier 3, and Tier 4 apps | — |
| **`ogun-component-sdk`** | Component lifecycle types — `OgunComponent` trait, component manifest types, `ComponentId`, ABI boundary utilities | — |
| **`ogun-device-sdk`** | Virtual device interface — contracts for virtual CPU, display monitor, network adapter, and host platform device abstractions | — |
| **`ogun-host-sdk`** | Host driver development interface — `OgunHost` trait, host event channels, driver lifecycle contracts; used by all platform host drivers | — |
| **`ogun-extension-sdk`** | Extension development interface — `OgunExtension` trait, `dlopen` ABI contract, operator approval manifest fields (opn-005) | — |
| **`ogun-service-sdk`** | OS service development interface — `OgunService` trait, service registry types, service lifecycle records; used by all Tier 1 services | — |
| **`ogun-plugin-sdk`** | Plugin development interface — `OgunPlugin` trait, plugin manifest types, OS feature addition layer contracts | — |
| **`ogun-kernel-sdk`** | Kernel module development interface — `OgunModule` trait, kernel extension lifecycle, module ABI verification contracts | — |
| **`ogun-package-sdk`** | Package development interface — `.opkg` format contracts, `ogun-component.toml` manifest schema, `opm` build toolchain types | — |
| **`ogun-driver-sdk`** | Driver development interface — `OgunDriver` trait, driver registration, host abstraction layer contracts for display, network, and host platform drivers | — |

**Milestone:** Full SDK surface published and ABI-stable for 0.1.0-beta. All downstream packages compile against these interfaces without internal kernel imports.

---

## Track 4 — ogun-os-runtime

The complete OS runtime stack, developed in boot-chain order. Each layer depends on the layer below it.

---

### 4.1 — ogun-emulator

The Tauri 2.0 application that is the main entry point of ogun OS. Initializes all virtual hardware before handing off to `ogun-uefi`. Top-level supervisor of the entire runtime.

| Package | Description | Status |
|---|---|---|
| **`ogun-cpu` (virtual CPU)** | Virtual CPU — unified tick/update clock for all OS components; eight-mode component lifecycle (`init`, `configure`, `start`, `tick`, `pause`, `freeze`, `reset`, `shutdown`); dynamically scaling Tokio thread pool; P0 synchronous kernel service ticks; starvation detection and promotion | — |
| **`ogun-display-monitor` (virtual display monitor)** | Virtual display monitor — renders via Tauri surfaces only; no direct framebuffer writes (I-24); manages display surfaces, theme data, and input event forwarding | — |
| **`ogun-network-adapter` (virtual network adapter)** | Virtual network adapter — software-emulated NIC; `NodeId` (ed25519-derived P2P address); OS sockets only, no raw packet injection (I-23); translation bridge between host network driver and network subsystem | — |
| **`ogun-platform-host` (virtual host platform)** | Virtual host platform — abstracts host OS APIs for all components above the emulator; the only component permitted to call WinAPI, POSIX, Bionic, or web-sys directly (I-31) | — |
| **`ogun-uefi` (virtual UEFI)** | Virtual UEFI layer — splash UI, boot menu (configurable timeout), `SecureBootPolicy` enforcement, `set_variable` lock after `ExitBootServices()` (I-22); hands off to `ogun-bootloader` | — |
| **`ogun-emulator`** | Tauri 2.0 application shell — owns virtual hardware initialization sequence; top-level supervisor; spawns and manages `ogun-host-service`; `ogun-desktop.exe` launcher target | — |

---

### 4.2 — ogun-bootloader

Three-stage cryptographic boot verification chain. Any stage failure calls `halt()` — nothing else runs (I-09).

| Package | Description | Status |
|---|---|---|
| **`ogun-bootloader`** | Three-stage boot verifier: **Stage 1** — ed25519 signature over R1+R2+R3 against `image-verify.pub`; ABI version check (`OGUN_ABI_VERSION`); `OGUNEND\x00` sentinel check; required section presence and hash validity. **Stage 2** — system manifest signature verification against `system.pub`; per-file rehash of all manifest-covered files. **Stage 3** — host key re-derivation and comparison against `host.key`. Produces `KernelBootBundle` on success; calls `halt()` on any failure | — |

---

### 4.3 — ogun-kernel

The kernel core and all 15 subsystems. All subsystem crates are `rlib` crates statically linked into `ogun-host-service`.

**Kernel Core**

| Package | Description | Status |
|---|---|---|
| **`ogun-kernel-core`** | Central orchestration kernel — initializes and supervises all 15 subsystems; owns the kernel supervisor loop; ABI version enforcement at all module/driver/app/extension load boundaries (I-16); receives `KernelBootBundle` from bootloader | — |

**Kernel Subsystems**

| Package | Subsystem | Responsibility | Status |
|---|---|---|---|
| `ogun-subsystem-telemetry` | #1 Telemetry | Structured logging; telemetry bus; `TelemetryBus::emit()` (fire-and-forget); `host_key` stamped on every telemetry event (I-14) | — |
| `ogun-subsystem-memory` | #2 Memory | Memory budget tracking; OOM detection; pressure levels | — |
| `ogun-subsystem-process` | #3 Process | Process table; `ogun-cpu` integration; scheduler; `operator_id` / `enterprise_id` / `workspace_id` context on all processes | — |
| `ogun-subsystem-ipc` | #4 IPC | Elegua Protocol IPC bus; channel registration; message routing; workspace isolation enforcement; `ogun-ipc-broker` Tier 1 service | — |
| `ogun-subsystem-storage` | #5 Storage | Persistent key-value storage (RustyDB backend for 0.1.0-beta); WAL; backup | — |
| `ogun-subsystem-vfs` | #6 VFS | Virtual filesystem; 12 canonical namespace registrations (`ogun://`, `system://`, `user://`, `security://`, `app://`, `data://`, `network://`, `agent://`, `enterprise://`, `workspace://`, `session://`, `telemetry://`); `OgunPath` resolution | — |
| `ogun-subsystem-security` | #7 Security | Ọpọn Protocol enforcement (unconditional; `opn_enforced = true` always reset); capability grants and denials; AES-256-GCM encrypted audit log; RBAC; policy engine; `host_key` stamped on every audit entry (I-15) | — |
| `ogun-subsystem-services` | #8 Services | Service registry; service lifecycle records | — |
| `ogun-subsystem-host` | #9 Host | Host driver event channels; driver lifecycle management | — |
| `ogun-subsystem-session` | #10 Session | Session context; operator records; RBAC; workspace contexts; enterprise contexts; session policy engine | — |
| `ogun-subsystem-display` | #11 Display | Display surfaces; themes; input events; window management | — |
| `ogun-subsystem-state` | #12 State | Session snapshots; checkpoint records; `CleanShutdownMarker`; crash scan on boot | — |
| `ogun-subsystem-components` | #13 Components | Module and extension loading; `OgunModule` lifecycle; ABI verification; `dlopen` gating (opn-005 operator approval required, I-29) | — |
| `ogun-subsystem-network` | #14 Network | OgunNet v2.0.0; `OgunNode`; Kademlia DHT; mDNS discovery; gossip pub/sub; named channels; file transfer; NAT punch; reputation | — |
| `ogun-subsystem-emulation` | #15 Emulation | Virtual hardware coordination; virtual host nesting (depth ≤ configured maximum, ≤ 10, I-25); emulator lifecycle | — |

**Device Drivers**

| Package | Description | Status |
|---|---|---|
| `ogun-display-driver` | Virtual display driver — translates `ogun-subsystem-display` surface operations to Tauri WebView rendering; no direct framebuffer access | — |
| `ogun-virtual-network-driver` | Virtual network driver — translates host OS networking APIs (TCP, UDP, TLS, DNS) into the kernel's unified network stream interface; pure translation layer | — |
| `ogun-host-platform-driver` | Virtual host platform driver — Windows x64 host driver; translates host OS APIs for all components via the `OgunHost` trait | — |

**Kernel Host Service**

| Package | Description | Status |
|---|---|---|
| `ogun-host-service` | Persistent system-level daemon managed by the emulator; creates, starts, supervises, and shuts down `ogun-host` instances; host service phase state machine; supervisor loop; `CleanShutdownMarker` written as absolute last act of every shutdown (I-17); exactly one instance per machine (I-26) | — |

**Kernel Plugins and Extensions**

| Package | Description | Status |
|---|---|---|
| `ogun-module-settings` | Kernel-level personalization and configuration management module | — |
| *(additional kernel plugins / extensions)* | Operator-approved extensions loaded via `dlopen`; each requires `operator_approved_at` in manifest (opn-005) | — |

---

### 4.4 — ogun-session-manager

| Package | Description | Status |
|---|---|---|
| **`ogun-session-manager`** | User session lifecycle — `SessionStartBundle` handoff from kernel; authentication (lockout threshold, lockout duration); session context binding (`operator_id`, `enterprise_id`, `workspace_id`, `trace_id`); OS-tier service initialization; session restore and crash recovery; workspace and profile switching; session snapshots (configurable interval); clean shutdown sequence | — |

---

### 4.5 — ogun-desktop-host-client

| Package | Description | Status |
|---|---|---|
| **`ogun-desktop-host-client`** | `ogun-desktop.exe` — user-facing launcher; starts `ogun-emulator` as a Tauri application; handles image modification, repair, and update; registered as the single autostart entry by `ogun-setup.exe` (I-21); exactly one autostart entry per machine | — |

---

### 4.6 — ogun-user-apps

All user-space applications. Tier 2 and Tier 3 apps are built into the OS runtime image. Tier 4 apps ship as `.opkg` packages. All apps depend only on `ogun-app-sdk` / `ogun-service-sdk` — zero kernel internal visibility (I-28).

**Tier 2 — OS Apps**

| Package | Description | Status |
|---|---|---|
| `ogun-desktop` | Desktop surface, window management, dock; enterprise-aware workspace-centric desktop environment | — |
| `ogun-shell` | Dual-surface shell — GUI shell panel (inside `ogun-command-center`) and TUI/CLI terminal emulator; `ShellRuntime` core shared across both surfaces | — |
| `ogun-explorer` | Graphical semantic filesystem navigator; resolves and browses `OgunPath` namespace addresses | — |
| `ogun-command-center` | Central command hub; shell output panel; quick actions; operational headquarters | — |
| `ogun-settings-center` | Unified OS and subsystem configuration center | — |
| `ogun-profile-center` | Multi-profile management with full isolation; operator profile and enterprise management | — |
| `ogun-security-center` | Capability-based security center; audit log viewer; capability grant review | — |
| `ogun-command-palette` | Universal keyboard-first command interface; global fuzzy command search | — |
| `ogun-workspaces` | Workspace creation, switching, and layout management; enterprise-aware workspace runtime | — |
| `ogun-system-manager` | System health; updates; crash reports; onboarding; administrative control plane | — |
| `ogun-app-manager` | Application and package management center; `opm` integration; app lifecycle management | — |
| `ogun-ui` | Rust UI design system and cross-platform display client; shared component library | — |
| `ogun-operator` | Operator identity and credential management | — |

**Tier 3 — Utility Apps**

| Package | Description | Status |
|---|---|---|
| `ogun-notes` | Persistent, searchable, enterprise-linked note-taking | — |
| `ogun-tasks` | Unified task management with enterprise linkage | — |
| `ogun-focus` | Focus session and time-blocking runtime | — |
| `ogun-schedule` | Schedule, calendar, and timeline management | — |
| `ogun-messenger` | Unified notifications and messaging client | — |
| `ogun-search` | Universal system-wide semantic search across all namespaces | — |
| `ogun-assistant` (OBA) | ogun Bounded AI assistant with conversational interface | — |
| `ogun-contacts` | Contact and network management | — |

**Tier 4 — User Apps (Personal Enterprise Suite · `.opkg` packages)**

The eight Tier 4 apps included in 0.1.0-beta are developed in the following order. `dongo` is the last Rust package to be developed and its completion marks the official end of 0.1.0-beta Rust development.

| # | Package | Description | Status |
|---|---|---|---|
| 1 | `enzo` | Personal Enterprise Management System — the central hub for managing the full personal enterprise lifecycle, including enterprises, engagements, assets, workflows, and value production | — |
| 2 | `kogi` | Software-Defined Office — autonomous, programmable workspace environment for independent work; coordinated project and operational execution | — |
| 3 | `ume` | Organization Operating System — organization-level structure and operations layer; governance, roles, and team coordination | — |
| 4 | `shango` | Solution Factory — ideation-to-execution pipeline for building and shipping solutions, products, and services | — |
| 5 | `heshima` | Identity Management System — operator and enterprise identity, credentials, trust, and reputation management | — |
| 6 | `igi` | Portfolio Management System — enterprise portfolio tracking; project and program prioritization aligned to strategic goals | — |
| 7 | `moto` | Project Management System — single-project lifecycle management with scope, budget, timeline, and tactic tracking | — |
| 8 | `dongo` | Financial Management System — personal and enterprise financial management; income streams, expenses, budgets, and financial health tracking. **Final Rust package — completion of this package marks the end of 0.1.0-beta development** | — |

---

## Track 5 — ogun-artifacts

Deliverable artifacts produced from the completed runtime and tooling.

| Artifact | Description |
|---|---|
| **ogun Desktop Edition — Windows Image** | Signed `ogun-kernel.img` for Windows x64 — produced by `ogun_image_tool.exe`; `ImageKind::Platform`; ed25519-signed; ABI version stamped; `OGUNEND\x00` sentinel present; `ImageFlags::SIGNATURE_REQUIRED` set |
| **ogun Desktop Edition 2026 — 0.1.0-beta Setup / Installer** | `ogun-setup.exe` — the end-user installer for Windows x64; bundles `ogun-installer`; installs the OS image, scaffolds `~/.ogun/`, generates cryptographic keys, registers `ogun-desktop.exe` as the autostart entry |
| **ogun Desktop Edition 2026 — 0.1.0-beta Runtime Executable** | `ogun-desktop.exe` + `ogun-emulator` (Tauri app) — the complete ogun OS runtime binary package for Windows x64 |
| **ogun Image Tool — 0.1.0-beta Runtime Executable** | `ogun_image_tool.exe` — the standalone build-pipeline image builder and signer; CI-facing; produces `.img` files for all configured targets |

---

## Release Gate — 0.1.0-beta → 0.1.0-rc

The following conditions must be met before transitioning from beta to release candidate:

1. `dongo` (Tier 4) development complete — all 0.1.0-beta Rust packages delivered
2. All four artifact builds passing clean on Windows x64
3. Three-stage boot verification passing on a clean install
4. Full session lifecycle (boot → login → session → clean shutdown) verified end-to-end
5. All design invariants (I-01 through I-35) confirmed enforced
6. Beta testing phase complete with no P0 blockers outstanding

**After gate:** tag `v0.1.0-beta`, open `0.1.0-rc` milestone, begin release candidate preparation.

---

## Known Limitations — 0.1.0-beta

- **Windows x64 only.** macOS Apple Silicon and Linux x86_64 Desktop Edition targets are designed and architected; packaging and testing are scheduled for a subsequent release.
- **Mobile Edition not included.** `ogun-host-android` and `ogun-host-ios` are in progress and will not ship in this release.
- **Web Edition not included.** `ogun-host-web` (WASM) is fully designed; not shipping in 0.1.0-beta.
- **Server Edition not included.** Multi-tenant `ogun-server-host` support is designed; not shipping in 0.1.0-beta.
- **Device Edition not included.** Designed; not shipping in 0.1.0-beta.
- **RustyDB backend.** The Storage subsystem uses RustyDB in 0.1.0-beta. Migration to the stable persistent backend is scheduled for 0.2.0.
- **Tier 4 apps — partial set.** The full personal enterprise suite (21 apps) ships incrementally; 0.1.0-beta includes: `enzo`, `kogi`, `ume`, `shango`, `heshima`, `igi`, `moto`, `dongo`. Remaining Tier 4 apps target subsequent releases.

---

*ogun OS · v0.1.0-beta Roadmap · Project Ogún · 2026*  
*Owner: Dominic Eaton (@eatondo)*
