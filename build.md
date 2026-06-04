# Building ogun OS

This file describes how to build the top-level `C:\dev\ogun` umbrella
repository and the Rust crates that live inside its git submodules.

The root `Cargo.toml` is a virtual workspace. It pulls together the active Rust
packages from:

- top-level support crates: `bula`, `elegua`, `jaku`, `oya`, `rustydb`
- runtime crates in `ogun-runtime/src/*`
- SDK crates in `ogun-sdk/src/*`
- device crates in `ogun-devices/src/*`
- OS client and server crates in `ogun-os/src/clients/*` and
  `ogun-os/src/servers/*`
- component apps, hosts, drivers, and services in `ogun-components/src/*`
- Tier-4 user apps in `ogun-apps/src/*`
- Tauri Rust backends in `ogun-tools/src/*/src-tauri`

Non-Rust documentation, configuration, site, and artifact submodules are kept in
the repo but are not Cargo workspace members.

## Requirements

- Windows x64 for the current beta target.
- Rust stable with Cargo.
- Git with submodule support.
- Node.js and npm for Tauri tool frontends.
- Tauri 2 platform prerequisites for setup and image tooling.

Check the installed Rust toolchain:

```powershell
cargo --version
rustc --version
```

## Submodules

Initialize or update submodules before building:

```powershell
cd C:\dev\ogun
git submodule update --init --recursive
```

After switching branches, run the same command again so nested workspaces stay
aligned with the root manifest.

## Fast Validation

Validate the Cargo workspace shape without compiling dependencies:

```powershell
cd C:\dev\ogun
cargo metadata --no-deps
```

Run a full type check for all root workspace members:

```powershell
cd C:\dev\ogun
cargo check --workspace
```

## Build

Debug build:

```powershell
cd C:\dev\ogun
cargo build --workspace
```

Release build:

```powershell
cd C:\dev\ogun
cargo build --workspace --release
```

Build one package:

```powershell
cargo build -p ogun-kernel
cargo build -p ogun-host-service
cargo build -p ogun-emulator
```

Run tests:

```powershell
cargo test --workspace
```

## Tauri Tools

The root Cargo workspace includes the Rust backends for the Tauri setup and
image tools. The web frontends still need npm dependencies inside each tool
directory.

Setup tool:

```powershell
cd C:\dev\ogun\ogun-tools\src\ogun-setup
npm install
npm run tauri dev
```

Image tool:

```powershell
cd C:\dev\ogun\ogun-tools\src\ogun-image-tool
npm install
npm run tauri dev
```

## Focused Workspace Checks

When working in one submodule, focused checks are faster:

```powershell
cd C:\dev\ogun\ogun-runtime
cargo check --workspace
```

```powershell
cd C:\dev\ogun\ogun-sdk
cargo check --workspace
```

```powershell
cd C:\dev\ogun\ogun-devices
cargo check --workspace
```

```powershell
cd C:\dev\ogun\ogun-components
cargo check --workspace
```

## Build Outputs

Cargo outputs are written under:

```text
C:\dev\ogun\target\
```

Release artifacts that are meant to be published should be copied or generated
through the release pipeline into:

```text
C:\dev\ogun\ogun-artifacts\
```

Do not commit private signing keys, local install state, or generated
`~/.ogun/` data.

## Clean

Remove Cargo build outputs:

```powershell
cd C:\dev\ogun
cargo clean
```

Remove npm dependencies for a Tauri tool only if you intend to reinstall them:

```powershell
cd C:\dev\ogun\ogun-tools\src\ogun-image-tool
Remove-Item -LiteralPath node_modules -Recurse -Force
```

## Development

```powershell

(cargo metadata --format-version 1 | ConvertFrom-Json).workspace_members | ForEach-Object { cargo install --path ($_ -split ' ')[0] }

cd ogun-so/src/ogun-desktop

cargo install --path .

cargo install --path .  --root

ogun_desktop

cargo tree --workspace --depth 0

cargo install cargo-workspaces
cargo ws list

```

## Current Scope

The first public target is `0.1.0-beta` for Windows x64 Desktop Edition. Other
platforms are represented by scaffolding and design documents, but release-grade
artifacts should only be produced when the corresponding code, docs, and
checksums are ready.
