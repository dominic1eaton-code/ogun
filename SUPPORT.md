# Support

This document explains where to get help with ogun OS, how to ask good
questions, and which channels to use for bugs, security issues, contribution
questions, and release problems.

## Project Status

ogun OS is currently alpha-stage source moving toward the planned
`0.1.0-beta` Windows x64 Desktop Edition. Support is best-effort until public
beta artifacts are released.

Expect some workspaces to be scaffolding, experimental, or temporarily out of
sync while the architecture is being consolidated.

## Where to Start

| Need | Start here |
|---|---|
| Understand the project | `README.md` |
| Understand architecture | `DESIGN.md` and `ogun-docs/0.1.0-beta-release/` |
| Report a bug | Open an issue in the relevant project space. |
| Report a vulnerability | Follow `SECURITY.md`; do not open a public issue. |
| Contribute a fix | Read `CONTRIBUTING.md`. |
| Understand leadership and decisions | Read `GOVERNANCE.md`. |
| Track release changes | Read `CHANGELOG.md`. |
| Check license terms | Read `LICENSE.md`. |

## Asking for Help

When asking for technical help, include:

- What you are trying to do.
- The exact workspace and component.
- The command you ran.
- The full error output or relevant log excerpt.
- Your host platform and target platform.
- Rust version, Node/npm version, and Tauri version when relevant.
- Whether you are using source, a local artifact, or a signed release artifact.

Example:

```text
Workspace: ogun-tools/src/ogun-image-tool
Command: npm run tauri dev
Host: Windows 11 x64
Rust: 1.xx.x
Node: 20.x
Problem: Tauri backend fails before window creation
Output: ...
```

## Common Workspaces

| Workspace | Common support topic |
|---|---|
| `ogun-runtime/` | Types, image format, bootloader, kernel, session manager. |
| `ogun-devices/` | Emulator, virtual UEFI, virtual devices. |
| `ogun-sdk/` | App, service, module, package, plugin, driver, host, and device contracts. |
| `ogun-components/` | OS apps, utility apps, hosts, drivers, services. |
| `ogun-apps/` | Tier-4 user apps and personal enterprise suite. |
| `ogun-tools/` | Setup, image tool, install, repair, and artifact inspection. |
| `ogun-config/` | Runtime config templates and safe defaults. |
| `ogun-artifacts/` | Images, installers, checksums, release metadata. |
| `ogun-docs/` | Product, architecture, release, and execution-model docs. |
| `elegua/` | IPC and typed communication protocol. |
| `rustydb/` | Embedded database behavior. |

## Bug Reports

Open a public issue for ordinary bugs. Include reproduction steps and keep the
report focused.

Use private security reporting for:

- Signature bypasses.
- Boot verification failures that continue into runtime.
- Sandbox escapes.
- Opon isolation breaks.
- Capability or audit bypasses.
- Key, secret, token, or private data exposure.
- Remote code execution or privilege escalation.

## Release and Install Support

For public beta and later artifacts, include:

- Artifact name and version.
- SHA-256 checksum you observed.
- Whether signature or checksum verification passed.
- Install path and host platform.
- `~/.ogun/logs/boot.log` excerpt if relevant, with private data removed.
- Whether this is a clean install, repair, update, or image replacement.

Never post private signing keys, system private keys, recovery secrets, tokens,
or full audit logs publicly.

## Development Commands

Focused Rust checks:

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

Tauri tool development:

```powershell
cd C:\dev\ogun\ogun-tools\src\ogun-image-tool
npm install
npm run tauri dev
```

If a command fails because the workspace is still alpha scaffolding, include the
failure and ask whether there is a narrower check for that area.

## Response Expectations

Support is best-effort during alpha. Maintainers and contributors may prioritize:

- Security reports.
- Release-blocking beta work.
- Reproducible boot, image, installer, kernel, and runtime failures.
- Clear merge requests with tests.
- Documentation fixes that unblock contributors.

Please avoid duplicate pings unless new information is available.
