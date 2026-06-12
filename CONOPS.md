# CONOPS.md — ogun OS DevOps Concept of Operations

**Document type:** Concept of Operations (CONOPS)  
**Version:** 0.1.0-beta  
**Owner:** Dominic Eaton ([@eatondo](https://gitlab.com/eatondo))  
**Organization:** The Ogun Foundation  
**Primary Repository:** https://gitlab.com/ogun-foundation/ogun  
**Classification:** Internal — Unrestricted  
**License:** GPL-3.0  
**Status:** Canonical · Supersedes `WORKFLOW.md`

---

## Table of Contents

**Part I — Operational Foundation**

1. [Executive Summary and Scope](#1-executive-summary-and-scope)
2. [Operational Vision](#2-operational-vision)
3. [Stakeholders and User Roles](#3-stakeholders-and-user-roles)

**Part II — System Context**

4. [Operational Context and Environment](#4-operational-context-and-environment)
5. [Toolchain and Architecture](#5-toolchain-and-architecture)
6. [Repository Graph](#6-repository-graph)

**Part III — Branch and Change Governance**

7. [Permanent Branches](#7-permanent-branches)
8. [Branch Naming Conventions](#8-branch-naming-conventions)
9. [Per-Repository Branching Rules](#9-per-repository-branching-rules)
10. [Merge Request Standards](#10-merge-request-standards)
11. [Commit Message Convention](#11-commit-message-convention)
12. [Branch Protection Rules](#12-branch-protection-rules)

**Part IV — Workflows and Scenarios**

13. [Feature Development Workflow](#13-feature-development-workflow)
14. [Release Workflow](#14-release-workflow)
15. [Hotfix and Security Workflow](#15-hotfix-and-security-workflow)
16. [ABI and Protocol Change Workflow](#16-abi-and-protocol-change-workflow)
17. [Submodule Synchronization Workflow](#17-submodule-synchronization-workflow)
18. [Rollback Procedures](#18-rollback-procedures)

**Part V — Versioning and Release**

19. [Versioning System — Full Reference](#19-versioning-system--full-reference)
20. [Release Strategy and Gates](#20-release-strategy-and-gates)
21. [Maturities, Canary Deployments, and Rollout Strategy](#21-maturities-canary-deployments-and-rollout-strategy)

**Part VI — Infrastructure and Environments**

22. [Sandboxing and Environments](#22-sandboxing-and-environments)
23. [Environment and Deployment Map](#23-environment-and-deployment-map)
24. [Configuration Management](#24-configuration-management)

**Part VII — Dependencies and Quality**

25. [Submodule and Dependency Management](#25-submodule-and-dependency-management)
26. [Testing Strategy](#26-testing-strategy)

**Part VIII — CI/CD Operations**

27. [CI/CD Environments and Strategies](#27-cicd-environments-and-strategies)
28. [CI/CD Pipeline Stages](#28-cicd-pipeline-stages)
29. [Scheduled Pipeline Jobs](#29-scheduled-pipeline-jobs)
30. [Repository-Specific CI Notes](#30-repository-specific-ci-notes)

**Part IX — Lifecycle and Maintenance**

31. [Pipeline Lifecycle and Maintenance](#31-pipeline-lifecycle-and-maintenance)
32. [Observability and Monitoring](#32-observability-and-monitoring)

**Part X — Risk and Governance**

33. [Risks and Mitigations](#33-risks-and-mitigations)
34. [Incident Response and Escalation](#34-incident-response-and-escalation)

**Appendices**

35. [Quick Reference Command Sheets](#35-quick-reference-command-sheets)
36. [Glossary](#36-glossary)

---

# Part I — Operational Foundation

---

## 1. Executive Summary and Scope

### 1.1 Purpose of This Document

This Concept of Operations defines how the ogun OS software development,
build, test, release, and deployment system is structured, operated, and
maintained. It serves as the authoritative alignment document between The Ogun
Foundation's engineering goals and the specific technical workflows that
implement them.

The document is intended to be read by:

- Contributors and maintainers implementing features or fixes
- Reviewers evaluating merge requests
- CI/CD operators configuring and maintaining the pipeline infrastructure
- Security reviewers auditing the release and signing chain
- Future contributors onboarding to the project

Where this document defines a rule, that rule governs. Where it references
another document (`DESIGN.md`, `CHANGELOG.md`, `SECURITY.md`), that document
provides the authoritative detail on the referenced topic.

### 1.2 What This System Is Responsible For

The ogun DevOps system is responsible for:

- Continuous integration of all Rust crates, Tauri applications, and
  configuration files across the full ogun repository graph (20+ repositories
  and 122+ Cargo manifests)
- Automated quality gates: format, lint, compile, test, and security audit on
  every merge request
- Artifact production: debug builds, release builds, cross-compiled Windows
  x64 binaries, Tauri application bundles, and `.ogpkg` distribution archives
- Version management: stamping consistent semver version strings across all
  manifests in the monorepo graph using `update_version.py`
- Release coordination: creating annotated git tags, GitLab releases, SBOM
  generation, build attestation signing, and artifact staging in `ogun-artifacts/`
- Security enforcement: supply-chain integrity checks, dependency auditing, and
  mandatory two-maintainer review for security-critical code paths
- Nightly regression detection: scheduled builds against the nightly Rust
  toolchain and weekly `cargo-audit` sweeps
- Canary rollout management (0.2.0+): progressive deployment of releases to
  opted-in operator fleets with automatic halt and rollback

### 1.3 What This System Is Not Responsible For

The ogun DevOps system is explicitly not responsible for:

- Cloud infrastructure provisioning (ogun OS installs on operator machines;
  it does not deploy to cloud servers)
- End-user update delivery in 0.1.0 (no auto-update mechanism ships in the
  first public release)
- Host OS configuration on developer or operator machines
- Third-party dependency patching (the supply-chain audit flags advisories;
  remediation is a manual developer task)
- Content of the ogun OS runtime itself — the DevOps system builds and
  delivers the runtime but does not define its behavior (see `DESIGN.md`)

### 1.4 Scope Boundaries

| In scope | Out of scope |
|---|---|
| All repositories under `gitlab.com/ogun-foundation/` | GitHub/Codeberg mirrors (read-only; no CI runs there) |
| `develop` and `main` branch CI pipelines | `ogun-test-features` experimental branches |
| GitLab CI/CD shared templates in `ogun-devops` | Developer IDE configuration |
| Release artifact production and signing | End-user installation support |
| Version tagging via `update_version.py` | Runtime telemetry collection and analysis |
| Scheduled nightly and weekly security pipelines | Legal, licensing, or compliance audits |

### 1.5 Current State (0.1.0-beta)

The project is at **0.1.0-beta** — the first public release of ogun OS. The
DevOps system is fully operational for the Desktop Edition (Windows x64). The
pipeline produces four signed artifacts: `ogun-setup.exe`, `ogun-desktop.exe`,
`ogun-emulator.exe`, and `ogun-host-service` (linked into the Tauri bundle),
plus the signed kernel image `ogun-windows-0.1.0-beta.img`.

The canary deployment mechanism, auto-update delivery, and multi-platform CI
targets are documented in this CONOPS but are not yet active; they are roadmap
items for 0.2.0 and beyond.

---

## 2. Operational Vision

### 2.1 Desired Future State

The ogun DevOps system aims to reach the following operational posture by the
0.2.0 stable release:

**Development velocity.** Every merged feature is automatically built, tested,
and available as a nightly artifact within 2 hours of merge. No manual steps
are required between a merged MR and a deployable build.

**Release confidence.** Stable releases are produced by a fully automated
pipeline that has verified correctness (tests pass), security (audit clean,
image signed), and reproducibility (two independent builds of the same tag
produce byte-identical artifacts) before the release page is published.

**Operator safety.** Canary deployments reach operators in tiers (1% → 10% →
100%), with automatic halt and rollback if crash rates, boot failure rates, or
image verification failures exceed defined thresholds. Operators who do not opt
in to canary never receive an unstable build.

**Supply-chain transparency.** Every release artifact is accompanied by a
signed SBOM (CycloneDX + SPDX) and a build attestation artifact that allows
operators and auditors to verify the provenance of every binary in the
distribution.

**Developer experience.** A developer can clone the umbrella repository,
initialize submodules, and have a passing local build in under 15 minutes on a
Windows x64 machine with the required toolchain installed. CI feedback on a
merge request arrives in under 10 minutes for the check and test stages.

### 2.2 Success Metrics

| Metric | Current (0.1.0-beta) | Target (0.2.0) |
|---|---|---|
| CI feedback time (check + test) | < 15 minutes | < 10 minutes |
| Release pipeline duration (full, tag to published release) | < 45 minutes | < 30 minutes |
| Nightly build success rate | Establishing baseline | ≥ 95% over rolling 30 days |
| Mean time to recovery (MTTR) from P0 | Not yet measured | < 4 hours from detection to fix merged |
| Mean time to detect (MTTD) regression | Manual | < 24 hours via nightly pipeline |
| Security advisory response time | 7-day SLA | 7-day SLA (unchanged) |
| Supply-chain audit coverage | All Rust repos | All Rust repos + SBOM on every release |
| Canary rollout automation | Not active | Tier 1 → GA automated; halt conditions active |
| Release frequency | On demand | ≥ 1 release per 6-week cycle for minors |

### 2.3 Guiding Principles

**Automation over manual steps.** Every repeatable operation — version bumping,
artifact packaging, release page creation, tag creation — is automated. Manual
steps exist only where a human decision is required (gate transition approvals,
signing key usage).

**Gate quality, not speed.** Pipeline stages are ordered so that the cheapest
checks run first. A failing `cargo fmt` never wastes CI time waiting for a
test suite to run. Speed is a goal but it never trades away correctness.

**Security is non-negotiable.** The three-key security model (image key,
system key, host key), the Ọpọn Protocol isolation boundary, and the
capability-gated IPC system are design invariants. The DevOps system enforces
these invariants automatically where possible (CI audit, mandatory tests) and
through process where not (two-maintainer review on security-critical paths).

**Reproducibility.** Every released artifact must be reproducible from its
tag. `CARGO_INCREMENTAL=0` is set globally. Vendored dependencies are verified
against `Cargo.lock` on `security/*` branches and `main`. The SBOM records the
exact dependency graph for every release.

**No surprises on `main`.** The `main` branch in every repository always
reflects released, tagged, production-quality code. Nothing lands on `main`
without passing the full pipeline. Nothing is released without a tag.

---

## 3. Stakeholders and User Roles

### 3.1 Role Definitions

The ogun DevOps system recognizes four operational roles. Each role has defined
responsibilities and access levels within the GitLab project structure.

---

**Project Owner — Dominic Eaton (@eatondo)**

The project owner holds final decision authority over all gate transitions,
architectural direction, and security model decisions. Specific responsibilities
include:

- Approving gate transitions (alpha → beta, beta → RC, RC → stable) per the
  decision matrix in §20.7
- Triggering the `version:stable` and `version:cm` CI jobs
- Signing off on release page content and public announcements
- Resolving disputes between maintainers on architecture or security decisions
- Maintaining the `OGUN_IMAGE_SIGNING_KEY_B64` and `OGUN_DEVOPS_DEPLOY_TOKEN`
  protected CI/CD variables

Access level: **Owner** on all repositories in `ogun-foundation/`.

---

**Maintainer**

Maintainers are trusted contributors with merge authority on `main` and
`develop`. There must be a minimum of two active maintainers at all times to
satisfy the two-approval requirement on security-critical MRs.

Responsibilities:

- Reviewing and approving merge requests targeting `develop` and `main`
- Providing the second approval on security-critical MRs (`ogun-runtime`,
  `elegua`, `abi/*` branches)
- Monitoring nightly build failures and assigning P0 investigations
- Executing release workflow phases 1–9 (§14) under project owner direction
- Maintaining branch protection rules in GitLab settings
- Responding to security advisory reports per `SECURITY.md`

Access level: **Maintainer** on assigned repositories.

---

**Developer / Contributor**

Developers implement features, fixes, and documentation. They do not have
direct push access to `main` or `develop`. All work arrives via merge request.

Responsibilities:

- Creating feature, fix, refactor, docs, chore, and CI branches from `develop`
- Running local checks before opening MRs (`cargo fmt`, `cargo check`,
  `cargo test`, `cargo clippy`)
- Writing tests for new behavior, meeting coverage targets in §26.8
- Updating `CHANGELOG.md` under `[Unreleased]` for every MR
- Keeping the MR description complete (summary, issue reference, affected
  workspaces, checks run, residual risk)

Access level: **Developer** on assigned repositories.

---

**CI/CD Operator**

The CI/CD operator role may be held by the project owner or a designated
maintainer. It is the operational role responsible for the pipeline
infrastructure itself, not for the software being built.

Responsibilities:

- Maintaining `ogun-devops/ogun-cicd/` YAML templates
- Managing GitLab Runner registration and health for Linux Docker and Windows
  native runners
- Rotating CI/CD secrets (`OGUN_IMAGE_SIGNING_KEY_B64`,
  `OGUN_DEVOPS_DEPLOY_TOKEN`, `SONAR_TOKEN`) on schedule or on compromise
- Monitoring pipeline success rates and addressing systematic failures
- Evaluating and applying GitLab platform updates
- Onboarding new repositories to the CI system per the procedure in §27.10

Access level: **Maintainer** on `ogun-devops`; **Owner** access to GitLab
group CI/CD variable settings.

---

**Quality Assurance (QA)**

QA personnel validate release candidates and beta builds against documented
acceptance criteria. QA is currently performed by the project owner and
maintainers; a dedicated QA role is anticipated for 0.2.0+.

Responsibilities:

- Executing the release gate validation checklist for each gate transition
- Triggering `version:test` builds via the CI web UI for structured test cycles
- Reporting issues against specific artifact versions using the full version
  string (`v0.1.0-beta.1.1`)
- Verifying the `ogun-setup.exe` installation on a clean Windows x64 machine
  before each RC promotion
- Confirming design invariants I-01 through I-35 hold end-to-end

Access level: **Reporter** on all repositories; may be promoted to **Developer**
for QA-specific tooling branches.

### 3.2 Responsibility Assignment Matrix (RACI)

| Activity | Project Owner | Maintainer | Developer | CI/CD Operator | QA |
|---|---|---|---|---|---|
| Gate transition approval | **A/R** | C | I | I | C |
| MR review and approval | A | **R** | I | I | I |
| Security MR second approval | A | **R** | I | I | I |
| version:stable trigger | **R** | I | I | I | I |
| version:tag / version:ci | A | **R** | I | R | I |
| Feature implementation | I | C | **R** | I | I |
| CI template maintenance | A | C | I | **R** | I |
| Runner health and registration | A | C | I | **R** | I |
| Secret rotation | **A/R** | C | I | R | I |
| Release gate validation | **A** | C | I | I | **R** |
| Beta artifact validation | A | C | I | I | **R** |
| SBOM and attestation review | **A/R** | C | I | C | I |
| Security advisory response | **A/R** | R | I | I | I |
| Nightly failure investigation | A | **R** | R | R | I |
| CHANGELOG updates | I | C | **R** | I | I |

*R = Responsible, A = Accountable, C = Consulted, I = Informed*

---

# Part II — System Context

---

## 4. Operational Context and Environment

### 4.1 System Boundaries

ogun OS is an operating system layer that installs on top of a host OS rather
than replacing it. This shapes every aspect of the DevOps system:

- There is no cloud server fleet to deploy to. Releases are distributed as
  signed installer artifacts that operators download and run.
- "Production" is the operator's Windows x64 machine after a successful
  installation by `ogun-setup.exe`.
- There is no staging server. The staging equivalent is a clean Windows x64
  machine running a release candidate build.
- Rollback is installation-level: reverting to a prior version means
  re-running `ogun-setup.exe` with the prior artifact.

The DevOps system boundary runs from source code commit (developer's machine
or MR push) to signed, published release artifact in `ogun-artifacts/` and
on the GitLab release page. What happens after an operator downloads and runs
the installer is the domain of the ogun OS runtime itself, not the DevOps
system — except for the canary telemetry loop described in §21.7.

### 4.2 Host Infrastructure

**GitLab.com** is the primary source of truth for all repositories, CI
pipelines, merge requests, issue tracking, and release pages. The organization
is at `gitlab.com/ogun-foundation/`.

**GitHub (mirror, read-only).** `github.com/dominic1eaton-code/ogun` is a
one-way mirror of the umbrella repository. No CI runs on GitHub. No pull
requests are accepted on the GitHub mirror.

**Codeberg (mirror, read-only).** `codeberg.org/eatondo000/ogun` is a second
one-way mirror. Same rules as GitHub.

**Cloudflare Workers Pages.** The public website (`ogun.eatondo000.workers.dev`)
and documentation site are deployed from `ogun-sites/` via Cloudflare Workers.
This is outside the GitLab CI scope but is an integration point for release
announcements.

**Windows x64 development machine.** All Rust development, Tauri development,
and final release validation occur on Windows x64. The canonical development
path is `C:\dev\ogun\`.

### 4.3 Required Integrations

| Integration | Purpose | How it connects |
|---|---|---|
| GitLab CI/CD | Pipeline execution | Native; templates in `ogun-devops/ogun-cicd/` |
| GitLab Container Registry | Docker images for CI runners | `rust:latest`, `python:3.12-slim` pulled at job start |
| GitLab Releases | Public release pages with artifact links | `release-cli` in `deploy.yml` |
| GitLab Pages | Internal rustdoc API documentation | `cargo doc` output, published in `package.yml` |
| RustSec Advisory Database | Dependency vulnerability scanning | `cargo-audit` in `sast.yml` |
| SonarQube (optional) | Static analysis and quality gate | `sonar-scanner` in `sast.yml`; requires `SONAR_HOST_URL` and `SONAR_TOKEN` |
| `ogun-devops` deploy token | `update_version.py` fetch at version job runtime | `OGUN_DEVOPS_DEPLOY_TOKEN` protected variable |
| Image signing key | Build attestation and SBOM signing | `OGUN_IMAGE_SIGNING_KEY_B64` protected variable |

### 4.4 Network and Access Constraints

GitLab CI runners must be able to reach:

- `crates.io` and `static.crates.io` — Cargo registry
- `github.com` — source dependencies referenced via git URLs
- `raw.githubusercontent.com` — `cargo-audit` advisory database
- `gitlab.com` — project API for release-cli and pipeline triggers
- `registry.npmjs.org` — npm packages for Tauri frontend builds (Windows runner)
- `sonarcloud.io` or the configured `SONAR_HOST_URL` (if ENABLE_SONAR=true)

The Windows native runner also requires access to Microsoft's WebView2
distribution servers during initial setup.

---

## 5. Toolchain and Architecture

### 5.1 Core Toolchain

| Tool | Version | Role |
|---|---|---|
| Rust stable | ≥ 1.80.0 | Primary implementation language for all crates |
| Rust nightly | Latest | Regression detection in nightly CI job only |
| Cargo | (ships with Rust) | Build system, test runner, dependency manager |
| rustfmt | (ships with Rust) | Code formatting enforcement |
| clippy | (ships with Rust) | Lint and static analysis |
| cargo-audit | Latest | Dependency vulnerability scanning (RustSec) |
| cargo-deny | Latest | License policy, duplicate dep policy, source policy |
| cargo-llvm-cov | Latest | Code coverage (activated by `ENABLE_COVERAGE=true`) |
| Tauri 2.x | ≥ 2.0.0 | Desktop application framework for `ogun-desktop`, `ogun-setup`, `ogun-image-tool` |
| Node.js LTS | 20.x | Tauri frontend build toolchain |
| npm | 10.x | Tauri frontend package manager |
| WebView2 | Latest | Windows rendering backend for Tauri |
| VS Build Tools 2022 | Latest | Windows native compilation for Tauri |
| Python 3.12 | 3.12.x | `update_version.py` execution environment |
| git | Latest | Version control; required by all pipelines |
| curl | Latest | `update_version.py` download in version jobs |

### 5.2 CI/CD Platform

| Component | Technology |
|---|---|
| CI/CD platform | GitLab CI |
| Template source | `ogun-devops/ogun-cicd/` (9 YAML template files) |
| Linux runner | Docker, `rust:latest` image |
| Windows runner | GitLab Runner on Windows x64; tags `windows` + `x64` |
| Version script | `update_version.py` (Python 3.12); fetched at runtime from `ogun-devops` |
| Artifact storage | GitLab job artifacts + `ogun-artifacts/` submodule |
| Release pages | GitLab Releases (`release-cli`) |
| API documentation | GitLab Pages (rustdoc output) |
| Secret management | GitLab CI/CD Protected + Masked variables |

### 5.3 Key Libraries and Protocols

| Library / Protocol | Repository | Role |
|---|---|---|
| Elegua Protocol | `elegua` | Typed capability-gated IPC between all ogun components |
| Ọpọn Protocol (SYS-001) | `ogun-runtime` | Isolation boundary between ogun OS and the host OS |
| RustyDB | `rustydb` | Embedded database backend (WAL, transactions, snapshots) |
| Bula | `bula` | UI generation support library |
| ring / sha2 / zstd | (Cargo deps) | Cryptography and compression in `ogun-image-format` |
| ed25519-dalek | (Cargo dep) | Image signing and verification |
| tokio | (Cargo dep) | Async runtime for kernel services and IPC bus |

### 5.4 Artifact Types

| Type | Extension | Produced by | Description |
|---|---|---|---|
| Kernel image | `.img` | `ogun-image-builder` CI | Signed, compressed platform kernel image |
| Desktop installer | `.exe` (NSIS/WiX bundle) | `build:tauri:setup` | `ogun-setup.exe` Windows installer |
| Desktop launcher | `.exe` | `build:tauri:desktop` | `ogun-desktop.exe` user-facing launcher |
| Distribution archive | `.ogpkg` | `package.yml` jobs | Versioned compressed tarball of a binary or bundle |
| Component library | `.dll` / `.so` | `build:components` | Runtime-loaded Tier-2/Tier-3 component libraries |
| SBOM | `.sbom.json` | `sast.yml` SBOM job | CycloneDX and SPDX dependency manifests |
| Attestation | `.attestation.json` | `deploy.yml` attest job | Signed build provenance record |

---

## 6. Repository Graph

### 6.1 Umbrella Repository

| Repository | GitLab Path | Role |
|---|---|---|
| `ogun` | `ogun-foundation/ogun` | Umbrella workspace; submodule host; release coordinator |

### 6.2 Rust Implementation Submodules

| Repository | GitLab Path | Workspace Members |
|---|---|---|
| `ogun-runtime` | `ogun-foundation/ogun-runtime` | `ogun-types`, `ogun-image-format`, `ogun-image-builder`, `ogun-bootloader`, `ogun-kernel-core`, `ogun-session-manager`, `ogun-host-service` |
| `ogun-devices` | `ogun-foundation/ogun-devices` | `ogun-emulator`, `ogun-emulator-backend`, `ogun-uefi`, `ogun-virtual-cpu`, `ogun-virtual-display-monitor`, `ogun-virtual-platform-host`, `ogun-virtual-network-adapter` |
| `ogun-os` | `ogun-foundation/ogun-os` | `ogun-desktop` (Tauri), `ogun-app`, `ogun-host-server`, `ogun-web` |
| `ogun-sdk` | `ogun-foundation/ogun-sdk` | `ogun-app-sdk`, `ogun-service-sdk`, `ogun-kernel-sdk`, `ogun-driver-sdk`, `ogun-module-sdk`, `ogun-device-sdk`, `ogun-plugin-sdk`, `ogun-component-sdk` |
| `ogun-components` | `ogun-foundation/ogun-components` | Tier-2 apps, Tier-3 apps, hosts, drivers, services |
| `ogun-apps` | `ogun-foundation/ogun-apps` | Tier-4 personal enterprise apps (`enzo`, `kogi`, `dongo`, `ume`, `shango`, `heshima`, `igi`, `moto`, and others) |
| `ogun-tools` | `ogun-foundation/ogun-tools` | `ogun-setup` (Tauri), `ogun-image-tool` (Tauri), future `ogun-ide` |

### 6.3 Protocol and Support Library Submodules

| Repository | GitLab Path | Role |
|---|---|---|
| `elegua` | `ogun-foundation/elegua` | Typed IPC and Elegua Protocol implementation |
| `rustydb` | `ogun-foundation/rustydb` | Embedded database backend; storage subsystem dependency |
| `bula` | `ogun-foundation/bula` | UI generation support library |
| `jaku` | `ogun-foundation/jaku` | Release automation tooling |
| `oya` | `ogun-foundation/oya` | Architecture generation and modeling |

### 6.4 Configuration, Artifact, and Documentation Submodules

| Repository | GitLab Path | Role |
|---|---|---|
| `ogun-config` | `ogun-foundation/ogun-config` | Seed configuration templates (`ogun.toml`, `display.toml`, `emulation.toml`, `uefi.toml`) |
| `ogun-artifacts` | `ogun-foundation/ogun-artifacts` | Staging area for built images, installers, checksums, and release metadata |
| `ogun-docs` | `ogun-foundation/ogun-docs` | Canonical product, architecture, release, and execution-model specifications |
| `ogun-sites` | `ogun-foundation/ogun-sites` | Public site and documentation site sources (Cloudflare Workers Pages) |
| `ogun-devops` | `ogun-foundation/ogun-devops` | Shared CI/CD YAML templates and `update_version.py` script |
| `ogun-test-features` | `ogun-foundation/ogun-test-features` | Experimental sandbox crates and prototype workspaces |

### 6.5 Layered Dependency Ordering

No submodule may depend on a submodule that is higher in this ordering. A
dependency inversion is a P0 architecture violation.

```
Layer 0 — Foundational (no inter-ogun dependencies):
  ogun-types

Layer 1 — Format and Protocol (depends on Layer 0 only):
  ogun-image-format  ·  elegua  ·  rustydb

Layer 2 — Runtime Libraries (depends on Layers 0–1):
  ogun-runtime  ·  ogun-devices  ·  bula

Layer 3 — SDK (depends on Layers 0–2):
  ogun-sdk  ·  oya  ·  jaku

Layer 4 — Applications (depends on Layers 0–3):
  ogun-os  ·  ogun-components  ·  ogun-apps

Layer 5 — Tools and Infrastructure (depends on Layers 0–4):
  ogun-tools  ·  ogun-config  ·  ogun-artifacts
  ogun-docs   ·  ogun-sites   ·  ogun-devops
  ogun-test-features (excluded from release scope)
```

---

# Part III — Branch and Change Governance

---

## 7. Permanent Branches

Every repository in the ogun graph maintains exactly two permanent branches.
No other branches are permanent; all feature, fix, release, and security
branches are deleted after merge.

### `main`

- Contains only production-ready, release-tagged code.
- Every commit on `main` must have passed the full CI pipeline.
- Direct pushes are blocked; merges arrive only via MR from `release/*` or
  `security/*` branches.
- Every merge into `main` must be immediately followed by a version tag.
- `main` is the source of truth for all public release artifacts.

### `develop`

- The integration branch for all active development.
- All `feat/*`, `fix/*`, `refactor/*`, `docs/*`, `chore/*`, `ci/*`, and
  `p0/*` branches merge into `develop`.
- `develop` must always be in a buildable state. A broken `develop` is a P0
  incident for the responsible workspace.
- `cargo check --workspace` and `cargo fmt --all` must pass on `develop` at all
  times.
- Nightly CI runs on `develop`; failures are investigated before the next
  working day.

---

## 8. Branch Naming Conventions

All branch names use lowercase kebab-case. The prefix determines which CI
pipeline rules fire and which merge targets are permitted.

| Prefix | Purpose | Merges into | Example |
|---|---|---|---|
| `feat/` | New feature or capability | `develop` | `feat/ogun-virtual-cpu-tick-loop` |
| `fix/` | Bug fix | `develop` | `fix/bootloader-halt-on-abi-mismatch` |
| `docs/` | Documentation only | `develop` | `docs/update-session-manager-readme` |
| `refactor/` | Refactor, no behavior change | `develop` | `refactor/elegua-message-routing` |
| `ci/` | CI/CD pipeline change | `develop` | `ci/add-windows-cross-check` |
| `chore/` | Housekeeping, dep updates, metadata | `develop` | `chore/update-cargo-lock` |
| `p0/` | Critical unplanned fix on `develop` | `develop` (fast-tracked) | `p0/kernel-crash-on-startup` |
| `release/` | Release preparation | `main` then back-merged to `develop` | `release/0.1.0-beta` |
| `security/` | Security vulnerability patch | `main` then back-merged to `develop` | `security/image-signature-bypass` |
| `abi/` | ABI or protocol change | `develop` | `abi/elegua-protocol-v2` |

**Branch naming rules:**

- Lowercase letters, digits, and hyphens only after the prefix slash.
- For changes scoped to a single submodule, prefix the description with the
  submodule name: `feat/ogun-sdk-plugin-loader`.
- For changes spanning multiple submodules, describe the functional area:
  `feat/component-hot-reload`.
- No path separators, dots, or consecutive hyphens.

---

## 9. Per-Repository Branching Rules

All repositories share the permanent branch model and naming scheme. The
following notes record repository-specific variations.

**`ogun` (Umbrella)** — Never contains implementation code. `feat/*` and
`fix/*` branches are for workspace manifest changes and documentation only.
Submodule pointer bumps arrive via `chore/bump-{submodule}-to-{sha}` branches.

**`ogun-runtime`** — Most security-critical repository. Changes to
`ogun-bootloader`, `ogun-image-format`, `ogun-session-manager`, or
`ogun-host-service` on security-critical code paths require two maintainer
approvals. ABI version constant changes always require an `abi/` branch.
`cargo test --workspace` must pass with zero failures before any MR is approved.

**`ogun-sdk`** — ABI stability is an explicit contract within a release series.
No public trait signature or `OGUN_ABI_VERSION` constant changes on `fix/*`
branches. All ABI changes require `abi/` branches.

**`ogun-devices`** — Virtual device implementations must include smoke tests
and a deterministic tick runner test for any feature MR. `ogun-emulator` changes
require the `ENABLE_WINDOWS_BUILD=true` pipeline flag.

**`ogun-os`** — Tauri frontend and Rust backend developed in the same branch;
split MRs not permitted. Changes must pass `npm run tauri dev` on the Windows
runner before merge.

**`ogun-components`** — New component crates require a corresponding
`ogun-component.toml` manifest and a minimum smoke test.

**`ogun-apps`** — App MRs must demonstrate that the app builds, ticks, responds
to IPC, and shuts down cleanly using the `OgunApp` SDK trait lifecycle.

**`ogun-tools`** — `ogun-setup` changes are release-gated; requires maintainer
with Windows installation environment access. `ogun-image-tool` format changes
must be coordinated with `ogun-image-format` via paired MRs.

**`elegua`** — Any change to message schema structs, IPC channel constants, or
the `operator_id`, `workspace_id`, `trace_id`, and `enterprise_id` context
fields requires an `abi/` branch and protocol invariant preservation
documentation.

**`rustydb`** — WAL format, key-value API, or transaction semantic changes must
include durability and crash-consistency tests. Schema migration work must be
coordinated with `ogun-runtime` via paired MRs.

**`ogun-devops`** — Template changes affect every downstream repository. All
changes must be tested by including the branch ref in a downstream pipeline
before merging. Use `ci/` branches for all changes.

---

## 10. Merge Request Standards

### Required in Every MR Description

1. **Summary** — One paragraph describing what changed and why.
2. **Issue reference** — `Closes #NNN` or `Relates to #NNN`.
3. **Affected workspaces and crates** — Every crate that changed.
4. **Checks run locally** — `cargo check --workspace`, `cargo test --workspace`,
   `cargo fmt --all`.
5. **Residual risk** — Known edge cases, temporary workarounds, or follow-up
   issues opened.

### Additional Requirements by Branch Type

| Branch type | Extra requirements |
|---|---|
| `abi/` | ABI checklist fully answered in description; two maintainer approvals |
| `security/` | Two maintainer approvals; confidential MR until published |
| `release/` | Release gate conditions documented and confirmed met |
| Changes to `ogun-bootloader`, `ogun-image-format`, `ogun-session-manager` | Two maintainer approvals |
| Changes to `elegua` message schemas | Protocol invariant preservation statement in description |

### What Reviewers Check

- **Correctness** — Implementation matches the documented specification.
- **Security properties** — All design invariants (I-01 through I-35) preserved.
- **Architecture boundaries** — No layer inversions; host OS calls confined to
  approved boundary crates.
- **Test coverage** — New behaviors are covered by tests.
- **Release scope** — Change stays within the declared release scope.
- **Documentation** — `CHANGELOG.md`, `README.md`, and design docs updated.

---

## 11. Commit Message Convention

```
area: short imperative summary (≤72 characters)

Optional longer explanation of why, not what. Wrap at 72 characters.
Reference design invariants, protocol fields, or security properties affected.

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

---

## 12. Branch Protection Rules

Configure in GitLab under **Settings → Repository → Protected Branches**.

### `main`

| Rule | Setting |
|---|---|
| Allowed to push | No one (merge commits only) |
| Allowed to merge | Maintainers only |
| Require MR before merge | Yes |
| Minimum approvals | 1 (2 for `ogun-runtime`, `elegua`, ABI changes) |
| Require pipeline to succeed | Yes (all stages) |
| Code owner approval | Yes |
| Force push | No |
| Deletions | No |

### `develop`

| Rule | Setting |
|---|---|
| Allowed to push | Developers and Maintainers (chore/submodule commits only) |
| Allowed to merge | Developers and Maintainers via MR |
| Require MR before merge | Yes |
| Minimum approvals | 1 |
| Require pipeline to succeed | Yes (check + test stages minimum) |
| Force push | No |
| Deletions | No |

### `release/*`

| Rule | Setting |
|---|---|
| Allowed to push | Maintainers only |
| Require pipeline to succeed | Yes (full pipeline) |
| Force push | No |

### Tags (`v*`)

| Rule | Setting |
|---|---|
| Allowed to create | Maintainers only (CI bot via deploy token) |
| Deletions | No (tags are immutable) |

---

# Part IV — Workflows and Scenarios

---

## 13. Feature Development Workflow

This is the standard path for new work: features, fixes, refactors, docs
updates, chores, and CI changes.

**Step 1 — Read before branching.** Before starting, read:
- `README.md` in the affected submodule
- `DESIGN.md` at the umbrella level for architecture boundaries
- `CONTRIBUTING.md` for coding standards
- `CHANGELOG.md` for current release scope
- Relevant design invariants (I-01 through I-35) for security-critical work

**Step 2 — Open or reference an issue.** Open a GitLab issue before any
non-trivial branch. Small documentation fixes and typo corrections may skip
this step.

**Step 3 — Create the branch from `develop`.**

```powershell
git checkout develop && git pull origin develop
git checkout -b feat/your-feature-name
```

For submodule work:

```powershell
cd C:\dev\ogun\ogun-sdk
git checkout develop && git pull origin develop
git checkout -b feat/plugin-loader-trait
```

**Step 4 — Implement and test locally.**

```powershell
cargo fmt --all
cargo check --workspace
cargo test --workspace
cargo clippy --workspace --all-targets --all-features -- -D warnings
```

**Step 5 — Commit using the convention.**

```
sdk: add OgunPlugin trait with on_load and on_unload lifecycle hooks
sdk: implement plugin manifest schema validation
sdk: add integration test for plugin loader capability gating
```

**Step 6 — Push and open MR.**

```powershell
git push -u origin feat/plugin-loader-trait
```

Open the MR targeting `develop`. Fill in all required fields (§10).

**Step 7 — CI pipeline runs.** Pipeline order: validate → check → test →
build:debug → audit. All stages must pass green before a reviewer approves.

**Step 8 — Code review.** At least one maintainer approval required. Two for
security-critical code in `ogun-runtime` or `elegua`.

**Step 9 — Merge and delete branch.** Use merge commit (not squash) for feature
branches. Delete the source branch after merge.

**Step 10 — Update submodule pointer (if applicable).**

```powershell
cd C:\dev\ogun
git checkout develop
git submodule update --remote ogun-sdk
git add ogun-sdk
git commit -m "chore: bump ogun-sdk submodule to include plugin loader trait"
git push origin develop
```

---

## 14. Release Workflow

Releases are coordinated from the umbrella repository and propagated to all
submodules in a defined order.

**Phase 1 — Feature freeze.** Announce feature freeze on all active `develop`
branches. Only `fix/*`, `docs/*`, and `p0/*` branches may merge during this
window.

**Phase 2 — Create the release branch.**

```powershell
# Umbrella
cd C:\dev\ogun
git checkout develop && git pull origin develop
git checkout -b release/0.1.0-beta

# Each active submodule
cd C:\dev\ogun\ogun-runtime
git checkout develop && git pull origin develop
git checkout -b release/0.1.0-beta
```

**Phase 3 — Release branch stabilization.** Apply only bug fixes, documentation
updates, and release metadata changes. Update `VERSION.md` and `CHANGELOG.md`
(move `[Unreleased]` entries to the release version section). Run the full CI
pipeline. Verify all release gate conditions from `DESIGN.md`.

**Phase 4 — Run the version tagging job.**

```
# Triggered via GitLab pipeline web UI:
OGUN_VERSION      = "0.1.0"
OGUN_GATE         = "beta"
OGUN_PUSH_BRANCH  = "release/0.1.0-beta"
```

This runs `update_version.py --version 0.1.0 --gate beta --all-files --commit --push release/0.1.0-beta` and produces a `v0.1.0-beta` tag.

**Phase 5 — Merge into `main`.**

```powershell
git checkout main
git merge --no-ff release/0.1.0-beta
git push origin main
```

Triggers the full release pipeline: release build, Tauri bundles, component
`.dll` build, SBOM generation, attestation signing, `.ogpkg` packaging, and
GitLab release creation.

**Phase 6 — Back-merge into `develop`.**

```powershell
git checkout develop
git merge --no-ff release/0.1.0-beta
git push origin develop
```

**Phase 7 — Submodule pointer freeze and umbrella tag.**

```powershell
cd C:\dev\ogun
git checkout main
git submodule update --remote
git add .
git commit -m "release: freeze submodule pointers for v0.1.0-beta"
git tag -a v0.1.0-beta -m "ogun OS 0.1.0-beta — Windows x64 Desktop Edition"
git push origin main --tags
```

**Phase 8 — Delete the release branch.** Delete `release/0.1.0-beta` from all
repositories after successful back-merge.

**Phase 9 — Increment `develop` to next version.**

```
# version:ci job with OGUN_VERSION="0.2.0", OGUN_GATE="alpha", OGUN_MATURITY="dev"
```

---

## 15. Hotfix and Security Workflow

### P0 Hotfix (Non-Security Critical)

A P0 hotfix is an unplanned critical fix that cannot wait for the normal
integration cycle. It targets `develop` directly via a fast-tracked `p0/`
branch.

```powershell
git checkout develop && git pull origin develop
git checkout -b p0/kernel-crash-on-clean-shutdown
# Implement fix; run cargo check, cargo test, cargo fmt
git commit -m "kernel: fix crash on clean shutdown when no active session"
git push -u origin p0/kernel-crash-on-clean-shutdown
```

A single maintainer approval is sufficient during a production incident. The
MR description must document the root cause and confirm no security invariants
are affected.

### Security Vulnerability Patch

Security patches land on `main` first, bypassing `develop`, to prevent
vulnerability details appearing in history before a fix is published.

**Use `SECURITY.md` before creating any branch for a security issue.**

```powershell
git checkout main && git pull origin main
git checkout -b security/image-signature-bypass
# Implement fix; run full test suite on Windows x64
git commit -m "bootloader: fix image signature bypass on malformed section table"
git push -u origin security/image-signature-bypass
```

Open a **confidential MR** targeting `main`. Two maintainer approvals required.
The `security/*` rule triggers the full security audit stage.

After merge into `main`:
1. Tag the security release immediately.
2. Back-merge into `develop`.
3. Publish a security advisory.
4. Update `CHANGELOG.md` under `### Security`.

---

## 16. ABI and Protocol Change Workflow

Any change to a public ABI surface — SDK trait signatures, `OGUN_ABI_VERSION`
constants, Elegua Protocol message schemas, `operator_id` / `workspace_id` /
`trace_id` / `enterprise_id` context fields, Ọpọn Protocol isolation semantics,
image format regions, `KernelBootBundle`, or `CleanShutdownMarker` — must use
an `abi/` branch regardless of scope.

```powershell
git checkout develop && git pull origin develop
git checkout -b abi/elegua-enterprise-id-in-all-messages
```

The CI pipeline detects `abi/*` branches and runs the `abi-change-notice` job,
displaying the mandatory reviewer checklist:

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

All items must be explicitly acknowledged in the MR description. Two maintainer
approvals are always required.

---

## 17. Submodule Synchronization Workflow

### Initializing After Clone

```powershell
git clone git@gitlab.com:ogun-foundation/ogun.git
cd ogun
git submodule update --init --recursive
```

### Updating a Single Submodule Pointer

```powershell
cd C:\dev\ogun
git submodule update --remote ogun-runtime
git add ogun-runtime
git commit -m "chore: bump ogun-runtime submodule to latest develop"
git push origin develop
```

### Cross-Submodule Feature Work (Paired MRs)

When a feature requires changes in multiple submodules:

1. Open MR A in the upstream submodule.
2. Open MR B in the downstream submodule (notes dependency on MR A).
3. Merge MR A. Update the upstream submodule pointer in the umbrella.
4. Merge MR B.

Never merge the downstream MR before the upstream MR is merged and the
submodule pointer is updated.

---

## 18. Rollback Procedures

### Rollback Scenario 1 — Reverting a Bad `develop` Merge

If a merged MR breaks `develop`:

```powershell
# Revert the merge commit on develop
git checkout develop
git revert -m 1 <merge-commit-sha>
git push origin develop
```

Open a `p0/` branch to fix the root cause. The revert commit itself does not
need an MR but must reference the issue.

### Rollback Scenario 2 — Reverting a Bad `main` Merge (Pre-Tag)

If a release branch merge into `main` introduces a critical issue before the
version tag is pushed:

```powershell
git checkout main
git revert -m 1 <merge-commit-sha>
git push origin main
# Do NOT push a version tag until main is clean
```

### Rollback Scenario 3 — Bad Release (Post-Tag, Pre-Public)

If a version tag has been pushed but the GitLab release has not yet been
published:

1. Do not publish the release page.
2. Open a `fix/*` branch targeting `develop`, then cut a new `release/*` branch.
3. The bad tag is left in place but not referenced by any release.
4. A new patch tag (`v0.1.1-rc.1.0`) is created for the corrected release.

Tags are immutable and are never deleted. A superseded tag is documented in
`CHANGELOG.md` under a `### Superseded` section.

### Rollback Scenario 4 — Live Canary Rollback (0.2.0+)

When automatic halt conditions are triggered during a canary rollout:

1. The canary delivery system automatically reverts affected operators to the
   prior stable artifact.
2. The project owner is notified by the observability alert.
3. A P0 issue is opened immediately.
4. The canary rollout is paused at its current tier until the root cause is
   identified and a fix is in RC.

The revert path for a canary operator install: prior stable artifact is
downloaded → image signature verified → `ogun-setup.exe` run in repair mode →
`ogun-desktop.exe` restarted.

### Rollback Scenario 5 — Stable Release Rollback

ogun OS does not provide an in-place downgrade mechanism for stable releases
in 0.1.0. An operator who needs to revert must:

1. Run `ogun-setup.exe /uninstall` to remove the current installation.
2. Download the prior stable release artifact from the GitLab release page.
3. Run the prior `ogun-setup.exe` to install the prior version.

A downgrade path via `ogun-desktop.exe` is a planned feature for 0.2.0.

---

# Part V — Versioning and Release

---

## 19. Versioning System — Full Reference

### 19.1 Version String Anatomy

ogun OS version strings are produced exclusively by `update_version.py`
(stored in `ogun-devops/ogun-scripts/`). No version string is written by hand.

```
{major}.{minor}.{patch}-{gate}.{gate_major}.{gate_minor}-{maturity_suffix}
```

| Segment | Values | Bumped when |
|---|---|---|
| `{major}` | `0`, `1`, … | ABI break, image-format break, security-model break |
| `{minor}` | `0`, `1`, … | New features, new subsystems, new host types |
| `{patch}` | `0`, `1`, … | Bug fixes, security patches, performance improvements |
| `{gate}` | `alpha` `beta` `canary` `rc` `stable` | Audience qualifier; see §20 |
| `{gate_major}` | `1`, `2`, … | Stream number; allows parallel pre-release streams |
| `{gate_minor}` | `0`, `1`, … | Auto-incremented from git tags within a stream |
| `{maturity_suffix}` | `dev-M.N.P` `nightly-YYYYMMDDTHHmmSS` `test-N` `cm-N` | Build iteration qualifier; see §21 |

The `stable` gate produces no gate segment: `{major}.{minor}.{patch}` only.

Representative version progression for the 0.1.0 release series:

```
v0.1.0-alpha.2.4-dev-0.0.4          ← development iteration
v0.1.0-alpha.2.7-nightly-20260609T032842  ← scheduled nightly
v0.1.0-beta                         ← first public beta (short form)
v0.1.0-beta.1.1                     ← beta iteration
v0.1.0-rc.1.0-cm-0                  ← rc + configuration-managed
v0.1.0                              ← stable
```

### 19.2 Gate Counter Resolution

**gate_major** (when `--gate-major` not explicitly passed): inspect existing
tags; take the largest `M` found; if none exist, start at `1`.

**gate_minor**: without maturity — increment highest existing `N` + 1; with
maturity — reuse current highest `N` (do not advance the gate counter for a
maturity build).

**New parallel stream**: pass `--gate-major N` explicitly.

### 19.3 Maturity Suffix Counter Resolution

Maturity suffixes are scoped per `(base_version + gate_segment)`.

| Maturity | Format | Increment rule |
|---|---|---|
| `dev` | `dev-M.N.P` | Patch `P` incremented per call |
| `nightly` | `nightly-YYYYMMDDTHHmmSS` | UTC wall clock; always unique |
| `test` | `test-N` | Integer `N` incremented per call |
| `cm` | `cm-N` | Integer `N` incremented per call |

### 19.4 Git Tag Convention

All git tags: `v` prefix, annotated, immutable, created by `version:tag` CI job.

```powershell
git tag -a v0.1.0-beta -m "ogun OS 0.1.0-beta — Windows x64 Desktop Edition — June 2026"
```

Tag trigger pattern: `^v[0-9]+\.[0-9]+\.[0-9]+`

### 19.5 Files Updated by `update_version.py`

| File | What is updated |
|---|---|
| `VERSION.md` | Every semver string; duplicate `v` prefixes collapsed |
| `Cargo.toml` | `version` key in `[package]` section only |
| `pyproject.toml` | `version` key in `[project]` or `[tool.poetry]` |
| `package.json` | Top-level `"version"` field only |

Use `--recursive` on the umbrella. Run without it on individual submodule
repositories.

### 19.6 Key CLI Flags

```powershell
# Standard alpha CI tag (auto-increments)
python update_version.py --version 0.1.0 --all-files --gate alpha --maturity dev `
  --commit --push develop

# Nightly (timestamped, no commit, no persistent tag)
python update_version.py --version 0.1.0 --all-files --maturity nightly --no-git-tag

# Release candidate (auto-increments rc.N.M)
python update_version.py --version 0.1.0 --all-files --gate rc --commit `
  --push release/0.1.0-rc

# Full stable release
python update_version.py --version 0.1.0 --all-files --gate stable --recursive `
  --commit --push main

# Dry run
python update_version.py --version 0.1.0 --all-files --gate beta --dry-run

# New parallel alpha stream
python update_version.py --version 0.1.0 --all-files --gate alpha --gate-major 2
```

### 19.7 `OGUN_ABI_VERSION` Constants

`OGUN_ABI_VERSION: u32` constants are code constants, not updated by
`update_version.py`. They must be bumped manually on `abi/` branches with two
maintainer approvals. The constant is frozen at `1` for the 0.1.0 release
series.

### 19.8 Script Output Prefixes

| Prefix | Meaning |
|---|---|
| `[updated]` | File written with new version |
| `[no-op]` | File already at target version |
| `[fix-v]` | Duplicate `v` prefixes collapsed |
| `[skip]` | No semver found or no `[package]` section |
| `[dry-run]` | Action previewed; nothing written |
| `[git]` | Output from a git operation |

---

## 20. Release Strategy and Gates

### 20.1 Release Path

```
develop → alpha (internal) → beta (public pre-release)
        → canary (continuous deploy from main, 0.2.0+)
        → rc (release candidate) → stable (public release)
```

Moving backward between gates is not a recognized operation. Regression
discoveries on a beta or RC branch open `fix/*` or `p0/*` branches against
`develop`.

### 20.2 Alpha Gate

**Audience:** Internal; The Ogun Foundation team; trusted contributors.

**Purpose:** Establish foundational runtime correctness; iterate on ABI and
architecture; validate the boot chain on real Windows x64 hardware.

**Version format:** `v0.1.0-alpha.{major}.{minor}[-{maturity}]`

**Exit criteria (advance to beta):**
- All 0.1.0-beta Rust packages build and deliver on Windows x64.
- All four artifact builds pass clean.
- Three-stage boot verification passes on a clean install.
- Full session lifecycle verified end-to-end.
- Design invariants I-01 through I-35 confirmed enforced.
- No P0 blockers outstanding.

**Permitted change surface:** All branch types. ABI changes expected at alpha.

### 20.3 Beta Gate

**Audience:** Public pre-release; external testers; developer partners.

**Version format:** `v0.1.0-beta` (short form for first public release);
`v0.1.0-beta.1.1` for subsequent iterations.

**Entry criteria:** All alpha exit criteria met; security audit clean; SBOM
signed; GitLab release page populated.

**Exit criteria (advance to RC):** No critical/high-severity bugs; all design
invariants hold; full-session-lifecycle test on a clean machine; CHANGELOG
reviewed.

**Permitted change surface:** `fix/*`, `docs/*`, `p0/*`, security patches only.
No new features, no ABI changes.

### 20.4 Canary Gate (0.2.0+)

**Audience:** Opted-in operators; automated integration pipelines.

**Purpose:** Continuous stream of latest `main` state for integration testing.

**Trigger:** Automated on every merge to `main` after 0.1.0 stable release.

**Distribution:** `ogun-artifacts/canary/`; not on public release page; 7-day
retention.

### 20.5 Release Candidate Gate

**Audience:** Final validation partners; organizations evaluating ogun OS.

**Version format:** `v0.1.0-rc.{major}.{minor}`

**Entry criteria:** All beta exit criteria met; SBOM signed and attested;
code-signing certificate applied to all Windows binaries.

**Exit criteria (advance to stable):** Zero critical/high issues; artifact
reproducibility verified across two independent CI runs; CHANGELOG
`[Unreleased]` section empty.

**Permitted change surface:** `fix/*` for critical regressions only.

### 20.6 Stable Gate

**Audience:** General public.

**Version format:** `v{major}.{minor}.{patch}` (no gate suffix)

**Entry criteria:** All RC exit criteria met; minimum 7 days at RC GA with zero
issues; project owner sign-off.

**Post-release actions:**
1. Tag `v0.1.0` on `main` in all submodules and umbrella.
2. Create GitLab release with all artifact links, SBOM, attestation.
3. Back-merge any release-day fixes into `develop`.
4. Bump `develop` to `0.2.0-alpha.1.0-dev-0.0.0`.
5. Archive `release/0.1.0-stable` branch.
6. Publish the security advisory index for 0.1.0.
7. Update public site and README version badge.

**Support window:** 12 months of security patches after the next stable release.

### 20.7 Gate Transition Decision Matrix

| Transition | Decision authority | Required documentation |
|---|---|---|
| alpha → beta | Project owner | DESIGN.md gate checklist, clean security audit |
| beta → RC | Project owner + one maintainer | Beta tracker closed/deferred, SBOM signed |
| RC → stable | Project owner | Zero critical issues 7 days, artifact reproduction verified |
| Any → hotfix | On-call maintainer | P0 issue + root cause in MR description |
| stable → next alpha | Project owner | Scope document committed to `ogun-docs` |

---

## 21. Maturities, Canary Deployments, and Rollout Strategy

### 21.1 Maturity Qualifiers

| Maturity | Suffix | Trigger | Purpose |
|---|---|---|---|
| `dev` | `dev-M.N.P` | `SCHEDULE_TYPE=ci` or manual | Rapid iteration; fine-grained sortable builds |
| `nightly` | `nightly-YYYYMMDDTHHmmSS` | `SCHEDULE_TYPE=nightly` (cron `0 2 * * *`) | Automated daily CI; timestamped; no counter |
| `test` | `test-N` | Manual or QA trigger | Ordered QA builds for structured test cycles |
| `cm` | `cm-N` | Manual only (`version:cm`) | Fully validated artifact; marks CM release input |

### 21.2 `dev` Maturity — Rapid Iteration

The `version:ci` CI job produces alpha + dev builds automatically on the CI
schedule. Subsequent calls always produce the correct next version without
manual bookkeeping.

```
v0.1.0-alpha.2.7-dev-0.0.0  →  v0.1.0-alpha.2.7-dev-0.0.1  →  0.0.2  →  …
```

### 21.3 `nightly` Maturity — Scheduled Builds

Nightly builds: no persistent git commit (`--no-git-tag`); artifacts expire in
7 days. Primary purpose: catch regressions from upstream Rust toolchain changes
or dependency updates. Failing nightly for two consecutive nights → `p0/` branch
investigation.

### 21.4 `cm` Maturity — Configuration-Managed Artifacts

A `cm` artifact has passed all gate conditions, a complete QA test cycle, security
audit, SBOM generation, and attestation signing. It is the input to the RC and
stable release pipeline. The `version:cm` job requires `OGUN_IMAGE_SIGNING_KEY_B64`.

### 21.5 Canary Rollout Tiers (0.2.0+)

Opt-in via `update_channel = "canary"` in `~/.ogun/config/ogun.toml`.

| Tier | Audience | Promotion criteria |
|---|---|---|
| Canary 1 | 1% of opted-in operators | Zero P0 crashes in 24 hours |
| Canary 2 | 10% of opted-in operators | Zero P0 crashes in 48 hours; performance within ±5% of prior stable |
| Canary GA | 100% of opted-in operators | 7-day soak; open feedback period |

**Automatic halt conditions:**
- Crash rate > 0.1% of canary installs per hour
- Boot failure rate > 0.01% of canary installs
- `CleanShutdownMarker` write failure detected in telemetry
- Any security advisory published against a canary dependency

**Rollback:** Automatic revert to prior stable on halt condition. No user
interaction required.

### 21.6 Rollout Monitoring Metrics

| Metric | P0 threshold | Warning threshold |
|---|---|---|
| Boot success rate | < 99.9% | < 99.99% |
| Clean shutdown rate | < 99.5% | < 99.9% |
| Crash rate (crashes/hour/install) | > 0.001 | > 0.0001 |
| Session restore success rate | < 98% | < 99% |
| Image verification pass rate | < 100% | — |

---

# Part VI — Infrastructure and Environments

---

## 22. Sandboxing and Environments

### 22.1 Runtime Isolation Layers

ogun OS enforces isolation at five layers within the runtime.

**Layer 1 — The Ọpọn Protocol (SYS-001).** Separates the ogun OS runtime from
the host OS. Only `ogun-emulator-backend` calls host OS APIs. This invariant
(I-03) is frozen for the 0.1.0 release series.

**Layer 2 — Enterprise isolation.** Ọpọn Protocol also isolates enterprises on
the same host. Cross-enterprise IPC requires explicit capability grants.

**Layer 3 — Capability gating.** All IPC messages are capability-gated. Grants
are assigned at install time, audited by `ogun-security-manager`, and immutable
for the session lifetime.

**Layer 4 — App tier isolation.** Tier 1: Tokio tasks in `ogun-host-service`.
Tier 2–3: OS child processes. Tier 4: runtime-loaded `cdylib` in a supervised
executor.

**Layer 5 — Image verification.** Every boot verifies the signed `.img` through
the three-stage boot verification pipeline. A single failure halts the boot.

### 22.2 CI/CD Execution Environments

**Linux Docker (default).** All `check`, `test`, `audit` jobs, plus the Linux
and cross-compiled Windows x64 release builds, run in `rust:latest` on a Linux
runner.

**Windows native runner.** Tauri application builds require a runner tagged
`windows` + `x64` with Rust stable, Node LTS, WebView2, VS Build Tools 2022,
and Tauri 2 installed.

**Python 3.12 slim.** All `version:*` jobs run in `python:3.12-slim`. No Cargo
access; produces no compiled artifacts.

### 22.3 Environment-to-Artifact Map

| Environment | Produces | Retention |
|---|---|---|
| Linux Docker + debug | `target/debug/` | 1 day |
| Linux Docker + release | `target/release/` (Linux x64 ELF) | 30 days |
| Linux Docker + Windows cross | `target/x86_64-pc-windows-gnu/release/*.exe` `*.dll` | 90 days |
| Windows runner + Tauri | `ogun-desktop` and `ogun-setup` Tauri bundles | 30 days |
| Package stage | `dist/*.ogpkg` | 90 days |
| Release stage | GitLab release + `*.sbom.json` + `*.attestation.json` | 1 year |

### 22.4 Developer Local Sandbox

Developers run the full stack locally on Windows x64 using the command sheets
in §35. For isolated submodule testing, use `cargo test --workspace` within the
submodule. For end-to-end testing, run `ogun-desktop.exe` from the debug build
directory after `cargo build --workspace`.

`ogun-test-features` provides experimental sandbox crates explicitly excluded
from CI requirements and release scope.

### 22.5 Staging Equivalence

ogun OS uses a clean Windows x64 installation as the staging equivalent. All
release gate criteria specify "clean install" to ensure test isolation. Only
CI-built and CI-signed artifacts may be committed to `ogun-artifacts/`.

---

## 23. Environment and Deployment Map

| Environment | Description | Trigger |
|---|---|---|
| **dev** | Local developer machine; debug install | Manual |
| **nightly** | Timestamped artifact from scheduled pipeline on `develop` | `SCHEDULE_TYPE=nightly` on `develop` |
| **alpha** | Internal artifact from alpha gate | `SCHEDULE_TYPE=ci` or `version:ci` job |
| **beta** | Public pre-release artifact | Merge of `release/0.1.0-beta` into `main` and tag |
| **rc** | Release candidate artifact | `version:rc` job on `release/*` |
| **stable** | Public stable release | `version:stable` job after RC validation |

---

## 24. Configuration Management

### 24.1 Configuration Scope

| Scope | Location | Who writes it | Immutability |
|---|---|---|---|
| Image-time | Baked into signed `.img` | CI image builder | Immutable after signing |
| Install-time | `~/.ogun/config/` | `ogun-setup.exe` on first install | Writable by `ogun-desktop.exe` for updates |
| Runtime | Session state + operator preferences | Session manager, operator apps | Writable per-session |

### 24.2 Configuration Files

| File | Managed by | Purpose |
|---|---|---|
| `~/.ogun/config/ogun.toml` | `ogun-setup.exe`, `ogun-desktop.exe` | Root config: `update_channel`, `operator_id`, `enterprise_id`, `install_id`, log levels, telemetry consent |
| `~/.ogun/config/display.toml` | Session manager | Virtual display config |
| `~/.ogun/config/emulation.toml` | Emulator | CPU tick rate, thread pool size, component rate dividers |
| `~/.ogun/config/uefi/vars.bin` | `ogun-uefi` | Virtual BIOS/CMOS variable store; written once at UEFI init |
| `~/.ogun/security/keys/system.pub` | `ogun-setup.exe` | System public key; `0o444` |
| `~/.ogun/security/keys/host.key` | `ogun-setup.exe` | Host key (HKDF-SHA256 derived); `0o400` |
| `~/.ogun/logs/boot.log` | Bootloader | Append-only boot log |
| `~/.ogun/logs/uefi-boot.log` | `ogun-uefi` | Append-only UEFI phase transition log |

Seed configuration templates live in `ogun-config/` and must be updated via MR
to `ogun-config` targeting `develop`.

### 24.3 `VERSION.md` as Configuration

`VERSION.md` at every repository root is the authoritative version record read
by CI validation jobs, the package stage, and `update_version.py`. Rules:

- Must exist. A missing `VERSION.md` fails `validate:version-file`, blocking
  all subsequent stages.
- Contains exactly one semver string.
- Always updated by `update_version.py` — never by hand.

### 24.4 Cargo Workspace Version Inheritance

All workspace member crates should use `version.workspace = true`. They inherit
the version from the umbrella `[workspace.package]` and are updated in a single
`update_version.py` run. Non-inheriting crates require a separate `--path`
invocation.

---

# Part VII — Dependencies and Quality

---

## 25. Submodule and Dependency Management

### 25.1 Adding a New Cargo Dependency

All new dependencies must pass:

1. **License check** — MIT, Apache-2.0, or BSD-2/3-Clause. GPL requires project
   owner approval. `cargo-deny` enforces this in CI.
2. **Security check** — Run `cargo-audit` locally before opening the MR. An
   active advisory blocks the CI `security:audit` job.
3. **Build cost** — A dependency pulling in 50+ transitive crates requires
   explicit justification.
4. **Maintenance health** — Avoid crates unmaintained for 24+ months or marked
   YANKED.
5. **Duplication** — `cargo-deny` bans duplicate crates. Justify or update
   existing before adding a second.

For `ogun-runtime`, `ogun-image-format`, or `elegua`, the MR description must
include an explicit security and license review section.

### 25.2 Updating Dependencies

```powershell
cd C:\dev\ogun\ogun-runtime
git checkout -b chore/update-ring-and-zstd
cargo update -p ring && cargo update -p zstd
cargo test --workspace && cargo audit
git add Cargo.lock
git commit -m "chore: update ring and zstd to latest patch versions"
```

Security advisory updates: 7-day SLA. Non-security updates: batched monthly.

### 25.3 Submodule Pointer Discipline

- `main` in the umbrella always points to tagged commits in each submodule.
- `develop` in the umbrella may point to submodule `develop` tips.
- Pointer updates to `develop` use `chore/bump-{submodule}-to-{sha}` branches.
- A submodule pointer update that fails `cargo metadata --no-deps` is a P0 incident.
- Never use `--remote` on the umbrella's `main` branch.

### 25.4 Paired MR Workflow

For features requiring coordinated changes across multiple submodules:

1. Open MR A (upstream). Open MR B (downstream; notes dependency on A).
2. Merge A → update submodule pointer → merge B.
3. For triple chains: strictly merge A, then B, then C.

### 25.5 Submodule Health Monitoring

The `validate:submodules` CI job verifies every expected submodule is non-empty
on every MR and `main` push. An empty submodule indicates a deploy key or access
token misconfiguration.

---

## 26. Testing Strategy

### 26.1 Testing Philosophy

Three principles govern all testing:

1. **Boot-chain correctness is non-negotiable.** Any PR removing or disabling a
   boot-chain test requires two maintainer approvals.
2. **Tests must be deterministic.** Flaky tests are bugs. A test that fails
   intermittently is fixed or removed; never merged as `allow_failure`.
3. **Tests live next to the code.** Unit tests in `#[cfg(test)]` modules.
   Integration tests in `tests/` directories. E2E tests in `ogun-test-features/`.

### 26.2 Test Pyramid

```
              E2E (ogun-test-features; excluded from release CI)
           Integration (cargo test --all --test '*')
        Unit (cargo test --all --lib)
     Doc tests (cargo test --doc --workspace)
  Static analysis (fmt + clippy + check; runs first, always)
```

### 26.3 Mandatory Security-Critical Tests

The following tests require two-maintainer approval to modify:

| Test | What it verifies |
|---|---|
| `test_image_signature_valid` | Correctly signed image passes all three boot stages |
| `test_image_signature_tampered` | Tampered image halts at Stage 1 |
| `test_abi_version_mismatch` | Wrong `OGUN_ABI_VERSION` halts the boot |
| `test_host_key_derivation` | HKDF-SHA256 produces expected host key |
| `test_clean_shutdown_marker` | `CleanShutdownMarker` written as absolute last act of shutdown |
| `test_crash_recovery_activates` | Missing `CleanShutdownMarker` activates crash recovery |
| `test_ipc_capability_gate_enforced` | IPC from non-capable app is rejected |
| `test_opqn_isolation_cross_enterprise` | Cross-enterprise IPC without grant is rejected |

### 26.4 Coverage Targets

| Repository | Minimum line coverage |
|---|---|
| `ogun-bootloader` | 85% |
| `ogun-image-format` | 90% |
| `ogun-session-manager` | 80% |
| `elegua` | 80% |
| `ogun-sdk` public API | 75% |

Coverage is a guide, not a gate. Mandatory security tests take precedence.

### 26.5 Test Execution on MRs

Order on every MR pipeline:

1. `validate:workspace` — cargo metadata resolves
2. `fmt` — `cargo fmt --all -- --check`
3. `clippy` — `cargo clippy --workspace --all-targets --all-features -- -D warnings`
4. `check:workspace` — `cargo check --workspace`
5. `test:workspace` — `cargo test --workspace --verbose -- --show-output`
6. `security:audit` — `cargo audit`
7. `build:debug` — after `test:workspace`

---

# Part VIII — CI/CD Operations

---

## 27. CI/CD Environments and Strategies

### 27.1 CI/CD Architecture

The pipeline is built on GitLab CI with a shared template library in
`ogun-devops/ogun-cicd/`. All child repositories include templates via
`include:` referencing `main` of `ogun-devops`. The template library is the
single source of truth for all pipeline behavior.

| File | Stage | Responsibility |
|---|---|---|
| `configure.yml` | (global) | Variables, Docker image, cache, branch rules, runner tags, workflow |
| `validate.yml` | `validate` | Workspace metadata, submodule health, `VERSION.md` sanity |
| `check.yml` | `check` | rustfmt, clippy, cargo check, ABI change notice |
| `test.yml` | `test` | Workspace, unit, integration, doc, coverage, nightly toolchain |
| `build.yml` | `build` | Debug, release Linux, cross Windows, Tauri desktop + setup, component libs, nightly build |
| `sast.yml` | `audit` | cargo-audit, cargo-deny, supply-chain, SBOM, SonarQube, weekly audit |
| `package.yml` | `package` + `pages` | .ogpkg packaging, Tauri bundle packaging, rustdoc → GitLab Pages |
| `deploy.yml` | `release` | GitLab release creation, build attestation |
| `version.yml` | `version` | Version bumping, git tagging, push via `update_version.py` |

### 27.2 Stage Execution Order

```
validate → check → test → build → audit → package → pages → version → release
```

### 27.3 Pipeline Trigger Matrix

| Trigger | Branch / condition | Stages |
|---|---|---|
| MR (any branch) | Any | validate, check, test, build:debug |
| Push to `develop` | Commit on develop | validate, check, test, build:debug, audit |
| Push to `main` | Commit on main | validate, check, test, build:release, build:windows-cross, audit, package, pages |
| Push to `release/*` | Release branch commit | validate, check, test, build:release, audit |
| Semver tag `v*.*.*` | Tag push | All stages including build:tauri, package, release |
| Schedule `nightly` | `SCHEDULE_TYPE=nightly` | build:nightly, test:nightly, version:nightly |
| Schedule `security` | `SCHEDULE_TYPE=security` | audit:weekly |
| Schedule `version` | `SCHEDULE_TYPE=version` | version:tag |
| Web / API trigger | `CI_PIPELINE_SOURCE=web/api` | validate, check, test, build:debug, build:release (+ Windows if `ENABLE_WINDOWS_BUILD=true`) |
| Web / API (version) | `version:tag` manual | version:tag only |
| Web / API (preview) | `version:preview` | version:preview (dry-run) |

### 27.4 Global CI Variables

| Variable | Default | Purpose |
|---|---|---|
| `CARGO_HOME` | `$CI_PROJECT_DIR/.cargo` | Cargo registry and cache |
| `CARGO_INCREMENTAL` | `0` | Disable incremental compilation for reproducibility |
| `RUSTFLAGS` | `-D warnings` | Treat all compiler warnings as errors |
| `RUST_BACKTRACE` | `1` | Enable backtraces in test output |
| `CARGO_TERM_COLOR` | `always` | Colored Cargo output in CI logs |
| `GIT_DEPTH` | `0` | Full clone for cargo-audit tag inspection |
| `OGUN_MAIN_BRANCH` | `main` | Branch name in pipeline rules |
| `OGUN_DEV_BRANCH` | `develop` | Branch name in pipeline rules |
| `VERSION_SCRIPT_URL` | (ogun-devops raw URL) | Source URL for `update_version.py` |
| `ARTIFACT_DIR` | `$CI_PROJECT_DIR/artifacts` | SBOM and attestation output directory |

Optional per-repository overrides:

| Variable | Repo | Effect |
|---|---|---|
| `ENABLE_WINDOWS_BUILD` | `ogun-os`, `ogun-devices` | Activates Windows cross-compiled build |
| `ENABLE_WINDOWS_CHECK` | `ogun-runtime` | Activates Windows `cargo check` on Linux runner |
| `ENABLE_SBOM` | `ogun-runtime`, `ogun-os` | Activates SBOM generation |
| `ENABLE_COVERAGE` | Any | Activates `cargo-llvm-cov` report |
| `ENABLE_SONAR` | Selected | Activates SonarQube scan |

### 27.5 Security-Critical Pipeline Overrides

| Override | Default | Security-critical repos override |
|---|---|---|
| `security:audit` `allow_failure` | `true` | `false` |
| Minimum approvals on `main` | 1 | 2 |
| `ENABLE_SBOM` | `false` | `true` |
| `ENABLE_WINDOWS_CHECK` | `false` | `true` |

### 27.6 `version.yml` Job Reference

| Job | Trigger | Effect |
|---|---|---|
| `version:tag` | Manual or `SCHEDULE_TYPE=version` | Bump files, commit, tag, push |
| `version:preview` | Web/API | Dry-run only |
| `version:nightly` | `SCHEDULE_TYPE=nightly` | Nightly timestamp; no commit, no persistent tag |
| `version:ci` | `SCHEDULE_TYPE=ci` or API | Alpha + dev; auto-increments; commits and pushes |
| `version:cm` | Manual or `SCHEDULE_TYPE=cm` | CM maturity; commits and pushes |
| `version:rc` | Manual or `SCHEDULE_TYPE=rc` | RC gate; auto-increments gate-minor |
| `version:stable` | Manual or `SCHEDULE_TYPE=stable` | Stable gate; no gate suffix |

All version jobs require `OGUN_DEVOPS_DEPLOY_TOKEN`.

### 27.7 Onboarding a New Repository to CI

1. Create the GitLab repository under `ogun-foundation/`.
2. Add as a submodule to the umbrella.
3. Create `.gitlab-ci.yml` with `include:` directives for the relevant templates.
4. Add `VERSION.md` at the repository root.
5. Group-level CI/CD variables are inherited automatically.
6. Set repo-specific overrides at the project level.
7. Add the repository to `EXPECTED_SUBMODULES` in the umbrella CI.
8. Open an MR in `ogun-devops` to document any non-standard pipeline requirements.

---

## 28. CI/CD Pipeline Stages

### `validate` Stage

Runs before any compilation; fastest and cheapest gate.

| Job | Checks |
|---|---|
| `validate:workspace` | `cargo metadata --no-deps` resolves all workspace members |
| `validate:submodules` | Every expected submodule exists and is non-empty |
| `validate:version-file` | `VERSION.md` exists and contains a valid semver |

### `check` Stage

Format and lint before compilation.

| Job | Checks |
|---|---|
| `fmt` | `cargo fmt --all -- --check` |
| `clippy` | `cargo clippy --workspace --all-targets --all-features -- -D warnings` |
| `check:workspace` | `cargo check --workspace --all-targets --all-features` |
| `abi-change-notice` | Reviewer checklist for `abi/*` branches (`allow_failure: true`) |

### `test` Stage

| Job | Runs |
|---|---|
| `test:workspace` | `cargo test --workspace --verbose -- --show-output` |
| Unit tests | `cargo test --all --lib` |
| Integration tests | `cargo test --all --test '*'` |
| Doc tests | `cargo test --doc --workspace` |
| Coverage | `cargo llvm-cov --workspace --lcov` (when `ENABLE_COVERAGE=true`) |
| `nightly:build` | `cargo +nightly build/test --workspace --all-features` (scheduled) |

### `build` Stage

| Job | Produces |
|---|---|
| `build:debug` | Debug build (Linux Docker); expires 1 day |
| `build:release` | Release build (Linux x64); expires 30 days |
| `build:release:windows` | Cross-compiled Windows x64 (`x86_64-pc-windows-gnu`); 90 days |
| `build:tauri:desktop` | `ogun-desktop` Tauri bundle (Windows native runner); 30 days |
| `build:tauri:setup` | `ogun-setup` Tauri bundle (Windows native runner); 30 days |
| `build:components` | `ogun-components` `.dll`/`.so` libraries; 30 days |

### `audit` Stage

| Job | Checks |
|---|---|
| `security:audit` | `cargo-audit` vs. RustSec advisory database |
| `dependency:deny` | `cargo-deny` — licenses, duplicates, source policy |
| Supply-chain check | Vendored sources match `Cargo.lock` (`security/*` and `main`) |
| SBOM generation | CycloneDX and SPDX formats (when `ENABLE_SBOM=true`) |
| `sonarqube` | SonarQube static analysis (when `ENABLE_SONAR=true`) |
| `weekly:audit` | Scheduled `cargo audit --deny warnings` |

### `package` Stage

| Job | Packages |
|---|---|
| `.job_package_app` | Any binary into a versioned `.ogpkg` archive |
| `.job_package_app_windows` | Windows binary into `.ogpkg` |
| `.job_package_tauri_bundle` | Tauri bundle directory into `.ogpkg` |

### `pages` Stage

Builds unified rustdoc (`cargo doc --workspace --no-deps --document-private-items`)
and publishes to GitLab Pages. Triggers on `main` merges.

### `version` Stage

See §27.6 for the full job reference.

### `release` Stage

| Job | Creates |
|---|---|
| `.job_release_crate` | GitLab release for library/crate repos |
| `.job_release_desktop` | GitLab release for `ogun-os` with Tauri bundle links |
| `.job_attest` | Signs the SBOM; creates build attestation artifact |

Triggers: semver tags matching `v[0-9]+.[0-9]+.[0-9]+`.

---

## 29. Scheduled Pipeline Jobs

Configure in GitLab under **CI/CD → Schedules**.

| Schedule | Repository | `SCHEDULE_TYPE` | Cron | Purpose |
|---|---|---|---|---|
| Nightly build | `ogun` umbrella | `nightly` | `0 2 * * *` | Timestamped release artifact; nightly Rust toolchain regression check |
| Weekly security audit | All Rust repos | `security` | `0 6 * * 1` | `cargo audit --deny warnings`; dependency update dry-run |
| Version CI tag | Active submodules | `ci` | On demand | Alpha + dev CI tag for integration testing |
| Version stable | `ogun` umbrella | `stable` | Manual | Stable release tagging |

---

## 30. Repository-Specific CI Notes

### `ogun-devops` and Shared Templates

When a child repo's pipeline breaks after an `ogun-devops` update, check
`configure.yml` global variables first: `CARGO_HOME`, `RUSTFLAGS`,
`CARGO_INCREMENTAL`, and `OGUN_MAIN_BRANCH`.

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

Mirroring is one-way from GitLab. Never open pull requests or push directly to
the GitHub or Codeberg mirrors. All contributions go through GitLab MRs.

### `ogun-test-features`

Explicitly excluded from release scope. Branches are not required to follow
the standard naming convention or maintain CI green status. Any prototype
promoted into a production workspace inherits full CI requirements from that
point forward.

### CI/CD Variable Requirements

Group-level variables (inherited by all child repositories):

| Variable | Scope | Purpose |
|---|---|---|
| `OGUN_DEVOPS_DEPLOY_TOKEN` | Protected, Masked | Fetches `update_version.py` from `ogun-devops` |
| `OGUN_IMAGE_SIGNING_KEY_B64` | Protected, Masked | Image signing key for attestation |
| `SONAR_HOST_URL` | Protected | SonarQube host (if `ENABLE_SONAR=true`) |
| `SONAR_TOKEN` | Protected, Masked | SonarQube authentication token |

---

# Part IX — Lifecycle and Maintenance

---

## 31. Pipeline Lifecycle and Maintenance

### 31.1 Template Update Process

Changes to `ogun-devops/ogun-cicd/` templates affect every downstream repository.
The update process is:

1. Create a `ci/` branch in `ogun-devops`.
2. Test the changed templates by including the branch ref in a downstream repo's
   pipeline using the `ref:` override in that repo's `.gitlab-ci.yml`:
   ```yaml
   include:
     - project: 'ogun-foundation/ogun-devops'
       ref: ci/your-template-change
       file: 'ogun-cicd/check.yml'
   ```
3. Verify the downstream pipeline passes with the branch ref.
4. Open an MR in `ogun-devops` and merge.
5. Monitor the first several downstream pipelines that pick up the new `main`
   of `ogun-devops` and confirm no regressions.

### 31.2 Runner Maintenance

**Linux Docker runners** are maintained by GitLab.com infrastructure. When the
`rust:latest` image is updated, the first pipeline run that pulls the new image
may produce different output (new lint warnings, new Rust edition changes). If
the `RUSTFLAGS=-D warnings` global flag causes new failures, open a `ci/`
branch to address them within 48 hours.

**Windows native runners** are self-managed. Required maintenance activities:

- Rust toolchain update: run `rustup update` monthly.
- Node LTS update: update when a new Node LTS is released.
- WebView2 update: Windows Update handles this automatically.
- VS Build Tools update: run annually or when new Windows SDK versions are
  required by a Tauri release.
- GitLab Runner update: follow the GitLab Runner release cadence.

Runner health is monitored by the CI/CD Operator. A runner that fails to accept
jobs for more than 30 minutes is investigated immediately. A runner offline for
more than 2 hours blocks the entire release pipeline and is treated as a P0
incident for CI/CD operations.

### 31.3 Secret Rotation

| Secret | Rotation schedule | Rotation procedure |
|---|---|---|
| `OGUN_IMAGE_SIGNING_KEY_B64` | Annually or on suspected compromise | Generate new ed25519 keypair; update CI variable; re-sign all in-flight artifacts; update `ogun-docs` key registry |
| `OGUN_DEVOPS_DEPLOY_TOKEN` | Every 6 months | Create new deploy token in GitLab; update CI variable; revoke old token |
| `SONAR_TOKEN` | Every 12 months | Regenerate in SonarQube; update CI variable |

On suspected compromise of `OGUN_IMAGE_SIGNING_KEY_B64`, treat as a P0 security
incident: rotate immediately, revoke all artifacts signed with the compromised
key, publish a security advisory, and re-release the current stable with new
signatures.

### 31.4 Dependency Update Cadence

| Category | SLA | Process |
|---|---|---|
| Critical security advisory (CVSS ≥ 9.0) | 24 hours | Emergency patch; `security/` branch; bypass normal cadence |
| High security advisory (CVSS 7.0–8.9) | 7 days | `fix/` or `security/` branch; fast-track review |
| Medium advisory / non-security patch | Monthly batch | `chore/update-deps` branch; standard review |
| Major version update | Evaluated per-dependency | Requires explicit justification MR; may require ABI review |

### 31.5 Pipeline Observability

GitLab provides native pipeline observability through pipeline job logs,
artifact download counts, and the pipeline analytics dashboard. For the ogun
project, additional observability signals:

- **Nightly build duration trend.** If nightly builds consistently exceed 30
  minutes, investigate cache invalidation patterns and consider splitting the
  workspace.
- **Test flakiness rate.** Any test that fails on more than 1% of runs without
  a code change is a flaky test and must be fixed or removed.
- **Cache hit rate.** A consistently low cache hit rate on `Cargo.lock`-keyed
  caches indicates frequent dependency updates or misconfigured cache policy.
- **Artifact size trend.** Artifact sizes are monitored over releases. A
  sudden increase in `.ogpkg` size is investigated before the artifact is
  published.

---

## 32. Observability and Monitoring

### 32.1 Build and Pipeline Observability

GitLab pipeline dashboards and job logs are the primary observability tools.
Key signals monitored by the CI/CD Operator:

| Signal | Normal range | Alert threshold |
|---|---|---|
| MR pipeline duration (check + test) | 8–12 minutes | > 20 minutes |
| Full release pipeline duration | 25–40 minutes | > 60 minutes |
| Nightly build success rate (rolling 30 days) | ≥ 95% | < 90% |
| Weekly security audit pass rate | 100% | Any failure |
| Cache hit rate on `Cargo.lock` key | ≥ 70% | < 50% |

### 32.2 Runtime Observability (Canary, 0.2.0+)

ogun OS runtime telemetry is forwarded from opted-in operator installations to
The Ogun Foundation's observability infrastructure via `ogun-system-manager`.
Telemetry is opt-in per operator; operators who have not opted in do not
contribute data.

Key runtime signals:

| Signal | Where captured | Retention |
|---|---|---|
| Boot success/failure events | `ogun-bootloader` telemetry | 90 days |
| Session start/end events | `ogun-session-manager` telemetry | 90 days |
| Clean shutdown marker writes | `ogun-session-manager` telemetry | 90 days |
| Crash reports | `ogun-system-manager` crash reporter | 90 days |
| Image verification pass/fail | `ogun-bootloader` telemetry | 90 days |

### 32.3 Security Observability

The weekly `security:audit` scheduled job produces `cargo-audit-report.json`
and `dep-update-dry-run.txt` artifacts. These are reviewed by the CI/CD Operator
and any findings with CVSS ≥ 7.0 are escalated to the project owner within 24
hours of the report artifact becoming available.

The `ogun-artifacts/` submodule contains SBOM files for every release. SBOM
files are immutable post-release and serve as the forensic record for any future
supply-chain investigation.

---

# Part X — Risk and Governance

---

## 33. Risks and Mitigations

### 33.1 Risk Register

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R-01 | Single project owner creates key-person dependency | Medium | High | Document all signing key procedures; rotate keys on a schedule; onboard a second trusted maintainer with full release authority |
| R-02 | Windows native runner goes offline during a release | Medium | High | Maintain a backup Windows runner configuration; document manual Tauri build procedure for emergency use |
| R-03 | `OGUN_IMAGE_SIGNING_KEY_B64` compromise | Low | Critical | Rotate immediately; treat as P0 security incident; re-sign and re-release all current artifacts |
| R-04 | `ogun-devops` template change breaks all downstream pipelines | Medium | High | Always test template changes with a `ref:` override in a downstream pipeline before merging |
| R-05 | Critical RustSec advisory in a transitive dependency | Medium | High | 7-day SLA for high advisories; `cargo-audit` runs on every MR and weekly schedule |
| R-06 | Canary rollout causes data loss or corruption in session state | Low | Critical | Three-stage boot verification; `CleanShutdownMarker` protocol; canary halt conditions with < 0.01% boot failure threshold |
| R-07 | Supply-chain attack via malicious Cargo crate update | Low | Critical | `cargo-deny` source policy; `Cargo.lock` vendoring verification on `security/*` and `main`; SBOM records exact dependency graph |
| R-08 | ABI break introduced without `abi/` branch workflow | Low | High | Mandatory ABI checklist enforced by `abi-change-notice` CI job; two-maintainer review |
| R-09 | Submodule pointer drift causes `cargo metadata` failure | Medium | Medium | `validate:submodules` CI job on every MR; `validate:workspace` confirms metadata resolution |
| R-10 | nightly Rust toolchain regression blocks releases | Medium | Low | `nightly:build` has `allow_failure: true`; stable toolchain is never nightly; 48-hour investigation window |
| R-11 | GitLab.com platform outage | Low | High | No single-platform mitigation in 0.1.0; GitHub/Codeberg mirrors preserve code but not CI state |
| R-12 | Tauri or WebView2 upstream breaking change | Low | Medium | Pin Tauri to a tested minor version; evaluate upgrades on `ci/` branch before adopting |
| R-13 | Developer commits directly to `main` | Very Low | High | Branch protection rules block all direct pushes; GitLab enforces this at the platform level |
| R-14 | Release artifact published without SBOM/attestation | Low | Medium | `job_attest` blocks the `release` stage if `OGUN_IMAGE_SIGNING_KEY_B64` is absent |
| R-15 | Adoption friction from complex multi-step release workflow | Medium | Medium | Document all steps in this CONOPS; automate all repeatable steps in CI; provide Quick Reference (§35) |

### 33.2 Legacy System Constraints

ogun OS has no legacy codebase dependencies. The primary constraints are:

**Windows-only Tauri builds.** Tauri 2 desktop application bundles require a
native Windows runner. Cross-compilation from Linux produces Rust binaries but
not the Tauri application bundle. This creates a hard dependency on the
Windows runner for every release build.

**Monorepo scale.** 122+ Cargo manifests across 20+ repositories means that
cache invalidation events (e.g., a change to `ogun-types`) can trigger
cascading rebuilds across the full workspace. The `.cargo_cache` key-on-Cargo.lock
strategy mitigates this but does not eliminate it.

**Cargo.lock dependency on git tags.** `update_version.py`'s counter resolution
logic reads all existing git tags. In very large repositories with hundreds of
tags, this becomes slow. `jaku` (the planned Rust replacement for
`update_version.py`) will address this.

### 33.3 Compliance Considerations

**GPL-3.0 licensing.** ogun OS is GPL-3.0 licensed. `cargo-deny` enforces that
all Cargo dependencies are MIT, Apache-2.0, or BSD-licensed. Any GPL-licensed
dependency requires explicit project owner approval and is reviewed for
compatibility.

**Code signing.** Windows authenticode signing of release binaries is required
for production distribution. The `OGUN_IMAGE_SIGNING_KEY_B64` CI variable holds
the signing key. Without this variable, the `release` stage fails intentionally.

**SBOM requirements.** The SBOM artifacts (CycloneDX and SPDX) generated for
each release provide the dependency transparency record required for supply-chain
security compliance. These are immutable post-release.

---

## 34. Incident Response and Escalation

### 34.1 Incident Severity Levels

| Level | Definition | Response time | Resolution target |
|---|---|---|---|
| P0 | `develop` broken; release pipeline blocked; security breach | Immediate (< 30 minutes to first response) | < 4 hours to fix merged |
| P1 | Single CI job consistently failing; Windows runner offline; nightly failure for 2+ days | < 2 hours | < 24 hours |
| P2 | Non-critical test flakiness; cache hit rate degradation; slow pipeline | < 1 working day | < 1 week |
| P3 | Documentation gap; cosmetic pipeline output issue | Next sprint | Backlog-managed |

### 34.2 P0 Response Procedure

1. **Detection.** P0 incidents are detected by: failed nightly pipeline
   notification, CI/CD Operator monitoring, maintainer discovery on MR, or
   security advisory report.
2. **Declaration.** The detecting party opens a GitLab issue titled `P0: {brief
   description}` and assigns it to the project owner and the CI/CD Operator.
3. **War room.** The project owner, CI/CD Operator, and at least one maintainer
   convene immediately.
4. **Containment.** If the P0 is a broken `develop` branch: the responsible MR
   is reverted immediately. If it is a security breach: the affected CI variable
   or artifact is revoked immediately.
5. **Fix.** A `p0/` or `security/` branch is opened. Standard MR process with
   expedited single-maintainer approval (two for security).
6. **Resolution.** Fix is merged. For security P0s, a security advisory is
   published.
7. **Post-mortem.** A post-mortem document is committed to `ogun-docs/incidents/`
   within 5 working days of resolution. It records: timeline, root cause,
   impact, fix, and preventive measures added.

### 34.3 Escalation Path

```
Developer discovers issue
    ↓
Opens GitLab issue (P0/P1 label)
    ↓
Notifies CI/CD Operator and nearest Maintainer
    ↓
CI/CD Operator + Maintainer assess severity
    ↓
P0 / security breach → Project Owner immediate notification
P1 → Project Owner notified within 2 hours
P2/P3 → Standard backlog; triaged at next working session
```

---

# Appendices

---

## 35. Quick Reference Command Sheets

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
cd C:\dev\ogun\ogun-runtime  && cargo check --workspace
cd C:\dev\ogun\ogun-sdk      && cargo check --workspace
cd C:\dev\ogun\ogun-devices  && cargo check --workspace
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
# Trigger version:tag job via GitLab pipeline UI:
OGUN_VERSION      = "0.1.0"
OGUN_GATE         = "beta"
OGUN_PUSH_BRANCH  = "release/0.1.0-beta"

# Or via CLI:
python ./update_version.py `
  --version 0.1.0 `
  --gate beta `
  --all-files `
  --commit `
  --recursive `
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

### ABI Change Checklist (for `abi/` branch MR descriptions)

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

---

## 36. Glossary

| Term | Definition |
|---|---|
| **ABI** | Application Binary Interface. The binary contract between compiled components. In ogun OS, governed by `OGUN_ABI_VERSION: u32` constants in each crate. |
| **Artifact** | A file produced by the CI pipeline: a compiled binary, `.ogpkg` archive, SBOM, attestation document, or Tauri application bundle. |
| **Attestation** | A signed document asserting the provenance and integrity of a release artifact, produced by `job_attest` in `deploy.yml`. |
| **Boot chain** | The ordered sequence from `ogun-desktop.exe` → `ogun-emulator` → virtual hardware → `ogun-uefi` → `ogun-bootloader` → `ogun-kernel-core` → `ogun-host-service` → `ogun-session-manager` → user apps. |
| **canary** | A release gate for continuous-deployment builds pushed from `main` to a small fraction of opted-in operators. |
| **CleanShutdownMarker** | A file written as the absolute last act of an ogun OS session shutdown. Its absence at boot activates crash recovery. |
| **cm** | Configuration-managed. A maturity qualifier marking the most mature artifact type: one that has passed all gates, test cycles, security audit, SBOM generation, and attestation. |
| **CONOPS** | Concept of Operations. This document. Describes how the ogun DevOps system is built, operated, and maintained. |
| **dev** | A maturity qualifier for rapid development iteration builds. Appends `dev-M.N.P` to the version string. |
| **Elegua Protocol** | The typed, capability-gated inter-process communication protocol used by all ogun OS components. |
| **gate** | A release audience qualifier in the version string: `alpha`, `beta`, `canary`, `rc`, or `stable`. |
| **gate_major** | The first counter component of the gate segment (`gate.{gate_major}.{gate_minor}`). Identifies a parallel pre-release stream. |
| **gate_minor** | The second counter component of the gate segment. Auto-incremented per release within a stream. |
| **host** | A running ogun OS instance. A complete self-contained runtime comprising bootloader, kernel core, and session manager. |
| **KernelBootBundle** | The data structure assembled by `ogun-bootloader` and handed off to `ogun-kernel-core` to initialize the kernel. |
| **maturity** | A build iteration qualifier appended after the gate segment: `dev`, `nightly`, `test`, or `cm`. |
| **MR** | Merge Request. GitLab's equivalent of a pull request. |
| **nightly** | A maturity qualifier for automated daily CI builds. Appends a UTC timestamp. |
| **OGUN_ABI_VERSION** | A `u32` constant in each ogun crate that encodes the current ABI version. Read at boot to verify compatibility. |
| **ogpkg** | The `.ogpkg` file format. A compressed tarball of a binary or Tauri bundle, versioned and named per the ogun artifact naming convention. |
| **Ọpọn Protocol (SYS-001)** | The isolation protocol that restricts direct host OS API calls to `ogun-emulator-backend` only. |
| **ogun-devops** | The repository containing shared CI/CD YAML templates and `update_version.py`. |
| **P0** | Priority 0. The highest severity incident level. Requires immediate response and < 4-hour resolution. |
| **rc** | Release candidate. A gate for near-final builds undergoing validation before stable promotion. |
| **SBOM** | Software Bill of Materials. A structured list of all dependencies in a build, in CycloneDX and SPDX formats. |
| **stable** | The final promoted release gate. Produces a version string with no gate or maturity suffix. |
| **submodule** | A git submodule. Each ogun workspace component is a separate GitLab repository referenced by the umbrella `ogun` repo as a submodule. |
| **test** | A maturity qualifier for QA builds. Appends a monotonically incrementing integer. |
| **umbrella** | The root `ogun` repository that declares the virtual Cargo workspace and hosts all submodule references. |
| **update_version.py** | The Python script stored in `ogun-devops/ogun-scripts/` that produces and records all version strings across the ogun repository graph. |
| **VERSION.md** | The authoritative version record file at the root of every repository. Always updated by `update_version.py`. |

---

*ogun OS · Project Ogún · 2026*  
*Owner: Dominic Eaton (@eatondo)*  
*Document: CONOPS.md*  
*Supersedes: WORKFLOW.md*  
*Licensed under GNU General Public License v3.0*
