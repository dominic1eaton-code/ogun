# CHANGELOG

All notable changes to ogun OS are documented in this file.

---

## [Unreleased]

### Notes
- Add release candidates to ogun release versioning system (e.g. `0.2.0-rc.1`, `0.2.0-rc.2`)
- Component rate divider for `ogun-cpu` / `ogun-virtual-cpu`: expose configurable tick rate divisions per component class (2/1, 1/1, 1/2, 1/4, 1/8, etc.) relative to the base 60 Hz / 100 Hz tick rate, allowing background and low-priority components to tick at sub-rates without consuming full pool capacity

---

## [0.1.0-beta] — Upcoming

**Release date:** June 2026
**Target platforms:** Windows x64 (initial release)
**Status:** Beta release — first public release of ogun OS

This is the first public beta release of ogun OS. It establishes the complete foundational runtime — virtual UEFI layer, bootloader, kernel, session manager, all 15 subsystems, the full emulation and execution model, the desktop host, drivers, OS apps, utility apps, user apps, and the SDK surface. All components listed below are new; there is no prior public release.

---

### OS Runtime

#### `ogun-desktop.exe` (User-Facing Launcher)

- User-facing launcher; the binary the user calls to start ogun OS
- Launches `ogun-emulator` — the main entry point (Tauri application)
- Manages modification, repair, and updating of the ogun OS image and binary installation
- Registered as the sole autostart entry by `ogun-setup.exe` via the host OS Task Scheduler; no other ogun binary is registered as an autostart entry

#### `ogun-emulator` (Main Entry Point)

- Tauri 2.0+ application; the top-level process and main entry point of the ogun OS application
- Initializes all four virtual hardware devices before calling `ogun-uefi`: `ogun-virtual-display-monitor`, `ogun-virtual-platform-host`, `ogun-virtual-cpu`, `ogun-virtual-network-adapter`
- Supervises `ogun-host-service` for the entire session lifetime
- `ogun-emulator-backend` is the sole component that calls host OS APIs directly (WinAPI, POSIX, Bionic, web-sys); no component above it calls host OS APIs

#### `ogun-uefi` (Virtual UEFI Firmware)

- Software virtual UEFI firmware layer; called by the emulator after virtual hardware initialization
- Four sequential phases: Pre-Init (emulator handoff) → Device Init → Boot Menu → Handoff (`ExitBootServices()`)
- Virtual BIOS/CMOS variable store persisted at `~/.ogun/config/uefi/vars.bin`; default store written and operator notified if corrupt or missing
- `SecureBootPolicy` — governs which image kinds are bootable; configurable only via boot menu between boot cycles
- ogun splash screen with boot progress bar rendered on the virtual monitor surface
- Timed boot menu interrupt window (configurable 1000ms–10000ms; `0` treated as 3000ms)
- `set_variable` locked unconditionally after `ExitBootServices()`; UEFI variables are immutable for the duration of the boot
- UEFI boot log written to `~/.ogun/logs/uefi-boot.log` on every phase transition and every error
- Boot does not halt on a missing or corrupt variable store; halts only on a Secure Boot policy violation

#### `ogun-bootloader`

- `rlib` statically linked into `ogun-host-service`; called at the start of each new `ogun-host` instance
- Three-stage boot verification pipeline:
  - Stage 1 — Image authenticity: ed25519 signature over SHA-256(R1+R2+R3), `ImageKind::Platform` enforcement, ABI version check, magic/sentinel validation, per-section SHA-256 hash verification
  - Stage 2 — Install integrity: re-hashes every manifest-covered file against the system-key-signed system manifest
  - Stage 3 — Host key re-derivation: `HKDF-SHA256(ikm: image_pubkey ‖ system_pubkey, salt: install_id, info: "ogun-host-key-v1", len: 32)` compared to stored `host.key`
- Any verification stage failure calls `halt()` with zero side effects; descriptive entry written to `~/.ogun/logs/boot.log`
- `validate_image_signature` treated as `true` unconditionally in all production builds
- Image parsing and section extraction via `ogun-image-format`
- `KernelBootBundle` assembly and handoff to the kernel core

#### `ogun-image-builder`

- CI-only tool for producing signed, platform-specific `.img` kernel image files; also distributed as `ogun_image_tool-windows-0.1.0-beta.exe` for local developer use
- Five-region image layout: `FileHeader` · `SectionTable` · `SectionData` · `ImageVerifyKey` · `SignatureBlock`
- zstd level-19 compression of all section blobs; per-section SHA-256 checksums recorded in the section table
- ed25519 signing of the full image payload; private key accepted via `--sign-key` or `OGUN_IMAGE_SIGN_KEY` environment variable — never written to disk on user machines
- Certificate and trust chain generation for the image signing pipeline
- Supports `Platform`, `Baseline`, `Patch`, and `Debug` image kinds
- Per-platform targets: `linux-x86_64`, `macos-apple-silicon`, `windows-x64`, WASM

#### `ogun-image-format`

- Single canonical implementation of all `.img` file operations shared by `ogun-image-builder`, `ogun-installer`, and `ogun-bootloader`; replaces three previously independent parse-header pipelines
- `parse_header` — validates magic bytes, sentinel, image kind, ABI version, and flags
- `parse_section_table` — deserializes all `SectionEntry` records with offset, compressed length, uncompressed length, and SHA-256 hash
- `sign_image` — appends `ImageVerifyKey` section and `SignatureBlock` to a finalized image
- `validate_image` — full post-build and post-install self-check; verifies `SignatureBlock` over all preceding image bytes
- `derive_host_key` — HKDF-SHA256 derivation of the runtime host identity key
- `OGUN_ABI_VERSION: u32` compatibility check at parse time

#### `ogun-setup.exe` and `ogun-installer`

- `ogun-setup.exe` is the user-facing setup binary that manages ogun OS images and OS installation; includes `ogun-installer` as its core installation engine
- One-time execution per machine per installation; nine installation steps: platform detection → image verification → directory scaffolding → initial configuration → security policy seeding → registry seeding → module extraction → security key generation → startup registration
- Calls `ogun-image-format::validate_image` before extracting any content; halts on signature failure
- Extracts all image sections to `~/.ogun/`; creates complete directory tree with 0o700 minimum permissions
- Generates the `SystemKey` ed25519 keypair: private key stored in host OS keychain (Windows DPAPI); public key written to `~/.ogun/security/keys/system.pub` (0o444)
- Derives and persists `HostKey` to `~/.ogun/security/keys/host.key` (0o400)
- Derives and persists `install_id` as a UUID v4 unique to this installation
- Computes the system manifest — SHA-256 hash table of every security-critical file — and signs it with the system private key
- Seeds the namespace registry (12 canonical namespaces), service registry, and package registry from the image's `NamespaceSeed` section
- Registers `ogun-desktop.exe` (the user-facing launcher) as the sole autostart entry with the host OS Task Scheduler; no other ogun binary is registered
- Silent install mode available via CLI flags for enterprise deployment

#### `ogun-kernel` / `ogun-kernel-core`

- The central orchestration runtime; implemented as `ogun-kernel-core` (`rlib`) statically linked into `ogun-host-service`
- Initializes all 15 subsystems in strict canonical order; a failure at any step calls `crash()` on the host instance
- Starts the 3 kernel-tier services, loads auto-start modules, and hands off to the session manager
- 17-step boot sequence: subsystem initialization → module loading → kernel service startup → lock screen → authentication → session context binding → OS service startup → session restore → desktop launch → extension loading → auto-start app launch → `lifecycle.boot_completed` broadcast

#### `ogun-session` / `ogun-session-manager`

- Implemented as `ogun-session-manager` (`rlib`) statically linked into `ogun-host-service`
- Manages the full user-space lifecycle from lock screen to clean shutdown
- `ActiveSessionContext` — live runtime session record carrying `operator_id`, `workspace_id`, `enterprise_id`, `session_id`, `host_key`, `started_at`, `boot_trace_id`
- Authentication pipeline: passkey (FIDO2) + TOTP/2FA on Desktop; biometric on Mobile; WebAuthn on Web; hardware on Device; skipped on Server
- Configurable lockout policy on repeated authentication failures; recovery codes supported for passkey-primary platforms
- Session supervisor loop: health monitoring, IPC draining, workspace persistence, crash detection
- Workspace switching: freezes departing workspace apps, saves records, activates target workspace, restores its running apps
- Profile switching: updates `enterprise_id` in session context; requires re-authentication
- Multi-enterprise operator support with Ọpọn Protocol isolation between enterprises
- Session snapshot persistence: written on configurable schedule (default 60s), on clean shutdown, and on workspace/profile switch
- Clean shutdown sequence: Tier 4 apps → Tier 2–3 apps → OS-tier services → final session state write → IPC drain → Tier 1 services → subsystem teardown (reverse order) → telemetry flush → `CleanShutdownMarker` written (absolute last act)
- Crash recovery: activated on missing `CleanShutdownMarker`; loads most recent valid snapshot; crash report queued to `ogun-system-manager`
- First-boot onboarding: three-step wizard (Operator Profile → Enterprise Intent → Workspace Provisioning) when `onboarding_state = "pending"`

#### `ogun-host-service`

- The single running ogun process inside `ogun-emulator`; exactly one instance at all times while the emulator is running
- Receives `KernelBootBundle` from the bootloader thread; spawns and supervises the full host thread hierarchy
- Thread architecture: Tauri main thread (emulator-owned) → host thread → bootloader thread; kernel thread (network thread); session thread (app/service/driver threads)
- Supervisor loop: monitors host health, drives crash recovery, handles clean shutdown, persists crash reports, drains IPC events, flushes telemetry; restarts crashed host instances with exponential backoff (max `max_restart_attempts`, default 3)
- Minimum thread count at idle: 1 main thread (Tauri, owned by emulator) + 1–2 Tokio worker threads; expands dynamically under load
- Manages `TenantRegistry` on server platforms for multi-tenant host instance tracking
- Writes `system://host/phase.json` and `system://boot/config.json` on every phase transition

#### `ogun-types`

- Zero-dependency foundational crate; no ogun crate depends on another ogun crate to resolve `ogun-types`
- `ProcessId`, `OperatorId`, `WorkspaceId`, `EnterpriseId`, `TraceId`, `SpanId` — first-class identity types used across all crates
- `OGUN_ABI_VERSION: u32 = 1` — single canonical source of truth; imported by all subsystems, SDKs, and host types
- `IMAGE_MAGIC`, `IMAGE_SENTINEL`, `HEADER_SIZE`, `SECTION_ENTRY_SIZE`, `SIGNATURE_BLOCK_SIZE`, `FORMAT_VERSION` — binary format constants
- `ImageKind` (`repr u16`) and `SectionKind` — canonical discriminants for image and section classification
- `paths` module — all `~/.ogun/…` path constants in one place
- `Platform`, `NativeHostType` — canonical enum definitions re-exported by every host crate
- `InstallationIdentity` — `install_id`, `image_pubkey_sha256`, `system_pubkey_sha256`, `host_key_sha256`
- `Ed25519PublicKey = [u8; 32]`, `Ed25519Signature = [u8; 64]`, `HostKey = [u8; 32]`
- Shared utilities: `now_ms()`, `generate_trace_id()`, `expand_tilde()`
- `serde`, `bitflags`, and `thiserror` as the only external dependencies

---

### Virtual Hardware & Execution Model

#### `ogun-virtual-display-monitor` (`ogun-virtual-monitor`)

- Virtual display monitor device managed by `ogun-emulator`
- Backed by a Tauri 2.0+ `WebviewWindow` surface; no direct framebuffer writes; no GPU dependency for virtual monitor rendering
- `VirtualMonitorSurface` wraps the Tauri window and presents a standard `OgunDisplayDriver` interface to `ogun-subsystem-display`
- Default configuration: resolution, scale factor, and refresh rate via `emulation.toml [virtual_monitor]`

#### `ogun-virtual-platform-host` (`ogun-virtual-host-platform`)

- Virtual platform host device managed by `ogun-emulator`
- Provides virtual filesystem, entropy, timers, shell execution, and process management to the boot chain
- Platform-specific implementations per host OS (Windows, Linux, macOS)
- When virtual hardware is fully initialized, this device's `ogun-bootloader` integration validates the ogun OS image and loads the ogun kernel

#### `ogun-virtual-cpu` / `ogun-cpu` (Virtual CPU Device)

- A software-defined execution scheduler; a virtual device managed by `ogun-emulator` alongside the other three virtual devices
- Acts as the unified execution clock for every in-process component in the ogun OS runtime; not a hardware emulator
- Kernel-level scheduling behavior coordinated through `ogun-subsystem-process` (Subsystem 3)
- Default tick rate: 100 Hz (one tick = 10ms); configurable in `ogun.toml [kernel.cpu]`
- Owns the component registry keyed by `ComponentId`; manages a Tokio-based dynamic thread pool that grows and shrinks based on observed utilization
- Dispatches tick calls to components respecting 8-level priority bands (P0–P7) and round-robin fairness within bands; P0 kernel services tick synchronously on the CPU's own Tokio task
- Enforces the 8 canonical lifecycle state transitions for all in-process components: `init → configure → start → tick → pause/freeze → reset → shutdown`
- Every component tick wrapped in `std::panic::catch_unwind(AssertUnwindSafe(...))`; a panicking component never crashes the execution loop or any other component
- Broadcasts `KernelEvent::SystemTick` to all loaded kernel modules at the end of every tick cycle
- Monitors per-component tick latency (p50/p95/p99), pool queue depth, and overall throughput; emits `CpuUtilizationSnapshot` to `telemetry://kernel/cpu/utilization` every 100 ticks (~1s)
- Dynamic thread pool: minimum 1 worker task; maximum `num_cpus - 1`; scale-up triggered when queue depth ≥ 8 or utilization ≥ 80% or p99 latency ≥ 2× timeslice; scale-down after utilization stays ≤ 30% for 5000ms; at most one worker added or removed per monitor cycle
- Starvation guard: components skipped for more than `starvation_threshold` ticks (default 200) temporarily promoted to P0 for one tick
- Background yield gate: P5–P7 components that ran within `background_yield_ns` of the current tick are skipped, allowing sub-rate ticking
- Process Control Block (PCB): kernel-maintained record for every in-process component; tracks identity (`pid`, `component_id`, `operator_id`, `workspace_id`, `trace_id`), scheduling counters (`last_tick_at`, `skipped_ticks`, `total_ticks`, `cpu_time_ns`, `inbox`), and lifecycle fields (`state`, `restart_count`, `crash_at`, `created_at`)
- `PcbTable` secondary index inside `ComponentSubsystem`: `ProcessId → ComponentId` for O(1) PID resolution

#### `ogun-virtual-network-adapter`

- Software-emulated NIC; virtual device managed by `ogun-emulator` and also a sub-component of `ogun-subsystem-network`
- Owns `NodeId` (ed25519-derived P2P address), X25519 ECDH session key derivation, AES-256-GCM per-session encryption, 4-byte big-endian length-prefix framing, handshake protocol, connection rate limiting (max 5 new inbound connections per IP per 60s), and handshake timeout enforcement (10s)
- Communicates exclusively through host OS TCP/UDP sockets — no raw socket access, no promiscuous mode, no ARP/ICMP manipulation
- `NodeId = SHA-256(verifying_key ‖ "ogunnet-node-id-v1")` via `SecureFrame` framing

#### `ogun-emulator-backend`

- The sole component that calls host OS APIs directly (WinAPI, POSIX, Bionic, web-sys); no component above it calls host OS APIs directly

---

### Kernel Subsystems (15 Subsystems)

All 15 subsystems implemented as separate `rlib` crates (`ogun-subsystem-*`) statically linked into `ogun-host-service`. Initialize in strict canonical order; subsystem handles are `Arc<RwLock<_>>` shared across the supervisor loop, session manager, and module contexts.

#### Subsystem 1 — `ogun-subsystem-telemetry`

- Structured telemetry bus; initialized first — all other subsystems emit through it
- `TelemetryEvent` with levels: `Trace`, `Debug`, `Info`, `Warn`, `Error`, `Fatal`
- `KernelTelemetryEvent` for kernel-internal structured events
- `host_key` stamped on every telemetry emission as the runtime identity token
- Telemetry buffer flushed on every supervisor loop tick and fully flushed before `CleanShutdownMarker` is written
- `TelemetryConfig` supports log sinks: file, in-memory ring buffer, and IPC forwarding

#### Subsystem 2 — `ogun-subsystem-memory`

- Memory budget tracking across all kernel components and processes
- OOM detection and configurable OOM policy (`OomPolicy`)
- Pressure level reporting (`PressureLevel`) to the supervisor loop and IPC bus
- Memory budget enforcement before process spawning

#### Subsystem 3 — `ogun-subsystem-process`

- Process table with full lifecycle tracking: `ProcessMetadata`, `ProcessState`, `ProcessId`
- `operator_id`, `enterprise_id`, `workspace_id`, and `trace_id` stamped on every process at session context bind; no process can be spawned without them after boot step 12
- Dynamic thread allocation coordinated with `ogun-virtual-cpu`; thread count scales up and down dynamically with load
- Process priority levels (`ProcessPriority`) with scheduler integration
- `OperatorId`, `EnterpriseId`, and `WorkspaceId` as first-class process attributes enforced at spawn time

#### Subsystem 4 — `ogun-subsystem-ipc`

- Full Elegua Protocol v0.3.0 implementation
- IPC bus with typed channels: unicast, multicast, broadcast, and request/reply patterns
- Channel registration at boot; all channels remain live for the full session lifetime
- Every message carries `operator_id`, `workspace_id`, `trace_id`, `span_id`, `protocol_version`, `timestamp`, `from`, `to`, `correlation_id`, `sender_pid`, `kind`, `payload`, and `priority`
- Workspace isolation routing: the IPC broker enforces `workspace_id` boundaries on all message delivery
- Ọpọn Protocol cross-enterprise isolation enforced at the broker level
- Core channels: `ogun.host`, `ogun.session`, `ogun.system`, `ogun.security`, `ogun.apps`, `ogun.network`, and all lifecycle broadcast channels
- Kernel-internal channels under `ipc://kernel/` namespace

#### Subsystem 5 — `ogun-subsystem-storage`

- Persistent key-value storage backed by **RustyDB** — a Rust-native embedded database
- Write-ahead log (WAL) for durability and crash consistency
- `StorageKey` / `StorageValue` typed API
- Used by: session state persistence, OgunNet node identity storage (`"ogunnet.identity.signing_key"`), operator records, module registry, security audit log indexes, and DHT seed persistence

#### Subsystem 6 — `ogun-subsystem-vfs`

- Virtual filesystem with 12 registered namespace schemes seeded from the image's `NamespaceSeed` section at boot step 6
- `OgunPath` resolution: translates namespace URIs to host filesystem paths via `CallContext`
- Workspace-scoped filesystem views: each `workspace_id` gets its own namespace root
- `ResourceHandle` for capability-gated filesystem resource access
- 12 namespaces: `ogun://`, `system://`, `user://`, `security://`, `app://`, `data://`, `network://`, `agent://`, `enterprise://`, `workspace://`, `session://`, `telemetry://`

#### Subsystem 7 — `ogun-subsystem-security`

- Ọpọn Protocol enforcement: cross-enterprise data isolation; `opn_enforced = true` is unconditional in all production builds; `security/opn-policy.json` is read-only after installation; reset to `true` unconditionally after every `ogun.toml` load
- Five Ọpọn rules: `opn-001` enterprise namespace isolation, `opn-002` agent authority bounds, `opn-003` contract-before-active enforcement, `opn-004` revenue attribution integrity, `opn-005` extension approval
- Capability system: `Capability`, `CapabilitySet`, and `SecurityPrincipal` types; every layer boundary crossing requires the caller to hold an appropriate capability
- Audit log: every capability grant or denial written to `~/.ogun/security/audit.log` (AES-256-GCM encrypted) before the result is returned
- ed25519 signature verification (via `ring` v0.17), SHA-256 hashing (via `sha2` v0.10), HKDF-SHA256 for host key derivation
- TLS trust anchor management for all outbound connections; certificate trust chain validation for image and system keys
- AES-256-GCM encryption and decryption utilities available to all subsystems via capability-gated API

#### Subsystem 8 — `ogun-subsystem-services`

- Service registry; baseline kernel service lifecycle records

#### Subsystem 9 — `ogun-subsystem-host`

- Host driver event channel lifecycle
- `OgunHostDriver` and `OgunDisplayDriver` handle registration
- Driver health monitoring and event forwarding to the IPC bus
- Platform capability detection and reporting to the kernel at boot

#### Subsystem 10 — `ogun-subsystem-session`

- Session context lifecycle: `SessionContext`, `OperatorRecord`, `OperatorLifecycleState`, `WorkspaceContext`
- Operator accounts, identity management, and multi-profile support (operators may have multiple profiles with independent workspace sets)
- Role-based access control (RBAC): roles, permissions, and policy enforcement
- Authentication pipeline: PIN, passphrase, and biometric (platform-dependent)
- Authorization: capability grant evaluation against operator roles and Ọpọn policy
- Session context binding: stamps `operator_id`, `workspace_id`, `enterprise_id`, `trace_id` on all processes after boot step 12

#### Subsystem 11 — `ogun-subsystem-display`

- Display surface registry and lifecycle management
- Theme and appearance state
- Input event routing (keyboard, pointer, touch)
- Window management and surface layering
- Driver event channel integration with `ogun-subsystem-host`
- `SurfaceId` assignment and surface context binding to `workspace_id`

#### Subsystem 12 — `ogun-subsystem-state`

- Session snapshots: `SnapshotRecord` written on a configurable schedule and at clean shutdown
- Checkpoint system: `CheckpointKind` with full and incremental checkpoint support
- `CleanShutdownMarker`: written as the final act of every host instance; its absence at boot unconditionally triggers crash-recovery mode
- Crash recovery: on missing marker, loads most recent snapshot, restores workspace layouts and running app states
- Update state tracking: records which updates have been applied and their rollback points

#### Subsystem 13 — `ogun-subsystem-components`

- `OgunModule` lifecycle management: load, initialize, tick, unload
- Dynamic loading of kernel modules (`cdylib`) via the Kernel Modules Manager
- ABI version verification at module load time; any mismatch rejects the module with a logged error
- `auto_load` module list processed at boot step 10; `ogun-module-settings` included as the baseline auto-loaded module
- Extension loading pipeline: `operator_approved_at` manifest check (`opn-005`) required before any `dlopen` call

#### Subsystem 14 — `ogun-subsystem-network` (OgunNet v2.0.0)

- **New in 0.1.0-beta.** Refactored from the monolithic `ogun-network-driver` into three properly layered components:
  - `ogun-virtual-network-driver` (`rlib`, Driver layer) — pure host translation layer; converts platform TCP/UDP/DNS/TLS APIs into the kernel's unified network stream interface; no P2P logic; implements `OgunNetworkDriver`; depends only on `ogun-driver-sdk`
  - `ogun-virtual-network-adapter` (`rlib`, Kernel sub-component) — software-emulated NIC; owns `NodeId`, X25519 session key derivation, AES-256-GCM per-session encryption, framing, handshake, rate limiting
  - `ogun-subsystem-network` (this subsystem, `rlib`) — the OgunNet kernel runtime; holds `NetworkManager` (`Arc<RwLock<NetworkManager>>`); owns all P2P protocol logic; accessed by all kernel services and apps via Elegua IPC channels
- The REPL previously embedded in the monolith is removed from this layer; interactive network commands are implemented as shell packages in `ogun-shell` communicating over `ogun.network.*` IPC channels
- Node identity: Ed25519 signing key persisted via `ogun-subsystem-storage`; `NodeId = SHA-256(verifying_key ‖ "ogunnet-node-id-v1")`; stable across restarts; human-readable alias (`adjective-noun-NNN`)
- Transport: TCP with 4-byte big-endian length-prefix framing; max message size 4 MiB; per-peer dedicated async write task
- Encryption: X25519 ECDH key exchange with Ed25519-signed DH public keys → per-session AES-256-GCM; all `Data`, `Chat`, `ChannelMsg`, and `FileChunk` payloads encrypted
- Kademlia DHT: 256-bucket XOR-metric routing table, k=20, α=3 parallel lookups; `put`/`get` with 1-hour TTL; iterative `FindNode` lookup
- mDNS local discovery: UDP multicast on `239.255.17.170:17171`; `LocalAnnounce` every 30s; LAN peer discovery without bootstrap configuration
- Peer Exchange (PEX): routing table shared with all connected peers every 60s for WAN-scale discovery
- Gossip pub/sub: topic-keyed publish/subscribe; flood propagation with TTL decrement; 2048-entry seen-cache for deduplication
- Named channels: IRC-style `#channel` multi-user rooms with AES-256-GCM channel key derived from channel name
- File transfer: chunked encrypted transfer; SHA-256 integrity verification; 64 KiB chunks; `FileOffer` / `FileOfferReply` / `FileChunk` / `FileChunkAck` / `FileComplete` protocol
- NAT punch: relay-assisted UDP hole-punch negotiation via `NatPunchRequest` / `NatPunchRelay`
- Reputation and ban system: per-peer integer scores; auto-ban at threshold −10; manual ban/unban; `PeerReport` propagation
- Rate limiting: max 5 new inbound connections per IP per 60s; handshakes must complete within 10s
- Elegua IPC channels registered: `ogun.network`, `ogun.network.gossip`, `ogun.network.dht`, `ogun.network.peers`, `ogun.network.channels`, `ogun.network.files`, `ogun.network.stats`

#### Subsystem 15 — `ogun-subsystem-emulation`

- **New in 0.1.0-beta.** Kernel Subsystem 15 — the last to initialize. Owns the `VirtualDeviceRegistry` and the full lifecycle of all virtual devices.
- Three baseline virtual devices: `ogun-virtual-monitor` (Tauri-backed display), `ogun-virtual-network-adapter` (OgunNet P2P NIC), and `ogun-virtual-host` (nested ogun OS host instance)
- `VirtualDeviceRegistry` — `Arc<RwLock<VirtualDeviceRegistry>>` authoritative record of all active virtual devices; keyed by `VirtualDeviceId` (`vdev:<kind>:<qualifier>[:<instance>]`)
- `ogun-drivers` — new emulation backend crate (`rlib`) implementing `OgunVirtualDriver` for all three baseline virtual devices
- `OgunVirtualDriver` trait defined in `ogun-driver-sdk`; ABI version verified against `OGUN_ABI_VERSION` at every driver initialization
- Virtual host: a fully running nested ogun OS instance of any `HostType` (`Desktop`, `Mobile`, `WebServer`, `CustomDevice`); Ọpọn Protocol enforced within every virtual host; maximum nesting depth ≤ 10 (configurable; `0` treated as `1`); `CleanShutdownMarker` required for every virtual host instance
- Capability gating: all virtual device provisioning, reads, and control require a `VirtualDeviceCapability` grant; every grant and denial written to the security audit log before the operation completes
- IPC channels registered at Subsystem 15 boot: `ogun.emulation`, `ogun.emulation.monitor`, `ogun.emulation.network`, `ogun.emulation.host`, `ogun.emulation.registry`; all five are session-lived and cannot be deregistered while the session is active
- VFS registration: virtual monitors at `device://vdev/monitor/<id>`, adapters at `device://vdev/network/<id>`, virtual hosts at `device://vdev/host/<id>`
- Telemetry: all significant emulation events emitted to the Telemetry Bus via `ogun-subsystem-telemetry`
- `ogun-drivers` never calls upward into `ogun-kernel-core`, any `ogun-subsystem-*`, `ogun-session-manager`, or any app/service SDK; sole upward communication path is `DriverEventSender`

---

### OS Components

#### Drivers

##### `ogun-host-windows`

- Windows host driver: translates Win32 and WinRT platform APIs into the ogun kernel's unified `OgunHostDriver` interface
- Process spawning, filesystem access, keychain integration (Windows DPAPI), and system event forwarding
- Host capability detection: reports platform features to the kernel at boot

##### `ogun-display-tauri`

- Tauri 2.0+ display driver: implements `OgunDisplayDriver` using the Tauri webview surface
- Window creation, resizing, and destruction
- Input event capture and forwarding (keyboard, pointer, scroll, touch on supported hardware)
- Theme application: maps ogun display surface themes to Tauri window styling
- IPC bridge between the Tauri webview layer and `ogun-subsystem-display`

##### `ogun-virtual-network-driver`

- Pure host translation layer for the network stack; converts platform TCP/UDP/DNS/TLS APIs into the kernel's unified network stream interface
- No P2P logic, no routing tables, no peer state; implements `OgunNetworkDriver` trait; depends only on `ogun-driver-sdk`

---

#### Tier-1 Kernel Services

| Service | Responsibility |
|---|---|
| `ogun-modules-manager` | Kernel module lifecycle: load, initialize, tick, unload |
| `ogun-process-manager` | Process table management, PCB tracking, process scheduling coordination |
| `ogun-ipc-broker` | Elegua Protocol message routing; workspace isolation enforcement |

---

#### Tier-2 OS Apps

##### `ogun-app-manager`

- Application lifecycle management: install, launch, suspend, resume, terminate, uninstall
- Package manager: `.opkg` ZIP-bundle installation via `opm`; manifest parsing, ABI verification, capability grant review, and operator approval flow
- App sandbox enforcement: capability sets applied at launch time
- App registry: tracks installed apps, their versions, ABI versions, declared capabilities, and operator approval state
- Auto-start app configuration management; app crash detection and restart policy

##### `ogun-command-center`

- Unified system command and control surface
- System status overview: host health, subsystem states, active operator and workspace, network node status
- Keyboard-driven navigation; integrates with `ogun-command-palette`

##### `ogun-command-palette`

- Universal command palette accessible from any surface
- Fuzzy search across system commands, installed apps, workspace contents, operator records, and OgunNet peers
- Extensible command registry: apps and services register commands at launch time
- Keyboard shortcut activation from any focus context

##### `ogun-desktop`

- Desktop environment: the primary graphical surface of ogun OS
- Workspace switcher and workspace visual management
- App launcher integration; notification surface
- System tray and status indicators (network node, memory pressure, session state)
- Theme and wallpaper management via `ogun-subsystem-display`

##### `ogun-explorer`

- File explorer for the ogun virtual filesystem
- Namespace-aware browsing: navigates across all 12 registered VFS namespace schemes
- File operations: copy, move, rename, delete, compress, extract
- File metadata and SHA-256 integrity display
- OgunNet file transfer integration: send files to peers directly from the explorer

##### `ogun-operator-center`

- Operator records management: personal and enterprise data, documents, and history
- Linktree management: operator public profile links and identity presentation
- Operator data management: structured records organized by enterprise and workspace
- Contact and relationship records linked to `ogun-contactbook` data

##### `ogun-profile-center`

- Operator profile management: display name, avatar, bio, and contact details
- Multi-profile creation and switching (requires re-authentication)
- Enterprise profile management: per-enterprise identity, branding, and contact details
- Profile data export and import

##### `ogun-security-center`

- Security posture dashboard: audit log viewer, active capability grants, Ọpọn policy status
- Certificate and trust chain viewer; key management UI
- Permission and capability grant management: operator-level review and revocation
- OgunNet peer reputation and ban list management

##### `ogun-settings-center`

- System-wide settings management across all subsystems and apps
- `ogun.toml` and `display.toml` configuration editing with validation
- Subsystem configuration panels: network, storage, display, security, session, telemetry
- App permission settings: per-app capability grant review
- Workspace configuration and namespace management

##### `ogun-shell`

- Primary command-line interface and scripting environment
- Dual-surface: GUI Shell Surface (styled panel in `ogun-command-center`) and Terminal Shell Surface (TUI/CLI mode)
- Shell packages: installable shell extensions that add commands and scripting capabilities via `OgunPackage` trait
- OgunNet interactive commands implemented as shell packages communicating over `ogun.network.*` IPC channels
- Access to all kernel subsystems via the shell SDK; integration with `ogun-command-palette`

##### `ogun-system-manager`

- System lifecycle management: update orchestration, onboarding, configuration management
- Update pipeline: downloads new `.img` files, verifies signatures, stages the update, applies on next boot
- Onboarding state machine for first-run setup
- Crash report collection and submission; snapshot and restore orchestration

##### `ogun-ui`

- ogun design system implementation
- UI component library used across all OS apps and exposed to third-party apps via `ogun-app-sdk`
- WASM-compatible `cdylib + rlib` components for cross-platform rendering
- Theme token system: CSS variables and design tokens applied by `ogun-subsystem-display`
- Input, layout, navigation, feedback, and data display component families

##### `ogun-workspaces`

- Workspace creation, configuration, and lifecycle management
- Content management: workspace-scoped content organization, tagging, and retrieval
- File management: workspace file views, bulk operations, and cross-workspace transfers (subject to Ọpọn policy)
- Workspace sharing and collaboration configuration for OgunNet-connected instances

---

#### Tier-3 Utility Apps

##### `ogun-assistant`

- AI-powered operator assistant
- Context-aware help across all OS surfaces and installed apps
- Command suggestion and workflow automation
- Integration with `ogun-search-engine` for knowledge retrieval

##### `ogun-calendar`

- Calendar and scheduling management; event creation, editing, and deletion
- Multi-enterprise calendar isolation (Ọpọn-enforced)
- Reminders and time-based notifications

##### `ogun-contactbook`

- Contact management: people, organizations, and relationships
- Multi-enterprise contact isolation
- Integration with `ogun-operator-center` and `ogun-messenger`; contact import and export

##### `ogun-focus`

- Focus session and deep work mode management
- Distraction blocking: suppresses non-critical notifications during focus sessions
- Focus session timer and history; integration with `ogun-tasks` for session-linked task tracking

##### `ogun-messenger`

- Secure messaging built on OgunNet
- End-to-end encrypted direct messages and group channels via OgunNet's named channel system
- Contact integration with `ogun-contactbook`; file sharing via OgunNet file transfer
- Multi-enterprise messaging isolation

##### `ogun-notes`

- Rich-text note-taking and knowledge management
- Workspace-scoped note organization; cross-note linking and tagging
- Integration with `ogun-search-engine` for full-text search

##### `ogun-search-engine`

- Full-text search across the ogun VFS, notes, contacts, tasks, and operator records
- Namespace-aware search: results scoped to current workspace by default
- Real-time indexing of new and modified content; integration surface for all Tier-2 and Tier-3 apps

##### `ogun-tasks`

- Task and to-do management
- Project and milestone organization linked to `moto` (Tier-4)
- Recurrence, deadlines, and priority levels; multi-enterprise task isolation

---

#### Tier-4 User Apps — Personal Enterprise Suite

| App | Role |
|---|---|
| `dongo` | Digital Wallet Management — multi-currency wallet, transaction history, integration with `enzo` |
| `enzo` | Personal Enterprise Management — enterprise creation, configuration, and multi-enterprise dashboard |
| `heshima` | Identity, Linktree, and Operator Communications Management — public profile publishing via OgunNet |
| `igi` | Portfolio Management — work samples, projects, and deliverables published via OgunNet |
| `kogi` | Digital Office Management — software-defined office; integration hub for all Tier-4 apps |
| `moto` | Project and Program Management — milestones, deliverables, tasks integrated with `ogun-tasks` |
| `shango` | Solution Management — solution design, lifecycle, and delivery tracking |
| `ume` | Entity, Organization, and Contract Management — legal entity records, contract lifecycle |

---

#### Hosts

##### `ogun-desktop-host`

- Desktop platform implementation of `OgunHost` (`ogun-host-windows` for 0.1.0-beta)
- Manages the full Tauri 2.0+ window surface for the desktop environment
- Coordinates `ogun-host-windows` and `ogun-display-tauri` driver integration
- Platform capability reporting to the kernel at boot; graceful shutdown and crash recovery integration

---

### OS SDK

#### `ogun-host-sdk`

- `OgunHost` trait definition: `boot`, `shutdown`, `enter_recovery`, `active_session`, `snapshot_session`, `restore_session`, `spawn_process`, `kill_process`, `check_capability`, `enforce_opn`, `publish`, `ns_read`, `ns_write`
- `HostType` enum: `Desktop`, `Web`, `Mobile`, `Device`, `Server`
- `HostStatus`, `HostResult`, `CrashReport` types; shared host types re-exported by all host type crates

#### `ogun-app-sdk`

- `OgunApp` trait definition: `on_init`, `on_configure`, `on_start`, `on_tick`, `on_message`, `on_pause`, `on_freeze`, `on_reset`, `on_shutdown`
- `AppMetadata`: tier, privilege level, version, description, declared capabilities
- `OGUN_ABI_VERSION` re-export for app manifest ABI version declarations
- App capability declaration types; system call interface for apps to communicate with kernel services

#### `ogun-service-sdk`

- `OgunService` trait definition for OS-tier services
- Service capability and lifecycle types

#### `ogun-kernel-sdk`

- `ModuleContext` — the interface by which kernel modules call kernel internals
- `OgunModule` trait: `module_name`, `abi_version`, `on_load`, `on_unload`, `on_tick`
- Kernel channel constants re-exported for module use; subsystem handle access API (capability-gated)

#### `ogun-driver-sdk`

- `OgunHostDriver` trait: platform capability reporting, process spawning, filesystem access, keychain access, system event forwarding
- `OgunDisplayDriver` trait: window lifecycle, input event capture, theme application
- `OgunVirtualDriver` trait: base trait for all virtual device driver implementations
- Driver event channel types; platform detection utilities

---

### OS Configuration

#### `ogun.toml`

- Primary runtime configuration file; loaded by the bootloader at every boot
- `validate_image_signature`: required field; treated as `true` unconditionally in production builds
- `[kernel]`: ABI version, image path, modules directory, auto-load module list
- `[kernel.cpu]`: `tick_rate_hz` (default 100), `min_worker_threads` (default 1), `max_worker_threads` (default `num_cpus - 1`), `scale_up_queue_depth` (default 8), `scale_up_utilization_pct` (default 0.80), `scale_down_utilization_pct` (default 0.30), `scale_down_cooldown_ms` (default 5000), `starvation_threshold` (default 200), `timeslice_ns` (default 10,000,000)
- `[network]`: OgunNet port, bootstrap addresses, mDNS enable, PEX enable, max peers, advertise address
- `[session]`: auto-lock timeout, crash recovery policy, snapshot interval, lockout threshold and duration
- `[storage]`: database path, WAL configuration
- `[telemetry]`: log level, log sinks, buffer size
- `[security]`: audit log path, Ọpọn policy path (`opn_enforced` is not configurable — always `true`)

#### `display.toml`

- Display and theming configuration
- `[theme]`: active theme name, color scheme (`light` / `dark` / `system`), accent color
- `[window]`: default window dimensions, scaling factor, animation enable
- `[fonts]`: primary font family (Cinzel for lock screen display), monospace font family, base font size
- `[surfaces]`: surface refresh rate, compositor settings

#### `emulation.toml`

- **New in 0.1.0-beta.** Emulation layer runtime configuration; a peer to `ogun.toml` and `display.toml`; loaded by `ogun-subsystem-emulation` at Subsystem 15 initialization
- `[devices.auto_provision]`: array of virtual device definitions initialized automatically at boot
- `[virtual_host]`: `max_nesting_depth` (positive integer ≤ 10; `0` treated as `1`), default `HostType` for auto-provisioned virtual hosts
- `[virtual_monitor]`: default resolution, scale factor, refresh rate
- `[virtual_network]`: adapter identity persistence key, connection rate limit, handshake timeout

#### `uefi.toml`

- **New in 0.1.0-beta.** Virtual UEFI configuration; loaded by `ogun-uefi` at UEFI Pre-Init phase
- Boot menu interrupt window timeout (1000ms–10000ms; `0` treated as 3000ms)
- Virtual Secure Boot policy settings
- UEFI boot log path

---

### OS Packages and Binaries

| Artifact | Description |
|---|---|
| `ogun-setup-windows-0.1.0-beta.exe` | `ogun-setup.exe` — manages ogun OS images and OS installation; includes `ogun-installer`; registers `ogun-desktop.exe` as autostart entry; silent install mode available |
| `ogun-desktop-windows-0.1.0-beta.exe` | `ogun-desktop.exe` — user-facing launcher; starts ogun OS by launching `ogun-emulator`; manages image modifications, repairs, and updates |
| `ogun-emulator-windows-0.1.0-beta.exe` | `ogun-emulator` — main entry point (Tauri application); initializes virtual hardware; supervises `ogun-host-service` for the full session lifetime |
| `ogun_desktop_windows-windows-0.1.0-beta.exe` | `ogun-host-service` for Windows; all subsystems statically linked; Authenticode-signed; runs inside `ogun-emulator` |
| `ogun-windows-0.1.0-beta.img` | Signed platform kernel image for Windows x64; contains all compressed section blobs (`KernelCore`, `SessionManager`, `BootConfig`, `SystemManifest`, `Modules`, `Assets`); signed with the 0.1.0-beta ed25519 image signing key |
| `ogun_image_tool-windows-0.1.0-beta.exe` | Windows binary for `ogun-image-builder`; produces signed `.img` files; for CI and local developer/operator image authoring |

---

### OS Dependencies

#### RustyDB

- Rust-native embedded database used as the backend for `ogun-subsystem-storage`; replaces the previously planned sled backend
- Write-ahead log (WAL) for crash consistency; key-value storage API consumed by `StorageSubsystem`
- Used by: session state persistence, OgunNet node identity storage, operator records, module registry, security audit log indexes, and DHT seed persistence

---

### Known Limitations — 0.1.0-beta

- **Windows x64 only.** macOS Apple Silicon and Linux x86_64 Desktop Edition targets are designed and architected; packaging and testing are scheduled for a subsequent release.
- **Mobile Edition not included.** `ogun-host-android` and `ogun-host-ios` are in progress; `ogun-mobile-host` marked in-progress in the crate dependency map.
- **Web Edition not included.** `ogun-host-web` (WASM) is fully designed; not shipping in 0.1.0-beta.
- **Server Edition not included.** Multi-tenant `ogun-server-host` support is designed; not shipping in 0.1.0-beta.
- **Device Edition not included.** Designed; not shipping in 0.1.0-beta.
- **`enterprise_id` not yet in all IPC messages.** `enterprise_id` is defined in the session context and the Elegua Protocol schema; explicit inclusion in all messages is an identified open issue to be resolved in a patch release.
- **RustyDB backend.** The Storage subsystem uses RustyDB in 0.1.0-beta. Migration to the stable persistent backend is scheduled for 0.2.0.
- **Beta qualifier.** This is a pre-release. All documented features are present; some rough edges and performance characteristics are expected to improve in the stable 0.1.0 release.

---

## [0.1.0-alpha] — Released (Internal)

**Release date:** 2026
**Status:** Internal development build; not publicly distributed

Starter version. Internal architecture development. Established foundational types, image format, bootloader structure, and host service skeleton. No public distribution.

---

*ogun OS · Project Ogún · 2026*
*Owner: Dominic Eaton (@eatondo)*