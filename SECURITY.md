# Security Policy

ogun OS includes boot verification, signed images, capability-gated IPC,
workspace and enterprise isolation, virtual devices, update tooling, and local
installation state. Security reports are welcome and should be handled
privately until a fix or mitigation is available.

## Supported Versions

| Version | Support status |
|---|---|
| `0.1.0-beta` | Planned first public beta; security fixes accepted once released. |
| `0.1.0-alpha` | Development preview; best-effort fixes only. |
| Older internal builds | Not supported. |

The current repository is alpha-stage source. Do not treat development builds,
unsigned artifacts, or locally staged files as production releases.

## Private Disclosure

Please do not open a public issue for a suspected vulnerability.

Preferred disclosure path:

1. Email the maintainer listed in `GOVERNANCE.md`, or use the private security
   reporting feature on the project host if available.
2. Include enough detail to reproduce or reason about the issue.
3. Wait for acknowledgement before publishing details.

If no private project-host reporting channel is available, email Dominic Eaton
(`@eatondo`) using the contact route listed on the project profile or website.

## What to Include

Helpful reports include:

- Affected workspace, crate, component, app, tool, or artifact.
- Affected version, branch, commit, or release artifact.
- Host platform and target platform.
- Impact: confidentiality, integrity, availability, privilege escalation,
  sandbox escape, data isolation break, signature bypass, or remote code
  execution.
- Reproduction steps or a minimal proof of concept.
- Relevant logs, crash output, screenshots, or config snippets.
- Whether secrets, signing keys, private user data, audit logs, or enterprise
  data may be exposed.

Please do not send private signing keys, production secrets, or unrelated
personal data.

## Security-Sensitive Areas

Use private disclosure for issues involving:

- Image signature validation, section hashing, image parsing, or bootloader
  handoff.
- Installer integrity checks, system manifest signing, host key derivation, or
  update staging.
- Opon Protocol enforcement or cross-enterprise data isolation.
- Capability grant, denial, audit, or escalation behavior.
- Elegua IPC routing, message spoofing, workspace isolation, or external
  gateway ingress.
- Host drivers, display drivers, virtual devices, emulator backend, or host OS
  API access.
- RustyDB storage corruption, unauthorized reads or writes, WAL recovery, or
  audit index tampering.
- Package, plugin, module, extension, or app loading.
- Tauri frontend/backend command exposure.
- Release artifact signing, checksums, installer behavior, or autostart
  registration.

## Response Process

The project will try to:

1. Acknowledge the report within 7 days.
2. Triage severity and affected versions.
3. Confirm whether the issue is reproducible.
4. Prepare a patch, mitigation, or documentation update.
5. Coordinate disclosure timing with the reporter when practical.
6. Credit the reporter if they want credit.

Alpha-stage reports may result in direct source fixes without a formal advisory
if no public release artifact is affected.

## Security Invariants

The following production invariants should not be weakened:

- Image signature validation is mandatory.
- Boot verification failure halts before runtime handoff.
- ABI compatibility is checked at component boundaries.
- Opon enforcement remains enabled in production.
- Capability grants and denials are audited before returning.
- System key private material is never written into `~/.ogun/`.
- Private image signing keys are never committed or stored in artifacts.
- Host OS APIs stay behind approved host, driver, emulator, setup, or tooling
  boundaries.
- External ingress is explicit, authenticated where required, and observable.

## No Bug Bounty

There is currently no public bug bounty program for ogun OS. Security research
is appreciated, but rewards are not guaranteed.

## Safe Harbor

Good-faith security research is welcome when it avoids data destruction,
service disruption, privacy violations, persistence on systems you do not own,
and access to data beyond what is needed to prove the issue. Stop testing and
report promptly if you encounter sensitive data.
