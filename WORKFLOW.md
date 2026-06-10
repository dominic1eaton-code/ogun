# WORKFLOW.md — ogun OS Git Branching Strategy and Workflow

**Version:** 0.1.0-beta  
**Owner:** Dominic Eaton ([@eatondo](https://gitlab.com/eatondo))  
**Organization:** The Ogun Foundation  
**Primary Repository:** https://gitlab.com/ogun-foundation/ogun  
**License:** GPL-3.0  

---

## Contents

1. [Repository Graph Overview](#1-repository-graph-overview)
2. [Permanent Branches](#2-permanent-branches)
3. [Branch Naming Conventions](#3-branch-naming-conventions)
4. [Per-Repository Branching Rules](#4-per-repository-branching-rules)
5. [Complete Feature Development Workflow](#5-complete-feature-development-workflow)
6. [Release Workflow](#6-release-workflow)
7. [Hotfix and Security Workflow](#7-hotfix-and-security-workflow)
8. [ABI and Protocol Change Workflow](#8-abi-and-protocol-change-workflow)
9. [Submodule Synchronization Workflow](#9-submodule-synchronization-workflow)
10. [Versioning and Tagging](#10-versioning-and-tagging)
11. [CI/CD Pipeline Stages](#11-cicd-pipeline-stages)
12. [Merge Request Standards](#12-merge-request-standards)
13. [Commit Message Convention](#13-commit-message-convention)
14. [Branch Protection Rules](#14-branch-protection-rules)
15. [Environment and Deployment Map](#15-environment-and-deployment-map)
16. [Scheduled Pipeline Jobs](#16-scheduled-pipeline-jobs)
17. [Repository-Specific Notes](#17-repository-specific-notes)
18. [Quick Reference Command Sheets](#18-quick-reference-command-sheets)

---

## 1. Repository Graph Overview

ogun OS is structured as a **monorepo umbrella** with git submodules. The root
repository (`ogun`) declares a virtual Cargo workspace (`Cargo.toml`) that
references member crates across every submodule. Each submodule is also an
independently cloneable, buildable repository with its own CI pipeline.

### Umbrella Repository

| Repository | GitLab Path | Role |
|---|---|---|
| `ogun` | `ogun-foundation/ogun` | Umbrella workspace; submodule host; release coordinator |

### Rust Implementation Submodules

| Repository | GitLab Path | Workspace Members |
|---|---|---|
| `ogun-runtime` | `ogun-foundation/ogun-runtime` | `ogun-types`, `ogun-image-format`, `ogun-image-builder`, `ogun-bootloader`, `ogun-kernel-core`, `ogun-session-manager`, `ogun-host-service` |
| `ogun-devices` | `ogun-foundation/ogun-devices` | `ogun-emulator`, `ogun-emulator-backend`, `ogun-uefi`, `ogun-virtual-cpu`, `ogun-virtual-display-monitor`, `ogun-virtual-platform-host`, `ogun-virtual-network-adapter` |
| `ogun-os` | `ogun-foundation/ogun-os` | `ogun-desktop` (Tauri), `ogun-app`, `ogun-host-server`, `ogun-web` |
| `ogun-sdk` | `ogun-foundation/ogun-sdk` | `ogun-app-sdk`, `ogun-service-sdk`, `ogun-kernel-sdk`, `ogun-driver-sdk`, `ogun-module-sdk`, `ogun-device-sdk`, `ogun-plugin-sdk`, `ogun-component-sdk` |
| `ogun-components` | `ogun-foundation/ogun-components` | Tier-2 apps, Tier-3 apps, hosts, drivers, services |
| `ogun-apps` | `ogun-foundation/ogun-apps` | Tier-4 personal enterprise apps (`enzo`, `kogi`, `dongo`, `ume`, `shango`, `heshima`, `igi`, `moto`, and others) |
| `ogun-tools` | `ogun-foundation/ogun-tools` | `ogun-setup` (Tauri), `ogun-image-tool` (Tauri), future `ogun-ide` |

### Protocol and Support Library Submodules

| Repository | GitLab Path | Role |
|---|---|---|
| `elegua` | `ogun-foundation/elegua` | Typed IPC and Elegua Protocol implementation |
| `rustydb` | `ogun-foundation/rustydb` | Embedded database backend; storage subsystem dependency |
| `bula` | `ogun-foundation/bula` | UI generation support library |
| `jaku` | `ogun-foundation/jaku` | Release automation tooling |
| `oya` | `ogun-foundation/oya` | Architecture generation and modeling |

### Configuration, Artifact, and Documentation Submodules

| Repository | GitLab Path | Role |
|---|---|---|
| `ogun-config` | `ogun-foundation/ogun-config` | Seed configuration templates (`ogun.toml`, `display.toml`, `emulation.toml`, `uefi.toml`) |
| `ogun-artifacts` | `ogun-foundation/ogun-artifacts` | Staging area for built images, installers, checksums, and release metadata |
| `ogun-docs` | `ogun-foundation/ogun-docs` | Canonical product, architecture, release, and execution-model specifications |
| `ogun-sites` | `ogun-foundation/ogun-sites` | Public site and documentation site sources (Cloudflare Workers Pages) |
| `ogun-devops` | `ogun-foundation/ogun-devops` | Shared CI/CD YAML templates and `update_version.py` script |
| `ogun-experimental` | `ogun-foundation/ogun-experimental` | Experimental sandbox crates and prototype workspaces |

---

## 2. Permanent Branches

Every repository in the ogun graph maintains the same two permanent branches.
No other branches are permanent; all others are deleted after merge.

### `main`

- Contains only production-ready, release-tagged code.
- Every commit on `main` must have passed the full CI pipeline including all
  check, test, build, audit, and validate stages.
- Direct pushes to `main` are blocked; merges arrive only through a merge
  request from a `release/*` branch (for planned releases) or a `security/*`
  branch (for emergency security patches).
- Every merge into `main` must be tagged immediately with a semver version
  using `update_version.py`.
- `main` is the source of truth for all public release artifacts and for the
  GitLab release page.

### `develop`

- The integration branch for all active development.
- All `feat/*`, `fix/*`, `refactor/*`, `docs/*`, `chore/*`, `ci/*`, and
  `p0/*` branches merge into `develop`, never directly into `main`.
- `develop` must always be in a buildable state. A broken `develop` branch
  is a P0 incident for the responsible workspace.
- `cargo check --workspace` and `cargo fmt --all` must pass on `develop` at
  all times.
- Nightly CI runs on `develop`; nightly build failures are investigated before
  the next working day.

---

## 3. Branch Naming Conventions

All branch names use lowercase kebab-case. The prefix determines which CI
pipeline rules fire and which merge targets are permitted.

| Prefix | Purpose | Merges Into | Example |
|---|---|---|---|
| `feat/` | New feature or capability | `develop` | `feat/ogun-virtual-cpu-tick-loop` |
| `fix/` | Bug fix | `develop` | `fix/bootloader-halt-on-abi-mismatch` |
| `docs/` | Documentation change only | `develop` | `docs/update-session-manager-readme` |
| `refactor/` | Refactor with no behavior change | `develop` | `refactor/elegua-message-routing` |
| `ci/` | CI/CD pipeline change | `develop` | `ci/add-windows-cross-check` |
| `chore/` | Housekeeping, dependency updates, metadata | `develop` | `chore/update-cargo-lock` |
| `p0/` | Critical unplanned fix on `develop` | `develop` (fast-tracked) | `p0/kernel-crash-on-startup` |
| `release/` | Release preparation branch | `main` then back-merged to `develop` | `release/0.1.0-beta` |
| `security/` | Security vulnerability patch | `main` then back-merged to `develop` | `security/image-signature-bypass` |
| `abi/` | ABI or protocol change requiring extra review | `develop` | `abi/elegua-protocol-v2` |

### Branch Naming Rules

- Use only lowercase letters, digits, and hyphens after the prefix slash.
- Keep names concise but descriptive enough to identify the workspace and
  change without reading the branch's commit history.
- For changes scoped to a single submodule, prefix the description with the
  submodule name: `feat/ogun-sdk-plugin-loader`, `fix/rustydb-wal-corruption`.
- For changes that span multiple submodules, describe the functional area
  instead: `feat/component-hot-reload`, `fix/boot-sequence-ordering`.
- Branch names must not contain path separators, dots, or consecutive hyphens.

---

## 4. Per-Repository Branching Rules

All repositories share the same permanent branch model and naming scheme.
The rules below note any repository-specific variations.

### `ogun` (Umbrella)

- Never contains implementation code; contains only `Cargo.toml`, top-level
  documentation, and `.gitmodules`.
- `feat/*` and `fix/*` branches in the umbrella are for workspace manifest
  changes, submodule pointer updates, and documentation changes only.
- Submodule pointer bumps always arrive via MR from a `chore/` branch:
  `chore/bump-ogun-runtime-to-abc1234`.
- Release preparation branches (`release/*`) live in the umbrella and are
  responsible for coordinating the submodule pointer freeze.

### `ogun-runtime`

- The most security-critical repository in the graph. Contains the bootloader,
  image format, kernel core, session manager, and host service.
- Any change to `ogun-bootloader`, `ogun-image-format`, `ogun-session-manager`,
  or `ogun-host-service` that touches security-critical code paths requires two
  maintainer approvals before merge.
- Changes to `OGUN_ABI_VERSION` must use an `abi/` branch regardless of scope.
- `cargo test --workspace` must pass with zero failures before any MR into
  `develop` is approved.

### `ogun-sdk`

- ABI stability is an explicit contract within a release series. SDK crates
  must not change public trait signatures or `OGUN_ABI_VERSION` constants on
  a `fix/*` branch. ABI changes always require an `abi/` branch.
- New SDK crates are introduced on `feat/` branches and land in `develop`
  before any downstream workspace can depend on them.

### `ogun-devices`

- Virtual device implementations (`ogun-virtual-cpu`, `ogun-virtual-display-monitor`,
  `ogun-virtual-platform-host`, `ogun-virtual-network-adapter`) must include
  smoke tests and a deterministic tick runner test for any new feature MR.
- The Tauri-dependent `ogun-emulator` crate requires a Windows runner for
  integration tests. MRs that touch `ogun-emulator-backend` must trigger the
  `ENABLE_WINDOWS_BUILD=true` pipeline flag.

### `ogun-os`

- Contains the user-facing launcher (`ogun-desktop`, Tauri) and the host server
  scaffold. Any change to the Tauri frontend must pass `npm run tauri dev` on
  the Windows runner before merge.
- The `ogun-desktop/src-tauri` Rust backend and the web frontend are developed
  in the same branch; split MRs are not permitted for Tauri apps.

### `ogun-components`

- Tier-2 and Tier-3 app components are independently releasable as `.dll`/`.so`
  runtime-loaded libraries. New component crates are introduced with a
  corresponding `ogun-component.toml` manifest and a minimum smoke test.
- The `ogun-components` workspace is always built with `cargo build --workspace`
  before `ogun-desktop` is built, as the desktop app loads components at runtime.

### `ogun-apps`

- Tier-4 personal enterprise apps (`enzo`, `kogi`, `dongo`, `ume`, `shango`,
  `heshima`, `igi`, `moto`). Each app is an independent `cdylib` crate.
- App feature work uses `feat/appname-feature` naming:
  `feat/enzo-portfolio-summary`, `feat/dongo-task-board`.
- App MRs must demonstrate that the app builds, ticks, responds to IPC, and
  shuts down cleanly using the `OgunApp` SDK trait lifecycle.

### `ogun-tools`

- Contains the `ogun-setup` installer and `ogun-image-tool` image builder,
  both Tauri applications.
- Changes to `ogun-setup` are release-gated; they must be reviewed by a
  maintainer with Windows installation environment access.
- Changes to `ogun-image-tool` that alter the image format must be accompanied
  by corresponding changes to `ogun-image-format` in `ogun-runtime`.

### `elegua`

- The Elegua Protocol is a core ABI surface. Any change to message schema
  structs, operator/workspace/trace context fields, or channel constants must
  use an `abi/` branch and include protocol invariant preservation documentation
  in the MR description.
- The `operator_id`, `workspace_id`, `trace_id`, and `enterprise_id` context
  fields on IPC messages are frozen for the 0.1.0 release series.

### `rustydb`

- The storage backend. Any change to the WAL format, key-value API, or
  transaction semantics must include durability and crash-consistency tests.
- Schema migration work that affects the session, modules, or security audit
  log tables must be coordinated with `ogun-runtime` via a paired MR set.

### `ogun-devops`

- The CI/CD template repository. Changes to shared YAML (`configure.yml`,
  `build.yml`, `check.yml`, `test.yml`, `validate.yml`, `sast.yml`,
  `package.yml`, `deploy.yml`, `version.yml`) affect every downstream repo.
- All changes to `ogun-devops` must be tested by including the branch ref in
  a downstream repo pipeline before merging.
- Use `ci/` branches for all `ogun-devops` changes.

---

## 5. Complete Feature Development Workflow

This is the standard path for all new work: features, fixes, refactors, docs
updates, chores, and CI changes.

### Step 1 — Read the relevant documentation

Before starting any implementation branch, read:

- `README.md` in the affected submodule
- `DESIGN.md` at the umbrella level for architecture boundaries and invariants
- `CONTRIBUTING.md` for coding standards and review expectations
- `CHANGELOG.md` for current release scope and known limitations
- The relevant design invariant list (I-01 through I-35 in `DESIGN.md`) for
  security-critical work

### Step 2 — Open or reference an issue

Open a GitLab issue in the affected submodule repository before starting any
non-trivial branch. The issue documents the expected behavior, scope, and any
residual risks. Reference the issue number in both the branch name (optional)
and the MR description (required).

Small documentation fixes and typo corrections may skip this step.

### Step 3 — Create the branch from `develop`

```powershell
# Always branch from the latest develop
git checkout develop
git pull origin develop

# Create the feature branch
git checkout -b feat/ogun-sdk-plugin-loader
```

For work in a submodule, create the branch in that submodule's repository:

```powershell
cd C:\dev\ogun\ogun-sdk
git checkout develop
git pull origin develop
git checkout -b feat/plugin-loader-trait
```

### Step 4 — Implement and test locally

Run the focused workspace check for the submodule you are changing:

```powershell
# From the relevant submodule directory
cargo fmt --all
cargo check --workspace
cargo test --workspace
cargo clippy --workspace --all-targets --all-features -- -D warnings
```

For Tauri tools:

```powershell
cd C:\dev\ogun\ogun-tools\src\ogun-image-tool
npm install
npm run tauri dev
```

### Step 5 — Commit using the convention

Write commits in the imperative form with a `area:` prefix. Each commit should
be atomic — one logical change per commit.

```text
sdk: add OgunPlugin trait with on_load and on_unload lifecycle hooks
sdk: implement plugin manifest schema validation
sdk: add integration test for plugin loader capability gating
```

### Step 6 — Push the branch and open a Merge Request

```powershell
git push -u origin feat/plugin-loader-trait
```

Open the MR in GitLab targeting `develop`. The MR description must include:

- A short summary of what changed and why.
- The issue number being resolved.
- Which workspaces and crates are affected.
- Which checks were run and passed locally.
- Any residual risk, known limitations, or follow-up issues.
- For ABI changes: explicit confirmation that invariants are preserved.

### Step 7 — CI pipeline runs automatically

The pipeline will run in this order for MRs:

1. **validate** — workspace metadata check, submodule health, VERSION.md check
2. **check** — `rustfmt`, `clippy`, `cargo check --workspace`
3. **test** — `cargo test --workspace`, doc tests, unit tests, integration tests
4. **build** — debug build (MRs); release build (on `main` merges and tags)
5. **audit** — `cargo-audit`, `cargo-deny`, supply-chain integrity check

All stages must pass green before a reviewer approves.

### Step 8 — Code review

At least one maintainer must review and approve the MR. For security-critical
code in `ogun-runtime` or `elegua`, two maintainer approvals are required.

Reviewers focus on: correctness, security properties, architecture boundary
preservation, test coverage, release scope accuracy, and documentation.
Style-only feedback should be kept minimal unless it affects maintainability.

### Step 9 — Merge and delete the branch

After approval, the MR author (or a maintainer) merges the branch using
GitLab's merge button. Use **merge commit** (not squash) for feature branches
so the history preserves individual commits for audit purposes.

Delete the source branch after merge. GitLab can be configured to do this
automatically.

### Step 10 — Update submodule pointer (if applicable)

If the work was in a submodule, the umbrella repository's submodule pointer
must be updated once the submodule's `develop` branch has been updated.

```powershell
cd C:\dev\ogun
git checkout develop
git submodule update --remote ogun-sdk
git add ogun-sdk
git commit -m "chore: bump ogun-sdk submodule to include plugin loader trait"
git push origin develop
```

---

## 6. Release Workflow

Releases are coordinated from the umbrella repository (`ogun`) and propagated
to all submodules in a defined order.

### Phase 1 — Feature freeze on `develop`

Announce a feature freeze on all active submodule `develop` branches. No new
`feat/*` branches are merged into `develop` during this window. Only `fix/*`,
`docs/*`, and `p0/*` branches may merge.

### Phase 2 — Create the release branch

Create a `release/*` branch from `develop` in the umbrella repository and in
each submodule that has changed since the last release.

```powershell
# Umbrella
cd C:\dev\ogun
git checkout develop
git pull origin develop
git checkout -b release/0.1.0-beta

# Each active submodule (example: ogun-runtime)
cd C:\dev\ogun\ogun-runtime
git checkout develop
git pull origin develop
git checkout -b release/0.1.0-beta
```

### Phase 3 — Release branch stabilization

On each `release/*` branch:

- Apply only bug fixes, documentation updates, and release metadata changes.
  No new features enter a release branch after creation.
- Update `VERSION.md` in each affected repository to the target version.
- Update `CHANGELOG.md` to move entries from `[Unreleased]` to the release
  version section with the correct release date.
- Run the full CI pipeline on the release branch. All stages must pass clean,
  including the Windows native Tauri build job.
- Verify the release gate conditions (from `DESIGN.md`) are all met:
  - All 0.1.0-beta Rust packages built and delivered.
  - All four artifact builds passing clean on Windows x64.
  - Three-stage boot verification passing on a clean install.
  - Full session lifecycle verified end-to-end.
  - Design invariants I-01 through I-35 confirmed enforced.
  - No P0 blockers outstanding.

### Phase 4 — Run the version tagging job

Use the `version:tag` CI job (from `version.yml`) to bump version files,
commit, and push a semver git tag:

```powershell
# Triggered via GitLab pipeline web UI or API with these variables:
# OGUN_VERSION = "0.1.0"
# OGUN_GATE    = "beta"
# OGUN_PUSH_BRANCH = "release/0.1.0-beta"
```

This runs `update_version.py --version 0.1.0 --gate beta --all-files --commit --push release/0.1.0-beta` and produces a `v0.1.0-beta` tag.

### Phase 5 — Merge the release branch into `main`

```powershell
# In each submodule (ogun-runtime example)
git checkout main
git merge --no-ff release/0.1.0-beta
git push origin main

# In the umbrella
git checkout main
git merge --no-ff release/0.1.0-beta
git push origin main
```

The merge into `main` triggers the full release pipeline: release build, Tauri
desktop bundle, Tauri setup bundle, component `.dll` build, SBOM generation,
attestation signing, packaging into `.ogpkg` archives, and GitLab release
creation.

### Phase 6 — Back-merge into `develop`

Immediately after merging into `main`, back-merge the release branch into
`develop` to ensure any release-day bug fixes are not lost:

```powershell
# In each submodule
git checkout develop
git merge --no-ff release/0.1.0-beta
git push origin develop

# In the umbrella
git checkout develop
git merge --no-ff release/0.1.0-beta
git push origin develop
```

### Phase 7 — Submodule pointer freeze and umbrella tag

After all submodule `main` branches are tagged, update the umbrella submodule
pointers to the tagged commits and tag the umbrella itself:

```powershell
cd C:\dev\ogun
git checkout main
git submodule update --remote
git add .
git commit -m "release: freeze submodule pointers for v0.1.0-beta"
git tag -a v0.1.0-beta -m "ogun OS 0.1.0-beta — Windows x64 Desktop Edition"
git push origin main --tags
```

### Phase 8 — Delete the release branch

After a successful release and back-merge, delete `release/0.1.0-beta` from
all repositories.

### Phase 9 — Increment develop to next version

After the release is complete, bump `develop` to the next development version:

```powershell
# Using the version:ci CI job with OGUN_VERSION="0.2.0", OGUN_GATE="alpha", OGUN_MATURITY="dev"
```

---

## 7. Hotfix and Security Workflow

### P0 Hotfix (Non-Security Critical Bug)

A P0 hotfix is an unplanned critical bug fix that cannot wait for the normal
`develop` integration cycle. It targets `develop` directly via a fast-tracked
`p0/` branch.

```powershell
git checkout develop
git pull origin develop
git checkout -b p0/kernel-crash-on-clean-shutdown

# Implement fix
# Run: cargo check, cargo test, cargo fmt

git commit -m "kernel: fix crash on clean shutdown when no active session"
git push -u origin p0/kernel-crash-on-clean-shutdown
```

Open an MR targeting `develop` with the `p0/` prefix. A single maintainer
approval is sufficient for a P0 merge during a production incident, but the
MR description must document the root cause and confirm no security invariants
are affected.

### Security Vulnerability Patch

Security patches follow a different path: they land on `main` first, bypassing
`develop`, then are back-merged. This prevents vulnerability details from
appearing in `develop` history before a fix is published.

**Use the private disclosure process in `SECURITY.md` before creating any
branch for a security issue.**

```powershell
# Branch from main
git checkout main
git pull origin main
git checkout -b security/image-signature-bypass

# Implement fix
# Run full test suite locally on Windows x64

git commit -m "bootloader: fix image signature bypass on malformed section table"
git push -u origin security/image-signature-bypass
```

Open the MR targeting `main` as a confidential MR in GitLab. Two maintainer
approvals are required. The `security/*` CI rule triggers the full security
audit stage in addition to the standard check/test/build pipeline.

After merge into `main`:

1. Tag the security release immediately.
2. Back-merge into `develop`.
3. Publish a security advisory.
4. Update `CHANGELOG.md` under `### Security`.

---

## 8. ABI and Protocol Change Workflow

Any change that modifies a public ABI surface — SDK trait signatures,
`OGUN_ABI_VERSION` constants, Elegua Protocol message schemas, operator/
workspace/trace context field layouts, or the Ọpọn Protocol isolation
boundary — must follow this workflow regardless of how small the change appears.

### When to Use `abi/` Branches

- Changing any `pub trait` in `ogun-sdk`
- Changing `OGUN_ABI_VERSION: u32` in any crate
- Changing Elegua Protocol message structs (especially `operator_id`,
  `workspace_id`, `trace_id`, `enterprise_id`)
- Changing Ọpọn Protocol isolation semantics (SYS-001)
- Changing the image format layout regions (`FileHeader`, `SectionTable`,
  `SectionData`, `ImageVerifyKey`, `SignatureBlock`)
- Changing the `KernelBootBundle` structure
- Changing the `CleanShutdownMarker` type or write protocol

### ABI Branch Workflow

```powershell
git checkout develop
git pull origin develop
git checkout -b abi/elegua-enterprise-id-in-all-messages
```

The CI pipeline detects `abi/*` branch names and automatically runs the
`abi-change-notice` job which displays the mandatory reviewer checklist:

```
[ ] VERSION.md bumped in every affected submodule
[ ] OGUN_ABI_VERSION constants verified stable or bumped
[ ] Elegua Protocol invariants preserved
    (operator_id / workspace_id / trace_id unchanged)
[ ] Opọn Protocol (SYS-001) isolation unchanged
[ ] Audit log remains append-only
[ ] Two maintainer approvals required before merge
[ ] CHANGELOG entry added under '### Breaking'
```

Every item on this checklist must be explicitly acknowledged in the MR
description before the MR can be merged.

Two maintainer approvals are always required for `abi/` branches. The
`allow_failure: true` setting on the `abi-change-notice` job means it will not
block the pipeline, but the MR cannot be approved without the checklist being
complete.

---

## 9. Submodule Synchronization Workflow

The umbrella `ogun` repository records a specific commit SHA for each
submodule. Keeping submodule pointers up to date is a regular maintenance
task.

### Initializing After Clone

```powershell
cd C:\dev\ogun
git clone git@gitlab.com:ogun-foundation/ogun.git
cd ogun
git submodule update --init --recursive
```

### After Switching Branches in the Umbrella

```powershell
git checkout develop
git submodule update --init --recursive
```

### Updating a Single Submodule Pointer to Latest `develop`

```powershell
cd C:\dev\ogun
git submodule update --remote ogun-runtime
git add ogun-runtime
git commit -m "chore: bump ogun-runtime submodule to latest develop"
git push origin develop
```

### Updating All Submodule Pointers

```powershell
cd C:\dev\ogun
git submodule update --remote
git add .
git commit -m "chore: bump all submodule pointers to latest develop"
git push origin develop
```

### Cross-Submodule Feature Work (Paired MRs)

When a feature requires changes in multiple submodules (for example, a new
SDK trait in `ogun-sdk` consumed by `ogun-components`), use paired MRs:

1. Open MR A in `ogun-sdk`: `feat/plugin-loader-trait` → `develop`
2. Open MR B in `ogun-components`: `feat/plugin-loader-integration` → `develop`
   - MR B's description notes it depends on MR A being merged first.
3. Merge MR A. Update the `ogun-sdk` submodule pointer in the umbrella.
4. Merge MR B.

Never merge the downstream MR (B) before the upstream MR (A) is merged and its
submodule pointer is updated. CI in the downstream repo will fail on a stale
pointer because it will be referencing a branch commit, not a `develop` tip.

---

## 10. Versioning and Tagging

### Version Format

ogun OS uses a structured version string defined by `update_version.py`:

```
{major}.{minor}.{patch}-{gate}.{gate_major}.{gate_minor}+{maturity}
```

| Component | Values | Example |
|---|---|---|
| `{major}.{minor}.{patch}` | Semver core | `0.1.0` |
| `{gate}` | `alpha`, `beta`, `canary`, `rc`, `stable` | `beta` |
| `{gate_major}` | Milestone number within gate | `1` |
| `{gate_minor}` | Iteration within milestone | `3` |
| `{maturity}` | `dev`, `nightly`, `test`, `cm` | `dev` |

Examples:

| Version String | Meaning |
|---|---|
| `0.1.0-alpha.3+dev` | Third internal alpha iteration, development build |
| `0.1.0-beta` | First public beta release |
| `0.1.0-rc.1` | First release candidate |
| `0.1.0-stable` | Stable release |
| `0.2.0-alpha.1+nightly` | Nightly build of 0.2.0 alpha |

### Git Tags

Tags always use the `v` prefix: `v0.1.0-beta`, `v0.1.0-rc.1`, `v0.1.0`.

Tags are created automatically by the `version:tag` CI job in `version.yml`.
Manual tagging is only permitted for hotfix releases when CI is unavailable.

Tags are annotated (`git tag -a`) with a message summarizing the release:

```powershell
git tag -a v0.1.0-beta -m "ogun OS 0.1.0-beta — Windows x64 Desktop Edition — June 2026"
```

### Which Files Are Updated by `update_version.py`

The `--all-files` flag updates version strings in:

- `VERSION.md` (root)
- `Cargo.toml` `workspace.package.version` field
- `package.json` `version` fields (Tauri frontend manifests)
- `tauri.conf.json` `version` field
- Any `ogun-component.toml` manifest `version` field

The `--recursive` flag walks all subdirectories, making it suitable for the
umbrella. For submodule repositories, run without `--recursive` to avoid
touching nested workspace manifests that have their own version lifecycle.

### Workspace Package Version in `Cargo.toml`

The umbrella `Cargo.toml` declares `version = "0.1.0-alpha.3"` under
`[workspace.package]`. All workspace member crates that inherit this with
`version.workspace = true` are updated in a single `update_version.py` run.

Crates that pin their own version (non-inheriting) must be updated manually
or via a separate `--path` invocation of `update_version.py`.

---

## 11. CI/CD Pipeline Stages

The shared pipeline templates in `ogun-devops/ogun-cicd/` define these stages
in order. All stages are defined in `configure.yml` and referenced by the child
repo's `.gitlab-ci.yml`.

### Stage Order

```
validate → check → test → build → audit → package → pages → version → release
```

### `validate` (validate.yml)

Runs before any compilation. Fastest and cheapest gate.

| Job | What it checks |
|---|---|
| `validate:workspace` | `cargo metadata --no-deps` resolves all workspace members |
| `validate:submodules` | Every expected submodule directory exists and is non-empty |
| `validate:version-file` | `VERSION.md` exists and contains a valid semver string |

Triggers: MRs, `main`, `feat/*`, `fix/*`, `abi/*`, version schedules.

### `check` (check.yml)

Format and lint before compilation.

| Job | What it checks |
|---|---|
| `fmt` | `cargo fmt --all -- --check` |
| `clippy` | `cargo clippy --workspace --all-targets --all-features -- -D warnings` |
| `check:workspace` | `cargo check --workspace --all-targets --all-features` |
| `abi-change-notice` | Reviewer checklist notice for `abi/*` branches (`allow_failure: true`) |

Optional per-subworkspace clippy: instantiate `.job_clippy_subworkspace` with
`SUBWORKSPACE_DIR` for focused checks in monorepo structures.

Triggers: MRs, `main`, `develop`, `feat/*`, `fix/*`, `abi/*`.

### `test` (test.yml)

| Job | What it runs |
|---|---|
| `test:workspace` | `cargo test --workspace --verbose -- --show-output` |
| Unit tests | `cargo test --all --lib` |
| Integration tests | `cargo test --all --test '*'` |
| Doc tests | `cargo test --doc --workspace` |
| Per-crate smoke tests | `.job_test_crate` with `CRATE_NAME` variable |
| Per-subworkspace tests | `.job_test_subworkspace` with `SUBWORKSPACE_DIR` variable |
| Coverage | `cargo llvm-cov --workspace --lcov` (when `ENABLE_COVERAGE=true`) |
| Nightly build | `cargo +nightly build/test --workspace --all-features` (scheduled; `allow_failure: true`) |

Triggers: MRs, `main`, `develop`, `feat/*`, `fix/*`, `abi/*`.

### `build` (build.yml)

| Job | What it produces |
|---|---|
| `build:debug` | Debug build on Linux (Docker); expires in 1 day |
| `build:release` | Release build on Linux x64; expires in 30 days |
| `build:release:windows` | Cross-compiled Windows x64 release (`x86_64-pc-windows-gnu`) |
| `build:tauri:desktop` | `ogun-desktop` Tauri bundle on Windows native runner |
| `build:tauri:setup` | `ogun-setup` Tauri bundle on Windows native runner |
| `build:components` | `ogun-components` `.dll`/`.so` libraries |
| Nightly build | Timestamped release artifact for integration testing (scheduled) |

The Windows native Tauri jobs (`build:tauri:desktop`, `build:tauri:setup`)
require a runner tagged `windows` + `x64` with Rust stable, Node LTS,
WebView2, VS Build Tools, and Tauri 2 installed.

Triggers: MRs (debug only), `main`, `develop`, `release/*`, version tags.

### `audit` (sast.yml)

| Job | What it checks |
|---|---|
| `security:audit` | `cargo-audit` against RustSec advisory database |
| `dependency:deny` | `cargo-deny` — licenses, duplicate deps, source policy |
| Supply-chain integrity | Vendored sources match `Cargo.lock` (`security/*` branches and `main`) |
| SBOM generation | CycloneDX and SPDX formats (when `ENABLE_SBOM=true`) |
| `sonarqube` | SonarQube static analysis (when `ENABLE_SONAR=true`) |
| `weekly:audit` | Scheduled weekly `cargo audit --deny warnings` |

`security:audit` has `allow_failure: true` by default. Security-critical repos
(e.g. `ogun-runtime`) override this to `allow_failure: false`.

### `package` (package.yml)

| Job | What it packages |
|---|---|
| `.job_package_app` | Any binary into a versioned `.ogpkg` archive |
| `.job_package_app_windows` | Windows cross-compiled binary into `.ogpkg` |
| `.job_package_tauri_bundle` | Tauri bundle directory into a versioned `.ogpkg` |

`.ogpkg` files are versioned archives (`appname-version-arch.ogpkg`) that
contain the binary or Tauri bundle and are stored in `ogun-artifacts/`.

Triggers: `main`, version tags, web/API triggers.

### `pages` (package.yml)

Builds unified `rustdoc` with `cargo doc --workspace --no-deps --document-private-items`
and publishes to GitLab Pages for internal API documentation.

Triggers: `main` merges.

### `version` (version.yml)

| Job | Trigger | Effect |
|---|---|---|
| `version:tag` | Manual (web/API) or `SCHEDULE_TYPE=version` | Bump, commit, tag, push |
| `version:preview` | Web/API | Dry-run; shows next version without writing |
| `version:nightly` | `SCHEDULE_TYPE=nightly` | Timestamped nightly tag; no commit |
| `version:ci` | `SCHEDULE_TYPE=ci` | Alpha+dev CI tag; auto-increments |
| `version:cm` | Manual (web/API) | Configuration-management tag |
| `version:rc` | Manual (web/API) | Release candidate tag |
| `version:stable` | Manual (web/API) | Stable release tag |

All version jobs require `OGUN_DEVOPS_DEPLOY_TOKEN` to fetch `update_version.py`
from `ogun-devops` at runtime.

### `release` (deploy.yml)

| Job | What it creates |
|---|---|
| `.job_release_crate` | GitLab release for library/crate repos |
| `.job_release_desktop` | GitLab release for `ogun-os` with Tauri bundle links |
| `.job_attest` | Signs the SBOM and creates a build attestation artifact |

The attestation job requires `OGUN_IMAGE_SIGNING_KEY_B64` as a protected and
masked CI/CD variable. If this variable is absent the job exits with an error
and blocks the release stage.

Triggers: semver tags matching `v[0-9]+.[0-9]+.[0-9]+`.

---

## 12. Merge Request Standards

### Required in Every MR Description

1. **Summary** — One paragraph describing what changed and why.
2. **Issue reference** — `Closes #NNN` or `Relates to #NNN`.
3. **Affected workspaces and crates** — List every crate that changed.
4. **Checks run locally** — e.g. `cargo check --workspace`, `cargo test --workspace`, `cargo fmt --all`.
5. **Residual risk** — Any known edge cases, temporary workarounds, or follow-up issues opened.

### Additional Requirements by Branch Type

| Branch type | Extra requirements |
|---|---|
| `abi/` | ABI checklist fully answered in description; two maintainer approvals |
| `security/` | Two maintainer approvals; confidential MR until published |
| `release/` | Release gate conditions documented and confirmed met |
| Changes to `ogun-bootloader`, `ogun-image-format`, `ogun-session-manager` | Two maintainer approvals |
| Changes to `elegua` message schemas | Protocol invariant preservation statement in description |

### What Reviewers Check

- **Correctness** — Does the implementation match the documented specification?
- **Security properties** — Are all design invariants (I-01 through I-35) preserved?
- **Architecture boundaries** — Does lower-layer code avoid depending on higher layers? Do host OS calls stay confined to the approved boundary crates?
- **Test coverage** — Are new behaviors covered by tests?
- **Release scope** — Does the change stay within the declared 0.1.0-beta scope? If it expands scope, is that explicitly acknowledged?
- **Documentation** — Are `CHANGELOG.md`, `README.md`, and design docs updated?

---

## 13. Commit Message Convention

### Format

```
area: short imperative summary (≤72 characters)

Optional longer explanation of why, not what. Wrap at 72 characters.
Reference design invariants, protocol fields, or security properties
that are affected.

Closes #NNN
```

### Area Prefixes

| Prefix | Used for |
|---|---|
| `runtime` | `ogun-runtime` workspace changes |
| `kernel` | Kernel core, subsystems, boot sequence |
| `bootloader` | `ogun-bootloader` changes |
| `session` | `ogun-session-manager` changes |
| `image` | `ogun-image-format`, `ogun-image-builder` |
| `devices` | `ogun-devices` workspace changes |
| `emulator` | `ogun-emulator`, `ogun-emulator-backend` |
| `uefi` | `ogun-uefi` changes |
| `sdk` | `ogun-sdk` workspace changes |
| `components` | `ogun-components` workspace changes |
| `apps` | `ogun-apps` workspace changes |
| `tools` | `ogun-tools` workspace changes |
| `desktop` | `ogun-os/ogun-desktop` Tauri app |
| `setup` | `ogun-setup` installer |
| `elegua` | Elegua Protocol changes |
| `rustydb` | RustyDB changes |
| `config` | Configuration template changes |
| `ci` | CI/CD pipeline changes |
| `docs` | Documentation-only changes |
| `release` | Release preparation commits |
| `chore` | Housekeeping, dependency updates, metadata |

### Examples

```
bootloader: halt with descriptive error on ABI version mismatch
sdk: add OgunPlugin trait with on_load and on_unload lifecycle hooks
kernel: initialize emulation subsystem as subsystem 15 in canonical order
elegua: add enterprise_id field to all IPC message context structs
ci: enable ENABLE_WINDOWS_CHECK on ogun-runtime MR pipelines
docs: clarify three-stage boot verification sequence in DESIGN.md
release: freeze submodule pointers for v0.1.0-beta
chore: bump ogun-sdk submodule to include plugin loader trait
```

---

## 14. Branch Protection Rules

Configure these rules in GitLab under **Settings → Repository → Protected Branches**
for every repository in the ogun graph.

### `main`

| Rule | Setting |
|---|---|
| Allowed to push | No one (force-push disabled; only merge commits) |
| Allowed to merge | Maintainers only |
| Require MR before merge | Yes |
| Minimum approvals required | 1 (2 for `ogun-runtime`, `elegua`, and ABI changes) |
| Require pipeline to succeed | Yes (all stages) |
| Code owner approval required | Yes |
| Allow force push | No |
| Allow deletions | No |

### `develop`

| Rule | Setting |
|---|---|
| Allowed to push | Developers and Maintainers (for chore/submodule pointer commits only) |
| Allowed to merge | Developers and Maintainers via MR |
| Require MR before merge | Yes |
| Minimum approvals required | 1 |
| Require pipeline to succeed | Yes (check + test stages minimum) |
| Allow force push | No |
| Allow deletions | No |

### `release/*`

| Rule | Setting |
|---|---|
| Allowed to push | Maintainers only |
| Allowed to merge | Maintainers only |
| Require pipeline to succeed | Yes (full pipeline) |
| Allow force push | No |

### Tags (`v*`)

| Rule | Setting |
|---|---|
| Allowed to create | Maintainers only (CI bot via deploy token) |
| Allow deletions | No (tags are immutable) |

---

## 15. Environment and Deployment Map

ogun OS does not deploy to cloud environments in the traditional sense. The
deployment model maps CI artifact promotion to installation targets.

| Environment | Description | Trigger |
|---|---|---|
| **dev** | Local developer machine; `cargo run` or debug install | Manual |
| **nightly** | Timestamped nightly artifact from scheduled pipeline on `develop` | `SCHEDULE_TYPE=nightly` on `develop` |
| **alpha** | Internal distribution; alpha-tagged artifact from `develop` | `SCHEDULE_TYPE=ci` or `version:ci` job |
| **beta** | Public distribution; first public release artifact | Merge of `release/0.1.0-beta` into `main` and tag |
| **rc** | Release candidate; final pre-stable validation artifact | `version:rc` job on `release/*` |
| **stable** | Public stable release | `version:stable` job after RC validation |

The `ogun-artifacts` submodule is the canonical staging directory for all
release-grade artifacts. Only CI-built and CI-signed artifacts should be
committed to `ogun-artifacts`. Never commit locally built artifacts,
developer test images, or unsigned binaries.

---

## 16. Scheduled Pipeline Jobs

Configure these in GitLab under **CI/CD → Schedules** for the relevant repository.

| Schedule | Repository | SCHEDULE_TYPE | Cron | Purpose |
|---|---|---|---|---|
| Nightly build | `ogun` (umbrella) | `nightly` | `0 2 * * *` | Timestamped release artifact; nightly Rust toolchain check |
| Weekly security audit | All Rust repos | `security` | `0 6 * * 1` | `cargo audit --deny warnings`; dependency update dry-run |
| Version CI tag | Active submodules | `ci` | On demand | Alpha+dev CI tag for integration testing |
| Version stable | `ogun` umbrella | `stable` | Manual | Stable release tagging |

---

## 17. Repository-Specific Notes

### `ogun-devops` and Shared Templates

The shared CI templates in `ogun-devops/ogun-cicd/` are included by child
repos via `include:` directives. When a child repo's pipeline breaks after an
`ogun-devops` update, always check the `configure.yml` global variables first:
`CARGO_HOME`, `RUSTFLAGS`, `CARGO_INCREMENTAL`, and `OGUN_MAIN_BRANCH`.

Child repos include templates in this pattern:

```yaml
include:
  - project: 'ogun-foundation/ogun-devops'
    ref: main
    file: 'ogun-cicd/configure.yml'
  - project: 'ogun-foundation/ogun-devops'
    ref: main
    file: 'ogun-cicd/validate.yml'
  - project: 'ogun-foundation/ogun-devops'
    ref: main
    file: 'ogun-cicd/check.yml'
  - project: 'ogun-foundation/ogun-devops'
    ref: main
    file: 'ogun-cicd/test.yml'
  - project: 'ogun-foundation/ogun-devops'
    ref: main
    file: 'ogun-cicd/build.yml'
  - project: 'ogun-foundation/ogun-devops'
    ref: main
    file: 'ogun-cicd/sast.yml'
  - project: 'ogun-foundation/ogun-devops'
    ref: main
    file: 'ogun-cicd/package.yml'
  - project: 'ogun-foundation/ogun-devops'
    ref: main
    file: 'ogun-cicd/deploy.yml'
  - project: 'ogun-foundation/ogun-devops'
    ref: main
    file: 'ogun-cicd/version.yml'
```

### GitHub and Codeberg Mirrors

The umbrella `ogun` repository is mirrored to GitHub
(`dominic1eaton-code/ogun`) and Codeberg (`eatondo000/ogun`). Mirroring is
one-way from GitLab. Never open pull requests or push directly to the GitHub
or Codeberg mirrors. All contributions must go through GitLab merge requests.

### `ogun-experimental`

This submodule is explicitly excluded from release scope. Branches in
`ogun-experimental` are not required to follow the same naming convention or
maintain CI green status. However, any prototype that is promoted into a
production workspace must follow the full workflow from that point forward:
clean history, tests, documentation, and full CI passage.

### CI/CD Variable Requirements

The following variables must be configured at the GitLab group level
(`ogun-foundation`) so they are inherited by all child repositories:

| Variable | Scope | Purpose |
|---|---|---|
| `OGUN_DEVOPS_DEPLOY_TOKEN` | Protected, Masked | Fetches `update_version.py` from `ogun-devops` |
| `OGUN_IMAGE_SIGNING_KEY_B64` | Protected, Masked | Image signing key for attestation job |
| `SONAR_HOST_URL` | Protected | SonarQube host (if ENABLE_SONAR=true) |
| `SONAR_TOKEN` | Protected, Masked | SonarQube authentication token |

Per-repo variables that override group defaults:

| Variable | Repo | Purpose |
|---|---|---|
| `ENABLE_WINDOWS_BUILD` | `ogun-os`, `ogun-devices` | Activates Windows cross-build job |
| `ENABLE_WINDOWS_CHECK` | `ogun-runtime` | Activates Windows compilation check |
| `ENABLE_SBOM` | `ogun-runtime`, `ogun-os` | Activates SBOM generation |
| `ENABLE_COVERAGE` | Any | Activates `cargo-llvm-cov` coverage report |
| `ENABLE_SONAR` | Selected repos | Activates SonarQube scan |

---

## 18. Quick Reference Command Sheets

### Daily Development

```powershell
# Start work on a new feature
git checkout develop && git pull origin develop
git checkout -b feat/your-feature-name

# Focused workspace check (run from the submodule you changed)
cargo fmt --all
cargo check --workspace
cargo test --workspace
cargo clippy --workspace --all-targets --all-features -- -D warnings

# Commit
git add -p
git commit -m "area: short imperative summary"

# Push and open MR
git push -u origin feat/your-feature-name
```

### Submodule Management

```powershell
# Initialize all submodules after clone
git submodule update --init --recursive

# Update one submodule pointer to latest develop
git submodule update --remote ogun-runtime
git add ogun-runtime
git commit -m "chore: bump ogun-runtime to latest develop"

# Update all submodule pointers
git submodule update --remote
git add .
git commit -m "chore: bump all submodule pointers"
```

### Building and Running

```powershell
# Validate workspace shape only
cd C:\dev\ogun && cargo metadata --no-deps

# Full type check
cargo check --workspace

# Debug build
cargo build --workspace

# Release build
cargo build --workspace --release

# Run tests
cargo test --workspace

# Focused submodule checks (faster during development)
cd C:\dev\ogun\ogun-runtime && cargo check --workspace
cd C:\dev\ogun\ogun-sdk     && cargo check --workspace
cd C:\dev\ogun\ogun-devices && cargo check --workspace
cd C:\dev\ogun\ogun-components && cargo check --workspace

# Build and run ogun-desktop (Tauri)
cd C:\dev\ogun\ogun-os\src\ogun-desktop
npm ci && npm run tauri dev

# Build and run ogun-setup (Tauri)
cd C:\dev\ogun\ogun-tools\src\ogun-setup
npm ci && npm run tauri dev

# Build and run ogun-image-tool (Tauri)
cd C:\dev\ogun\ogun-tools\src\ogun-image-tool
npm ci && npm run tauri dev
```

### Release Tagging (via CI)

```
# Trigger version:tag job via GitLab pipeline UI with these variables:
OGUN_VERSION      = "0.1.0"
OGUN_GATE         = "beta"
OGUN_PUSH_BRANCH  = "release/0.1.0-beta"

# Or via CLI using update_version.py directly:
python ./update_version.py \
  --version 0.1.0 \
  --gate beta \
  --all-files \
  --commit \
  --recursive \
  --push main
```

### Pipeline Triggers (Web/API)

```
# On-demand debug build
CI_PIPELINE_SOURCE = "web"

# On-demand Windows build
CI_PIPELINE_SOURCE = "web"
ENABLE_WINDOWS_BUILD = "true"

# Nightly schedule
SCHEDULE_TYPE = "nightly"

# Weekly security audit
SCHEDULE_TYPE = "security"

# Version preview (dry run)
Trigger: version:preview job via web UI
```

---

*ogun OS · Project Ogún · 2026*  
*Owner: Dominic Eaton (@eatondo)*  
*Document: WORKFLOW.md*  
*Licensed under GNU General Public License v3.0*
