# Governance

ogun OS is currently governed as an early-stage founder-led open-source project.
The goal of governance at this stage is to keep architecture coherent, protect
security invariants, and make contribution decisions predictable while the
runtime moves toward the first public beta.

## Project Steward

Primary steward:

- Dominic Eaton (`@eatondo`)

The project steward has final responsibility for release scope, security
decisions, repository structure, licensing, and architectural direction until a
larger maintainer group is formally appointed.

## Maintainer Roles

As the project grows, maintainers may be assigned by area:

| Role | Scope |
|---|---|
| Runtime maintainer | Bootloader, image format, kernel, session manager, storage, and subsystem runtime. |
| Device maintainer | Emulator, virtual UEFI, virtual CPU, virtual monitor, virtual host platform, and network adapter. |
| SDK maintainer | ABI contracts, component traits, manifests, and examples. |
| Components maintainer | OS apps, utility apps, hosts, drivers, and services. |
| Apps maintainer | Tier-4 user applications and personal enterprise workflows. |
| Tools maintainer | Setup, image tooling, packaging, repair, update, and release tooling. |
| Docs maintainer | Product specs, architecture docs, release notes, and support docs. |
| Security maintainer | Vulnerability triage, advisories, security review, and disclosure coordination. |

One person may hold multiple roles. Maintainers are expected to review within
their scope and escalate cross-cutting changes.

## Decision Model

Most decisions are made by lazy consensus:

1. A contributor opens an issue or merge request.
2. Maintainers review for correctness, security, scope, and maintainability.
3. If no blocking objection remains, the change can merge.

The project steward makes final calls for:

- Release scope and release dates.
- Security advisories and embargo timing.
- Licensing and third-party dependency policy.
- Architecture invariants.
- Public project positioning.
- Maintainer appointment or removal.

## Request for Comments

Use an RFC-style issue or document for changes that affect:

- Boot flow, image layout, or installer/update behavior.
- ABI, SDK traits, manifests, or component loading.
- Security policy, Opon enforcement, capabilities, audit logs, or key material.
- IPC routing, Elegua message shape, gateways, or external ingress.
- Workspace, enterprise, session, or identity models.
- Repository layout, release artifacts, or supported platforms.
- User-facing app tier structure.

An RFC should include motivation, design, compatibility impact, security impact,
test plan, rollout plan, and alternatives considered.

## Merge Authority

A merge request may be merged when:

- The relevant maintainer or steward approves it.
- Required checks pass, or known check blockers are documented.
- Security-sensitive changes have had appropriate review.
- Documentation and changelog updates are included when needed.

The steward may fast-track urgent security fixes or release-blocking fixes.

## Release Governance

Release readiness is based on:

- Tagged source state for each affected workspace.
- Passing or explicitly waived checks.
- Updated `CHANGELOG.md`.
- Current release docs under `ogun-docs/`.
- Built and verified artifacts under `ogun-artifacts/`.
- Checksums and signature metadata for each release artifact.
- Known limitations documented before publication.

Pre-release labels such as alpha, beta, and release candidate must describe the
actual stability and support level of the artifacts.

## Security Governance

Security reports follow `SECURITY.md`.

The security maintainer or steward coordinates:

- Private triage.
- Severity assessment.
- Fix ownership.
- Advisory content.
- Disclosure timing.
- Reporter credit.

Security fixes may be developed privately until disclosure is safe.

## Conflict Resolution

If contributors disagree:

1. Try to resolve the issue in the merge request with concrete technical
   evidence.
2. Move broad design questions to an RFC-style issue.
3. Ask the relevant maintainer for a recommendation.
4. The project steward makes the final decision if consensus does not emerge.

Personal attacks, harassment, or bad-faith conduct are handled under
`CODE_OF_CONDUCT.md`.

## Changes to Governance

This document can be changed by merge request. Material changes require steward
approval until a broader governing body exists.
