# ogun OS Design

This document summarizes the architecture and development boundaries for the
top-level ogun OS repository. The detailed release specifications live in
`ogun-docs/0.1.0-beta-release/`; this file is the short map contributors should
read before changing code.

## System Goal

ogun OS is a hosted operating-system layer. It runs on a host OS, presents a
consistent virtual hardware and runtime environment, verifies a signed platform
image, initializes a kernel and session manager, then runs services and
applications inside capability-gated workspaces.

The first public target is Windows x64 Desktop Edition. Other editions are
architected but not the initial beta release target.

## Lifecycle

```text
compile time
  -> Rust crates, Tauri apps, SDKs, services, drivers, and tools

build time
  -> ogun-image-builder creates signed .img platform images
  -> ogun-artifacts stages installers, images, checksums, and metadata

installation time
  -> ogun-setup / ogun-installer verifies the image
  -> ~/.ogun/ is scaffolded
  -> SystemKey and HostKey material are created or derived
  -> startup registration is configured

boot time
  -> ogun-desktop launches ogun-emulator
  -> virtual devices initialize
  -> ogun-uefi performs pre-boot policy and handoff
  -> ogun-bootloader verifies image, manifest, and host key
  -> ogun-host-service starts kernel and session runtime

runtime
  -> kernel subsystems initialize
  -> services start
  -> session context binds operator, workspace, enterprise, and trace IDs
  -> apps, packages, modules, plugins, extensions, and devices run
```

## Main Layers

| Layer | Responsibility |
|---|---|
| Host OS | Provides real process, filesystem, window, socket, keychain, and platform APIs. |
| Emulator and virtual devices | Present stable virtual monitor, CPU, host platform, network adapter, and UEFI layers. |
| Bootloader and image format | Verify signed platform images and installation integrity before runtime handoff. |
| Host service | Owns the single session-lifetime runtime process. |
| Kernel core | Initializes subsystems, services, modules, IPC, storage, security, display, and emulation. |
| Session manager | Owns authentication, operator/workspace context, session snapshots, crash recovery, and shutdown. |
| SDKs | Define ABI-stable contracts for apps, services, modules, packages, plugins, drivers, hosts, and devices. |
| Components and apps | Provide OS apps, utility apps, user apps, hosts, drivers, and services. |
| Tools and artifacts | Build, inspect, install, repair, update, and publish signed runtime artifacts. |

## Boot Chain

```text
ogun-desktop.exe
  -> ogun-emulator
      -> ogun-virtual-display-monitor
      -> ogun-virtual-native-host-platform
      -> ogun-virtual-cpu
      -> ogun-virtual-network-adapter
      -> ogun-uefi
      -> ogun-host-service
          -> ogun-bootloader
          -> ogun-kernel-core
          -> ogun-session-manager
```

Production boot must fail closed. If image authenticity, installation
integrity, ABI compatibility, or host key verification fails, the bootloader
halts before any higher runtime code executes.

## Kernel Subsystems

The planned beta runtime initializes 15 kernel subsystems in a strict order:

| Order | Subsystem |
|---|---|
| 1 | `ogun-subsystem-telemetry` |
| 2 | `ogun-subsystem-memory` |
| 3 | `ogun-subsystem-process` |
| 4 | `ogun-subsystem-ipc` |
| 5 | `ogun-subsystem-storage` |
| 6 | `ogun-subsystem-vfs` |
| 7 | `ogun-subsystem-security` |
| 8 | `ogun-subsystem-services` |
| 9 | `ogun-subsystem-host` |
| 10 | `ogun-subsystem-session` |
| 11 | `ogun-subsystem-display` |
| 12 | `ogun-subsystem-state` |
| 13 | `ogun-subsystem-components` |
| 14 | `ogun-subsystem-network` |
| 15 | `ogun-subsystem-emulation` |

Subsystems are statically linked `rlib` crates in the runtime. Shared handles
should remain explicit, typed, and capability-gated where they cross privilege
boundaries.

## Communication

Elegua is the canonical communication protocol. Cross-boundary runtime
communication should use typed messages carrying context metadata such as
operator, workspace, enterprise, trace, span, sender, priority, and timestamp.

Rules:

- Do not introduce silent side channels between runtime components.
- Do not pass raw untyped bytes across layer boundaries when an Elegua message
  or SDK type exists.
- Preserve workspace and enterprise context when forwarding messages.
- Route external ingress through explicit gateway, host, driver, or tool
  boundaries.

## Storage and Namespaces

`ogun-subsystem-storage` currently uses RustyDB as the embedded database
backend. The VFS exposes namespaced resource addresses such as:

```text
ogun://
system://
user://
security://
app://
data://
network://
agent://
enterprise://
workspace://
session://
telemetry://
```

Generated installation state belongs under `~/.ogun/`, not in source
workspaces. Private keys and local secrets must not be committed.

## Security Model

Security depends on layered verification:

- Image signing key verifies `.img` authenticity.
- System key signs and verifies local installation manifest state.
- Host key is derived from image and system identity for the running
  installation.
- Opon Protocol enforces cross-enterprise isolation.
- Capabilities gate IPC, VFS, virtual devices, package loading, extensions, and
  privileged operations.
- Audit entries are written before grant or denial results are returned.

## Component Boundaries

- SDK crates define contracts; runtime crates enforce them.
- Apps do not call kernel internals directly.
- Modules use module context APIs, not arbitrary subsystem references.
- Drivers translate platform APIs into Ogun traits and do not call upward into
  app or service layers.
- Host OS APIs are isolated to hosts, drivers, emulator backend, setup, and
  tooling.
- Tools can inspect and build artifacts but should not weaken runtime security
  assumptions.

## UI and App Boundaries

Tier-2 OS apps provide core operating surfaces such as desktop, shell, explorer,
settings, app manager, security center, command center, and UI components.

Tier-3 utility apps provide notes, tasks, focus, calendar, contacts, messenger,
search, and assistant surfaces.

Tier-4 user apps implement the personal enterprise suite, including `enzo`,
`kogi`, `dongo`, `ume`, `heshima`, `shango`, `igi`, and `moto`.

Apps should declare capabilities, use SDK traits, communicate through IPC, and
keep workspace and enterprise context intact.

## Release Scope Discipline

For `0.1.0-beta`, Windows x64 Desktop Edition is the release target. Linux,
macOS, web, server, mobile, and device editions may have design or scaffolding
work, but should not be documented as shipped unless release artifacts and tests
exist.

When a change affects beta scope, update:

- `CHANGELOG.md`
- `ogun-docs/0.1.0-beta-release/`
- relevant workspace README files
- artifact expectations in `ogun-artifacts/`

## Non-Negotiable Invariants

- Production boot verifies image signatures.
- `validate_image_signature` cannot disable production verification.
- ABI version mismatches reject components.
- Opon isolation remains enforced in production.
- Capability grants and denials are audited.
- `CleanShutdownMarker` is written last during clean shutdown.
- Private signing keys are never committed.
- Generated release artifacts are never overwritten in place.
- Lower layers do not depend on higher layers.
