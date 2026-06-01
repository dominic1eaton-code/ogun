# ogun OS

ogun OS is a Rust-native operating-system layer for independent workers. It
runs on top of an existing host operating system rather than replacing it, then
presents a signed, capability-gated, workspace-oriented runtime with its own
boot chain, virtual devices, kernel subsystems, SDKs, applications, tools, and
release artifacts.

This top-level repository is the umbrella workspace for the Ogun ecosystem. It
collects the implementation workspaces, product documentation, configuration
templates, release artifacts, protocol libraries, and supporting crates used to
build the planned `0.1.0-beta` Windows x64 Desktop Edition.

## Status

Current development state: `0.1.0-alpha`

Planned first public beta: `0.1.0-beta`, targeted for Windows x64 Desktop
Edition in June 2026.

The beta release is intended to establish the foundational runtime: virtual UEFI
layer, bootloader, kernel core, session manager, 15 kernel subsystems, emulator,
virtual devices, desktop host, drivers, OS apps, user apps, tools, SDKs, signed
images, and installer artifacts.

## Key Features

- Runs as a hosted OS layer on Windows first, with Linux, macOS, web, mobile,
  server, and device editions designed for later targets.
- Uses a signed `.img` platform image format with ed25519 verification and
  per-section SHA-256 checks.
- Boots through `ogun-emulator`, virtual hardware, `ogun-uefi`,
  `ogun-bootloader`, `ogun-host-service`, `ogun-kernel-core`, and
  `ogun-session-manager`.
- Exposes a capability-gated IPC and namespace system through the Elegua
  Protocol.
- Enforces the Opon Protocol for cross-enterprise data isolation in production
  builds.
- Organizes runtime behavior into 15 statically linked kernel subsystems.
- Supports Tier-1 kernel services, Tier-2 OS apps, Tier-3 utility apps, and
  Tier-4 personal enterprise applications.
- Provides SDK crates for apps, services, modules, packages, plugins, drivers,
  hosts, devices, and components.
- Uses RustyDB as the current embedded storage backend for session state,
  registries, audit indexes, and node identity.

## Repository Map

| Path | Purpose |
|---|---|
| `ogun-os/` | Main OS workspace, clients, host server scaffold, and beta tracking. |
| `ogun-runtime/` | Runtime crates such as types, image format, bootloader, kernel, and session manager. |
| `ogun-devices/` | Emulator, virtual UEFI, virtual CPU, virtual display, virtual host platform, and virtual network adapter. |
| `ogun-components/` | Tier-2 and Tier-3 apps, hosts, drivers, and services. |
| `ogun-apps/` | Tier-4 personal enterprise application suite. |
| `ogun-sdk/` | Public SDK traits, ABI constants, and component contracts. |
| `ogun-tools/` | Setup and image tooling, including Tauri-based installer and image tool workspaces. |
| `ogun-config/` | Seed configuration templates for `ogun.toml`, `display.toml`, and UEFI/runtime configuration. |
| `ogun-artifacts/` | Staging area for built images, installers, checksums, and release metadata. |
| `ogun-docs/` | Canonical product, architecture, release, and execution-model documents. |
| `ogun-sites/` | Public site and documentation site sources. |
| `elegua/` | Ogun's typed communication and IPC protocol. |
| `rustydb/` | Embedded database backend used by the storage subsystem. |
| `bula/`, `jaku/`, `oya/` | Supporting libraries and experiments used by the wider ecosystem. |
| `ogun-test-features/` | Test feature sandboxes and prototypes. |

## Runtime Shape

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
          -> services, apps, drivers, modules, and packages
```

## Development Requirements

Required for most workspaces:

- Rust stable toolchain with Cargo.
- Git.
- Windows x64 for the current beta target.

Required for Tauri tools and desktop surfaces:

- Node.js and npm.
- Tauri 2 prerequisites for the target platform.
- Platform SDKs as required by the specific host or driver crate.

Optional depending on the workspace:

- WASM target support for browser-facing work.
- Android NDK or Xcode for future mobile hosts.

## Quick Start

Clone the umbrella workspace and inspect the release docs:

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
```

Run a Tauri tool during development:

```powershell
cd C:\dev\ogun\ogun-tools\src\ogun-image-tool
npm install
npm run tauri dev
```

The top-level `Cargo-temp.toml` captures the intended combined workspace
membership. The repo currently favors focused checks inside each project
workspace until the umbrella workspace is promoted to a canonical top-level
`Cargo.toml`.

## Documentation

- `CHANGELOG.md` tracks release-facing changes and current beta scope.
- `DESIGN.md` summarizes the architecture and development boundaries.
- `CONTRIBUTING.md` explains contribution workflow and review expectations.
- `SECURITY.md` explains vulnerability disclosure and supported versions.
- `GOVERNANCE.md` describes project roles and decision making.
- `SUPPORT.md` lists where to get help.
- `ogun-docs/0.1.0-beta-release/` contains the current beta product,
  architecture, and execution-model specs.

## License

This repository is licensed under GPL-3.0. See `LICENSE.md` for the full text.
