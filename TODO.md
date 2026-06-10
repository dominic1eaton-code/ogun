# ogun OS 0.1.0-beta Umbrella TODO

Last updated: 2026-06-07

Purpose: concise, actionable umbrella TODO for C:\dev\ogun. This document
combines a short repository survey with a prioritized, restructured task list
matching the top-level TODO items you requested. Each top-level section maps to
concrete sub-tasks and recommended owners/places to implement work.

----

## Quick repository survey (automated scan)

- Cargo manifests discovered: 122 (multiple crates across the workspace).
- Key top-level projects and folders:
  - ogun-os, ogun-runtime, ogun-components, ogun-sdk, ogun-tools, ogun-apps
  - ogun-artifacts, ogun-docs, ogun-devices, ogun-config, ogun-sites
  - ogun-experimental, ogun-devops, bula, elegua, jaku, oya, rustydb, aya/oya
- Status notes from quick scan:
  - The workspace is large and contains many example/test crates and Tauri frontends.
  - Several manifests and crate path dependencies are stale (referencing moved/old ogun-types locations).
  - Many runtime components are scaffolds or log-only placeholders.

----

## Top-level TODOs

* @TODO: also create developer API

### 1) add plugins, extensions, packages

- Goal: provide a stable plugin/module/package runtime and an ecosystem registry.
- Where: `ogun-sdk` (plugin/package SDK), `ogun-components/src/extensions` (loader), `ogun-artifacts` (package artifacts), `ogun-sites` (registry UI).
- Actions:
  - Define plugin/package formats and on-disk layout (spec in `ogun-artifacts/docs`).
  - Implement `ogun_plugin_sdk` and `ogun_pkg_sdk` adapters in `ogun-sdk`.
  - Implement library loader in `ogun-components/src/extensions/ogun-libloader` and ensure safe sandboxing.
  - Seed a local package registry (file-backed) under `ogun-artifacts` and wire a publishing CLI in `ogun-tools/ogun-image-tool`.
  - Add integration tests: package install/upgrade/remove, version resolution, capability gating.

---

### 2) implement virtual hardware loops

- Goal: implement stable, testable device tick loops and a device trait for beta.
- Where: `ogun-devices`, `ogun-experimental/virtual_*`, `ogun-emulator` (planned in `ogun-os` or `ogun-runtime`).
- Actions:
  - Define `OgunDevice` trait (tick lifecycle, init/shutdown, serialize state) in `ogun-device-sdk`.
  - Implement `ogun-virtual-cpu`, `ogun-virtual-display-monitor`, `ogun-virtual-network-adapter`, `ogun-virtual-platform-host` as rlib components.
  - Provide supervisor harness in `ogun-emulator` that starts device loops and exposes control APIs.
  - Add device smoke tests and a reproducible deterministic tick runner for CI.

---

### 3) implement kernel subsystems

- Goal: implement the 15 kernel subsystems and provide a canonical kernel boot flow.
- Where: `ogun-runtime/src/ogun-kernel` (or split into `ogun-subsystem-*` crates depending on decision).
- Actions:
  - Decide module vs crate split for subsystems; update workspace accordingly.
  - Implement minimal, testable behavior for each subsystem (telemetry, memory, process, IPC, storage, VFS, security, services, host, session, display, state, components, network, emulation).
  - Provide typed `KernelBootBundle` and boot sequencing tests.
  - Add subsystem diagnostics and structured `KernelRuntimeReport` output.

---

### 4) develop and integrate in rustydb persistence layer

- Goal: use `rustydb` as the single-file or embedded persistent store for runtime state.
- Where: `rustydb`, `ogun-runtime` (storage subsystem), `ogun-session`, `ogun-host-service`.
- Actions:
  - Audit `rustydb` for required features: transactions, snapshots, compacting, WAL.
  - Design DB schemas for `session`, `modules`, `installations`, `system-manifest`, and `telemetry` indices.
  - Implement storage adapters under `ogun-runtime/src/subsystems/storage` to use `rustydb` and add migrations.
  - Add DB integration tests and a small local CLI for inspecting DB contents in `rustydb/src/rustydb-shell`.

---

### 5) get calendar utility app working end to end (frontend+backend+db+ui+ticking)

- Goal: deliver one complete app as a reference for app integration (calendar).
- Where: `ogun-apps` (identify calendar crate), `ogun-components` (app host integration), `ogun-sdk` (app SDK), `rustydb` for persistence.
- Actions:
  - Identify the calendar app crate in `ogun-apps` (if missing, scaffold `ogun-apps/src/ogun-calendar`).
  - Implement backend state sync and persistence with `rustydb` schema.
  - Hook UI assets (HTML/CSS/JS) into app packaging and ensure `tauri` backend bindings (if applicable).
  - Add ticking/scheduler tests to validate calendar alarms and UI refresh.

---

### 6) get rest of apps working end to end

- Goal: make Tier-2 user apps functional with documented integration pattern.
- Where: `ogun-components/src/apps/*`, `ogun-apps` crates.
- Actions:
  - Prioritize Tier-2 apps (workspaces, settings, command-center, explorer) and provide a short checklist for each: build, backend API, persistence, UI wiring, smoke test.
  - Create an `apps/integration` CI job (local script) that runs each app in a headless test harness.

----

## Roadmap sections you requested (preserve and expand)

---

* implement ogun-emulator and virtual device hardware loops
  - See section "implement virtual hardware loops" above; add emulator harness in `ogun-os`.

* implement kernel subsystems and persistant storage
  - See sections above on kernel subsystems and `rustydb` integration.

* split ui among seperate .html files
  - Refactor `ogun-tools` setup UI and `ogun-components` app UIs to use modular HTML pages and shared assets; consolidate client JS in `ogun-tools/src/**/*.js`.

* implement user app rust backends
  - Use `ogun_app_sdk` to standardize IPC and lifecycle; add templates in `ogun-sdk` and `ogun-tools`.

---

* implement plugin, module and package systems
  - Reuse work items in "add plugins, extensions, packages" to implement package manager and module loader.

* replace ogun-image-tool and develop `ogun-ide` for developing, building and deploying ogun artifacts and components (applications, images, packages, installers, etc.), with ogun sdk built in
  - Short-term: stabilize `ogun-image-tool` and add CLI publish/pack commands.
  - Mid-term: scaffold `ogun-ide` (electron/tauri) under `ogun-tools/ogun-ide` with project templates and integrated SDK.

---

release 0.1.0 beta !

- Release checklist (candidate):
  - All P0 manifest fixes applied and `cargo check --workspace` succeeds.
  - Installer and launcher integration complete and tested on Windows x64.
  - Core subsystems implemented minimally with boot smoke test.
  - Packaging and artifact naming normalized to `0.1.0-beta`.

---

0.2.0  release

* figure out mobile and webhost implementations
* implement more user apps tier 4
* refine and cleanup architecture and design
* generate documentation, update websites
* figure out oshun operating system enterprise scaling automated runtime environment design, architecture and implementation

----

- [ ] Implement section decompression and extraction.
- [ ] Implement zstd level-19 compression/decompression where the docs require it.
- [ ] Implement ed25519 verification over the signed payload.
- [ ] Implement `sign_image` with the documented verify-key and signature-block layout.
- [ ] Implement `derive_host_key` via HKDF-SHA256 using image public key, system public key, and `install_id`.
- [ ] Reject `ImageKind::Baseline` and `ImageKind::Patch` in production boot.
- [ ] Treat `validate_image_signature` as true in production regardless of config.
- [ ] Verify required beta sections are present:
  - `KernelCore`
  - `SessionManager`
  - `BootConfig`
  - `SystemManifest`
  - `Modules`
  - `Assets`
- [ ] Write descriptive fatal halt entries to `~/.ogun/logs/boot.log`.
- [ ] Add unit tests for parse, malformed header rejection, missing sentinel rejection, section hash mismatch, signature mismatch, image-kind rejection, and ABI mismatch.

## P0: Bootloader

- [ ] Fix current syntax errors so `ogun-bootloader` compiles.
- [ ] Replace the stub bundle path in `run_bootloader()` / `boot()` with real config-driven image loading.
- [ ] Implement the three-stage verification sequence:
  - image authenticity
  - install integrity/system manifest
  - host key re-derivation
- [ ] Ensure failed verification performs zero side effects before halt.
- [ ] Read installed verification keys from the documented security layout.
- [ ] Read and validate the installed system manifest.
- [ ] Re-hash every manifest-covered file on every boot.
- [ ] Verify system manifest ed25519 signature.
- [ ] Compare derived host key against `~/.ogun/security/keys/host.key`.
- [ ] Produce a typed `KernelBootBundle`.
- [ ] Send `KernelBootBundle` to `ogun-host-service` through a typed channel.
- [ ] Add tests for each verification stage and all fatal halt reasons.

## P0: Installer And Setup

- [ ] Split or clearly define `ogun-setup.exe` and `ogun-installer` responsibilities.
- [ ] Remove `0.2.0-alpha` from `ogun-tools/src/ogun-setup`.
- [ ] Make setup verify `.img` files through `ogun-image-format::validate_image` before extracting anything.
- [ ] Extract image sections into the documented `~/.ogun/` tree.
- [ ] Generate a real UUID v4 `install_id`; remove pseudo-random install IDs.
- [ ] Generate a `SystemKey` ed25519 keypair at install time.
- [ ] Store the system private key in Windows DPAPI for beta.
- [ ] Ensure the system private key is never written under `~/.ogun/`.
- [ ] Write `system.pub`, `image-verify.pub`, and `host.key` with documented Windows ACLs.
- [ ] Compute and sign `system-manifest.json`.
- [ ] Seed:
  - `opn-policy.json`
  - `capability-defaults.json`
  - namespace registry
  - service registry
  - package registry
  - module index
  - app index
- [ ] Extract module libraries into `~/.ogun/modules/`.
- [ ] Register only `ogun-desktop.exe` as the Windows Task Scheduler autostart entry.
- [ ] Implement install, repair, update, modify, and uninstall flows.
- [ ] Implement silent install CLI flags for enterprise deployment.
- [ ] Convert setup backend `.unwrap()` calls that can fail on IO/serialization into typed installer errors.
- [ ] Add install/repair/update/uninstall smoke tests using a temporary install root.

## P0: Host Service And Supervisor

- [ ] Rename or publish `ogun-components/src/services/ogun_host_service` as the canonical `ogun-host-service` beta runtime binary.
- [ ] Replace log-only startup with the documented supervisor thread hierarchy.
- [ ] Decide whether the beta runtime is one OS process with threads or launcher/emulator/host-service processes; update docs and code to agree.
- [ ] Receive `KernelBootBundle` from the bootloader thread through a typed channel.
- [ ] Spawn and supervise:
  - host thread
  - kernel thread
  - session thread
  - device/service/app threads or child processes
- [ ] Implement crash detection.
- [ ] Implement restart with exponential backoff and max restart attempts.
- [ ] Implement clean shutdown ordering.
- [ ] Guarantee `CleanShutdownMarker` is the absolute final write.
- [ ] Persist crash reports.
- [ ] Surface crash reports to `ogun-system-manager`.
- [ ] Drain IPC and flush telemetry during supervisor ticks and before shutdown.
- [ ] Add tests for phase transitions, clean shutdown, crash restart, restart exhaustion, and final marker behavior.

## P0: Kernel Core And 15 Subsystems

- [ ] Rename or reshape `ogun-runtime/src/ogun-kernel` into the documented `ogun-kernel-core` rlib.
- [ ] Replace log-only `OgunKernel::boot()` with the real boot sequence.
- [ ] Decide whether the 15 subsystems are separate crates or modules in beta.
- [ ] If separate crates, scaffold the missing `ogun-subsystem-*` crates and add them to the workspace.
- [ ] If modules, document the beta exception and keep public boundaries equivalent to the spec.
- [ ] Add missing Subsystem 8: Services.
- [ ] Add missing Subsystem 15: Emulation.
- [ ] Initialize subsystems in strict canonical order:
  - telemetry
  - memory
  - process
  - IPC
  - storage
  - VFS
  - security
  - services
  - host
  - session
  - display
  - state
  - components
  - network
  - emulation
- [ ] Fail boot immediately if a required subsystem fails.
- [ ] Start Tier-1 kernel services:
  - `ogun-modules-manager`
  - `ogun-process-manager`
  - `ogun-ipc-broker`
- [ ] Add shared subsystem handles, likely `Arc<RwLock<_>>`, or document an equivalent sharing model.
- [ ] Implement structured `KernelRuntimeReport` output for boot/status/tests.
- [ ] Add kernel tests for canonical order, failure propagation, service startup, and shutdown reversal.

## P0: Security Model And Invariants

- [ ] Implement image signature verification on every boot.
- [ ] Implement system manifest signature verification on every boot.
- [ ] Re-hash manifest-covered files on every boot.
- [ ] Re-derive and compare `host_key` on every boot.
- [ ] Enforce no side effects after a failed boot verification stage.
- [ ] Enforce Opon Protocol unconditionally in the security subsystem.
- [ ] Ensure `opn_enforced` is reset to true after every config load.
- [ ] Ensure `validate_image_signature` cannot be disabled in production.
- [ ] Implement capability grant/denial checks.
- [ ] Write audit entries before returning grant/denial results.
- [ ] Stamp `host_key` on telemetry and audit log entries.
- [ ] Stamp `operator_id`, `enterprise_id`, `workspace_id`, and `trace_id` on every process after session context binding.
- [ ] Stamp the same context on every Elegua IPC message after session context binding.
- [ ] Ensure no private signing keys or system private keys can be committed or written under `~/.ogun/`.
- [ ] Add automated tests for all design invariants I-01 through I-35 that can be exercised in beta.

## P0: Execution Model And Virtual CPU

- [ ] Implement `ogun-virtual-cpu` as a software-defined scheduler, not a placeholder binary.
- [ ] Implement a component registry keyed by `ComponentId`.
- [ ] Implement `ProcessControlBlock`.
- [ ] Implement `PcbTable`.
- [ ] Implement the eight canonical lifecycle modes:
  - init
  - configure
  - start
  - tick
  - pause
  - freeze
  - reset
  - shutdown
- [ ] Implement canonical lifecycle transitions and invalid-transition errors.
- [ ] Implement a Tokio-based dynamic thread pool.
- [ ] Enforce min/max worker thread settings.
- [ ] Implement priority bands P0-P7.
- [ ] Tick P0 kernel components synchronously.
- [ ] Wrap all component ticks in `catch_unwind`.
- [ ] Implement queue depth tracking.
- [ ] Implement latency and utilization tracking.
- [ ] Implement scale-up and scale-down behavior.
- [ ] Implement starvation guard.
- [ ] Implement background yield gate.
- [ ] Implement rate divisors:
  - double
  - full
  - half
  - quarter
  - eighth
  - sixteenth
  - custom
- [ ] Implement armed-message staging.
- [ ] Flush armed messages at end of tick.
- [ ] Support unicast, multicast, broadcast, pub/sub, and request/response message paths.
- [ ] Emit CPU telemetry to `telemetry://kernel/cpu/utilization`.
- [ ] Add scheduler tests for priority, starvation, panic isolation, rate divisors, scale behavior, and message flush order.

## P0: IPC And Elegua Protocol

- [ ] Decide whether `elegua` is a standalone protocol crate used by `ogun-subsystem-ipc` or only a spec repository for beta.
- [ ] Replace `elegua/src/lib.rs` placeholder `run()` with real protocol types or move the protocol types into a dedicated SDK/runtime crate.
- [ ] Implement the beta Elegua message schema.
- [ ] Ensure every message carries:
  - operator ID
  - enterprise ID
  - workspace ID
  - trace ID
  - span ID
  - sender PID
  - timestamp
  - protocol version
  - correlation ID
  - routing target/source
  - message kind
  - payload
  - priority
- [ ] Add `enterprise_id` everywhere, even where older docs treated it as optional/unresolved.
- [ ] Implement unicast, multicast, broadcast, pub/sub, and request/reply.
- [ ] Enforce workspace isolation in the broker.
- [ ] Enforce Opon cross-enterprise isolation in the broker.
- [ ] Register core channels:
  - `ogun.host`
  - `ogun.session`
  - `ogun.system`
  - `ogun.security`
  - `ogun.apps`
  - `ogun.network`
  - `ogun.emulation`
  - lifecycle channels
  - `ipc://kernel/*`
- [ ] Add IPC schema tests.
- [ ] Add workspace route-isolation tests.
- [ ] Add enterprise route-isolation tests.

## P0: Session Manager

- [ ] Rename or reshape `ogun-runtime/src/ogun-session` into the documented `ogun-session-manager` rlib.
- [ ] Fix current compile error around `info!`.
- [ ] Replace `uid: ""` placeholder state with real session state.
- [ ] Implement session flow:
  - lock screen
  - auth
  - session context bind
  - OS service startup
  - restore/onboarding
  - desktop launch
- [ ] Implement Desktop auth with passkey plus TOTP/2FA for beta, or document a beta-safe temporary fallback.
- [ ] Implement lockout policy.
- [ ] Implement recovery codes.
- [ ] Implement `ActiveSessionContext` with:
  - operator ID
  - enterprise ID
  - workspace ID
  - session ID
  - host key
  - started time
  - boot trace ID
- [ ] Implement workspace switching:
  - freeze current workspace
  - save snapshot
  - activate target workspace
  - restore target state
- [ ] Implement profile switching with enterprise context update and re-authentication.
- [ ] Persist session snapshots on interval, workspace/profile switch, and clean shutdown.
- [ ] Implement crash recovery when `CleanShutdownMarker` is missing.
- [ ] Implement first-boot onboarding state machine.
- [ ] Add integration tests for auth, context stamping, restore, crash recovery, workspace switching, profile switching, and clean shutdown.

## P0: Storage, VFS, And RustyDB

- [ ] Decide whether `rustydb` is the beta storage backend or only a future backing crate.
- [ ] Replace empty `rustydb/src/db.rs` with a real embedded database API if RustyDB is beta-critical.
- [ ] Implement WAL-backed key-value storage for:
  - session state
  - node identity
  - operator records
  - module registry
  - audit indexes
  - DHT seeds
- [ ] Replace stale `sled` references in config, manifests, generated configs, and setup docs.
- [ ] Implement storage crash-consistency tests.
- [ ] Implement the 12 canonical VFS namespace schemes:
  - `ogun://`
  - `system://`
  - `user://`
  - `security://`
  - `app://`
  - `data://`
  - `network://`
  - `agent://`
  - `enterprise://`
  - `workspace://`
  - `session://`
  - `telemetry://`
- [ ] Seed namespace registry from the image `NamespaceSeed` section.
- [ ] Implement `OgunPath` resolution.
- [ ] Implement namespace access controls.
- [ ] Add VFS namespace tests and path canonicalization tests.

## P0: Display, Desktop Host, And Drivers

- [ ] Implement `ogun-desktop-host` as the beta Desktop `OgunHost` implementation for Windows x64.
- [ ] Implement `ogun-windows-host-driver` with:
  - process spawning
  - filesystem access
  - DPAPI keychain access
  - system event forwarding
  - Windows path/ACL behavior
- [ ] Keep `ogun-host-driver` and `ogun-display-driver` as generic interfaces or rename them if they are concrete stubs.
- [ ] Replace stub `ogun-display-driver` status behavior with real driver lifecycle.
- [ ] Implement `ogun-tauri-display-driver` / `ogun-display-tauri` with a real Tauri 2 `WebviewWindow` surface.
- [ ] Implement `OgunDisplayDriver` window lifecycle, resize, input capture, theme application, and IPC bridge.
- [ ] Implement `ogun-virtual-display-monitor`.
- [ ] Expose a virtual monitor handle to UEFI and the display subsystem.
- [ ] Enforce no direct framebuffer writes.
- [ ] Add Windows driver smoke tests where possible.
- [ ] Add host-driver and display-driver contract tests.

## P0: Network And Virtual Network Adapter

- [ ] Implement `ogun-virtual-network-adapter` as a software-emulated NIC over host OS sockets.
- [ ] Replace placeholder startup text.
- [ ] Decide what from `ogun-experimental/ogunnet` is promoted into production crates.
- [ ] Implement OgunNet node identity.
- [ ] Implement secure frame framing.
- [ ] Implement handshake timeout.
- [ ] Implement connection rate limiting.
- [ ] Implement X25519 session derivation if retained in beta.
- [ ] Implement AES-256-GCM session encryption if retained in beta.
- [ ] Implement DHT/gossip/peer/channel/file-transfer paths or explicitly narrow beta network scope.
- [ ] Ensure virtual network adapters use OS TCP/UDP sockets only.
- [ ] Ensure no raw packet injection, promiscuous mode, ARP manipulation, or ICMP manipulation.
- [ ] Register `ogun.network.*` IPC channels.
- [ ] Add tests for framing, handshake failure, rate limits, encrypted payloads, and channel routing.

## P1: SDK Surface

- [ ] Finish `ogun-app-sdk` with the documented `OgunApp` trait:
  - `on_init`
  - `on_configure`
  - `on_start`
  - `on_tick`
  - `on_message`
  - `on_pause`
  - `on_freeze`
  - `on_reset`
  - `on_shutdown`
- [ ] Finish `ogun-service-sdk` with service lifecycle, context, and capability types.
- [ ] Finish `ogun-kernel-sdk` with `ModuleContext`, `OgunModule`, channel constants, and capability-gated subsystem handle access.
- [ ] Finish `ogun-driver-sdk` with:
  - `OgunHostDriver`
  - `OgunDisplayDriver`
  - `OgunVirtualDriver`
  - driver event channel types
  - platform detection helpers
- [ ] Finish `ogun-host-sdk` with:
  - `OgunHost`
  - `HostType`
  - `HostStatus`
  - `HostResult`
  - `CrashReport`
- [ ] Finish component SDK lifecycle and ABI contracts.
- [ ] Define the canonical component/package manifest schema.
- [ ] Enforce ABI version checks at every load boundary.
- [ ] Remove placeholder `initialize()` APIs from SDK crates once real traits are implemented.
- [ ] Add compile-fail tests or contract tests for ABI mismatch and layer-boundary violations.

## P1: Component And App Implementations

- [ ] Replace placeholder Tier-2 app crates with minimum useful beta surfaces or mark them excluded from beta packaging.
- [ ] Implement minimum beta functionality for:
  - `ogun-desktop`
  - `ogun-shell`
  - `ogun-command-center`
  - `ogun-app-manager`
  - `ogun-system-manager`
  - `ogun-security-center`
- [ ] Decide whether all listed Tier-2 apps ship in beta.
- [ ] Replace placeholder Tier-3 utility apps with minimal shippable implementations or beta-excluded stubs.
- [ ] Decide whether all listed Tier-3 apps ship in beta.
- [ ] Replace placeholder Tier-4 apps with minimal shippable implementations or beta-excluded stubs.
- [ ] Decide whether all Tier-4 personal enterprise apps ship in beta or only the core subset.
- [ ] Add or verify `ogun-component.toml` manifests for every app/service/driver/module packaged into the beta image.
- [ ] Add package manifest validation.
- [ ] Implement package install/launch/suspend/resume/terminate/uninstall for `.opkg` / `.ogun` packages.
- [ ] Add smoke tests for beta-included app startup.

## P1: Image Builder And Release Artifacts

- [ ] Rename or wrap `ogun-image-tool` as the documented `ogun-image-builder`.
- [ ] Keep the Tauri image tool as a developer/operator UI if desired, but make the CI builder a deterministic CLI.
- [ ] Remove dev-mode stub build success from production builds.
- [ ] Ensure missing builder binary does not return stub success outside explicit dev mode.
- [ ] Stop embedding empty binary stubs in platform images.
- [ ] Make missing required binaries fail release builds.
- [ ] Replace placeholder ed25519 functions with real signing/verification.
- [ ] Replace placeholder verify-key behavior with real public-key handling.
- [ ] Replace pass-through compression with real zstd where still missing.
- [ ] Generate signed `ogun-windows-0.1.0-beta.img`.
- [ ] Produce all Windows beta executables.
- [ ] Authenticode-sign Windows executables.
- [ ] Write release checksums.
- [ ] Write artifact manifest.
- [ ] Prevent generated release artifacts from being overwritten in place.
- [ ] Add artifact inspection tests.
- [ ] Add packaging smoke test for every beta artifact.

## P1: Configuration And Policy

- [ ] Update `ogun-config/configuration/ogun.toml` to `0.1.0-beta`.
- [ ] Replace `0.2.0-alpha` in setup-generated config templates.
- [ ] Replace stale `sled` backend references with RustyDB or an explicitly chosen beta backend.
- [ ] Add missing `emulation.toml` if it is required by beta docs.
- [ ] Rename or reconcile `ogun-display.toml` versus `display.toml`.
- [ ] Keep `display.toml`, `emulation.toml`, `uefi.toml`, and `ogun.toml` schema docs synchronized.
- [ ] Update `kernel-subsystem-manifest.json` from 12-subsystem alpha to 15-subsystem beta.
- [ ] Update app, module, package, service, image, and registry manifests to beta names/versions.
- [ ] Validate config invariants after load:
  - `opn_enforced = true`
  - `validate_image_signature = true`
  - boot image kind is platform
  - Windows x64 beta defaults are used
- [ ] Add config migration/version checks so alpha configs cannot silently boot as beta.
- [ ] Add schema validation tests for every config and manifest file.

## P1: Docs, Sites, And Public Claims

- [ ] Update top-level README stale `Cargo-temp.toml` note.
- [ ] Update `ogun-os/README.md` and `ogun-runtime/README.md` from alpha/current placeholders to current beta implementation truth.
- [ ] Update docs that still describe 13 subsystems to 15 subsystems or mark them as historical alpha docs.
- [ ] Reconcile `ogun-docs/0.1.0-beta-release`, top-level `DESIGN.md`, `CHANGELOG.md`, `GUIDE.md`, and runtime/component README files.
- [ ] Replace public wording that says beta features ship if they are not yet backed by artifacts/tests.
- [ ] Add a dated known-limitations file for beta.
- [ ] Add build instructions for the umbrella workspace and every independently supported submodule workspace.
- [ ] Add operator docs for install, repair, update, modify, uninstall, launch, shutdown, and crash recovery.
- [ ] Update `ogun-sites/README.md`; it currently says the directory is a scaffold even though `src/*-site` directories exist.
- [ ] Add or document the site build/deploy system for Cloudflare Workers pages.
- [ ] Tie download/release pages to signed artifact manifests and checksums.
- [ ] Keep website release claims gated by the artifact manifest.
- [ ] Add docs-site generation path from `ogun-docs`.

## P1: Supporting Ecosystem Submodules

- [ ] `elegua`: replace placeholder `run()` implementation with actual protocol library exports or mark the crate spec-only for beta.
- [ ] `elegua`: fix incorrect print text that says "starting the bula generator".
- [ ] `elegua`: add message schema structs, routing/channel types, and serialization tests if production code depends on it.
- [ ] `rustydb`: implement the database wrapper if RustyDB is beta-critical.
- [ ] `rustydb`: add core API for open/get/put/delete/scan/transaction/flush/repair.
- [ ] `rustydb`: add durability and crash-consistency tests.
- [ ] `bula`: decide whether Bula is required for beta UI generation or only a future ecosystem language.
- [ ] `bula`: replace placeholder crate implementation with parser/lowering/runtime modules if beta-critical.
- [ ] `bula`: keep examples in sync with actual parser support.
- [ ] `jaku`: decide whether Jaku is required for beta release automation or remains future tooling.
- [ ] `jaku`: replace placeholder crate implementation with CLI/library modules if required.
- [ ] `jaku`: define whether beta packaging uses Jaku or conventional scripts.
- [ ] `oya`: decide whether Oya is required for beta architecture generation or remains future tooling.
- [ ] `oya`: replace placeholder crate implementation with model/graph/simulation modules if required.
- [ ] `oya`: document any generated architecture artifacts used by Ogun.
- [ ] Keep support-library README claims distinct from implemented functionality.
- [ ] Add simple compile checks for support crates once the umbrella manifest can load.

## P1: Test Sandboxes And Prototype Promotion

- [ ] Audit `ogun-experimental` for prototypes that should be promoted into production modules.
- [ ] Specifically evaluate:
  - `ogunnet`
  - `virtual_monitor`
  - `virtual_platform`
  - `config`
  - `thread`
  - `server`
  - `client`
  - `comms`
  - `bula`
  - `test_tauri_app_0`
- [ ] Move production-ready prototype code into the owning runtime/component/device/tool submodule.
- [ ] Leave experimental code in `ogun-experimental` with clear labels and dates.
- [ ] Remove checked-in binaries from test feature directories unless intentionally retained and documented.
- [ ] Add README coverage for how to run each test feature.
- [ ] Add a promotion checklist for turning a sandbox into production code.

## P1: Tests And Verification

- [ ] Add `cargo fmt --all` gates for each supported workspace.
- [ ] Add `cargo clippy --workspace --all-targets` gates for each supported workspace.
- [ ] Add top-level CI once `cargo metadata` works.
- [ ] Add unit tests for image parse/sign/verify.
- [ ] Add unit tests for host key derivation.
- [ ] Add unit tests for manifest hashing.
- [ ] Add boot integration test using a signed temporary platform image.
- [ ] Add installer integration test with a temporary install root.
- [ ] Add emulator smoke test.
- [ ] Add UEFI handoff smoke test.
- [ ] Add host-service smoke test that reaches `RUNNING` and shuts down cleanly.
- [ ] Add security invariant tests for boot rejection, image kind rejection, ABI mismatch, manifest mismatch, and host-key mismatch.
- [ ] Add IPC isolation tests.
- [ ] Add Windows packaging smoke test.
- [ ] Add release smoke test:
  - install
  - launch
  - authenticate/onboard
  - desktop visible
  - clean shutdown
  - relaunch
  - restore
- [ ] Add `node --check` or equivalent JS syntax checks for tool/site frontends.
- [ ] Add Tauri build checks for setup and image tool once Rust manifests load.

## P2: Cleanup, Metadata, And Hygiene

- [ ] Update `VERSION.md` files when beta branch/release policy is decided.
- [ ] Update `CHANGELOG.md` to match shipped beta scope exactly.
- [ ] Update `ogun-os/CHANGELOG.md` or remove duplication if top-level changelog is canonical.
- [ ] Normalize package descriptions and README snippets that still use generic "Baseline Ogun component crate" language.
- [ ] Replace placeholder binary output strings like "running user application..." with component-specific startup behavior.
- [ ] Replace incorrect placeholder text in virtual device binaries that says "running ogun installer".
- [ ] Normalize crate names using hyphenated package names and underscored lib/bin names consistently.
- [ ] Confirm all `manifest.json` and `ogun-component.toml` files agree on IDs, versions, tiers, capabilities, and beta inclusion.
- [ ] Remove or document checked-in generated screenshots and binary artifacts.
- [ ] Add an ownership/status table for each submodule.
- [ ] Add a machine-readable beta readiness manifest.

## Explicit Non-Blockers For 0.1.0-beta

- [ ] Do not block Windows Desktop beta on macOS packaging.
- [ ] Do not block Windows Desktop beta on Linux packaging.
- [ ] Do not block Windows Desktop beta on Web Edition.
- [ ] Do not block Windows Desktop beta on Mobile Edition.
- [ ] Do not block Windows Desktop beta on Server Edition.
- [ ] Do not block Windows Desktop beta on Device Edition.
- [ ] Do not block Windows Desktop beta on fully implementing Bula unless beta UI generation explicitly depends on it.
- [ ] Do not block Windows Desktop beta on fully implementing Jaku unless release automation explicitly depends on it.
- [ ] Do not block Windows Desktop beta on fully implementing Oya unless generated architecture artifacts explicitly depend on it.
- [ ] Do not block Windows Desktop beta on post-beta storage backend migrations beyond the chosen RustyDB/beta storage scope.
- [ ] Do not block Windows Desktop beta on public website polish beyond accurate release, download, docs, and limitation pages.

## Suggested First Fix Sequence

- [ ] Fix `ogun-os/src/servers/ogun-host-server/Cargo.toml` merge conflict.
- [ ] Fix stale `ogun_types` path in `ogun-components/src/drivers/ogun-windows-host-driver/Cargo.toml`.
- [ ] Rename `ogun-devices/src/ogun-virtual-cpu` package/bin.
- [ ] Fix `ogun-runtime/src/ogun-bootloader/src/boot.rs`.
- [ ] Fix `ogun-runtime/src/ogun-session/src/session.rs`.
- [ ] Fix `ogun-sdk/src/ogun_component_sdk/src/component.rs`.
- [ ] Add resolver/removal manifest cleanup across nested workspaces.
- [ ] Rerun `cargo metadata --format-version 1 --no-deps`.
- [ ] Rerun `cargo check --workspace`.
- [ ] Once the umbrella workspace loads, rerun focused checks for every submodule and replace this snapshot with the new failures.

