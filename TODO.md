# ogun OS 0.1.0-beta TODO

Last populated: 2026-06-01

Beta target from `../ogun-docs/0.1.0-beta-release`: Desktop Edition for Windows x64 only.

## Current State Snapshot

- `ogun-os/TODO.md` was empty before this pass.
- `ogun-os`, `ogun-runtime`, `ogun-sdk`, `ogun-components`, `ogun-devices`, `ogun-tools`, `ogun-apps`, `ogun-config`, and `ogun-artifacts` all exist as separate local workspaces/directories.
- Versioning is inconsistent: most code and artifacts are still `0.1.0-alpha`, `ogun-config/ogun.toml` says `0.2.0-alpha`, while the planned release docs target `0.1.0-beta`.
- The planned 0.1.0-beta docs describe a Windows desktop runtime with `ogun-desktop.exe`, `ogun-emulator`, `ogun-uefi`, `ogun-host-service`, signed images, 15 kernel subsystems, virtual devices, SDKs, apps, and release artifacts.
- The implementation is currently closer to alpha scaffolding: many crates are placeholders, `ogun-image-format` accepts stub images, `ogun-bootloader` uses stub drivers/images, the kernel/session/host service paths mostly log intent, and many component/app crates expose empty `initialize()` functions.
- Compile status checked on 2026-06-01:
  - `../ogun-apps`: `cargo check --workspace` passes.
  - `../ogun-tools/src/ogun-image-tool/src-tauri`: `cargo check` passes with warnings.
  - `../ogun-tools/src/ogun-setup/src-tauri`: `cargo check` passes with warnings.
  - `../ogun-runtime`: `cargo check --workspace` fails because `ogun-session` depends on invalid `tracing = "1.0"`.
  - `../ogun-sdk`: `cargo check --workspace` fails in `ogun_component_sdk/src/component.rs`.
  - `../ogun-os`: `cargo check --workspace` fails because `ogun-web`, `ogun-mobile`, and `ogun-host-server` use `tracing`/`tracing_subscriber` without declaring them.
  - `../ogun-components`: `cargo check --workspace` fails because component crates depend on `../../../../ogun-os/src/ogun-types`, which does not exist.
  - `../ogun-devices`: `cargo check --workspace` fails because `ogun-virtual-cpu` and `ogun-virtual-display-monitor` are both named `ogun-virtual-monitor`.

## P0: Make The Workspaces Build

- [ ] Decide the canonical Cargo workspace shape for beta: one root workspace, or intentionally separate workspaces with explicit path dependencies.
- [ ] Replace or remove `Cargo-temp.toml`; if it is the intended root manifest, rename/adopt it and fix members such as `ogun-os/src/*`.
- [ ] Add `resolver = "3"` to each virtual workspace using edition 2024 crates, or explicitly pin the intended resolver.
- [ ] Remove invalid `workspace.target-dir` and `profile.dev.disable-default-features` keys from workspace manifests.
- [ ] Fix `../ogun-runtime/src/ogun-session/Cargo.toml`: change `tracing = "1.0"` to a valid version such as `0.1`, and add any missing `tracing-subscriber` dependency only where needed.
- [ ] Fix `../ogun-sdk/src/ogun_component_sdk/src/component.rs`: remove invalid trait-item visibility, add or replace missing `ogun_types::OResult`, implement the trait for `OComponent`, and make the tests compile.
- [ ] Fix `../ogun-os/src/clients/ogun-web`, `../ogun-os/src/clients/ogun-mobile`, and `../ogun-os/src/servers/ogun-host-server` manifests so their tracing imports resolve, or remove the unused tracing setup.
- [ ] Rename `../ogun-devices/src/ogun-virtual-cpu` package/bin from `ogun-virtual-monitor` / `ogun_virtual_monitor` to `ogun-virtual-cpu` / `ogun_virtual_cpu`.
- [ ] Fix `../ogun-components` path dependencies currently pointing at missing `../ogun-os/src/ogun-types`; point all users to the canonical `../ogun-runtime/src/ogun-types` crate or a promoted shared crate.
- [ ] Fix syntax errors and obvious skeleton typos in runtime crates, including `../ogun-runtime/src/ogun-kernel/src/telemtry.rs`.
- [ ] Add CI commands for every beta workspace and require all to pass before cutting a beta artifact.

## P0: Align Source Layout With The Beta Architecture

- [ ] Pick canonical crate names from the beta docs and rename alpha leftovers to match them (`ogun-kernel-core`, `ogun-session-manager`, `ogun-host-service`, `ogun-image-builder`, etc.).
- [ ] Decide whether `ogun-runtime`, `ogun-components`, `ogun-devices`, and `ogun-sdk` remain separate repositories or become subtrees of `ogun-os`.
- [ ] Move or re-export `ogun-types` so every crate imports the same ABI/version/type source.
- [ ] Update `ogun-os/README.md`, `ogun-runtime/README.md`, and stale docs from 13-subsystem alpha wording to 15-subsystem 0.1.0-beta wording.
- [ ] Normalize release version constants to `0.1.0-beta`; remove stale `0.2.0-alpha` values from config templates and setup output.
- [ ] Create missing beta config templates: `emulation.toml` and `uefi.toml`.
- [ ] Update `ogun-config/ogun.toml` to match the beta docs: RustyDB storage, `[kernel.cpu]`, current namespace names, Windows x64 desktop defaults, and beta paths.
- [ ] Define which non-Windows host crates remain design-only for beta and exclude them from the beta build/release path unless they are required for tests.

## P0: Runtime Entry Chain

- [ ] Implement `ogun-desktop.exe` as the user-facing launcher, not only a log-only binary.
- [ ] Make `ogun-desktop.exe` launch `ogun-emulator` and manage update/repair/modify flows for the image and installed binaries.
- [ ] Implement the `ogun-emulator` Tauri app as the true main entry point.
- [ ] Add an `ogun-emulator-backend` boundary and enforce that it is the only layer calling host OS APIs directly.
- [ ] Initialize all four virtual devices before boot handoff: display monitor, platform host, virtual CPU, and virtual network adapter.
- [ ] Make `ogun-emulator` start and supervise exactly one `ogun-host-service` instance for the session lifetime.
- [ ] Add process singleton/lock enforcement so only one emulator/host-service instance runs per machine.
- [ ] Emit and persist host phase state to `system://host/phase.json` and boot config state to `system://boot/config.json`.

## P0: Virtual UEFI

- [ ] Create the `ogun-uefi` crate.
- [ ] Implement UEFI phases: Pre-Init, Device Init, Boot Menu, Handoff.
- [ ] Implement virtual variable store at `~/.ogun/config/uefi/vars.bin`, including corruption/missing-store recovery behavior.
- [ ] Implement `SecureBootPolicy` and enforce platform-image-only boot decisions before bootloader handoff.
- [ ] Implement splash/progress rendering through the virtual monitor surface.
- [ ] Implement boot menu interrupt window with the documented 1000ms-10000ms behavior and `0` treated as 3000ms.
- [ ] Lock `set_variable` after `ExitBootServices()`.
- [ ] Write `~/.ogun/logs/uefi-boot.log` for every phase transition and UEFI error.
- [ ] Wire UEFI handoff into `ogun-emulator -> ogun-uefi -> ogun-bootloader`.

## P0: Image Format And Boot Verification

- [ ] Replace `ogun-image-format` stub image loading with a real parser for the beta image layout.
- [ ] Implement `parse_header` with magic, sentinel, image kind, ABI version, and flag validation.
- [ ] Implement `parse_section_table` with offset, compressed length, uncompressed length, section kind, priority, and SHA-256 validation.
- [ ] Implement section decompression and section extraction.
- [ ] Implement `validate_image` with ed25519 verification over the signed payload.
- [ ] Implement `sign_image` and ensure the image verify key and signature block format matches the docs.
- [ ] Implement `derive_host_key` using HKDF-SHA256 with image public key, system public key, and `install_id`.
- [ ] Make production boot reject non-`ImageKind::Platform` images.
- [ ] Make production boot treat `validate_image_signature` as true regardless of config.
- [ ] Remove `ImageLoadMode::AllowStub` from the production boot path.
- [ ] Write `~/.ogun/logs/boot.log` with descriptive fatal halt entries.

## P0: Installer And Setup

- [ ] Split/define `ogun-setup.exe` and `ogun-installer` responsibilities according to the beta docs.
- [ ] Make setup verify the `.img` with `ogun-image-format::validate_image` before extracting anything.
- [ ] Extract image sections to the documented `~/.ogun/` tree.
- [ ] Generate a real UUID v4 `install_id`; replace pseudo-random install IDs.
- [ ] Generate the `SystemKey` ed25519 keypair at install time.
- [ ] Store the system private key in Windows DPAPI for beta; never write it under `~/.ogun/`.
- [ ] Write `system.pub`, `image-verify.pub`, and `host.key` with the documented permissions/ACLs on Windows.
- [ ] Compute and sign the system manifest covering every security-critical installed file.
- [ ] Seed `opn-policy.json`, `capability-defaults.json`, namespace registry, service registry, and package registry from image sections.
- [ ] Extract module libraries into `~/.ogun/modules/`.
- [ ] Register only `ogun-desktop.exe` as the Windows Task Scheduler autostart entry.
- [ ] Implement silent install CLI flags for enterprise deployment.
- [ ] Add install, repair, update, and uninstall smoke tests using a temporary install root.

## P0: Host Service And Supervisor

- [ ] Rename/promote `../ogun-components/src/services/ogun_host_service` to the canonical `ogun-host-service` beta runtime binary.
- [ ] Replace log-only startup with the documented thread hierarchy and bootloader handoff.
- [ ] Receive `KernelBootBundle` from the bootloader thread through a typed channel.
- [ ] Spawn and supervise the host thread, kernel thread, session thread, and device/service/app threads as specified.
- [ ] Implement crash detection and restart with exponential backoff and max restart attempts.
- [ ] Implement clean shutdown ordering and ensure `CleanShutdownMarker` is the absolute final write.
- [ ] Persist crash reports and surface them to `ogun-system-manager`.
- [ ] Drain IPC and flush telemetry during supervisor ticks and before shutdown.
- [ ] Add tests for phase transitions, clean shutdown, crash restart, restart exhaustion, and marker behavior.

## P0: Kernel Core And 15 Subsystems

- [ ] Rename/reshape `ogun-kernel` into the documented `ogun-kernel-core` rlib.
- [ ] Replace the current log-only `OgunKernel::boot()` with the full boot sequence.
- [ ] Implement all 15 beta subsystems as real `ogun-subsystem-*` crates or explicit modules with the same API boundary.
- [ ] Add missing Subsystem 8: Services.
- [ ] Add missing Subsystem 15: Emulation.
- [ ] Initialize subsystems in strict canonical order: telemetry, memory, process, IPC, storage, VFS, security, services, host, session, display, state, components, network, emulation.
- [ ] Fail boot immediately if a required subsystem fails to initialize.
- [ ] Start Tier-1 kernel services: `ogun-modules-manager`, `ogun-process-manager`, and `ogun-ipc-broker`.
- [ ] Add `Arc<RwLock<_>>` subsystem handles or another documented sharing model for supervisor/session/module access.
- [ ] Implement structured `KernelRuntimeReport` output for boot, status, and tests.

## P0: Security Model

- [ ] Implement image signature verification on every boot.
- [ ] Implement system manifest signature verification on every boot.
- [ ] Re-hash every manifest-covered file on every boot.
- [ ] Re-derive and compare `host_key` on every boot.
- [ ] Enforce no side effects after a failed boot verification stage.
- [ ] Enforce Opon Protocol in the security subsystem unconditionally.
- [ ] Add capability grant/denial checks with audit-before-operation semantics.
- [ ] Stamp `host_key` on every telemetry event and audit log entry.
- [ ] Stamp `operator_id`, `enterprise_id`, `workspace_id`, and `trace_id` on every process and IPC message after session context binding.
- [ ] Add tests for each design invariant I-01 through I-35 that can be automated in beta.

## P0: Execution Model And Virtual CPU

- [ ] Implement `ogun-virtual-cpu` as a software-defined execution scheduler, not a placeholder binary.
- [ ] Implement the component registry keyed by `ComponentId`.
- [ ] Implement `ProcessControlBlock` and `PcbTable`.
- [ ] Implement the eight canonical lifecycle modes: init, configure, start, tick, pause, freeze, reset, shutdown.
- [ ] Implement a Tokio-based dynamic thread pool with min/max worker enforcement.
- [ ] Implement priority bands P0-P7 and make P0 kernel services tick synchronously.
- [ ] Wrap all component ticks in `catch_unwind`.
- [ ] Implement queue depth, latency, utilization, scale-up, and scale-down behavior.
- [ ] Implement starvation guard and background yield gate.
- [ ] Add the component rate-divider feature from notes: 2/1, 1/1, 1/2, 1/4, 1/8, 1/16, and custom divisors.
- [ ] Implement armed-message staging and end-of-tick flush for unicast, multicast, broadcast, pub/sub, and request/response paths.
- [ ] Emit CPU telemetry to `telemetry://kernel/cpu/utilization`.

## P0: IPC And Elegua Protocol

- [ ] Implement the beta Elegua Protocol schema in the IPC subsystem.
- [ ] Ensure every message carries operator, enterprise, workspace, trace, span, sender PID, timestamp, protocol version, correlation ID, routing, kind, payload, and priority.
- [ ] Add `enterprise_id` to all IPC messages, even though docs allow unresolved messages as a patch issue.
- [ ] Implement unicast, multicast, broadcast, pub/sub, and request/reply.
- [ ] Enforce workspace isolation routing in the broker.
- [ ] Enforce Opon cross-enterprise isolation in the broker.
- [ ] Register core channels: `ogun.host`, `ogun.session`, `ogun.system`, `ogun.security`, `ogun.apps`, `ogun.network`, lifecycle channels, and `ipc://kernel/*`.
- [ ] Add IPC schema tests and route-isolation tests.

## P0: Session Manager

- [ ] Rename/reshape `ogun-session` into the documented `ogun-session-manager` rlib.
- [ ] Implement lock screen -> auth -> session context bind -> OS service startup -> restore/onboarding -> desktop launch.
- [ ] Implement Desktop auth with passkey plus TOTP/2FA for beta, or document a beta-safe temporary auth fallback.
- [ ] Implement lockout policy and recovery codes.
- [ ] Implement `ActiveSessionContext` with operator, workspace, enterprise, session, host key, started time, and boot trace ID.
- [ ] Implement workspace switching with freeze/save/activate/restore behavior.
- [ ] Implement profile switching with enterprise context update and re-authentication.
- [ ] Implement session snapshot persistence on interval, workspace/profile switch, and clean shutdown.
- [ ] Implement crash recovery when `CleanShutdownMarker` is missing.
- [ ] Implement first-boot onboarding state machine.
- [ ] Add session integration tests for auth, context stamping, restore, crash recovery, and clean shutdown.

## P0: Storage, VFS, And RustyDB

- [ ] Decide whether the local `../rustydb` crate is the beta storage backend and wire it into `ogun-subsystem-storage`.
- [ ] Replace stale `sled` config references with RustyDB.
- [ ] Implement WAL-backed key-value storage for session state, node identity, operator records, module registry, audit indexes, and DHT seeds.
- [ ] Implement the 12 canonical VFS namespace schemes from the beta docs.
- [ ] Seed namespace registry from the image `NamespaceSeed` section.
- [ ] Implement `OgunPath` resolution and namespace access controls.
- [ ] Add storage crash-consistency tests and VFS namespace tests.

## P0: Display, Desktop Host, And Drivers

- [ ] Implement `ogun-desktop-host` as the beta Desktop `OgunHost` implementation for Windows x64.
- [ ] Implement `ogun-host-windows` / Windows host driver with process spawning, filesystem access, DPAPI keychain access, and system event forwarding.
- [ ] Implement `ogun-display-tauri` with a real Tauri 2 WebviewWindow surface.
- [ ] Implement `OgunDisplayDriver` window lifecycle, resize, input capture, theme application, and IPC bridge.
- [ ] Implement `ogun-virtual-display-monitor` and expose a virtual monitor handle to UEFI and display subsystem.
- [ ] Enforce no direct framebuffer writes.
- [ ] Add Windows driver smoke tests where possible and host-driver contract tests.

## P0: Network And Virtual Network Adapter

- [ ] Implement `ogun-virtual-network-adapter` as a real software-emulated NIC over host OS sockets.
- [ ] Implement OgunNet node identity, secure frame framing, handshake timeout, and connection rate limiting.
- [ ] Implement X25519 session derivation and AES-256-GCM session encryption if retained in beta scope.
- [ ] Implement DHT/gossip/peer/channel/file-transfer paths listed in the release docs, or explicitly narrow the beta network scope.
- [ ] Ensure no raw packet injection, promiscuous mode, ARP, or ICMP manipulation.
- [ ] Register `ogun.network.*` IPC channels.
- [ ] Add network unit tests for framing, handshake failure, rate limits, and channel routing.

## P1: SDK Surface

- [ ] Finish `ogun-app-sdk` with the documented `OgunApp` trait: `on_init`, `on_configure`, `on_start`, `on_tick`, `on_message`, `on_pause`, `on_freeze`, `on_reset`, `on_shutdown`.
- [ ] Finish `ogun-service-sdk` with service lifecycle, context, and capability types.
- [ ] Finish `ogun-kernel-sdk` with `ModuleContext`, `OgunModule`, channel constants, and capability-gated subsystem handle access.
- [ ] Finish `ogun-driver-sdk` with `OgunHostDriver`, `OgunDisplayDriver`, `OgunVirtualDriver`, event channel types, and platform detection helpers.
- [ ] Finish `ogun-host-sdk` with `OgunHost`, `HostType`, `HostStatus`, `HostResult`, and `CrashReport`.
- [ ] Define the canonical component/package manifest schema and ABI version checks.
- [ ] Remove placeholder `initialize()` APIs from SDK crates once real traits are implemented.
- [ ] Add compile-fail or contract tests for ABI mismatch and layer-boundary violations.

## P1: Component And App Implementations

- [ ] Replace placeholder Tier-2 app crates with useful beta surfaces or mark them excluded from beta packaging.
- [ ] Implement minimum usable `ogun-desktop`, `ogun-shell`, and `ogun-command-center` because the beta boot flow launches them.
- [ ] Implement minimum `ogun-app-manager`, `ogun-system-manager`, and `ogun-security-center` flows required by install/update/crash/security stories.
- [ ] Decide whether all listed Tier-2 apps must ship in beta; if not, update release docs and package manifests.
- [ ] Replace placeholder Tier-3 utility apps with either minimal shippable implementations or beta-excluded stubs.
- [ ] Replace placeholder Tier-4 apps with either minimal shippable implementations or beta-excluded stubs.
- [ ] Add `ogun-component.toml` manifests for every app/service/driver/module packaged into the beta image.
- [ ] Implement package install/launch/suspend/resume/terminate/uninstall paths for `.opkg` / `.ogun` packages.

## P1: Image Builder And Release Artifacts

- [ ] Rename or wrap `ogun-image-tool` as the documented `ogun-image-builder` developer/CI utility.
- [ ] Remove dev-mode stub build success from production builds.
- [ ] Replace placeholder ed25519 functions with real signing/verification.
- [ ] Use real zstd compression and decompression, not pass-through stubs.
- [ ] Stop embedding empty binary stubs in platform images; missing required binaries should fail release builds.
- [ ] Generate signed `ogun-windows-0.1.0-beta.img`.
- [ ] Produce `ogun-setup-windows-0.1.0-beta.exe`.
- [ ] Produce `ogun-desktop-windows-0.1.0-beta.exe`.
- [ ] Produce `ogun-emulator-windows-0.1.0-beta.exe`.
- [ ] Produce `ogun_desktop_windows-windows-0.1.0-beta.exe` or rename this artifact to a clearer `ogun-host-service` artifact and update docs.
- [ ] Produce `ogun_image_tool-windows-0.1.0-beta.exe`.
- [ ] Authenticode-sign Windows executables.
- [ ] Write release checksums and artifact manifest.
- [ ] Move alpha-dev artifacts out of the beta artifact directory or label them clearly.

## P1: Configuration And Policy

- [ ] Update `ogun.toml` beta schema and loader.
- [ ] Add `display.toml` beta schema and loader.
- [ ] Add `emulation.toml` beta schema and loader.
- [ ] Add `uefi.toml` beta schema and loader.
- [ ] Add `opn-policy.json` beta seed file.
- [ ] Add `capability-defaults.json` beta seed file.
- [ ] Add `audit-schema.json` if audit logs are structured.
- [ ] Validate config invariants after load, especially `opn_enforced = true` and `validate_image_signature = true`.
- [ ] Add config migration/version checks so alpha configs cannot silently boot as beta.

## P1: Tests And Verification

- [ ] Add `cargo fmt --all` and `cargo clippy --workspace --all-targets` gates for each workspace.
- [ ] Add unit tests for image parse/sign/verify, host key derivation, and manifest hashing.
- [ ] Add boot integration test using a signed temporary platform image.
- [ ] Add installer integration test with a temporary install root.
- [ ] Add emulator smoke test that starts virtual devices and reaches UEFI handoff.
- [ ] Add host-service smoke test that reaches `RUNNING` and shuts down cleanly.
- [ ] Add security invariant tests for boot rejection, image kind rejection, ABI mismatch, manifest mismatch, and host-key mismatch.
- [ ] Add IPC isolation tests for workspace and enterprise boundaries.
- [ ] Add Windows packaging smoke test for all beta artifacts.
- [ ] Add release smoke test: install -> launch -> authenticate/onboard -> desktop visible -> clean shutdown -> relaunch -> restore.

## P2: Docs And Release Notes

- [ ] Update `ogun-os/README.md` from alpha to beta.
- [ ] Update `ogun-os/VERSION.md` to `0.1.0-beta` when the beta branch is ready.
- [ ] Update `ogun-os/CHANGELOG.md` so it exactly matches the shipped beta scope.
- [ ] Document any beta deviations from the planned docs before release.
- [ ] Add a beta architecture map that points from planned components to actual crate paths.
- [ ] Add developer build instructions for the current multi-workspace layout.
- [ ] Add operator install, repair, update, and uninstall documentation.
- [ ] Add known limitations that are truly beta limitations, not unimplemented core release promises.

## Explicit Non-Blockers For 0.1.0-beta

- [ ] Do not block Windows Desktop beta on macOS or Linux desktop packaging.
- [ ] Do not block Windows Desktop beta on Web Edition.
- [ ] Do not block Windows Desktop beta on Mobile Edition.
- [ ] Do not block Windows Desktop beta on Server Edition.
- [ ] Do not block Windows Desktop beta on Device Edition.
- [ ] Do not block 0.1.0-beta on the later stable storage-backend migration planned for 0.2.0.
