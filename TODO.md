# ogun OS 0.1.0-beta Umbrella TODO

Last updated: 2026-06-02

Beta target from `ogun-docs/0.1.0-beta-release`: Windows x64 Desktop Edition only.

This file tracks the top-level `C:\dev\ogun` umbrella repository and all local
submodules. It intentionally separates release-blocking beta work from broader
ecosystem scaffolding so the Windows desktop beta does not get held hostage by
future web/mobile/server/device ambitions.

## Survey Snapshot

- The umbrella repo currently has 17 configured submodules:
  - `bula`, `elegua`, `jaku`, `oya`, `rustydb`
  - `ogun-apps`, `ogun-artifacts`, `ogun-components`, `ogun-config`, `ogun-devices`
  - `ogun-docs`, `ogun-os`, `ogun-runtime`, `ogun-sdk`, `ogun-sites`, `ogun-test-features`, `ogun-tools`
- All submodules are checked out and no submodule reported local dirty files during `git submodule foreach --recursive git status --short`.
- The top-level worktree is dirty only in `TODO.md` before this rewrite.
- A top-level `Cargo.toml` now exists and is the intended umbrella workspace. Earlier TODO references to `Cargo-temp.toml` are stale.
- Versioning is inconsistent:
  - Top-level workspace and most Ogun crates are still `0.1.0-alpha`.
  - Some supporting crates use plain `0.1.0`.
  - `ogun-tools/src/ogun-setup` and generated setup UI/config text still use `0.2.0-alpha`.
  - Beta docs and release artifacts target `0.1.0-beta`.
- Architecture for beta runtime should be: `ogun-desktop.exe -> ogun-emulator -> virtual devices -> ogun-uefi -> ogun-bootloader -> ogun-kernel-core -> ogun-host-service -> ogun-host-client -> ogun-session-manager -> ogun-user-apps`.
  - ogun-desktop.exe is main OS executable
  - ogun-emulator handles entire OS runtime and lifecycle
  - virtual ogun-devices handle low level interface functionality between ogun platform and target host platform (windows, linux, mac, redox, etc.)
  - ogun-uefi handles boot startup
  - ogun-bootloader handles image integrity verification and kernel loading
  - ogun-kernel handles OS kernel space runtime functionality
  - ogun-host-service handles ogun-host management and host client supervision and orchestration
  - ogun-host (host client) handles user space runtime functionality
  - ogun-session-manager handles user session management, login, authentation, user space applications and packages
  - ogun-user-apps are directly used by users during active host sessions
- Local implementation is still alpha scaffolding:
  - Many crates expose placeholder `initialize()` or `run()` functions.
  - `ogun-image-format` still supports stub images.
  - `ogun-bootloader` still permits `ImageLoadMode::AllowStub` and uses stub driver info.
  - `ogun-kernel` and `ogun-session` are partial/log-only.
  - `ogun-devices` virtual devices are mostly print-only binaries.
  - `bula`, `elegua`, `jaku`, `oya`, and `rustydb` have substantial README/spec claims but very small or empty code.
- `ogun-sites` now contains multiple site source directories under `src/`, so its README statement that the workspace is only a scaffold is stale.
- `ogun-artifacts` currently contains alpha-dev artifacts, not the beta artifact set.

## Current Build Snapshot

Checked locally on 2026-06-02.

- Top-level `cargo metadata --format-version 1 --no-deps`: fails before metadata generation because `ogun-components/src/drivers/ogun-windows-host-driver` depends on missing `ogun-os/src/ogun-types`.
- Top-level `cargo check --workspace`: blocked by the same manifest-loading failure.
- `ogun-apps`: `cargo check --workspace` passes.
- `ogun-runtime`: `cargo check --workspace` fails:
  - `src/ogun-bootloader/src/boot.rs` has malformed import text: `gun_types::{...}` instead of a valid `use ogun_types::{...};`.
  - `src/ogun-session/src/session.rs` calls `info!` without importing `tracing::info` or qualifying the macro.
  - Workspace manifest still warns about missing resolver and unused `workspace.target-dir` / `profile.dev.disable-default-features`.
- `ogun-sdk`: `cargo check --workspace` fails in `ogun_component_sdk/src/component.rs`:
  - trait item has invalid `pub` visibility.
  - `ogun_types` is referenced without a dependency.
  - the trait default method attempts to assign `self.mode` on unconstrained `Self`.
  - `ogun_types::OResult` does not exist in the current `ogun-types`; the available alias is `OgunResult`.
- `ogun-components`: `cargo check --workspace` fails during manifest loading:
  - `src/drivers/ogun-windows-host-driver/Cargo.toml` points `ogun_types` to missing `../../../../ogun-os/src/ogun-types`.
- `ogun-devices`: `cargo check --workspace` fails during manifest loading:
  - `ogun-virtual-cpu` and `ogun-virtual-display-monitor` are both named `ogun-virtual-monitor`.
- `ogun-os`: `cargo check --workspace` fails during manifest parsing:
  - `src/servers/ogun-host-server/Cargo.toml` contains unresolved merge-conflict markers.
- Supporting crates `bula`, `elegua`, `jaku`, `oya`, `rustydb`, and the Tauri tool crates cannot currently be checked in isolation with Cargo because the parent umbrella workspace fails first.
- JavaScript syntax checks passed:
  - `node --check ogun-tools/src/ogun-image-tool/src/main.js`
  - `node --check ogun-tools/src/ogun-setup/src/main.js`

## P0: Restore Cargo Workspace Load And Basic Compile

- [ ] Resolve the merge conflict in `ogun-os/src/servers/ogun-host-server/Cargo.toml`; choose the canonical package/bin name and remove all `<<<<<<<`, `=======`, `>>>>>>>` markers.
- [ ] Fix every stale `ogun_types` path dependency so all crates point to `ogun-runtime/src/ogun-types` or to a promoted top-level shared crate.
- [ ] Specifically fix `ogun-components/src/drivers/ogun-windows-host-driver/Cargo.toml` from `../../../../ogun-os/src/ogun-types` to the canonical `ogun-types` location.
- [ ] Search all manifests for `ogun-os/src/ogun-types` and remove every remaining stale path.
- [ ] Rename `ogun-devices/src/ogun-virtual-cpu` package/bin from `ogun-virtual-monitor` / `ogun_virtual_monitor` to `ogun-virtual-cpu` / `ogun_virtual_cpu`.
- [ ] Fix `ogun-runtime/src/ogun-bootloader/src/boot.rs` malformed `gun_types::{...}` import.
- [ ] Fix `ogun-runtime/src/ogun-session/src/session.rs` missing `tracing::info` import or replace the log call with a local logging path.
- [ ] Fix `ogun-sdk/src/ogun_component_sdk/src/component.rs` so the trait compiles:
  - remove invalid trait-item visibility
  - depend on or avoid `ogun-types`
  - replace `OResult` with `OgunResult` or add the intended alias
  - avoid assigning `self.mode` unless the trait requires a mode accessor/mutator
  - implement the runtime trait for `OComponent`
- [ ] Add `resolver = "3"` to nested virtual workspaces using edition 2024 crates:
  - `ogun-runtime/Cargo.toml`
  - `ogun-sdk/Cargo.toml`
  - `ogun-components/Cargo.toml`
  - `ogun-devices/Cargo.toml`
  - `ogun-os/Cargo.toml`
- [ ] Remove invalid or unused manifest keys from nested workspace manifests:
  - `workspace.target-dir`
  - `profile.dev.disable-default-features`
- [ ] Decide whether nested submodule workspaces should remain independently runnable or only be members of the umbrella workspace.
- [ ] If nested workspaces remain independently runnable, make `cargo check --workspace` pass from each submodule directory.
- [ ] If only the umbrella workspace is canonical, document that and remove/replace nested workspace manifests that confuse Cargo.
- [ ] After manifest fixes, rerun:
  - `cargo metadata --format-version 1 --no-deps`
  - `cargo check --workspace`
  - focused `cargo check --workspace` in each submodule workspace
- [ ] Add a repeatable build-status section or script so these checks do not depend on manual notes in this file.

## P0: Align Repository Layout With Beta Architecture

- [ ] Treat the top-level `Cargo.toml` as the canonical umbrella manifest or explicitly document why it is only a convenience manifest.
- [ ] Update stale README note that still refers to `Cargo-temp.toml`.
- [ ] Pick canonical crate names from the beta docs and apply them consistently:
  - `ogun-kernel-core` instead of alpha-era `ogun-kernel` where appropriate
  - `ogun-session-manager` instead of `ogun-session`
  - `ogun-host-service` instead of `ogun_host_service`
  - `ogun-image-builder` instead of or in addition to `ogun-image-tool`
- [ ] Decide whether `ogun-runtime`, `ogun-components`, `ogun-devices`, and `ogun-sdk` remain separate repositories or become first-class members of one umbrella workspace.
- [ ] Move, re-export, or publish `ogun-types` so every crate resolves one ABI/type source.
- [ ] Ensure no crate depends upward into a higher layer for common types.
- [ ] Normalize source paths in docs, manifests, and package metadata after any crate renames.
- [ ] Remove or quarantine future-edition scaffolds from the beta build path:
  - web edition
  - mobile edition
  - server edition
  - device edition
  - non-Windows desktop targets
- [ ] Add an architecture map from planned beta component names to actual local paths.
- [ ] Keep the map current whenever a crate is renamed, moved, or split.

## P0: Version, Scope, And Release Discipline

- [ ] Decide whether all beta source manifests should report `0.1.0-beta` or remain `0.1.0-alpha` until release cut.
- [ ] Remove `0.2.0-alpha` from setup UI, generated config, generated manifests, and installer text.
- [ ] Normalize artifact names to the beta docs:
  - `ogun-setup-windows-0.1.0-beta.exe`
  - `ogun-desktop-windows-0.1.0-beta.exe`
  - `ogun-emulator-windows-0.1.0-beta.exe`
  - `ogun-host-service-windows-0.1.0-beta.exe`
  - `ogun-windows-0.1.0-beta.img`
  - `ogun_image_tool-windows-0.1.0-beta.exe`
- [ ] Resolve docs disagreement between `ogun_desktop_windows-windows-0.1.0-beta.exe` and `ogun-host-service-windows-0.1.0-beta.exe`.
- [ ] Move alpha-dev artifacts out of beta artifact directories or label them explicitly as historical alpha artifacts.
- [ ] Replace release docs language that claims all beta features are present until artifacts and tests prove the claim.
- [ ] Document beta exclusions with concrete paths and rationale.
- [ ] Keep Windows x64 Desktop Edition as the only P0 release target.

## P0: Runtime Entry Chain

- [ ] Implement `ogun-desktop.exe` as the user-facing launcher rather than a placeholder client.
- [ ] Make the launcher start `ogun-emulator` and expose install/update/repair/modify flows.
- [ ] Implement `ogun-emulator` as the Tauri main runtime entry point, not just a print-only binary.
- [ ] Add an `ogun-emulator-backend` boundary and keep host OS API calls behind that boundary.
- [ ] Initialize the four beta virtual devices before UEFI handoff:
  - `ogun-virtual-display-monitor`
  - `ogun-virtual-platform-host`
  - `ogun-virtual-cpu`
  - `ogun-virtual-network-adapter`
- [ ] Make virtual devices `rlib` components used in-process unless release docs explicitly choose a process boundary.
- [ ] Start and supervise exactly one `ogun-host-service` instance per emulator session.
- [ ] Add singleton/lock enforcement so duplicate emulator/host-service instances cannot run for the same install.
- [ ] Persist host phase state to `system://host/phase.json`.
- [ ] Persist boot config state to `system://boot/config.json`.
- [ ] Add an emulator smoke test that reaches UEFI handoff.
- [ ] Add a full entry-chain smoke test: launcher -> emulator -> devices -> UEFI -> host service.

## P0: Virtual UEFI

- [ ] Convert `ogun-devices/src/ogun-uefi` from print-only startup into a real virtual UEFI component.
- [ ] Implement UEFI phases:
  - Pre-Init
  - Device Init
  - Boot Menu
  - Handoff
- [ ] Implement the variable store at `~/.ogun/config/uefi/vars.bin`.
- [ ] Define missing/corrupt variable-store recovery behavior.
- [ ] Implement `SecureBootPolicy`.
- [ ] Reject non-platform images before bootloader handoff.
- [ ] Render splash/progress through the virtual display monitor surface.
- [ ] Implement boot-menu interrupt window behavior:
  - default 3000ms
  - allowed 1000ms to 10000ms
  - config value `0` treated as 3000ms
- [ ] Lock `set_variable` after `ExitBootServices()`.
- [ ] Write `~/.ogun/logs/uefi-boot.log` for every phase transition and error.
- [ ] Wire `ogun-emulator -> ogun-uefi -> ogun-bootloader`.
- [ ] Add UEFI tests for variable locking, corrupt-store recovery, secure-boot rejection, and handoff bundle generation.

## P0: Image Format And Boot Verification

- [ ] Replace `ogun-image-format` stub loading with a real parser for the beta five-region image format.
- [ ] Keep `ImageLoadMode::AllowStub` available only for explicitly named test/dev paths.
- [ ] Remove `ImageLoadMode::AllowStub` from production boot.
- [ ] Implement `parse_header` with:
  - `OGUNIMG\0` magic validation
  - header size validation
  - sentinel validation
  - image kind validation
  - ABI version validation
  - image flags validation
  - header self-hash validation
- [ ] Implement `parse_section_table` with:
  - section offsets
  - compressed length
  - uncompressed length
  - section kind
  - priority
  - per-section SHA-256
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
- [ ] Decide what from `ogun-test-features/ogunnet` is promoted into production crates.
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

- [ ] Audit `ogun-test-features` for prototypes that should be promoted into production modules.
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
- [ ] Leave experimental code in `ogun-test-features` with clear labels and dates.
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
