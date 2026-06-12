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
19. [Versioning System — Full Reference](#19-versioning-system--full-reference)
20. [Release Strategy and Gates](#20-release-strategy-and-gates)
21. [Maturities, Canary Deployments, and Rollout Strategy](#21-maturities-canary-deployments-and-rollout-strategy)
22. [Sandboxing and Environments](#22-sandboxing-and-environments)
23. [Configuration Management](#23-configuration-management)
24. [Submodule and Dependency Management](#24-submodule-and-dependency-management)
25. [Testing Strategy](#25-testing-strategy)
26. [CI/CD Environments and Strategies](#26-cicd-environments-and-strategies)

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
| `ogun-test-features` | `ogun-foundation/ogun-test-features` | Experimental sandbox crates and prototype workspaces |

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

### `ogun-test-features`

This submodule is explicitly excluded from release scope. Branches in
`ogun-test-features` are not required to follow the same naming convention or
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

## 19. Versioning System — Full Reference

This section is the canonical reference for the ogun OS version string format,
the `update_version.py` script that generates and records every version, the git
tag convention, and the rules that govern which files are rewritten on each
version operation. Sections 10 and 20–21 extend this reference with release
strategy and rollout specifics.

### 19.1 Version String Anatomy

ogun OS version strings are produced exclusively by `update_version.py`
(stored in `ogun-devops/ogun-scripts/`). No version string is ever written by
hand. The full format is:

```
{major}.{minor}.{patch}-{gate}.{gate_major}.{gate_minor}-{maturity_suffix}
```

| Segment | Type | Values | Notes |
|---|---|---|---|
| `{major}` | Integer | `0`, `1`, … | Bumped on ABI break, image-format break, or security-model break |
| `{minor}` | Integer | `0`, `1`, … | Bumped on new features, new subsystems, new host types |
| `{patch}` | Integer | `0`, `1`, … | Bumped on bug fixes, security patches, performance work |
| `{gate}` | Enum | `alpha` `beta` `canary` `rc` `stable` | Release audience qualifier; see §20 |
| `{gate_major}` | Integer | `1`, `2`, … | Stream number; allows parallel pre-release streams |
| `{gate_minor}` | Integer | `0`, `1`, … | Auto-incremented from git tags within a stream |
| `{maturity_suffix}` | String | `dev-M.N.P` `nightly-YYYYMMDDTHHmmSS` `test-N` `cm-N` | Build iteration qualifier; see §21 |

The `stable` gate produces no gate segment — the version string is exactly
`{major}.{minor}.{patch}`.

When gate and maturity are both present, the gate segment is always written
before the maturity suffix:

```
0.1.0-alpha.2.7-nightly-20260609T032842   ← gate=alpha, maturity=nightly
0.1.0-alpha.2.4-dev-0.0.4                 ← gate=alpha, maturity=dev
0.1.0-beta                                ← gate=beta, no maturity, first stream
0.1.0-rc.1.2-cm-0                         ← gate=rc, maturity=cm
0.2.0                                     ← gate=stable, no maturity
```

### 19.2 Gate Segment Counter Resolution

The `gate_major.gate_minor` counter is derived automatically from existing git
tags; manual counter tracking is not required.

**gate_major resolution** (when `--gate-major` is not explicitly passed):
1. Inspect all existing tags matching `v{base}-{gate}.{M}.{N}[...]`.
2. Take the largest `M` found — stay in the same stream.
3. If no matching tags exist, start at `gate_major = 1`.

**gate_minor resolution:**
- Without a maturity qualifier: increment the highest existing `N` for the
  resolved `gate_major` by 1. If no match exists, start at 0.
- With a maturity qualifier: reuse the current highest `N` (do not advance the
  gate counter when a maturity build is stamped against an existing gate version).

**Starting a new parallel stream** requires an explicit `--gate-major N` flag.
Example: `--gate alpha --gate-major 3` starts `alpha.3.0` independently of any
existing `alpha.1.x` or `alpha.2.x` tags.

### 19.3 Maturity Suffix Counter Resolution

Maturity suffixes are scoped per `(base_version + gate_segment)`. An `alpha`
stream and a `beta` stream have fully independent maturity counter namespaces.

| Maturity | Format | Counter source | Increment rule |
|---|---|---|---|
| `dev` | `dev-M.N.P` | git tags matching `v{version_prefix}-dev-M.N.P` | Patch component `P` incremented; wraps to next minor at 99 |
| `nightly` | `nightly-YYYYMMDDTHHmmSS` | UTC wall clock at CI run time | Always unique; no counter state required |
| `test` | `test-N` | git tags matching `v{version_prefix}-test-N` | Integer `N` incremented |
| `cm` | `cm-N` | git tags matching `v{version_prefix}-cm-N` | Integer `N` incremented |

### 19.4 Git Tag Convention

All git tags use the `v` prefix: `v{full_version}`. Every tag is annotated:

```powershell
git tag -a v0.1.0-beta -m "ogun OS 0.1.0-beta — Windows x64 Desktop Edition — June 2026"
```

Tags are created by the `version:tag` CI job in `version.yml`. Manual tagging
is only permitted for emergency hotfixes when CI is unavailable. Tags are
immutable; deletion is blocked by branch protection. When a tag already exists
in a given repository, `update_version.py` skips it silently rather than
overwriting.

Tag pattern used by release-triggering CI rules: `^v[0-9]+\.[0-9]+\.[0-9]+`
This matches both plain stable tags (`v0.1.0`) and all pre-release variants
(`v0.1.0-beta`, `v0.1.0-rc.1.2`, `v0.1.0-alpha.2.7-nightly-20260609T032842`).

### 19.5 Files Updated by `update_version.py`

The `--all-files` flag (default for all CI version jobs) rewrites version
strings in the following file types anywhere under the search root:

| File | What is updated |
|---|---|
| `VERSION.md` | Every semver string replaced with the new full version (including `v` prefix). Duplicate leading `v` characters (`vv0.1.0`) are collapsed to `v0.1.0` before replacement. |
| `Cargo.toml` | Only the `version` key inside the `[package]` section. Dependency version constraints in `[dependencies]` and similar sections are untouched. Workspace roots without a `[package]` section are skipped. |
| `pyproject.toml` | The `version` key inside `[project]` (PEP 621) or `[tool.poetry]`. Only the first matching section is updated. |
| `package.json` | The top-level `"version"` field only. Nested version strings in `"dependencies"`, `"devDependencies"`, etc. are not modified. |

The `--recursive` flag walks all subdirectories (excluding hidden directories).
Use `--recursive` on the umbrella; run without it on individual submodule
repositories to avoid touching nested workspace manifests that carry their own
version lifecycle.

Crates that pin their own version (non-inheriting `version` in `Cargo.toml`)
must be updated with a separate `--path` invocation of `update_version.py` or
manually.

### 19.6 `update_version.py` — Key CLI Flags

```
# Minimum: update all files, tag, no push
python update_version.py --version 0.2.0 --all-files

# Standard alpha CI tag (auto-increments)
python update_version.py --version 0.1.0 --all-files --gate alpha --maturity dev \
  --commit --push develop

# Nightly (timestamped, no commit, no persistent tag)
python update_version.py --version 0.1.0 --all-files --maturity nightly --no-git-tag

# Release candidate (auto-increments rc.N.M)
python update_version.py --version 0.1.0 --all-files --gate rc --commit --push release/0.1.0-rc

# Full stable release
python update_version.py --version 0.1.0 --all-files --gate stable --recursive \
  --commit --push main

# Dry run — preview without writing anything
python update_version.py --version 0.1.0 --all-files --gate beta \
  --commit --push release/0.1.0-beta --dry-run

# Start a new parallel alpha stream (alpha.2.x independent of alpha.1.x)
python update_version.py --version 0.1.0 --all-files --gate alpha --gate-major 2

# Bare tags (no "v" prefix)
python update_version.py --version 0.1.0 --all-files --gate rc --tag-prefix ""

# Parent repo only — skip all submodule processing
python update_version.py --version 0.1.0 --all-files --no-submodules
```

### 19.7 `update_version.py` Execution Order (Full Pipeline)

For each repository, processed in submodule-first order (submodules before parent):

1. Find and update `VERSION.md` files (if `--md` or `--all-files`)
2. Find and update `Cargo.toml` files (if `--cargo` or `--all-files`)
3. Find and update `pyproject.toml` files (if `--pyproject` or `--all-files`)
4. Find and update `package.json` files (if `--package-json` or `--all-files`)
5. `git add . && git commit` (if `--commit`)
6. `git tag -a {tag} -m "Release {version}"` (if git tagging is on, which is the default)
7. `git push origin {branch} --tags` (if `--push BRANCH`)

Submodules are pushed before the parent repository to ensure every submodule's
new commits and tags are on the remote before the parent pushes its updated
submodule pointer, preventing dangling references.

### 19.8 Script Output Prefixes

| Prefix | Meaning |
|---|---|
| `[updated]` | File was written with the new version |
| `[no-op]` | File already contains the target version; left unchanged |
| `[fix-v]` | Duplicate `v` prefixes collapsed in a `VERSION.md` file |
| `[skip]` | File found but has no semver to replace, or no `[package]` section |
| `[dry-run]` | Action that would have been taken; nothing written |
| `[git]` | Output from a git operation (commit, tag, push, or error) |

### 19.9 `OGUN_ABI_VERSION` Constants

ABI version constants live inside individual crates (e.g. `ogun-sdk`,
`ogun-image-format`). They are **not** updated automatically by
`update_version.py` — they are code constants that must be bumped manually
on any `abi/` branch that changes a public ABI surface. The version bump of
the crate's `Cargo.toml` and the bump of `OGUN_ABI_VERSION: u32` inside the
source are two separate acts, and both must appear in the same commit on an
`abi/` branch.

---

## 20. Release Strategy and Gates

This section defines the full release path from the first alpha commit to a
stable production release, the gate transitions that govern audience expansion,
and the gate-specific acceptance criteria that must be met before each transition.

### 20.1 Release Path Overview

```
[develop] → alpha (internal) → beta (public pre-release)
         → canary (continuous deploy from main) → rc (release candidate)
         → stable (public stable release)
```

Each gate represents a widening of the distribution audience and a narrowing of
the permissible change surface. Moving backward (e.g., from beta back to alpha)
is not a recognized operation — any regression discovery on a beta branch opens
a `fix/*` or `p0/*` branch targeting `develop`, not a gate rollback.

### 20.2 Alpha Gate (`alpha`)

**Audience:** Internal development; The Ogun Foundation team; trusted
contributors with explicit access.

**Purpose:** Establish foundational runtime correctness, iterate rapidly on ABI
and architecture decisions, and validate the boot chain on real Windows x64
hardware before any public exposure.

**Version format:** `v0.1.0-alpha.{major}.{minor}[-{maturity}]`

**Entry criteria:**
- The `develop` branch builds clean on Windows x64 (`cargo build --workspace --release`).
- The three-stage boot verification passes on a clean Windows x64 installation.
- No P0 blockers on the core boot chain (bootloader → kernel → session manager).

**Exit criteria (to advance to beta):**
- All 0.1.0-beta Rust packages build and deliver on Windows x64.
- All four artifact builds (setup, desktop, emulator, host-service) pass clean.
- Three-stage boot verification passes on a clean install.
- Full session lifecycle verified end-to-end.
- Design invariants I-01 through I-35 confirmed enforced.
- `CHANGELOG.md` entries complete for all changes since the prior alpha.
- No P0 blockers outstanding.
- Release gate conditions in `DESIGN.md` §Release Gates all met.

**Permitted change surface:** All `feat/*`, `fix/*`, `refactor/*`, `abi/*`,
and `docs/*` branches. ABI changes are expected and permitted at alpha.

**Distribution:** Internal GitLab release only. Artifacts stored in
`ogun-artifacts/` but not publicly announced.

### 20.3 Beta Gate (`beta`)

**Audience:** Public pre-release. External testers, early adopters, and
developer partners with an explicit understanding that the software is
pre-release.

**Purpose:** Validate the full feature set under real-world operator conditions,
surface edge cases in the session lifecycle and app runtime, and harden the
security model before RC.

**Version format:** `v0.1.0-beta.{major}.{minor}[-{maturity}]`

The first public beta uses the short form `v0.1.0-beta` (no gate counter) for
marketing clarity. Subsequent beta iterations use the full counter form:
`v0.1.0-beta.1.1`, `v0.1.0-beta.1.2`.

**Entry criteria (from alpha):**
- All alpha exit criteria met and verified.
- Security audit (`cargo-audit --deny warnings`) clean on `ogun-runtime` and `elegua`.
- SBOM generated and signed.
- GitLab release page populated with all four installable artifacts and checksums.
- Public-facing `CHANGELOG.md` entries reviewed for clarity.

**Exit criteria (to advance to RC):**
- No critical or high-severity bugs outstanding in the beta tracker.
- All design invariants I-01 through I-35 remain enforced.
- Minimum one complete full-session-lifecycle test cycle on a clean Windows x64
  machine not previously used for development.
- All `### Breaking` entries in `CHANGELOG.md` reviewed and acknowledged.
- `ogun-setup.exe` silent-install mode verified.

**Permitted change surface:** `fix/*`, `docs/*`, `p0/*`, and security patches.
No new features and no ABI changes on a beta branch. Any ABI change discovered
in beta must be logged as a `[Unreleased]` item for the next minor version.

**Distribution:** Public GitLab release page. Mirrored to GitHub and Codeberg
announcement-only issues. No auto-update mechanism in 0.1.0-beta.

### 20.4 Canary Gate (`canary`)

**Audience:** Automated downstream integration testing pipelines; opt-in
operators who have explicitly enrolled in the canary channel.

**Purpose:** Provide a continuous stream of the latest-merged `main` state for
integration testing between beta and RC cycles. Not a human-facing release
channel in 0.1.0; reserved for 0.2.0+ when an update delivery mechanism exists.

**Version format:** `v0.2.0-canary.{major}.{minor}`

**Trigger:** Automated. The `version:canary` CI job runs on every merge to
`main` after the 0.1.0 stable release, producing a timestamped canary artifact.

**Acceptance:** Canary artifacts are consumed only by downstream CI pipelines
(e.g., integration test suites for `ogun-sdk` consumers). A canary artifact
failing its downstream integration test immediately opens a P0 issue.

**Distribution:** `ogun-artifacts/canary/` subdirectory. Not surfaced on the
public release page. Retention: 7 days.

### 20.5 Release Candidate Gate (`rc`)

**Audience:** Final validation partners; organizations planning to integrate
ogun OS into their deployment workflows; security researchers.

**Purpose:** Freeze the feature set completely, validate the full release
pipeline (packaging, signing, attestation, release page), and confirm all
acceptance criteria before the stable release declaration.

**Version format:** `v0.1.0-rc.{major}.{minor}`

**Entry criteria (from beta):**
- All beta exit criteria met.
- SBOM signed and attestation artifact present in `ogun-artifacts/`.
- `ogun-setup.exe` enterprise silent-install tested and passing.
- Code-signing certificate applied to all Windows binaries.

**Exit criteria (to advance to stable):**
- Zero outstanding critical or high-severity issues in the RC tracker.
- All four artifact builds reproducing byte-for-byte across two independent CI
  runs on the same tag.
- Release page draft reviewed and approved by the project owner.
- `CHANGELOG.md` `[Unreleased]` section is empty.

**Permitted change surface:** Only `fix/*` for critical regressions found
during RC validation. No refactors, no documentation restructuring. Any
non-critical issue is logged for the next release.

**Distribution:** Same as beta. RC artifacts replace prior beta artifacts on
the GitLab release page.

### 20.6 Stable Gate (`stable`)

**Audience:** General public.

**Purpose:** The final promoted, fully validated release. All gate conditions
met, all release artifacts signed and attested, all known limitations
documented.

**Version format:** `v{major}.{minor}.{patch}` (no gate suffix)

**Entry criteria (from RC):**
- All RC exit criteria met.
- At least one RC iteration with zero issues opened against it for a minimum of
  7 days.
- Project owner sign-off.

**Post-release actions:**
1. Tag `v0.1.0` on `main` in all submodules and the umbrella.
2. Create the GitLab release with all artifact links, SBOM, and attestation.
3. Back-merge any release-day fixes into `develop`.
4. Bump `develop` to `0.2.0-alpha.1.0-dev-0.0.0`.
5. Archive the `release/0.1.0-stable` branch.
6. Publish the security advisory index for 0.1.0.
7. Update the public site and README version badge.

**Support window:** Each stable release receives security patches for a minimum
of 12 months after the next stable release is published.

### 20.7 Gate Transition Decision Matrix

| Transition | Decision authority | Required documentation |
|---|---|---|
| alpha → beta | Project owner | DESIGN.md release gate checklist, clean security audit |
| beta → RC | Project owner + one additional maintainer | Beta tracker closed or deferred, SBOM signed |
| RC → stable | Project owner | Zero critical issues for 7 days, full artifact reproduction verified |
| Any → hotfix | On-call maintainer | P0 issue + root cause in MR description |
| Stable → next alpha | Project owner | Scope document for next version committed to `ogun-docs` |

---

## 21. Maturities, Canary Deployments, and Rollout Strategy

### 21.1 Maturity Qualifiers — Purpose and Usage

Maturity qualifiers describe the iteration mechanic of a build. They are
orthogonal to gates: a maturity qualifier can be used alone or combined with
a gate. When combined, the gate segment is written first.

| Maturity | Suffix format | Typical trigger | Purpose |
|---|---|---|---|
| `dev` | `dev-M.N.P` | `SCHEDULE_TYPE=ci` or manual | Rapid local iteration; fine-grained sortable builds for development |
| `nightly` | `nightly-YYYYMMDDTHHmmSS` | `SCHEDULE_TYPE=nightly` (cron `0 2 * * *`) | Automated daily CI build; timestamped; no counter state |
| `test` | `test-N` | Manual or QA pipeline trigger | QA / test-cycle builds needing a simple monotonic sequence |
| `cm` | `cm-N` | Manual only (`version:cm` job) | Configuration-managed artifact; marks a build that has passed all gates and test cycles; highest maturity level |

### 21.2 `dev` Maturity — Rapid Iteration

The `dev` maturity is for local development iteration and CI alpha builds. It
appends a `dev-M.N.P` suffix where only the patch component `P` is incremented
on each call.

```
v0.1.0-alpha.2.7-dev-0.0.0   ← first dev build on alpha.2.7
v0.1.0-alpha.2.7-dev-0.0.1   ← second
v0.1.0-alpha.2.7-dev-0.0.2   ← third
```

The `version:ci` CI job runs `--gate alpha --maturity dev --commit --push develop`
and is the standard mechanism for stamping CI builds of `develop` between formal
gate releases. It auto-increments from existing tags, so calling the job
repeatedly always produces the correct next version without manual bookkeeping.

### 21.3 `nightly` Maturity — Scheduled Builds

The nightly maturity appends a UTC ISO-compact timestamp to the full version.
Every call produces a unique, time-ordered tag. No counter state is required.

```
v0.1.0-alpha.2.7-nightly-20260609T021606
v0.1.0-alpha.2.7-nightly-20260609T025735
v0.1.0-alpha.2.7-nightly-20260609T032842
```

Nightly builds are produced by the `version:nightly` CI job on the `0 2 * * *`
UTC schedule. They do not create a persistent git commit (`--no-git-tag`
omits the permanent tag) and artifacts expire in 7 days. Their primary purpose
is catching regressions introduced by dependency updates, upstream Rust
toolchain changes, or nightly Rust feature flags.

If a nightly build fails, the on-call maintainer investigates before the next
working day. A failing nightly is not an immediate P0 but is treated as a
warning. If the same failure persists for two consecutive nights, a `p0/` branch
is opened on `develop`.

### 21.4 `test` Maturity — QA Builds

The `test` maturity is for dedicated QA pipeline builds. It appends a
monotonically incrementing integer (`test-0`, `test-1`, …) scoped to the current
base+gate version, giving QA a simple, ordered sequence of build identifiers
without the overhead of timestamp parsing.

Use the `version:test` job (triggered manually from the CI web UI) when handing
a build to a QA partner or when running a structured test cycle that requires
fixed, named builds.

### 21.5 `cm` Maturity — Configuration-Managed Artifacts

The `cm` maturity marks the most mature artifact type. A `cm` build has passed:

- All gate conditions for the current release series
- A complete QA test cycle (at least one `test-N` build validated without issues)
- Security audit (`cargo-audit`, `cargo-deny`, supply-chain check)
- SBOM generation and signing
- Attestation job with `OGUN_IMAGE_SIGNING_KEY_B64`

A `cm` artifact is the input to the RC or stable release pipeline. The
`version:cm` job is triggered manually by the project owner and requires the
`OGUN_IMAGE_SIGNING_KEY_B64` CI variable to be present.

```
v0.1.0-rc.1.2-cm-0   ← first cm build on rc.1.2 — the release input
v0.1.0-rc.1.2-cm-1   ← second cm build if the first required a fix
```

### 21.6 Canary Deployment and Rollout Strategy

The canary deployment mechanism is designed for 0.2.0+ when an over-the-air
update delivery system is implemented. The design is documented here for
planning purposes.

**Canary channel enrollment.** Operators opt in to the canary channel by
setting `update_channel = "canary"` in `~/.ogun/config/ogun.toml`. The Desktop
Edition's `ogun-desktop.exe` launcher checks this field at startup.

**Rollout tiers.** A canary release progresses through three rollout tiers
before being promoted to general availability:

| Tier | Audience fraction | Promotion criteria |
|---|---|---|
| Canary 1 | 1% of opted-in operators | Zero P0 crashes in 24 hours across canary 1 fleet |
| Canary 2 | 10% of opted-in operators | Zero P0 crashes in 48 hours; performance metrics within ±5% of prior stable |
| Canary GA | 100% of opted-in operators | 7-day soak; open to feedback before stable promotion |

**Automatic halt conditions.** The rollout is automatically halted if:
- Crash rate exceeds 0.1% of canary installs per hour.
- Boot failure rate exceeds 0.01% of canary installs.
- A `CleanShutdownMarker` write failure is detected in telemetry.
- Any security advisory is published against a dependency in the canary build.

**Rollback.** Canary installs revert to the prior stable version automatically
when a halt condition is detected. Reversion does not require user interaction.
The revert path is: download prior stable artifact → verify image signature →
install over the failed canary → restart `ogun-desktop.exe`.

**Stable promotion from canary.** After Canary GA completes its 7-day soak
without a halt condition, the `version:stable` job is triggered manually by the
project owner to promote the canary build to stable and publish the GitLab
release.

### 21.7 Rollout Monitoring

Rollout health is tracked via `ogun-system-manager` telemetry forwarded to the
Ogun Foundation's observability infrastructure. Key metrics per rollout tier:

| Metric | P0 threshold | Warning threshold |
|---|---|---|
| Boot success rate | < 99.9% | < 99.99% |
| Clean shutdown rate | < 99.5% | < 99.9% |
| Crash rate (crashes/hour/install) | > 0.001 | > 0.0001 |
| Session restore success rate | < 98% | < 99% |
| Image verification pass rate | < 100% | — |

Telemetry is opt-in per operator. Operators who have not opted in do not
contribute to rollout metrics. A rollout does not proceed past Canary 1 unless
at least 50 opted-in operators are active on that tier.

---

## 22. Sandboxing and Environments

### 22.1 Runtime Isolation Layers

ogun OS enforces isolation at multiple layers within the runtime. These layers
are not CI/CD environments — they are the security and execution boundaries that
govern what each component is permitted to do at runtime.

**Layer 1 — The Ọpọn Protocol (SYS-001).** The outermost isolation boundary.
Separates the ogun OS runtime from the host operating system. Only
`ogun-emulator-backend` is permitted to call host OS APIs (WinAPI, POSIX,
Bionic, web-sys). No component above it reaches the host OS directly. This
invariant (I-03) is frozen for the 0.1.0 release series and must never be
violated.

**Layer 2 — Enterprise isolation.** The Ọpọn Protocol also enforces isolation
between enterprises on the same ogun host. An operator running multiple
enterprise profiles cannot share IPC channels, filesystem namespaces, or session
state across enterprise boundaries without explicit cross-enterprise capability
grants.

**Layer 3 — Capability gating.** All IPC messages and system calls are
capability-gated. An app that does not hold the `ogun.storage.write` capability
cannot write to the VFS. Capabilities are granted at installation time,
audited by `ogun-security-manager`, and immutable for the session lifetime.

**Layer 4 — App tier isolation.** Tier 1 kernel apps run as Tokio tasks inside
`ogun-host-service`. Tier 2 and Tier 3 apps are OS child processes. Tier 4 user
apps are runtime-loaded `cdylib` libraries running in a supervised executor.
Tier 4 apps cannot call any system API not mediated by the `OgunApp` SDK trait.

**Layer 5 — Image verification.** Every boot verifies the signed `.img` kernel
image through the three-stage boot verification pipeline. A single failed
verification halts the boot with no side effects.

### 22.2 CI/CD Execution Environments

CI pipelines run in one of three execution environments. Each has a distinct
security posture and artifact retention policy.

**Linux Docker (default).** All `check`, `test`, and `audit` jobs, plus the
Linux cross-compiled Windows x64 release build, run in the `rust:latest` Docker
image on a Linux runner. This environment has no access to Windows APIs and
cannot run Tauri desktop applications.

**Windows native runner.** Tauri application builds (`build:tauri:desktop`,
`build:tauri:setup`, `build:tauri:app`) require a runner tagged `windows` +
`x64` with Rust stable, Node LTS, WebView2, VS Build Tools, and Tauri 2
installed. This runner has access to Windows APIs and can produce code-signed
executables when the signing certificate CI variable is configured.

**Python 3.12 slim (version jobs).** All `version:*` jobs run in the
`python:3.12-slim` image and have access only to the `update_version.py` script,
git, and curl. They have no Cargo access and produce no compiled artifacts.

### 22.3 Environment-to-Artifact Map

| Environment | Produces | Retention |
|---|---|---|
| Linux Docker + debug | `target/debug/` (unstripped) | 1 day |
| Linux Docker + release | `target/release/` (stripped Linux x64 ELF) | 30 days |
| Linux Docker + Windows cross | `target/x86_64-pc-windows-gnu/release/*.exe` `*.dll` | 90 days |
| Windows runner + Tauri | `ogun-desktop` and `ogun-setup` Tauri bundles (NSIS, WiX) | 30 days |
| Windows runner + components | `ogun-components *.dll` | 30 days |
| Package stage | `dist/*.ogpkg` versioned archives | 90 days |
| Release stage | GitLab release + `artifacts/*.sbom.json` + `*.attestation.json` | 1 year |

### 22.4 Developer Local Sandbox

The developer local sandbox is the `dev` environment in the deployment map
(§15). It is not managed by CI. The developer runs the full stack locally on
their Windows x64 machine using the command sheets in §18.

For isolated testing of a single submodule without spinning up the full boot
chain, the developer uses the submodule's own `cargo test --workspace` suite.
For end-to-end testing, the developer runs `ogun-desktop.exe` from the debug
build directory after a local `cargo build --workspace` pass.

The `ogun-test-features` submodule provides experimental sandbox crates for
prototyping work that is explicitly excluded from CI requirements. Any prototype
promoted into a production workspace inherits full CI and branch protection
requirements from that point forward.

### 22.5 Staging vs. Production Distinction

ogun OS does not use a traditional staging server because the runtime installs
on operator machines rather than deploying to cloud infrastructure. The staging
equivalent is a clean Windows x64 machine that has never had a prior ogun OS
installation. All release gate criteria in §20 specify "clean install" to ensure
test isolation equivalent to a staging environment.

The `ogun-artifacts/` submodule serves as the canonical artifact staging area.
Only CI-built and CI-signed artifacts are committed there. Locally built
artifacts, unsigned binaries, and developer test images must never be committed
to `ogun-artifacts/`.

---

## 23. Configuration Management

### 23.1 Configuration Scope

ogun OS configuration spans three distinct scopes:

| Scope | Location | Who writes it | Immutability |
|---|---|---|---|
| Image-time | Baked into the signed `.img` file | CI image builder | Immutable after signing |
| Install-time | `~/.ogun/config/` | `ogun-setup.exe` on first install | Writable by `ogun-desktop.exe` for updates |
| Runtime | Session state + operator preferences | Session manager, operator apps | Writable per-session |

### 23.2 Configuration Files

| File | Managed by | Purpose |
|---|---|---|
| `~/.ogun/config/ogun.toml` | `ogun-setup.exe`, `ogun-desktop.exe` | Root configuration: `update_channel`, `operator_id`, `enterprise_id`, `install_id`, log levels, telemetry consent |
| `~/.ogun/config/display.toml` | Session manager | Virtual display configuration: resolution, refresh rate, DPI |
| `~/.ogun/config/emulation.toml` | Emulator | CPU tick rate, thread pool size, component rate dividers |
| `~/.ogun/config/uefi/vars.bin` | `ogun-uefi` | Virtual BIOS/CMOS variable store; written once at UEFI init |
| `~/.ogun/security/keys/system.pub` | `ogun-setup.exe` | System public key; `0o444` permissions |
| `~/.ogun/security/keys/host.key` | `ogun-setup.exe` | Host key derived via HKDF-SHA256; `0o400` permissions |
| `~/.ogun/logs/boot.log` | Bootloader | Append-only boot log; one entry per boot stage, one per error |
| `~/.ogun/logs/uefi-boot.log` | `ogun-uefi` | Append-only UEFI phase transition log |

Seed configuration templates for all of the above live in `ogun-config/` and
are committed to the repository. Changes to seed templates must go through an
MR to `ogun-config` targeting `develop`. Seed template changes that affect the
install sequence must be coordinated with a paired MR to `ogun-runtime`.

### 23.3 `OGUN_ABI_VERSION` Configuration Management

`OGUN_ABI_VERSION: u32` constants in crates are the source of truth for
binary compatibility across a release series. Rules:

- The constant is read at boot time by `ogun-bootloader::parse_header()` and
  compared against the value encoded in the `.img` file's `FileHeader`.
- A mismatch halts the boot with `halt(ABI_VERSION_MISMATCH)`.
- `OGUN_ABI_VERSION` may only be bumped on an `abi/` branch with two maintainer
  approvals.
- The constant is frozen at `1` for the 0.1.0 release series.

### 23.4 Configuration Change Workflow

For changes to `ogun-config/` seed templates:

```powershell
# Branch from develop in the ogun-config submodule
cd C:\dev\ogun\ogun-config
git checkout develop
git pull origin develop
git checkout -b feat/update-emulation-defaults

# Edit seed templates
# Validate: confirm the changed defaults work on a clean Windows x64 install

# Commit and push
git commit -m "config: set default CPU tick rate to 100Hz in emulation.toml"
git push -u origin feat/update-emulation-defaults
```

Open an MR targeting `ogun-config/develop`. The MR description must include:
- Which template files changed.
- The effect on a fresh install vs. an existing install.
- Whether `ogun-desktop.exe` migration logic needs updating (if an existing
  install would be affected).

### 23.5 Version File (`VERSION.md`) as Configuration

`VERSION.md` in every repository root is the authoritative version record for
that repository. It is the single source of truth read by the CI pipeline
(`validate:version-file` job), the package stage (`VERSION=$(cat VERSION.md)`),
and the `update_version.py` script. Rules:

- `VERSION.md` must exist at every repository root. A missing `VERSION.md` fails
  the `validate:version-file` CI job, blocking all subsequent pipeline stages.
- `VERSION.md` contains exactly one semver string. Additional prose is
  permitted but the first match of the SEMVER regex is the canonical value.
- `VERSION.md` is always updated by `update_version.py` — never by hand.
- The `validate:version-file` job checks that `VERSION.md` is present and
  contains a valid `v?[0-9]+.[0-9]+.[0-9]+` string before any version operation
  is attempted.

### 23.6 Cargo Workspace Version Inheritance

The umbrella `ogun/Cargo.toml` declares `version = "{current_version}"` under
`[workspace.package]`. All workspace member crates that use:

```toml
[package]
version.workspace = true
```

inherit this value and are updated in a single `update_version.py` run on the
umbrella. Crates that pin their own `version = "..."` (non-inheriting) must be
updated with a separate `--path` invocation or manually. The preferred pattern
for new crates is always `version.workspace = true`.

---

## 24. Submodule and Dependency Management

### 24.1 Submodule Architecture

The ogun umbrella repository (`ogun`) uses git submodules to compose the full
workspace from independently versioned repositories. Each submodule is a
separate GitLab repository with its own CI pipeline, branch protection, and
release lifecycle.

The full submodule graph has a strict dependency ordering. No submodule may
depend on a submodule that is higher in the ordering:

```
Layer 0 (foundational — no inter-ogun dependencies):
  ogun-types           ← pure types, constants, no runtime behavior

Layer 1 (format and protocol — depends on Layer 0 only):
  ogun-image-format    ← depends on ogun-types
  elegua               ← Elegua Protocol; depends on ogun-types
  rustydb              ← embedded DB; no ogun-* dependencies

Layer 2 (runtime libraries — depends on Layers 0–1):
  ogun-runtime         ← bootloader, kernel-core, session-manager, host-service
  ogun-devices         ← virtual CPU, display, platform-host, network adapter
  bula                 ← UI support library

Layer 3 (SDK — depends on Layers 0–2):
  ogun-sdk             ← all SDK crates (app, service, kernel, driver, etc.)
  oya                  ← architecture generation; depends on ogun-types
  jaku                 ← release automation; depends on ogun-types

Layer 4 (applications — depends on Layers 0–3):
  ogun-os              ← ogun-desktop (Tauri), ogun-host-server, ogun-web
  ogun-components      ← Tier-2 and Tier-3 app components
  ogun-apps            ← Tier-4 personal enterprise apps

Layer 5 (tools and infrastructure — depends on Layers 0–4):
  ogun-tools           ← ogun-setup (Tauri), ogun-image-tool (Tauri)
  ogun-config          ← seed configuration templates (no Rust dependencies)
  ogun-artifacts       ← release artifact staging (no Rust dependencies)
  ogun-docs            ← documentation (no Rust dependencies)
  ogun-sites           ← public sites (no Rust dependencies)
  ogun-devops          ← CI templates and scripts (no Rust dependencies)
  ogun-test-features   ← experimental sandbox (excluded from release scope)
```

No cross-layer dependency inversions are permitted. An MR that introduces a
Layer 1 crate depending on a Layer 3 SDK crate is a P0 architecture violation
and must be rejected regardless of any other merit.

### 24.2 Adding a New Dependency (Cargo Crate)

All new dependencies must be evaluated for:

1. **License compatibility.** Must be MIT, Apache-2.0, or BSD-2/3-Clause.
   GPL-licensed crates require explicit approval from the project owner.
   `cargo-deny` enforces the license policy in the `audit` stage.

2. **Security track record.** Run `cargo-audit` locally before opening an MR
   that adds a new dependency. A new dependency with an active advisory in the
   RustSec database will fail the `security:audit` CI job.

3. **Build-time cost.** Prefer crates with minimal transitive dependency trees.
   Adding a dependency that pulls in 50 additional crates requires explicit
   justification in the MR description.

4. **Maintenance health.** Avoid crates that have not been updated in over 24
   months or that are marked as `YANKED` in the RustSec database.

5. **Duplication policy.** If a crate providing similar functionality is already
   in the workspace (`cargo-deny` bans duplicates by default), justify the
   addition or update the existing dependency rather than adding a second.

For adding a dependency to `ogun-runtime`, `ogun-image-format`, or `elegua`,
the MR description must include an explicit security and license review section.

### 24.3 Updating Existing Dependencies

Dependency updates use `cargo update` and are committed on a `chore/` branch:

```powershell
cd C:\dev\ogun\ogun-runtime
git checkout develop
git pull origin develop
git checkout -b chore/update-ring-and-zstd

cargo update -p ring
cargo update -p zstd
cargo test --workspace
cargo audit

git add Cargo.lock
git commit -m "chore: update ring and zstd to latest patch versions"
git push -u origin chore/update-ring-and-zstd
```

The weekly `security:audit` scheduled job (`SCHEDULE_TYPE=security`) runs
`cargo update --dry-run` and reports available updates. Security-relevant
updates (flagged by `cargo-audit`) must be addressed within 7 days of the
weekly report. Non-security updates are batched monthly.

### 24.4 Submodule Pointer Discipline

The umbrella `ogun/` records a specific commit SHA for each submodule. Submodule
pointers must obey the following rules:

- The umbrella's `main` branch always points to tagged commits in each submodule
  (never to branch tips). An MR into the umbrella's `main` must include a
  submodule pointer freeze step (§6 Phase 7).
- The umbrella's `develop` branch may point to submodule `develop` tips. Pointer
  updates to `develop` are committed as `chore/bump-{submodule}-to-{sha}` branches.
- A submodule pointer update that causes `cargo metadata --no-deps` to fail
  in the umbrella is a P0 incident.
- Never use `git submodule update --init --recursive --remote` on the umbrella's
  `main` branch; this would pull submodule `main` tips rather than the pinned
  tagged commits.

### 24.5 Paired MR Workflow (Cross-Submodule Changes)

When a feature requires coordinated changes in multiple submodules (for example,
a new SDK trait in `ogun-sdk` that is consumed by `ogun-components`):

1. Open MR A in the upstream submodule (`ogun-sdk`): new trait on `feat/` branch.
2. Open MR B in the downstream submodule (`ogun-components`): integration branch.
   MR B explicitly notes its dependency on MR A in its description.
3. Merge MR A into `ogun-sdk/develop`.
4. Update the `ogun-sdk` submodule pointer in the umbrella.
5. Merge MR B into `ogun-components/develop`.

Never merge the downstream MR (B) before the upstream MR (A) is merged and the
submodule pointer is updated. The downstream repo's CI will fail on a stale
pointer because it references a feature branch commit, not a `develop` tip.

For triple-dependency chains (A → B → C), the merge order is strictly A, then
B, then C. Open all three MRs simultaneously but merge in order.

### 24.6 Submodule Health Monitoring

The `validate:submodules` CI job runs on every MR and `main` push, verifying
that every expected submodule directory is non-empty. An empty submodule
directory indicates a deploy key or access token misconfiguration that will
cause silent build failures downstream.

The full list of expected submodules is:
```
bula elegua jaku oya rustydb
ogun-sdk ogun-runtime ogun-devices
ogun-os ogun-components ogun-apps ogun-tools
ogun-artifacts ogun-config ogun-devops
ogun-docs ogun-sites ogun-experimental
```

Override `EXPECTED_SUBMODULES` in a child repo's `.gitlab-ci.yml` to match
that repo's actual submodule set.

---

## 25. Testing Strategy

### 25.1 Testing Philosophy

Tests in ogun OS are organized around three principles:

1. **Boot-chain correctness is non-negotiable.** The three-stage boot
   verification, kernel subsystem initialization order, and session lifecycle
   must have test coverage at every step. A PR that removes or disables a
   boot-chain test requires two maintainer approvals.

2. **Tests must be deterministic.** Flaky tests are treated as bugs. A test
   that fails intermittently must be fixed or removed; it is never merged as
   `allow_failure: true` in the production CI config.

3. **Tests live next to the code.** Unit tests (`#[cfg(test)]` modules) live in
   the same file as the code under test. Integration tests live in `tests/`
   directories within each workspace member. End-to-end tests live in
   `ogun-test-features/` and are explicitly excluded from release-gate CI.

### 25.2 Test Pyramid

```
                ┌──────────────────────┐
                │  End-to-end (E2E)    │  ogun-test-features/
                │  Full boot on Windows│  Not in release CI
                └──────────────────────┘
              ┌────────────────────────────┐
              │  Integration tests         │  cargo test --all --test '*'
              │  Cross-crate flows         │  version.yml test:workspace
              └────────────────────────────┘
            ┌──────────────────────────────────┐
            │  Unit tests                      │  cargo test --all --lib
            │  Per-function, per-module        │  In every crate
            └──────────────────────────────────┘
          ┌────────────────────────────────────────┐
          │  Doc tests                             │  cargo test --doc --workspace
          │  Code examples in rustdoc comments     │  All public API examples
          └────────────────────────────────────────┘
        ┌──────────────────────────────────────────────┐
        │  Static analysis (check + clippy + fmt)      │  Fastest; runs first
        │  No compilation required for fmt and check   │  check.yml
        └──────────────────────────────────────────────┘
```

### 25.3 Unit Tests

Unit tests live in `#[cfg(test)]` blocks within each `.rs` source file. They
test individual functions and methods in isolation.

Requirements for all unit tests:
- Must be deterministic: no random seeds without a fixed seed for test runs.
- Must run in under 1 second. Tests that perform disk I/O or network calls must
  use fixtures or mocks.
- Test coverage for all public API functions in security-critical crates
  (`ogun-bootloader`, `ogun-image-format`, `ogun-session-manager`) is mandatory.

Run unit tests:
```powershell
cargo test --all --lib -- --show-output
```

### 25.4 Integration Tests

Integration tests live in `tests/` directories within each workspace member.
They test cross-function and cross-module flows, typically involving multiple
structs or the initialization sequence of a component.

For `ogun-runtime`: integration tests must cover the full three-stage boot
verification pipeline. A `KernelBootBundle` construction test and a clean
shutdown + `CleanShutdownMarker` write test are required.

For `ogun-devices`: integration tests must include a deterministic tick runner
test for every virtual device. The tick runner test initializes a device, runs
it for a fixed number of ticks, and asserts the expected post-tick state.

For `ogun-sdk`: integration tests must verify that `OgunApp`, `OgunService`,
and `OgunPlugin` trait implementations load, initialize, tick, receive IPC, and
shut down cleanly through the full SDK lifecycle.

Run integration tests:
```powershell
cargo test --all --test '*' -- --show-output
```

### 25.5 Doc Tests

All public API functions in `ogun-sdk`, `elegua`, and `ogun-image-format` must
include a working rustdoc example. Doc tests are compiled and run in CI by
`cargo test --doc --workspace`.

Doc tests that demonstrate error paths must show both the success case and the
relevant error variant. Panicking examples must use `should_panic` or be
wrapped in `Result`-returning examples.

Run doc tests:
```powershell
cargo test --doc --workspace
```

### 25.6 Security-Critical Test Requirements

For `ogun-runtime`, `ogun-image-format`, and `elegua`, the following tests are
mandatory and may not be disabled:

| Test | What it verifies |
|---|---|
| `test_image_signature_valid` | A correctly signed image passes all three boot stages |
| `test_image_signature_tampered` | A tampered image (bit flip in payload) halts at Stage 1 |
| `test_abi_version_mismatch` | An image with a wrong `OGUN_ABI_VERSION` halts the boot |
| `test_host_key_derivation` | HKDF-SHA256 produces the expected host key for a known set of inputs |
| `test_clean_shutdown_marker` | `CleanShutdownMarker` is written as the absolute last act of shutdown |
| `test_crash_recovery_activates` | Missing `CleanShutdownMarker` activates crash recovery at next boot |
| `test_ipc_capability_gate_enforced` | An IPC message from a non-capable app is rejected |
| `test_opqn_isolation_cross_enterprise` | Cross-enterprise IPC without explicit grant is rejected |

Two-maintainer approval is required for any MR that modifies these tests.

### 25.7 Performance Tests

Performance baselines are tracked in `ogun-test-features/benches/`. Criterion
benchmarks are run manually before each RC release to confirm that boot time,
session startup time, IPC throughput, and `ogun-cpu` tick latency remain within
the targets defined in `DESIGN.md`.

Performance regression over the baseline by more than 10% is treated as a
`fix/*` item before the RC is promoted to stable.

### 25.8 Coverage

Code coverage is produced by `cargo-llvm-cov` and is activated by setting
`ENABLE_COVERAGE=true` in the pipeline variables. Coverage reports are uploaded
to GitLab as Cobertura XML and displayed in MR diff views.

Coverage targets (minimum):
- `ogun-bootloader`: 85% line coverage
- `ogun-image-format`: 90% line coverage
- `ogun-session-manager`: 80% line coverage
- `elegua`: 80% line coverage
- `ogun-sdk` public API: 75% line coverage

Coverage is a guide, not a gate. A test suite with 95% coverage that does not
include the mandatory security-critical tests (§25.6) is insufficient.

### 25.9 Nightly Rust Regression Testing

The `nightly:build` CI job runs on the `SCHEDULE_TYPE=nightly` schedule, compiling
and testing the workspace with `cargo +nightly build --workspace --all-features`
and `cargo +nightly test --workspace --all-features`. It has `allow_failure: true`
because nightly Rust regressions are expected and the ogun workspace uses only
stable features; the nightly job exists to catch upstream regressions early.

A persistent nightly failure for more than two consecutive nights triggers a
`fix/` branch investigation. If the failure is caused by a nightly Rust
regression rather than ogun code, a tracking issue is opened and the nightly
job's `allow_failure` setting remains `true`.

### 25.10 Test Execution in Pull Request Pipelines

The following test jobs run on every MR, in order:

1. `validate:workspace` — cargo metadata resolves
2. `fmt` — `cargo fmt --all -- --check`
3. `clippy` — `cargo clippy --workspace --all-targets --all-features -- -D warnings`
4. `check:workspace` — `cargo check --workspace`
5. `test:workspace` — `cargo test --workspace --verbose -- --show-output`
6. `security:audit` — `cargo audit` (allow_failure: true for non-runtime repos)

The `build:debug` job runs after `test:workspace`. The full release build and
Windows Tauri builds run only on `main` merges and version tags.

---

## 26. CI/CD Environments and Strategies

### 26.1 CI/CD Architecture Overview

The ogun CI/CD system is built on GitLab CI and uses a shared template library
stored in `ogun-devops/ogun-cicd/`. All child repositories include these
templates via `include:` directives referencing `main` of `ogun-devops`. The
template library is the single source of truth for all pipeline behavior.

The nine template files and their responsibilities:

| File | Stage | Responsibility |
|---|---|---|
| `configure.yml` | (global) | Global variables, Docker image, cache templates, branch rules, runner tags, workflow rules |
| `validate.yml` | `validate` | Workspace metadata check, submodule health, `VERSION.md` sanity |
| `check.yml` | `check` | `rustfmt`, `clippy`, `cargo check`, ABI change notice |
| `test.yml` | `test` | Workspace tests, unit, integration, doc, coverage, nightly |
| `build.yml` | `build` | Debug, release Linux, cross Windows, Tauri desktop + setup, component libs, nightly build |
| `sast.yml` | `audit` | `cargo-audit`, `cargo-deny`, supply-chain, SBOM, SonarQube, weekly audit |
| `package.yml` | `package` + `pages` | `.ogpkg` packaging, Tauri bundle packaging, rustdoc → GitLab Pages |
| `deploy.yml` | `release` | GitLab release creation, build attestation, environment deploy |
| `version.yml` | `version` | Version bumping, git tagging, push via `update_version.py` |

### 26.2 Stage Execution Order

```
validate → check → test → build → audit → package → pages → version → release
```

Every stage must pass before the next stage begins. The `release` stage only
fires on semver tags (`v[0-9]+.[0-9]+.[0-9]+`). The `version` stage only fires
on manual trigger, API trigger, or scheduled pipeline with `SCHEDULE_TYPE` set.

### 26.3 Pipeline Trigger Matrix

| Trigger source | Branch / condition | Stages that run |
|---|---|---|
| MR (any branch) | All | validate, check, test, build:debug |
| Push to `develop` | Commit on develop | validate, check, test, build:debug, audit |
| Push to `main` | Commit on main | validate, check, test, build:debug, build:release, build:windows-cross, audit, package, pages |
| Push to `release/*` | Release branch commit | validate, check, test, build:debug, build:release, audit |
| Semver tag `v*.*.*` | Tag push | validate, check, test, build:release, build:windows-cross, build:tauri, audit, package, release |
| Schedule `nightly` | `SCHEDULE_TYPE=nightly` | build:nightly, test:nightly, version:nightly |
| Schedule `security` | `SCHEDULE_TYPE=security` | audit:weekly |
| Schedule `version` | `SCHEDULE_TYPE=version` | version:tag |
| Web / API trigger | `CI_PIPELINE_SOURCE=web/api` | validate, check, test, build:debug, build:release (+ Windows if `ENABLE_WINDOWS_BUILD=true`) |
| Web / API (version) | `version:tag` manual | version:tag only |
| Web / API (preview) | `version:preview` | version:preview (dry-run) |

### 26.4 Global CI Variables

All child repositories inherit the following global variables from `configure.yml`.
Override at the project level only when genuinely necessary.

| Variable | Default | Purpose |
|---|---|---|
| `CARGO_HOME` | `$CI_PROJECT_DIR/.cargo` | Cargo registry and cache directory inside the CI workspace |
| `CARGO_INCREMENTAL` | `0` | Disable incremental compilation; required for reproducible builds |
| `RUSTFLAGS` | `-D warnings` | Deny all compiler warnings; treat them as errors |
| `RUST_BACKTRACE` | `1` | Enable backtraces in test output |
| `CARGO_TERM_COLOR` | `always` | Force colored Cargo output in CI logs |
| `GIT_DEPTH` | `0` | Full clone; required for `cargo-audit` tag inspection |
| `OGUN_MAIN_BRANCH` | `main` | Branch name used in pipeline rules |
| `OGUN_DEV_BRANCH` | `develop` | Branch name used in pipeline rules |
| `VERSION_SCRIPT_URL` | (ogun-devops raw URL) | Source URL for `update_version.py` |
| `ARTIFACT_DIR` | `$CI_PROJECT_DIR/artifacts` | Output directory for SBOM and attestation files |

Per-repository variables that activate optional pipeline features:

| Variable | Repo | Effect |
|---|---|---|
| `ENABLE_WINDOWS_BUILD` | `ogun-os`, `ogun-devices` | Activates Windows cross-compiled build job |
| `ENABLE_WINDOWS_CHECK` | `ogun-runtime` | Activates Windows `cargo check` on the Linux runner |
| `ENABLE_SBOM` | `ogun-runtime`, `ogun-os` | Activates SBOM generation in the `audit` stage |
| `ENABLE_COVERAGE` | Any repo | Activates `cargo-llvm-cov` coverage report |
| `ENABLE_SONAR` | Selected repos | Activates SonarQube scan |

### 26.5 Cargo Cache Strategy

The `.cargo_cache` template uses a pull-push policy keyed on `Cargo.lock` +
`$CI_JOB_NAME-$CI_COMMIT_REF_SLUG`. This ensures:

- Different jobs on the same branch share registry downloads but have separate
  `target/` directories (avoiding cross-job artifact contamination).
- Cache is invalidated automatically when `Cargo.lock` changes.
- Cache misses fall back to a cold build; they do not fail the pipeline.

The read-only `.cargo_cache_ro` variant is used for jobs that must not pollute
the shared cache (e.g., nightly toolchain jobs that may write incompatible
incremental artifacts).

### 26.6 Windows Runner Requirements and Configuration

The Windows native runner must have the following installed before it can
execute Tauri build jobs:

| Requirement | Minimum version | Notes |
|---|---|---|
| Rust stable toolchain | 1.80.0 | `rustup default stable` |
| Node.js LTS | 20.x | Required by Tauri's frontend bundler |
| npm | 10.x | Comes with Node LTS |
| WebView2 | Latest | Required by Tauri 2 on Windows |
| VS Build Tools | 2022 | `Microsoft.VisualCpp.Tools.HostX64.TargetX64` workload |
| Tauri CLI | 2.x | Installed via `npm install -g @tauri-apps/cli` |
| GitLab Runner | Latest | Registered with `windows` + `x64` tags |

The runner must also have `OGUN_IMAGE_SIGNING_KEY_B64` configured as a
Protected + Masked CI/CD variable at the project or group level. Without this
variable, the `attestation` job in the `release` stage will exit with an error
and block the release pipeline.

### 26.7 Security-Critical Pipeline Overrides

Repositories containing security-critical code (`ogun-runtime`, `elegua`,
`ogun-image-format`) override the shared template defaults as follows:

| Override | Default in templates | Override value |
|---|---|---|
| `security:audit` `allow_failure` | `true` | `false` — audit failures block the pipeline |
| Minimum approvals on `main` | 1 | 2 — two maintainer approvals required |
| `ENABLE_SBOM` | `false` | `true` — SBOM always generated on main and tags |
| `ENABLE_WINDOWS_CHECK` | `false` | `true` — Windows compilation verified on every MR |

### 26.8 Release Pipeline Flow

The full release pipeline runs automatically when a semver tag is pushed to any
submodule's `main` branch. The flow is:

```
1. validate → check → test                  (correctness gate)
2. build:release (Linux)                     (Linux artifact)
3. build:release:windows (cross-compiled)    (Windows EXE/DLL)
4. build:tauri:desktop + build:tauri:setup   (Windows native runner)
5. audit (cargo-audit, cargo-deny, SBOM)     (security gate)
6. package (.ogpkg archives for each app)    (distribution archives)
7. pages (rustdoc → GitLab Pages)            (API documentation)
8. release (GitLab Release + attestation)    (public release record)
```

The attestation job (`job_attest`) in step 8 requires `OGUN_IMAGE_SIGNING_KEY_B64`.
If the key is absent, the entire `release` stage fails. This is intentional:
an unsigned release is not a valid release.

### 26.9 `version.yml` Job Reference

All version jobs are opt-in. None run automatically on push.

| Job | Trigger | Effect |
|---|---|---|
| `version:tag` | Manual (web/API) or `SCHEDULE_TYPE=version` | Bumps version files, commits, creates annotated tag, pushes branch + tags |
| `version:preview` | Web/API | Dry-run; shows what `version:tag` would do without writing anything |
| `version:nightly` | `SCHEDULE_TYPE=nightly` | Appends nightly timestamp to version files; no commit, no persistent tag |
| `version:ci` | `SCHEDULE_TYPE=ci` or API with `SCHEDULE_TYPE=ci` | Alpha gate + dev maturity; auto-increments; commits and pushes |
| `version:cm` | Manual (web/API) or `SCHEDULE_TYPE=cm` | CM maturity; marks a fully validated artifact; commits and pushes |
| `version:rc` | Manual (web/API) or `SCHEDULE_TYPE=rc` | RC gate; auto-increments gate-minor; commits and pushes |
| `version:stable` | Manual (web/API) or `SCHEDULE_TYPE=stable` | Stable gate; no gate suffix on version string; commits and pushes |

All version jobs require `OGUN_DEVOPS_DEPLOY_TOKEN` to fetch `update_version.py`
from `ogun-devops` at runtime. Without this token, all version jobs fail at the
`before_script` stage.

### 26.10 Enabling a Child Repository's CI Pipeline

To add a new submodule repository to the ogun CI/CD system:

1. Create the GitLab repository under the `ogun-foundation` group.
2. Add the repository as a submodule to the umbrella:
   ```powershell
   cd C:\dev\ogun
   git submodule add git@gitlab.com:ogun-foundation/{new-repo}.git {new-repo}
   git add .gitmodules {new-repo}
   git commit -m "chore: add {new-repo} submodule"
   ```
3. Create a `.gitlab-ci.yml` in the new repository with `include:` directives
   for `configure.yml` and the relevant template files.
4. Add `VERSION.md` at the repository root with the current version string.
5. Configure group-level CI/CD variables (`OGUN_DEVOPS_DEPLOY_TOKEN`,
   `OGUN_IMAGE_SIGNING_KEY_B64`) are inherited automatically.
6. Set any repo-specific variables (`ENABLE_WINDOWS_BUILD`, `ENABLE_SBOM`, etc.)
   at the project level.
7. Add the repository to `EXPECTED_SUBMODULES` in the umbrella's
   `validate:submodules` job override.
8. Open an MR in `ogun-devops` to document the new repository's pipeline
   requirements if they differ from the shared defaults.

---

*ogun OS · Project Ogún · 2026*  
*Owner: Dominic Eaton (@eatondo)*  
*Document: WORKFLOW.md*  
*Licensed under GNU General Public License v3.0*
