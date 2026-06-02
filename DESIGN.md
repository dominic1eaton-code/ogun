# Ogun OS Design part I

This document summarizes the architecture and development boundaries for the
top-level ogun OS repository. The detailed release specifications live in
`ogun-docs/0.1.0-beta-release/`; this file is the authoritative short-form
reference contributors should read before changing code.

---

## System Goal

ogun OS is a hosted operating-system layer for independent workers. It runs on
top of a host OS rather than on bare metal, presenting a consistent virtual
hardware and runtime environment, verifying a signed platform image, initializing
a kernel and session manager, then running services and applications inside
capability-gated workspaces.

Every running instance of ogun OS is called an **ogun host** — a complete,
self-contained runtime comprising a virtual UEFI layer, a bootloader, a kernel
core, and a session manager. The system is structured around five host types
(Desktop, Web, Mobile, Device, Server), each adapting the same core runtime to
its platform's capabilities and constraints.

The first public target is **Windows x64 Desktop Edition**. Other editions are
architected but not the initial beta release target.

---

## Product Purpose

ogun OS is a **programmable operating environment for independent workers**.
Unlike conventional operating systems that organize files, applications, and
windows, ogun OS organizes enterprises, engagements, assets, workflows, agents,
intelligence systems, and value production.

Every independent worker — freelancer, creator, founder, investor — is already
running an enterprise. ogun OS makes the enterprise explicit, structured,
measurable, and compounding. Applications are not isolated utilities — they are
runtime systems sharing a common process model, IPC bus, semantic filesystem,
observability layer, and workspace context.

---

## Software Lifecycle

```text
compile time
  -> Rust crates (rlib/cdylib), Tauri apps, SDKs, services, drivers, and tools
  -> ogun-types provides zero-dependency foundational types to all crates
  -> OGUN_ABI_VERSION is the single source of truth for ABI compatibility

build time
  -> ogun-image-builder creates signed .img platform images (CI only)
  -> Five-region image layout: FileHeader · SectionTable · SectionData · ImageVerifyKey · SignatureBlock
  -> zstd level-19 compression; ed25519 signing; per-section SHA-256 checksums
  -> ogun-artifacts stages installers, images, checksums, and metadata

installation time
  -> ogun-setup.exe runs ogun-installer (nine steps, one-time per machine)
  -> Validates .img signature before extracting anything
  -> ~/.ogun/ directory tree scaffolded with 0o700 minimum permissions
  -> SystemKey ed25519 keypair generated; private key into host OS keychain (DPAPI)
  -> HostKey derived via HKDF-SHA256 and written to ~/.ogun/security/keys/host.key
  -> install_id UUID v4 generated; system manifest computed and signed
  -> 12 canonical namespaces, service registry, and package registry seeded
  -> ogun-desktop.exe registered as the sole autostart entry (Task Scheduler)

boot time
  -> ogun-desktop.exe (user-facing launcher) starts ogun-emulator (Tauri app)
  -> ogun-emulator initializes four virtual devices:
       ogun-virtual-display-monitor, ogun-virtual-platform-host,
       ogun-virtual-cpu, ogun-virtual-network-adapter
  -> ogun-uefi performs four phases: Pre-Init → Device Init → Boot Menu → Handoff
  -> ogun-bootloader runs three-stage verification (image → manifest → host key)
  -> ogun-kernel-core reads ogun-host-service/ogun-component.toml (auto_start = true) and starts it as a kernel process
  -> ogun-host-service supervises host instances and drives session manager startup

runtime
  -> ogun-kernel-core initializes 15 subsystems in strict canonical order
  -> Three Tier-1 kernel services start (modules-manager, process-manager, ipc-broker)
  -> Session manager handles lock screen, authentication, and session context binding
  -> operator_id, workspace_id, enterprise_id, trace_id stamped on all processes
  -> OS apps, utility apps, user apps, modules, plugins, and extensions run
  -> ogun-cpu ticks all in-process components at 100 Hz base clock rate
  -> CleanShutdownMarker written as the absolute last act of every shutdown
```

---

## Main Layers

| Layer | Responsibility |
|---|---|
| Host OS | Provides real process, filesystem, window, socket, keychain, and platform APIs. |
| Emulator and virtual devices | Present stable virtual monitor, CPU, host platform, network adapter, and UEFI layers. `ogun-emulator-backend` is the sole component that calls host OS APIs directly. |
| Virtual UEFI | Software virtual UEFI firmware: splash screen, boot menu, variable store, secure boot policy, and `ExitBootServices()` handoff. |
| Bootloader and image format | Three-stage boot verification (image signature → system manifest → host key re-derivation) before any kernel code executes. |
| Host service | Persistent kernel process auto-started by `ogun-kernel-core` via its `ogun-component.toml` service manifest (`auto_start = true`); supervises host instances, drives crash recovery, coordinates clean shutdown. |
| Kernel core | Initializes 15 subsystems in canonical order; drives the 17-step boot sequence; owns the supervisor loop. |
| Session manager | Owns authentication, operator/workspace context, session snapshots, crash recovery, workspace switching, and clean shutdown. |
| SDKs | Define ABI-stable contracts for apps, services, modules, packages, plugins, drivers, hosts, and devices. |
| Components and apps | Tier-1 kernel services, Tier-2 OS apps, Tier-3 utility apps, Tier-4 user apps (personal enterprise suite). |
| Tools and artifacts | Build, inspect, install, repair, update, and publish signed runtime artifacts. |

---

## Boot Chain

```text
ogun-desktop.exe  (user-facing launcher; registered autostart entry)
  -> ogun-emulator  (Tauri 2.0+ application; main entry point)
      -> ogun-virtual-display-monitor   (Tauri WebviewWindow surface)
      -> ogun-virtual-platform-host     (filesystem, entropy, timers, process mgmt)
      -> ogun-virtual-cpu               (software-defined execution scheduler)
      -> ogun-virtual-network-adapter   (software-emulated NIC; NodeId via ed25519)
      -> ogun-uefi                      (virtual UEFI firmware; splash + boot menu)
      -> ogun-bootloader                (three-stage verification; KernelBootBundle)
      -> ogun-kernel-core               (15 subsystems; 17-step boot sequence)
          -> ogun-host-service          (persistent daemon; supervises host instances)
              -> ogun-session-manager   (auth; session context; workspace lifecycle)
                  -> Tier-1 kernel services (modules-manager, process-manager, ipc-broker)
                  -> Tier-2 OS apps         (desktop, shell, explorer, security-center, ...)
                  -> Tier-3 utility apps    (notes, tasks, focus, calendar, messenger, ...)
                  -> Tier-4 user apps       (enzo, kogi, dongo, ume, shango, igi, moto, ...)
```

Production boot must fail closed. Any failure in image authenticity, installation
integrity, ABI compatibility, or host key verification causes the bootloader to
`halt()` before any higher runtime code executes.

---

## Virtual UEFI Layer

`ogun-uefi` is a software virtual UEFI firmware layer called by `ogun-emulator`
after virtual hardware initialization. It does not emulate CPU registers, ACPI
tables, or interrupt vectors — it emulates the *conceptual* services UEFI
provides: a variable store, a device list, a boot order, and runtime services.

**Four sequential phases:**

| Phase | Description |
|---|---|
| Pre-Init | Receives initialized device handles from `ogun-os-emulator`; loads `~/.ogun/config/uefi/vars.bin`. |
| Device Init | Presents virtual devices to the UEFI services interface; renders ogun splash screen on virtual monitor. |
| Boot Menu | Opens a timed interrupt window (default 3s; configurable 1000–10000ms via `uefi.toml`). Operator may interrupt to access advanced boot settings. |
| Handoff | `ExitBootServices()` is called; variable store is locked; `UefiBootBundle` passed to `ogun-bootloader`. |

**UEFI invariants:**
- `set_variable` is locked unconditionally after `ExitBootServices()`; UEFI
  variables are immutable for the duration of every boot.
- Boot does not halt on a missing or corrupt variable store; a fresh default
  store is written and the operator is notified.
- Boot halts on a Secure Boot policy violation.
- Every phase transition and every error writes to `~/.ogun/logs/uefi-boot.log`.

---

## Three-Stage Boot Verification

The bootloader runs three sequential verification stages inside `ogun-kernel-core`
at the start of every new host instance. Any failure is fatal — `halt()` is
called with zero side effects; a descriptive entry is written to
`~/.ogun/logs/boot.log`.

**Stage 1 — Image authenticity:**
- `OGUNIMG\x00` magic and `OGUNEND\x00` end sentinel validated.
- Region 1 header self-hash (SHA-256 of bytes 0x00–0x9F) verified.
- ABI version in header must equal `OGUN_ABI_VERSION` (`u32`).
- Only `ImageKind::Platform` images are accepted; `Baseline` and `Patch` images halt boot.
- ed25519 signature over SHA-256(R1+R2+R3) verified against `image-verify.pub`.
- All required sections present; per-section SHA-256 hashes verified.

**Stage 2 — Install integrity:**
- `system-manifest.json` read; every manifest-covered file re-hashed.
- Manifest ed25519 signature verified against `system.pub`.
- Proves extracted binaries have not been tampered with since installation.

**Stage 3 — Host key re-derivation:**
```text
host_key = HKDF-SHA256(
    ikm:  image_pubkey_bytes ‖ system_pubkey_bytes,
    salt: install_id_bytes,
    info: "ogun-host-key-v1",
    len:  32
)
```
- Derived value compared to `~/.ogun/security/keys/host.key`.
- Mismatch means the image was updated outside the update flow, or
  the installation has been tampered with. Both are fatal.

---

## Kernel Subsystems

All 15 subsystems are implemented as separate `rlib` crates (`ogun-subsystem-*`)
statically linked into `ogun-kernel-core`. They initialize in strict canonical
order; a failure at any step calls `crash()` on the host instance. Subsystem
handles are `Arc<RwLock<_>>` shared across the supervisor loop, session manager,
and module contexts.

| Order | Subsystem | Reason for position |
|---|---|---|
| 1 | `ogun-subsystem-telemetry` | Must be first; all other subsystems emit telemetry through it. |
| 2 | `ogun-subsystem-memory` | Required before any allocation; OOM detection and pressure reporting. |
| 3 | `ogun-subsystem-process` | Required before concurrent activity; owns `ogun-cpu` virtual CPU and dynamic thread pool. |
| 4 | `ogun-subsystem-ipc` | Required before inter-subsystem messages; Elegua Protocol v0.3.0 bus. |
| 5 | `ogun-subsystem-storage` | Required before VFS needs to persist; RustyDB-backed WAL key-value store. |
| 6 | `ogun-subsystem-vfs` | Registers 12 canonical namespaces from `NamespaceSeed`; workspace-scoped filesystem views. |
| 7 | `ogun-subsystem-security` | Ọpọn Protocol enforcement begins here; all subsequent operations are governed. |
| 8 | `ogun-subsystem-services` | Service registry and baseline kernel service lifecycle records. |
| 9 | `ogun-subsystem-host` | Host driver event channels; `OgunHostDriver`/`OgunDisplayDriver` handle registration. |
| 10 | `ogun-subsystem-session` | Session context lifecycle, RBAC, authentication pipeline, multi-profile support. |
| 11 | `ogun-subsystem-display` | Display surfaces, themes, input routing, window management. |
| 12 | `ogun-subsystem-state` | Session snapshots, `CleanShutdownMarker`, crash scan on boot. |
| 13 | `ogun-subsystem-components` | `OgunModule` lifecycle, dynamic `cdylib` loading, ABI verification at every load boundary. |
| 14 | `ogun-subsystem-network` | OgunNet v2.0.0: Kademlia DHT, mDNS, gossip pub/sub, named channels, file transfer. |
| 15 | `ogun-subsystem-emulation` | `VirtualDeviceRegistry` and full lifecycle for all virtual devices; initializes last. |

---

## Execution Model

`ogun-cpu` is one of the four virtual devices initialized and managed by
`ogun-emulator`. It is a **software-defined execution scheduler** — not a
hardware emulator — that acts as the unified execution clock for every
in-process component in the ogun OS runtime.

**Key properties:**

- **Single binary, few threads by default.** The entire runtime runs in one OS
  process (`ogun-host-service`). Minimum thread count at idle: `1 main thread
  (Tauri) + 1–2 Tokio worker threads`. The pool expands only when actual work
  demands it.
- **All in-process components tick through ogun-cpu.** Tier-1 kernel services,
  Tier-2 OS apps (when in-process), modules, plugins, and extensions all share
  the same clock. No component runs its own background thread unless explicitly
  promoted to a worker task.
- **Tier-4 apps and OS-tier services are OS child processes.** They are managed
  by `ogun-subsystem-process` and communicate with the CPU through IPC only.
- **Dynamic scaling is transparent.** Components implement their tick function;
  the execution model handles parallelism.

**Default tick rate:** 100 Hz (one tick = 10ms). Configurable in
`ogun.toml [kernel.cpu]`.

### Component Rate Division

Every component declares a `RateDivisor` controlling how many base ticks must
elapse between each effective call to its `tick()` implementation:

| RateDivisor | Effective rate (@ 100 Hz base) |
|---|---|
| `Double(2)` | 200 Hz (burst slot — tick called 2× per base tick) |
| `Full(1)` | 100 Hz — called every base tick |
| `Half(2)` | 50 Hz — called every 2nd base tick |
| `Quarter(4)` | 25 Hz — called every 4th base tick |
| `Eighth(8)` | 12.5 Hz — called every 8th base tick |
| `Sixteenth(16)` | 6.25 Hz — called every 16th base tick |
| `Custom(n)` | (100/n) Hz — arbitrary integer divisor |

### Eight Canonical Component Lifecycle Modes

Every component that participates in ogun OS execution exposes exactly eight
canonical lifecycle modes. These are the only modes the ogun-cpu understands.
They form a deterministic state machine.

| Mode | Alias | Description |
|---|---|---|
| `init` | — | Memory allocated, invariants established; no external calls. |
| `configure` | — | Receives configuration; reads `config://` namespace paths. |
| `start` | — | Heavy initialization: opens handles, registers IPC channels, subscribes to events. |
| `tick` | `update` | Main per-tick work; must complete within the timeslice (default 10ms). |
| `pause` | `soft stop` | Suspends active behavior; preserves all state in memory; tick calls cease. |
| `freeze` | `hard stop` | Serializes full state via `on_snapshot()`; releases expensive resources. |
| `reset` | `restart` | Tears down and re-runs `init → configure → start`; used for crash recovery. |
| `shutdown` | — | Flushes state, closes connections, releases all resources; removed from registry. |

**Valid state transitions:**
```text
init → configure → start → tick ↔ pause → freeze → (thaw) → start
                              ↓                    ↓
                            crash              shutdown
                              ↓
                          recovering → start (with backoff)
                              ↓ (max restarts exceeded)
                          terminated
```

### Priority Bands

| Band | Label | Execution lane |
|---|---|---|
| P0 | Critical kernel | Synchronous on CPU's own Tokio task — never deferred |
| P1–P4 | Normal | Dynamic Tokio thread pool |
| P5–P7 | Background | Pool workers with BackgroundYieldGate; tick at lower effective rate |

**Starvation guard:** any component skipped for more than `starvation_threshold`
ticks (default 200) is temporarily promoted to P0 for one tick, then returns to
its original priority.

**Panic isolation:** every component tick is wrapped in
`std::panic::catch_unwind(AssertUnwindSafe(...))`. A panicking component never
crashes the execution loop or any other component.

### Dynamic Thread Pool

The ogun-cpu manages a dynamic Tokio worker pool:

| Parameter | Default | Description |
|---|---|---|
| `min_worker_threads` | 1 | Pool never shrinks below this. |
| `max_worker_threads` | `num_cpus - 1` | Hard ceiling; Tauri main thread is reserved. |
| `scale_up_queue_depth` | 8 | Pending ticks that trigger scale-up. |
| `scale_up_utilization_pct` | 0.80 | Worker utilization fraction that triggers scale-up. |
| `scale_down_utilization_pct` | 0.30 | Utilization fraction threshold for scale-down. |
| `scale_down_cooldown_ms` | 5000 | Duration below threshold before a worker is removed. |
| `starvation_threshold` | 200 | Ticks skipped before starvation guard promotes to P0. |
| `timeslice_ns` | 10,000,000 | Nominal time budget per component per tick (10ms). |

Scale-up adds at most one worker per monitor cycle. Scale-down removes at most
one worker per cooldown period. No in-flight tick is ever interrupted.

### Armed Message Communications

Components *arm* outbound messages (unicast, broadcast, multicast) into a
staging area during their `tick()`. At the end of the tick slot, the armed queue
is flushed — delivering inbound messages and routing outbound ones. This keeps
all message I/O inside the component's tick boundary and prevents mid-tick races
across the shared IPC bus.

### Process Control Block (PCB)

The kernel maintains a `ProcessControlBlock` for every in-process component:

- **Identity:** `pid`, `component_id`, `operator_id`, `workspace_id`, `trace_id`
- **Scheduling:** `last_tick_at`, `skipped_ticks`, `total_ticks`, `cpu_time_ns`, `inbox`
- **Lifecycle:** `state`, `restart_count`, `crash_at`, `created_at`

A `PcbTable` secondary index inside `ComponentSubsystem` provides
`ProcessId → ComponentId` resolution in O(1).

---

## Communication

The **Elegua Protocol** (v0.3.0) is the canonical communication protocol. Named
after Èṣù-Ẹlẹ́gbára — the Yoruba orisha of crossroads and communication — it is
the unified specification for all component-to-component, layer-to-layer, and
process-to-process communication in ogun OS.

Every message carries: `operator_id`, `workspace_id`, `enterprise_id`,
`trace_id`, `span_id`, `protocol_version`, `timestamp`, `from`, `to`,
`correlation_id`, `sender_pid`, `kind`, `payload`, and `priority`.

**Supported patterns:** unicast · multicast · broadcast · request/reply · pub/sub

**Core IPC channels** (registered at boot, live for the entire session):

| Channel | Key messages |
|---|---|
| `ogun.host` | `phase.changed`, `status.changed`, `ready`, `crashed`, `shutdown_completed` |
| `ogun.session` | `session.started`, `operator.login`, `workspace.switched`, `context.updated` |
| `ogun.system` | `snapshot.written`, `crash.report`, `update.available`, `config.updated` |
| `ogun.security` | `capability.granted`, `capability.denied`, `opn.violation` |
| `ogun.apps` | `app.launched`, `app.terminated`, `app.crashed`, `app.installed` |
| `ogun.network` | `peer.connected`, `peer.disconnected`, `channel.opened` |
| `ogun.emulation` | `device.provisioned`, `device.terminated`, `registry.updated` |

**Communication rules:**
- Do not introduce silent side channels between runtime components.
- Do not pass raw untyped bytes across layer boundaries when an Elegua message
  or SDK type exists.
- Preserve workspace and enterprise context when forwarding messages.
- Route external ingress through explicit gateway, host, driver, or tool
  boundaries.
- `enterprise_id` must be present in all IPC messages after session context bind
  (Step 12 of the boot sequence).

---

## Security Model

Security depends on three layered keys and enforced protocol rules.

### The Three Keys

**Image Key** — ed25519 keypair owned exclusively by the CI build pipeline.
Private key never leaves the CI secrets vault. Public key embedded in every
`.img` file as the `ImageVerifyKey` section, extracted to
`~/.ogun/security/keys/image-verify.pub` at install time, and verified by the
bootloader on every boot.

**System Key** — ed25519 keypair generated by `ogun-installer` exactly once at
first installation. Private key stored in the host OS keychain (Windows DPAPI)
only — never in `~/.ogun/`. Public key at `~/.ogun/security/keys/system.pub`
(0o444). Signs the system manifest covering every security-critical extracted
file. Persists across image updates.

**Host Key** — 32-byte derived key (not a keypair) computed via HKDF-SHA256
from the image public key, system public key, and `install_id`. Unique per
image+installation pair; deterministic; changes when the image is updated;
stamped on every telemetry event, audit log entry, IPC message, and capability
grant. Verified by the bootloader on every boot (Stage 3).

### Cryptographic Primitives

- **ed25519** via `ring` v0.17 — image and manifest signing/verification
- **SHA-256** via `sha2` v0.10 — per-section checksums and self-hashes
- **HKDF-SHA256** — host key derivation
- **zstd level 19** — section compression
- **AES-256-GCM** — audit log encryption and OgunNet per-session encryption
- **X25519 ECDH** — OgunNet session key exchange

### Ọpọn Protocol

Named after the Ọpọn Ifá — the Yoruba divination tray, upon which no reading for
one supplicant may be contaminated by the marks of another — the Ọpọn Protocol
is the cross-enterprise data isolation system enforced at the kernel Security
subsystem.

`opn_enforced = true` is reset unconditionally after every `ogun.toml` load. No
operator, app, or IPC message can disable it.

**Five immutable rules:**

| Rule | Description |
|---|---|
| `opn-001` | Enterprise namespace isolation: data tagged `enterprise_id = A` cannot be read by a process with `enterprise_id = B` without an explicit cross-enterprise grant. |
| `opn-002` | Agent authority bounds: agents may not execute actions outside their declared authority level without operator approval. |
| `opn-003` | Contract-before-active enforcement: enterprise workflows in active/billable states require an associated contract record. |
| `opn-004` | Revenue attribution integrity: revenue events must carry a valid `attribution_id` traceable to an operator-verified source. |
| `opn-005` | Extension approval gate: extensions require `operator_approved_at` in their manifest before `dlopen`. |

Every capability grant or denial is written to the audit log
(`~/.ogun/security/audit.log`, AES-256-GCM encrypted) *before* the operation
completes.

### Capability System

Every process has a capability set declared in its `ogun-component.toml`
manifest and checked by `ogun-subsystem-security` at the point of every system
call. Capability tiers are inherited from `capability-defaults.json` (read-only
after installation) and can only be narrowed — never widened — by operator
policy.

---

## Storage and Namespaces

`ogun-subsystem-storage` uses **RustyDB** — a Rust-native embedded database
with a write-ahead log (WAL) — as the backend. Used by session state
persistence, OgunNet node identity storage, operator records, module registry,
security audit log indexes, and DHT seed persistence.

`ogun-subsystem-vfs` registers exactly **12 canonical namespace schemes** at
boot Step 6 from the image's `NamespaceSeed` section:

```text
ogun://         system://       user://         security://
app://          data://         network://      agent://
enterprise://   workspace://    session://      telemetry://
```

Each namespace is a hierarchical address space resolvable via `OgunPath`.
Namespace paths are the canonical way all components address resources — no raw
filesystem paths are used outside the `ogun-types::paths` module.

Virtual device VFS registrations:
```text
device://vdev/monitor/<id>    (virtual display monitors)
device://vdev/network/<id>    (virtual network adapters)
device://vdev/host/<id>       (virtual host instances)
```

Generated installation state belongs under `~/.ogun/`, not in source
workspaces. Private keys and local secrets must never be committed.

---

## Session Management

The session manager (`ogun-session-manager`, `rlib` inside `ogun-kernel-core`)
owns the full user-space lifecycle from lock screen to clean shutdown.

**`ActiveSessionContext`** — live runtime session record:
```rust
pub struct ActiveSessionContext {
    pub operator_id:    Uuid,
    pub enterprise_id:  Uuid,
    pub workspace_id:   Uuid,
    pub session_id:     Uuid,
    pub host_key:       HostKey,
    pub started_at:     u64,
    pub boot_trace_id:  Uuid,
}
```

From Step 12 of the boot sequence onward, every process spawned is stamped with
all four context identifiers. The IPC broker uses them to enforce workspace
isolation routing.

**Authentication pipeline by platform:**

| Platform | Primary | Secondary |
|---|---|---|
| Desktop | Passkey (FIDO2) | TOTP/2FA |
| Web | WebAuthn (`navigator.credentials`) | — |
| Mobile iOS | FaceID / TouchID | PIN |
| Mobile Android | Fingerprint | PIN |
| Device | Hardware (NFC / PIN pad / certificate) | Device-specific |
| Server | Skipped | Skipped |

**Workspace switching:** freezes departing workspace apps, saves
`WorkspaceSessionRecord`, activates target workspace, restores its running apps.
IPC broker updates routing rules.

**Session snapshot:** written on configurable schedule (default 60s), on clean
shutdown, and on workspace/profile switch. Format: MessagePack-serialized
`SessionSnapshotState`, zstd-compressed.

**Crash recovery:** triggered by missing `CleanShutdownMarker` at boot. Loads
most recent valid snapshot; queues crash report to `ogun-system-manager`.

**Multi-enterprise support:** operators may hold multiple enterprise profiles
with independent workspace sets. Profile switching updates `enterprise_id` in
session context and requires re-authentication. Ọpọn Protocol enforces
cross-enterprise data isolation at the IPC broker and Security subsystem.

---

## Clean Shutdown Sequence

```text
1.  ipc://host/shutdown received → host transitions to ShuttingDown
2.  Tier-4 user apps receive ComponentMode::shutdown (grace period: 5s default)
3.  Tier-2–3 OS apps shut down in reverse load-order
4.  OS-tier services shut down in reverse load-order
5.  Session manager writes final session state and snapshot
6.  IPC channels drained and closed
7.  Tier-1 kernel services shut down
8.  15 kernel subsystems tear down in reverse initialization order
9.  Telemetry flushed
10. CleanShutdownMarker written  ← absolute last act
11. lifecycle.shutdown_completed broadcast; process exits 0
```

---

## Network Layer (OgunNet v2.0.0)

The network subsystem is split into three properly scoped components:

| Component | Kind | Layer |
|---|---|---|
| `ogun-subsystem-network` | `rlib` | Kernel Subsystem 14 — owns all P2P protocol logic |
| `ogun-virtual-network-adapter` | `rlib` | Sub-component of Network Subsystem — owns NodeId, session key derivation, framing, handshake |
| `ogun-virtual-network-driver` | `rlib` | Driver (Host Abstraction Layer) — pure TCP/UDP/DNS/TLS translation; no P2P logic |

**Transport:** TCP with 4-byte big-endian length-prefix framing; max message
size 4 MiB.

**Encryption:** X25519 ECDH key exchange with Ed25519-signed DH public keys →
per-session AES-256-GCM. All `Data`, `Chat`, `ChannelMsg`, and `FileChunk`
payloads encrypted.

**Node identity:** `NodeId = SHA-256(verifying_key ‖ "ogunnet-node-id-v1")`;
Ed25519 signing key persisted via `ogun-subsystem-storage`; stable across
restarts; human-readable alias (`adjective-noun-NNN`).

**Discovery:**
- Kademlia DHT: 256-bucket XOR-metric routing table, k=20, α=3 parallel
  lookups; `put`/`get` with 1-hour TTL; iterative `FindNode` lookup.
- mDNS: UDP multicast on `239.255.17.170:17171`; `LocalAnnounce` every 30s.
- Peer Exchange (PEX): routing table shared with all connected peers every 60s.

**Features:** gossip pub/sub (flood propagation with TTL decrement; 2048-entry
seen-cache), IRC-style named channels (AES-256-GCM key from channel name),
chunked encrypted file transfer (64 KiB chunks; SHA-256 integrity), relay-assisted
NAT punch, reputation and ban system (auto-ban at threshold −10).

**Rate limiting:** max 5 new inbound connections per IP per 60s; handshakes
must complete within 10s.

---

## Component Boundaries

- SDK crates define contracts; runtime crates enforce them.
- Apps do not call kernel internals directly — only SDK trait methods.
- Modules use `ModuleContext` APIs, not arbitrary subsystem references.
- Drivers translate platform APIs into ogun traits and do not call upward into
  app or service layers.
- `ogun-emulator-backend` is the **sole** component that calls host OS APIs
  directly (WinAPI, POSIX, Bionic, web-sys). No component above it — including
  `ogun-uefi`, `ogun-bootloader`, drivers, kernel, session manager, or apps —
  calls host OS APIs directly.
- Host OS APIs are isolated to hosts, drivers, emulator backend, setup, and
  tooling.
- Tools can inspect and build artifacts but must not weaken runtime security
  assumptions.
- Virtual devices are rlib components in a single process; never spawned as
  separate OS processes.
- Tauri owns the main thread. No Tauri window is created in a child process.

---

## App Tiers

ogun OS organizes all executable components into a strict tier hierarchy. Tier
determines privilege, sandbox level, SDK access, and execution model.

| Tier | Name | SDK | Execution | Privilege |
|---|---|---|---|---|
| 1 | Kernel Services | `ogun-kernel-sdk` | Tokio tasks in-process; P0 | Full kernel access |
| 2 | OS Apps | `ogun-app-sdk` (elevated) | OS child processes; P2 | Session manager access |
| 3 | Utility Apps | `ogun-app-sdk` | OS child processes; P3 | Standard operator access |
| 4 | User Apps | `ogun-app-sdk` | OS child processes | Standard operator access |

Non-app component types (not tiers):
- **Drivers** — Host Abstraction Layer; depend only on `ogun-driver-sdk`; statically linked per platform.
- **Modules** — Kernel Extension Layer; loaded as `cdylib` at boot; extend kernel behavior; depend on `ogun-kernel-sdk`.
- **Plugins** — OS Feature Addition Layer; extend OS app functionality without replacing defaults.
- **Extensions** — OS Behavior Override Layer; replace default OS behaviors; require explicit operator approval (`opn-005`).
- **Shell Packages** — extend `ogun-shell` with new commands via `OgunPackage` trait.

### Tier-1 Kernel Services

| Service | Responsibility |
|---|---|
| `ogun-modules-manager` | Kernel module lifecycle: load, initialize, tick, unload. |
| `ogun-process-manager` | Process table management, PCB tracking, scheduling coordination. |
| `ogun-ipc-broker` | Elegua Protocol message routing; workspace and enterprise isolation enforcement. |

### Tier-2 OS Apps

`ogun-app-manager` · `ogun-command-center` · `ogun-command-palette` ·
`ogun-desktop` · `ogun-explorer` · `ogun-operator-center` · `ogun-profile-center` ·
`ogun-security-center` · `ogun-settings-center` · `ogun-shell` ·
`ogun-system-manager` · `ogun-ui` · `ogun-workspaces`

### Tier-3 Utility Apps

`ogun-assistant` · `ogun-calendar` · `ogun-contactbook` · `ogun-focus` ·
`ogun-messenger` · `ogun-notes` · `ogun-search-engine` · `ogun-tasks`

### Tier-4 User Apps — Personal Enterprise Suite

| App | Role |
|---|---|
| `enzo` | Personal Enterprise Management — enterprise creation, KPI dashboards, portfolio tracking. |
| `kogi` | Software-Defined Office — pipeline management, engagement tracking, desk intelligence. |
| `dongo` | Financial Management — multi-currency wallets, double-entry accounting, tax reserve. |
| `ume` | Organization Operating System — legal entities, contracts, cap tables, SOPs. |
| `heshima` | Identity Management — credentials, verification, reputation, linktree, OgunNet identity. |
| `shango` | Solution Factory — build environments, solution lifecycle, CI/CD, distribution. |
| `igi` | Portfolio Management — asset tracking, EVS computation, passive income trajectory. |
| `moto` | Project and Program Management — milestones, deliverables, tasks. |
| `akeel` | Knowledge Management — documentation, research, institutional memory. |
| `zamani` | Estate Management — physical asset management, wealth systems, estate planning. |
| `orun` | Semantic Filesystem Runtime — enterprise-linked namespace paths, VFS. |
| `mizeez` | Version and Change Control — artifact versioning, change management. |
| `shaba` | Strategic Management — OKRs, roadmap, strategic intent tracking. |
| `kanna` | Governance Management — hubs, policies, standards, cooperative governance. |
| `qala` | Observatory and Analytics — metrics, insights, telemetry, scenario modeling. |
| `sambara` | Agent Management System — autonomous agents, authority levels, orchestration. |
| `zuri` | Digital Marketplace — store management, listing distribution, buyer discovery. |
| `didara` | IP Tracking and Management — patents, trademarks, licensing, royalties. |
| `apapo` | Hypergrid Domain Operating System Dev Platform. |
| `ayo` | Digital Spaces Management — independent worker social platform. |

---

## Agent System (Sambara)

**Sambara** is the AI agents operating system embedded within ogun OS. Agents
are first-class runtime entities with kernel-level identity (`agent_id`),
workspace-bounded execution, operator-governed authority, and a continuously
improving intelligence model. Every agent action is written to
`~/.ogun/logs/agent-actions.log` (encrypted at rest) *before* the action
completes. Agents cannot bypass or inspect their own governance block.

**Agent authority levels:**

| Level | Capability |
|---|---|
| `OBSERVE` | Read-only; monitors and contributes to MetricSnapshots; no actions. |
| `RECOMMEND` | Generates `InsightRecord`s and drafts for operator review; no automated actions. |
| `EXECUTE_BOUNDED` | Takes actions within explicitly declared parameter ranges; exceptions escalate. |
| `FULL_AUTONOMY` | Operates within declared domain without per-action approval; requires `OPTIMIZED` lifecycle stage. |

Authority escalation cannot be triggered by agent logic, policy rules, or
Observatory recommendations — it requires explicit operator interaction.

**LLM Drivers:** Sambara is model-agnostic. Built-in drivers: `anthropic-claude`
(`claude-opus-4-6`, `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`) ·
`openai-chatgpt` (`gpt-4o`, `o1`, `o3-mini`) · `deepseek`
(`deepseek-chat`, `deepseek-reasoner`) · `ollama-local` (any locally served
model). Custom drivers can be registered by operators on the `ENTERPRISE`
governance tier.

---

## SDK Surface

| Crate | Purpose |
|---|---|
| `ogun-types` | Zero-dependency foundational types — `ProcessId`, `OperatorId`, `WorkspaceId`, `EnterpriseId`, `TraceId`, `OGUN_ABI_VERSION`, binary format constants. No ogun crate depends on another ogun crate to resolve `ogun-types`. |
| `ogun-app-sdk` | `OgunApp` trait — `on_init`, `on_configure`, `on_start`, `on_tick`, `on_message`, `on_pause`, `on_freeze`, `on_reset`, `on_shutdown`; `AppMetadata`; capability declaration types. |
| `ogun-service-sdk` | `OgunService` trait for OS-tier services. |
| `ogun-kernel-sdk` | `OgunModule` trait and `ModuleContext` for kernel-level module authors; capability-gated subsystem handle access. |
| `ogun-driver-sdk` | `OgunHostDriver`, `OgunDisplayDriver`, `OgunVirtualDriver` traits; driver event channel types. |
| `ogun-host-sdk` | `OgunHost` trait — `boot`, `shutdown`, `enter_recovery`, `active_session`, `snapshot_session`, `spawn_process`, `check_capability`, `enforce_opn`, `publish`, `ns_read`, `ns_write`; `HostType` enum. |

---

## Configuration

| File | Description |
|---|---|
| `ogun.toml` | Primary runtime configuration — boot, kernel, CPU scheduler, network, session, storage, telemetry, security. `validate_image_signature` treated as `true` unconditionally in production. |
| `display.toml` | Display and theming — theme name, color scheme, accent color, window dimensions, fonts. |
| `emulation.toml` | Emulation layer — virtual device auto-provisioning, virtual host nesting depth (max 10), virtual monitor and network adapter settings. |
| `uefi.toml` | Virtual UEFI — boot menu interrupt window (1000–10000ms; 0 treated as 3000ms), virtual Secure Boot policy, UEFI boot log path. |

`opn_enforced` in `security/opn-policy.json` is reset to `true` unconditionally
after every `ogun.toml` load.

### Key `ogun.toml` sections

```toml
[kernel.cpu]
tick_rate_hz              = 100
min_worker_threads        = 1
max_worker_threads        = 0       # 0 = auto (num_cpus - 1)
scale_up_queue_depth      = 8
scale_up_utilization_pct  = 0.80
scale_down_utilization_pct = 0.30
scale_down_cooldown_ms    = 5000
starvation_threshold      = 200
timeslice_ns              = 10_000_000

[network]
port                      = 17170
mdns_enabled              = true
pex_enabled               = true
max_peers                 = 50

[session]
snapshot_interval_ms      = 60000
lockout_threshold         = 5
lockout_duration_ms       = 300000

[security]
opn_enforced              = true    # always reset to true; cannot be disabled
audit_log_encrypted       = true
```

---

## Release Artifacts (0.1.0-beta, Windows x64)

| Artifact | Description |
|---|---|
| `ogun-setup-windows-0.1.0-beta.exe` | `ogun-setup.exe` — manages ogun OS images and OS installation; nine-step pipeline; silent install mode available. |
| `ogun-desktop-windows-0.1.0-beta.exe` | `ogun-desktop.exe` — user-facing launcher; starts ogun OS; manages image modification, repair, and update. |
| `ogun-emulator-windows-0.1.0-beta.exe` | `ogun-emulator` — main entry point (Tauri application); initializes virtual hardware; runs boot chain through to `ogun-kernel-core`. |
| `ogun_desktop_windows-windows-0.1.0-beta.exe` | `ogun-host-service` for Windows — all subsystems statically linked; Authenticode-signed. |
| `ogun-windows-0.1.0-beta.img` | Signed platform kernel image — sections: `KernelCore`, `SessionManager`, `BootConfig`, `SystemManifest`, `Modules`, `Assets`. |
| `ogun_image_tool-windows-0.1.0-beta.exe` | `ogun-image-builder` — produces signed `.img` files for CI and local developer use. |

---

## On-Disk Security Layout

```text
~/.ogun/                          (0o700 — owner only; no directory is world-readable)
│
├── kernel/
│   ├── ogun-kernel.img           (0o640) — boot-time trust anchor
│   ├── installation.json         (0o440) — install_id, key fingerprints
│   └── version.json              (0o640)
│
├── security/
│   ├── keys/
│   │   ├── image-verify.pub      (0o444) — 32-byte ed25519 pubkey (image key)
│   │   ├── system.pub            (0o444) — 32-byte ed25519 pubkey (system key)
│   │   └── host.key              (0o400) — 32-byte derived host key
│   ├── system-manifest.json      (0o444) — hash table of all critical files
│   ├── system-manifest.sig       (0o444) — ed25519 sig over manifest
│   ├── opn-policy.json           (0o444) — Ọpọn Protocol policy (immutable after install)
│   ├── capability-defaults.json  (0o444) — capability tier ceilings (immutable after install)
│   └── audit.log                 (0o640) — AES-256-GCM encrypted
│
├── config/
│   ├── ogun.toml                 — primary kernel configuration
│   ├── display.toml              — display subsystem configuration
│   ├── emulation.toml            — emulation layer configuration
│   └── uefi.toml                 — UEFI layer configuration
│
└── logs/
    ├── boot.log                  (0o640) — written by bootloader on halt or start
    ├── uefi-boot.log             (0o640) — written by ogun-uefi on every phase transition
    └── agent-actions.log         (0o640) — encrypted; written before every agent action
```

The system key private half is stored exclusively in the host OS keychain
(Windows DPAPI). It never appears under `~/.ogun/`.

---

## Release Scope Discipline

For `0.1.0-beta`, **Windows x64 Desktop Edition** is the release target. Linux,
macOS, web, server, mobile, and device editions may have design or scaffolding
work, but must not be documented as shipped unless release artifacts and tests
exist.

When a change affects beta scope, update:

- `CHANGELOG.md`
- `ogun-docs/0.1.0-beta-release/`
- relevant workspace `README.md` files
- artifact expectations in `ogun-artifacts/`

Planned post-beta targets: macOS Apple Silicon, Linux x86_64 (Desktop Edition);
Android arm64, iOS arm64 (Mobile Edition, in progress); browser WASM (Web
Edition); headless Linux (Server Edition); IoT/embedded (Device Edition).

---

## Non-Negotiable Invariants

The following invariants are unconditional. No configuration switch, operator
setting, runtime flag, or IPC message can disable them.

**Boot and image integrity:**
- Production boot verifies image ed25519 signature on every boot before anything else executes.
- `validate_image_signature` is treated as `true` unconditionally in all production builds; it cannot be set to `false`.
- Only `ImageKind::Platform` images are bootable; `Baseline` and `Patch` images halt boot unconditionally.
- ABI version mismatches reject components at every load boundary.
- End sentinel `OGUNEND\x00` must be present — no truncated images.
- All bootloader-required sections must be present and hash-valid.
- System manifest signature verified on every boot (Stage 2).
- Host key re-derived and compared on every boot (Stage 3).
- Any stage failure calls `halt()` with zero side effects before exit.
- `ImageFlags::SIGNATURE_REQUIRED` is always set in production images.

**Security and keys:**
- `opn-policy.json` is read-only (0o444) after install; `opn_enforced` is reset to `true` after every `ogun.toml` load.
- Ọpọn Protocol is enforced unconditionally; it cannot be configured away.
- Every capability grant and denial is written to the audit log *before* the result is returned.
- `host_key` is stamped on every telemetry event and every audit log entry.
- No directory under `~/.ogun/` is world-readable (0o700 minimum).
- System key private half never appears in `~/.ogun/`; keychain only.
- Private signing keys are never committed to source.

**Runtime architecture:**
- ABI version is checked at every module, driver, app, and extension load boundary.
- `CleanShutdownMarker` is written as the absolute last act of every shutdown; its absence at boot unconditionally triggers crash recovery.
- `ogun-desktop.exe` is the only autostart entry; exactly one Task Scheduler entry per machine.
- `set_variable` is locked after UEFI `ExitBootServices()`; UEFI variables are immutable for the duration of every boot.
- Virtual network adapters use OS sockets only — no raw packet injection.
- Virtual monitor renders via Tauri surfaces only — no direct framebuffer writes.
- Virtual host nesting depth ≤ configured maximum (≤ 10).
- `ogun-emulator-backend` is the only component that calls host OS APIs directly; nothing above it touches WinAPI, POSIX, Bionic, or web-sys.
- Lower layers do not depend on higher layers.
- Generated release artifacts are never overwritten in place.

**Execution model:**
- P0 components always tick synchronously on the ogun-cpu's own Tokio task; they cannot be deferred to the pool.
- Every component tick is wrapped in `catch_unwind`; a panicking component never crashes the execution loop or any other component.
- The thread pool never exceeds `max_worker_threads` and never drops below `min_worker_threads`.
- No in-flight tick is interrupted; scale-down closes worker channels and waits for the current work item to complete.
- `operator_id`, `enterprise_id`, `workspace_id`, and `trace_id` are mandatory on every process and every Elegua message after Step 12 of the boot sequence.
- Apps and services depend only on `ogun-app-sdk` / `ogun-service-sdk`; they have zero visibility into kernel internals, driver handles, or the UEFI variable store.
- Extensions require explicit operator approval (`opn-005`) before `dlopen`; absence of `operator_approved_at` blocks loading and logs to the audit trail.s

---

# OS Design part II

# ogun OS — Design Document

**Version:** 0.1.0-beta
**Project:** Ogún · 2026
**Owner:** Dominic Eaton (@eatondo)
**Status:** Canonical Design Reference

---

## Canonical Runtime Architecture

The canonical boot and runtime chain for the ogun OS beta runtime is:

```
ogun-desktop.exe
  → ogun-emulator
    → virtual devices
      → ogun-uefi
        → ogun-bootloader
          → ogun-kernel-core
            → ogun-host-service
              → ogun-host-client
                → ogun-session-manager
                  → ogun-user-apps
```

### Component Definitions

**`ogun-desktop.exe`** — Main OS executable and user-facing launcher. The only binary registered as the host OS autostart entry (via Task Scheduler on Windows, launchd on macOS, systemd user service on Linux). Responsible for:
- Launching `ogun-emulator` as a Tauri application
- Managing ogun OS image modifications, repairs, and updates
- Registered by `ogun-setup.exe` as the single autostart entry per machine

**`ogun-emulator`** — Handles the entire OS runtime and lifecycle. The main entry point of the ogun OS application; a Tauri 2.0+ application. Owns and manages:
- Top-level supervision of the entire ogun OS runtime
- Initialization of all virtual devices before handing off to `ogun-uefi`
- The Tauri event loop on the main thread (no Tauri window is created in a child process)
- Passing the boot chain to `ogun-bootloader` and then `ogun-kernel-core` after UEFI handoff

**Virtual Devices** — Handle low-level interface functionality between the ogun platform and the target host platform (Windows, Linux, macOS, Redox, etc.). Initialized by `ogun-emulator` before the boot sequence begins. Four virtual devices:

- **`ogun-virtual-display-monitor`** — Virtual display surface; pushes frames to the Tauri `WebviewWindow` on desktop. Renders exclusively via Tauri surfaces — no direct framebuffer writes.
- **`ogun-virtual-platform-host`** — Virtual filesystem, entropy, timers, shell execution, and process management. Platform-specific implementations per host OS. The only layer that calls host OS APIs (`WinAPI`, `POSIX`, `Bionic`, `web-sys`) directly — no component above it does so.
- **`ogun-virtual-cpu`** — Software-defined execution scheduler (not a hardware emulator). Acts as the unified execution clock for every in-process component in the runtime. Managed by the emulator alongside the other virtual devices; kernel-level scheduling coordinated through `ogun-subsystem-process`.
- **`ogun-virtual-network-adapter`** — Software-emulated NIC. Owns a `NodeId` (ed25519-derived P2P address); presents an addressable endpoint to the network subsystem. Uses OS sockets only — no raw packet injection.

**`ogun-uefi`** — Handles boot startup. A virtual UEFI firmware layer — the first ogun-specific component that executes after the emulator has initialized virtual hardware. Provides the conceptual equivalent of UEFI services for the ogun OS virtual hardware stack:
- Splash screen and boot progress UI
- Timed boot menu interrupt window (default 3 s; configurable 1–10 s)
- Virtual BIOS/CMOS variable store (locked after `ExitBootServices()`)
- Receives initialized virtual device handles from the emulator
- Hands the initialized `UefiBootBundle` to `ogun-bootloader`

**`ogun-bootloader`** — Handles image integrity verification and kernel loading. An `rlib` crate linked into `ogun-kernel-core`; called at the start of each new `ogun-host` instance via `ogun_bootloader::run()`. Performs three-stage boot verification before assembling the `KernelBootBundle` for handoff to the kernel:
- **Stage 1 — Image authenticity:** Verifies the ed25519 signature of `ogun-kernel.img` against `image-verify.pub`; checks magic bytes, end sentinel, header self-hash, ABI version, `ImageKind::Platform` constraint, and all section hashes.
- **Stage 2 — Install integrity:** Re-hashes every security-critical file listed in `system-manifest.json` and verifies the manifest's ed25519 signature against `system.pub`.
- **Stage 3 — Host key re-derivation:** Re-derives the `HostKey` via `HKDF-SHA256` from `image_pubkey_bytes ‖ system_pubkey_bytes` and compares it to the stored `host.key`. Any mismatch is fatal.

Any verification failure calls `halt()` — nothing else runs.

**`ogun-kernel-core`** — Handles OS kernel space runtime functionality. An `rlib` crate that is the central runtime binary. Receives the `KernelBootBundle` from the bootloader and runs for the entire session lifetime. Owns and drives:
- All 15 kernel subsystems (initialized in strict canonical order)
- The 17-step boot sequence from step 7 onward
- Kernel module loading (`auto_load` modules via `dlopen`)
- Reading `ogun-component.toml` service manifests and auto-starting services marked `auto_start = true` (including `ogun-host-service`)
- Tier 1 kernel service startup (`ogun-modules-manager`, `ogun-process-manager`, `ogun-ipc-broker`)
- Lock screen presentation and IPC channel registration
- The `HostServicePhase` state machine (22-variant enum)
- The supervisor loop (ticks `ogun-cpu`, drains IPC, health-checks processes, manages snapshots, checks watchdog)

The 15 kernel subsystems (initialized in order): Telemetry+Logging → Memory → Process+Scheduler → IPC+Event Bus → Storage+Backup → File+VFS+Namespace → Security+Governance → Services → Host+Drivers → Session+Account+RBAC → Display+UI+Window → State+Snapshot+Recovery → Components (Modules) → Network (OgunNet v2.0.0) → Emulation.

**`ogun-host-service`** — Handles ogun-host management, host client supervision and orchestration. A kernel process declared in its `ogun-component.toml` manifest with `auto_start = true` and `kind = "kernel-service"`; the kernel reads this manifest during boot and auto-starts `ogun-host-service` as a managed kernel process. Responsibilities:
- Creating, starting, supervising, and shutting down `ogun-host` instances
- Monitoring the `ogun.host` IPC channel for phase change events and health reports
- Crash detection and restart (up to `max_restart_attempts`, default 3, with exponential backoff)
- Coordinating clean shutdown on host OS shutdown signals
- Loading `~/.ogun/config/ogun.toml` and distributing `BootConfig` to each host instance
- Writing the `system://` namespace root (`system://host/phase.json`, `system://boot/config.json`)
- On server platforms: managing the `TenantRegistry`

`ogun-host-service` is not a user-facing autostart entry — it is a kernel-managed process launched automatically by `ogun-kernel-core` during boot because its `ogun-component.toml` declares `auto_start = true`. `ogun-desktop.exe` is the only binary registered as the host OS autostart entry; it starts the emulator, which runs the boot chain through to the kernel, which reads the service manifest and starts the host service.

**`ogun-host`** (host client) — Handles user space runtime functionality. A complete, isolated ogun OS runtime instance managed by `ogun-host-service`. Each instance contains:
- `ogun-uefi` — virtual UEFI layer, runs before the bootloader
- `ogun-bootloader` — three-stage verification; produces `KernelBootBundle`
- `ogun-kernel-core` — 15 subsystems; drives boot from step 7 onward; runs the supervisor loop
- `ogun-session-manager` — operator auth, session context, workspace state, OS-tier service lifecycle
- All running processes — every Tier 1–4 process is a child of the host instance

The host instance is the unit of restart. Crashing an individual app does not crash the host instance. Crashing the host instance causes the host service to create a new one. The host service itself is never restarted by a host instance crash.

**`ogun-session-manager`** — Handles user session management, login, authentication, user space applications and packages. An `rlib` crate linked into `ogun-kernel-core`. Activated at boot Step 10 via `SessionStartBundle`. Owns:
- Operator authentication (passkey + TOTP/2FA on Desktop; WebAuthn on Web; biometric on Mobile)
- `ActiveSessionContext` construction and binding (`operator_id`, `workspace_id`, `enterprise_id`, `session_id`)
- OS-tier service lifecycle (`ogun-security-manager`, `ogun-system-manager`, `ogun-app-manager`)
- Session restore and crash recovery
- Workspace and profile switching
- Session persistence (snapshot interval, clean shutdown writes, workspace/profile switch writes)
- Ọpọn Protocol enforcement at the user-space level (via `ogun-security-manager`)
- Package management via `opm` (ogun Package Manager)

**`ogun-user-apps`** — Directly used by users during active host sessions. All user-space applications organized into tiers:

| Tier | Name | SDK | Execution | Privilege |
|------|------|-----|-----------|-----------|
| 1 | Kernel Services | `ogun-kernel-sdk` | Tokio tasks in-process | Full kernel access |
| 2 | OS Apps | `ogun-app-sdk` (elevated) | OS child processes | Session manager access |
| 3 | Utility Apps | `ogun-app-sdk` | OS child processes | Standard operator access |
| 4 | User Apps | `ogun-app-sdk` | OS child processes | Standard operator access |

Tier 4 user apps (the personal enterprise suite): `enzo`, `kogi`, `dongo`, `ume`, `heshima`, `shango`, `igi`, `akeel`, `moto`, `zamani`, `apapo`, `orun`, `mizeez`, `shaba`, `kanna`, `qala`, `sambara`, `zuri`, `didara`, `misimu`, `ayo`. All distributed as `.opkg` packages.

---

## Runtime Supervision Hierarchy

```
runtime:
    ogun-desktop.exe                       ← user-facing launcher; registered autostart entry
        ogun-emulator                      ← main entry point (Tauri application)
            ogun-virtual-display-monitor   ← virtual device: display surface
            ogun-virtual-platform-host     ← virtual device: host platform (fs, entropy, process)
            ogun-virtual-cpu               ← virtual device: software-defined execution scheduler
            ogun-virtual-network-adapter   ← virtual device: software-emulated NIC
            ogun-uefi                      ← virtual UEFI; splash UI; boot menu; variable store
            ogun-bootloader                ← three-stage boot verification; KernelBootBundle
            ogun-kernel-core               ← 15 subsystems; supervisor loop; drivers
                ogun-host-service          ← persistent daemon; started and managed by kernel
                    ogun-host              ← one complete ogun OS runtime instance per session
                        ogun-session-manager   ← operator auth; session context; workspace lifecycle
                        apps (tier 1–4):
                            tier 1 — kernel services  ← ogun-modules-manager,
                                                         ogun-process-manager, ogun-ipc-broker
                            tier 2 — OS apps          ← ogun-desktop, ogun-shell,
                                                         ogun-command-center, ogun-explorer, etc.
                            tier 3 — utility apps     ← ogun-notes, ogun-tasks,
                                                         ogun-assistant, etc.
                            tier 4 — user apps        ← enzo, kogi, dongo, ume,
                                                         and the full personal enterprise suite
```

---

## Boot Sequence (17 Steps)

**Steps 1–6 — Bootloader phase:**

1. User launches `ogun-desktop.exe` → starts `ogun-emulator` → emulator initializes virtual hardware → `ogun-uefi` presents splash/menu → `ogun-bootloader` runs three-stage verification → `ogun-kernel-core` initializes → kernel starts `ogun-host-service` → host-service creates a new `ogun-host` instance → calls `ogun_bootloader::run()`
2. Platform detection via `cfg!()` into the `Platform` enum
3. `OgunHostDriver::initialize()` — platform-specific host driver init
4. `OgunDisplayDriver::initialize()` — display driver init for lock screen
5. Three-stage boot verification (image authenticity → install integrity → host key re-derivation)
6. `KernelBootBundle` assembly and handoff to kernel core

**Steps 7–17 — Kernel and session phase:**

7. Initialize all 15 kernel subsystems in canonical order
8. Load `auto_load` kernel modules via `dlopen`
9. Start Tier 1 kernel services (`ogun-modules-manager`, `ogun-process-manager`, `ogun-ipc-broker`)
10. Present lock screen; register all IPC channels; construct and send `SessionStartBundle`
11. Operator authentication
12. Session context binding — construct `ActiveSessionContext`; broadcast `session.context.updated`
13. OS-tier services start (`ogun-security-manager` → `ogun-system-manager` → `ogun-app-manager`)
14. Session restore or crash recovery
15. Desktop environment launch (`ogun-desktop`, `ogun-shell`, `ogun-command-center`)
16. Plugins and extensions loaded (require `operator_approved_at` per `opn-005`)
17. Auto-start Tier 4 user apps; broadcast `lifecycle.boot_completed`; phase set to `RUNNING`

---

## Software Lifecycle Phases

| Phase | Description |
|-------|-------------|
| **Phase 1 — Build Pipeline** | CI-only. `ogun-image-builder` produces signed `.img` files per target platform. No private key material leaves CI. |
| **Phase 2 — Installation** | `ogun-setup.exe` (includes `ogun-installer`) runs once per machine. Verifies image, scaffolds `~/.ogun/`, generates `SystemKey`, derives `HostKey`, registers `ogun-desktop.exe` as autostart. |
| **Phase 3 — Boot Chain** | User launches `ogun-desktop.exe` → `ogun-emulator` → virtual hardware → `ogun-uefi` → bootloader verification → kernel init → kernel starts host-service → session login → desktop. |
| **Phase 4 — Runtime** | `ogun-host` instance runs for the entire session lifetime. Host service supervises it, restarts on crash, coordinates clean shutdown. |

---

## Security Model — The Three Keys

**Image Key (`ImageSigningKey`)** — ed25519 keypair owned exclusively by the CI build pipeline. Private key never leaves the CI secrets vault. Public key embedded in every `.img` file as `ImageVerifyKey` section, extracted to `~/.ogun/security/keys/image-verify.pub` at install time, verified by the bootloader on every boot.

**System Key (`SystemKey`)** — ed25519 keypair generated by `ogun-installer` once at first installation. Private key stored exclusively in the host OS keychain (Windows DPAPI, macOS Keychain, Linux Secret Service). Public key at `~/.ogun/security/keys/system.pub`. Signs the system manifest; persists across image updates; changes only on full reinstall.

**Host Key (`HostKey`)** — 32-byte derived identity token (not a keypair). Derived via:
```
host_key = HKDF-SHA256(
    ikm:  image_pubkey_bytes ‖ system_pubkey_bytes,
    salt: install_id_bytes,
    info: b"ogun-host-key-v1",
    len:  32
)
```
Stored at `~/.ogun/security/keys/host.key` (0o400). Stamped on every telemetry event, audit entry, IPC message, and capability grant. Re-derived and compared by the bootloader on every boot (Stage 3).

---

## Execution Model — ogun-cpu

`ogun-cpu` is a software-defined execution scheduler that acts as the unified execution clock for every in-process component. It ticks all running components in a priority-respecting round-robin on a shared Tokio thread pool.

**Default tick rate:** 100 Hz (10 ms per tick). Configurable in `ogun.toml [kernel.cpu]`.

**Priority bands:**

| Band | Label | Execution lane |
|------|-------|----------------|
| P0 | Critical kernel | Synchronous on CPU's own Tokio task — never deferred |
| P1–P4 | Normal | Thread pool workers |
| P5–P7 | Background | Pool workers with BackgroundYieldGate |

**Component lifecycle modes:** `init → configure → start → tick ↔ pause → freeze → reset → shutdown`

**Thread pool:** Dynamically scales between `min_worker_threads` (default: 1) and `max_worker_threads` (default: `num_cpus - 1`). Scale-up when utilization > 80% or queue depth > 8; scale-down after utilization < 30% for 5 s cooldown. One worker added or removed per monitor cycle.

---

## The Elegua Protocol — IPC

Named after Èṣù-Ẹlẹ́gbára — Yoruba orisha of crossroads and communication. The unified communications specification for all component-to-component, layer-to-layer, and process-to-process communication in ogun OS.

**Version:** 0.3.0

**Core channels:**

| Channel | Key messages |
|---------|-------------|
| `ogun.host` | `phase.changed`, `status.changed`, `ready`, `crashed`, `shutdown_completed` |
| `ogun.session` | `session.started`, `operator.login`, `workspace.switched`, `context.updated`, `session.ended` |
| `ogun.system` | `onboarding.state`, `snapshot.written`, `crash.report`, `update.available`, `config.updated` |
| `ogun.security` | `capability.granted`, `capability.denied`, `opn.violation` |
| `ogun.apps` | `app.launched`, `app.terminated`, `app.crashed`, `app.installed` |
| `ogun.network` | `peer.connected`, `peer.disconnected`, `channel.opened`, `channel.closed` |

Every IPC message carries `operator_id`, `enterprise_id`, `workspace_id`, and `trace_id`. The IPC broker enforces workspace isolation routing — messages from `workspace_id = A` are not delivered to `workspace_id = B` without an explicit cross-workspace route.

---

## The Ọpọn Protocol — Data Governance

Cross-enterprise data isolation system enforced at the kernel Security subsystem. Rules are defined in `opn-policy.json` (read-only after installation, 0o444) and evaluated by `ogun-subsystem-security` before every cross-enterprise data access.

| Rule | Enforcement |
|------|-------------|
| `opn-001` | Enterprise namespace isolation — no cross-enterprise data reads without explicit grant |
| `opn-002` | Agent authority bounds — agents cannot act outside declared authority without operator approval |
| `opn-003` | Contract-before-active — enterprise workflows in active/billable states require an associated contract record |
| `opn-004` | Revenue attribution integrity — revenue events must carry a valid `attribution_id` |
| `opn-005` | Extension approval — extensions require `operator_approved_at` before `dlopen` |

`opn_enforced = true` is reset unconditionally after every load of `ogun.toml`. No operator, app, or IPC message can disable it.

---

## Product Editions

| Edition | Platform | Host Type | Status |
|---------|----------|-----------|--------|
| Desktop | Windows x64, macOS Apple Silicon, Linux x86_64 | `HostType::Desktop` | **0.1.0-beta (Windows x64 only)** |
| Web | Chrome, Firefox, Safari (WASM) | `HostType::Web` | Designed; not shipping |
| Mobile | Android arm64, iOS arm64 | `HostType::Mobile` | In progress |
| Server | Headless Linux | `HostType::Server` | Designed; not shipping |
| Device | IoT / embedded / custom hardware | `HostType::Device` | Designed; not shipping |

---

## Workspace Layout

```
ogun-os/
├── launcher/
│   └── ogun-desktop/           ← ogun-desktop.exe; registered autostart entry
├── emulator/
│   ├── ogun-emulator/          ← main entry point (Tauri app)
│   ├── ogun-emulator-backend/  ← host OS calls (WinAPI / POSIX / Bionic / web-sys)
│   └── ogun-os-emulator/       ← four virtual devices
├── boot/
│   ├── ogun-bootloader/        ← rlib; three-stage verification
│   └── ogun-uefi/              ← rlib; virtual UEFI firmware
├── drivers/
│   ├── ogun-host-platform-driver/
│   ├── ogun-display-driver/
│   └── ogun-virtual-network-driver/
├── kernel/
│   ├── ogun-kernel-core/
│   ├── ogun-session-manager/
│   └── subsystems/             ← 15 subsystem crates
├── sdk/
│   ├── ogun-types/
│   ├── ogun-image-format/
│   ├── ogun-app-sdk/
│   ├── ogun-service-sdk/
│   ├── ogun-kernel-sdk/
│   ├── ogun-driver-sdk/
│   └── ogun-host-sdk/
├── hosts/
│   ├── ogun-desktop-host/      ← 0.1.0-beta
│   ├── ogun-web-host/          ← planned
│   ├── ogun-mobile-host/       ← in progress
│   ├── ogun-device-host/       ← planned
│   └── ogun-server-host/       ← planned
├── runtime/
│   └── ogun-host-service/      ← RUNTIME BINARY (managed by ogun-kernel-core)
├── tools/
│   ├── ogun-image-builder/     ← CI tool; produces signed .img files
│   └── ogun-installer/         ← included in ogun-setup.exe
├── apps/
└── config/
    ├── ogun.toml
    ├── display.toml
    ├── emulation.toml
    └── uefi.toml
```

---

## Key Design Invariants

- `ogun-desktop.exe` is the only autostart entry — exactly one per machine.
- `ogun-emulator-backend` is the only component that calls host OS APIs directly.
- ed25519 signature over the kernel image is verified on every boot before anything executes.
- Only `ImageKind::Platform` images are bootable — `Baseline` and `Patch` images halt boot.
- `opn_enforced = true` is reset unconditionally after every `ogun.toml` load.
- Every capability grant/denial is written to the audit log before the operation completes.
- `CleanShutdownMarker` is written as the absolute last act of every shutdown.
- Tier 1 services run as Tokio tasks in-process; Tier 2–4 apps run as OS child processes.
- Virtual network adapters use OS sockets only — no raw packet injection.
- Virtual monitor renders via Tauri surfaces only — no direct framebuffer writes.
- Virtual host nesting depth ≤ configured maximum (≤ 10).
- Every component tick is wrapped in `catch_unwind` — a panicking component never crashes the execution loop.
- `operator_id`, `enterprise_id`, `workspace_id`, and `trace_id` are mandatory on every process and every Elegua Protocol message after boot Step 12.

---

*ogun OS · v0.1.0-beta · Project Ogún · 2026*
*Owner: Dominic Eaton (@eatondo)*
*Document: DESIGN.md*