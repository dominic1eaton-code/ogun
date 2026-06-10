# Contributing to ogun OS

Thank you for helping build ogun OS. This project is still early, so the most
valuable contributions are precise, well-scoped changes that preserve the
system's security, boot, ABI, and layering invariants.

## Before You Start

Read these files first:

- `README.md` for the umbrella repository map and quick-start commands.
- `DESIGN.md` for architecture boundaries and invariants.
- `SECURITY.md` before reporting vulnerabilities or changing security-sensitive
  code.
- `CHANGELOG.md` for release scope and known limitations.
- `ogun-docs/0.1.0-beta-release/` for the current beta architecture and product
  specs.

If implementation and documentation disagree, call that out in the issue or
merge request. Do not silently broaden the release scope.

## Ways to Contribute

- Fix bugs in runtime, device, SDK, component, app, or tool workspaces.
- Improve tests for boot, image validation, IPC, capability checks, storage,
  configuration loading, and app lifecycle behavior.
- Clarify docs when architecture, release scope, or developer setup is hard to
  follow.
- Prototype features in `ogun-experimental/` before promoting them into a
  runtime workspace.
- Improve platform support while preserving the shared host, driver, and SDK
  contracts.

## Issue Guidelines

When reporting a bug, include:

- A short summary of the expected and actual behavior.
- The workspace and component involved, such as `ogun-runtime/src/ogun-kernel`
  or `ogun-tools/src/ogun-image-tool`.
- Host platform, Rust version, Node/npm version when relevant, and target
  platform.
- Reproduction steps, logs, stack traces, screenshots, or sample config.
- Whether the issue affects boot, image verification, capability enforcement,
  Opon isolation, or release artifacts.

Do not include secrets, signing keys, private images, tokens, audit logs with
personal data, or vulnerability details in a public issue. Use the process in
`SECURITY.md` for private disclosure.

## Merge Request Workflow

1. Open or reference an issue for non-trivial work.
2. Create a focused branch from the current development branch.
3. Keep changes scoped to the relevant workspace and component boundary.
4. Add or update tests for behavioral changes.
5. Update documentation when behavior, architecture, commands, or release scope
   changes.
6. Run the relevant checks before requesting review.
7. Summarize the change, tests run, and any residual risk in the merge request.

Small documentation fixes may skip the issue step.

## Development Checks

Run checks from the workspace you changed:

```powershell
cd C:\dev\ogun\ogun-runtime
cargo check --workspace
cargo test --workspace
```

```powershell
cd C:\dev\ogun\ogun-sdk
cargo check --workspace
cargo test --workspace
```

```powershell
cd C:\dev\ogun\ogun-devices
cargo check --workspace
cargo test --workspace
```

For Tauri tools:

```powershell
cd C:\dev\ogun\ogun-tools\src\ogun-image-tool
npm install
npm run tauri dev
```

If a workspace cannot currently pass a full check because of known alpha
scaffolding, run the narrowest meaningful command and document the blocker in
the merge request.

## Coding Standards

- Prefer existing local patterns over new abstractions.
- Keep Rust crates small, typed, and explicit about ownership and lifecycle.
- Preserve SDK ABI constants within a release series.
- Use structured parsers for structured formats such as TOML, JSON, manifests,
  image headers, and package metadata.
- Avoid direct host OS calls outside host, driver, emulator backend, setup, and
  tooling layers.
- Keep generated artifacts, private keys, local config, and build outputs out of
  source directories unless they belong in `ogun-artifacts/` as release outputs.
- Write comments for non-obvious constraints, not for obvious control flow.

## Architecture Invariants

Production code must preserve these rules:

- Image signatures are always verified before boot.
- Bootable runtime images must be platform images with a compatible ABI.
- The bootloader must halt on verification failure without continuing into the
  runtime.
- Opon isolation remains enforced in production.
- Every capability grant or denial is audited before returning to the caller.
- IPC messages are typed Elegua messages with context metadata.
- Kernel, session, app, service, module, driver, device, and host boundaries stay
  explicit.
- Lower layers do not depend on higher layers.
- Host OS APIs are accessed only through approved host, driver, emulator, setup,
  or tooling boundaries.
- `CleanShutdownMarker` remains the final clean-shutdown act.

## Commit and Review Expectations

Use clear commit messages:

```text
area: short imperative summary
```

Examples:

- `runtime: validate image section hashes before handoff`
- `sdk: document app capability manifest fields`
- `tools: add image inspection error state`

Reviewers should focus on correctness, security properties, architecture
boundaries, tests, and release scope. Style-only feedback should be kept small
unless it affects maintainability.

## Documentation Updates

Update docs when you:

- Change commands, setup steps, artifact names, or supported platforms.
- Add, remove, or rename a workspace, crate, app, service, driver, or tool.
- Change boot flow, image layout, ABI handling, IPC, capability checks, storage,
  config, or security policy behavior.
- Fix a known limitation or introduce a new one.

Release-visible changes should also update `CHANGELOG.md`.

## License

By contributing, you agree that your contribution is licensed under the same
license as this repository, GPL-3.0, unless a subproject explicitly states a
different license for its own files.
