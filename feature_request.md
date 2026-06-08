---
name: Bug Report
about: Report a defect in behavior, output, or runtime invariant violations
labels: "type::bug"
---

## Bug Report

### Summary

<!-- One-sentence description of what is wrong. Be specific: component name, observed behavior, expected behavior. -->

### Affected Component

<!-- Select the component(s) where the bug manifests. -->

**Repository / Workspace:**
- [ ] `ogun` (monorepo root)
- [ ] `ogun-runtime` (types, image-format, bootloader, kernel, session)
- [ ] `ogun-devices` (emulator, uefi, virtual hardware)
- [ ] `ogun-os` (desktop, web, mobile clients, host-server)
- [ ] `ogun-components` (drivers, modules, plugins, extensions, apps, UI)
- [ ] `ogun-sdk` (kernel-sdk, app-sdk, svc-sdk, driver-sdk, mod-sdk, etc.)
- [ ] `ogun-apps` (Tier-4 user applications)
- [ ] `ogun-cyber` (cybersecurity crates and services)
- [ ] `elegua` (Elegua Protocol / IPC)
- [ ] `bula` (Bula UI language / compiler)
- [ ] `oya` (system design / orchestration platform)
- [ ] `jaku` (DevOps / build / CI/CD platform)
- [ ] `ogun-tools` (ogun-setup, ogun-image-tool)
- [ ] `ogun-config` (configuration templates)
- [ ] `ogun-artifacts` (release artifact staging)
- [ ] `ogun-devops` (CI/CD pipelines, scripts, containers)
- [ ] `ogun-docs` (documentation)
- [ ] `ogun-sites` (web properties)
- [ ] `rustydb` (database wrapper)
- [ ] Other: ___

**Specific crate or file (if known):** <!-- e.g. ogun-kernel-core, ogun-cyber-audit, bula-lower -->

**App tier (if applicable):**
- [ ] Tier 1 — Kernel App
- [ ] Tier 2 — OS App
- [ ] Tier 3 — Utility App
- [ ] Tier 4 — User App
- [ ] N/A

### Severity

- [ ] 🔴 Critical — runtime crash, boot failure, data loss, security invariant broken
- [ ] 🟠 High — major feature non-functional, incorrect output, capability bypass
- [ ] 🟡 Medium — degraded behavior, incorrect UI/output, non-blocking error
- [ ] 🟢 Low — cosmetic, typo, minor inconvenience

### Protocol / Invariant Violation (if applicable)

<!-- Check if this bug violates a documented invariant or protocol rule. -->

- [ ] Elegua Protocol invariant violated (typed IPC, capability-gating, observability)
- [ ] Ọpọn Protocol violated — cross-enterprise data isolation (`SYS-001` / `opn-001` through `opn-005`)
- [ ] ABI version mismatch (`OGUN_ABI_VERSION`)
- [ ] Boot chain invariant broken (image signature, UEFI handoff, kernel init order)
- [ ] Kernel subsystem init-order violation (subsystems 1–15)
- [ ] Cyber policy violated (`CYBER-001` through `CYBER-010`)
- [ ] Audit log invariant violated (`CY-I-01` through `CY-I-14`)
- [ ] None / unknown

### Steps to Reproduce

<!-- Numbered, minimal reproduction steps. -->

1. 
2. 
3. 

### Expected Behavior

<!-- What should happen according to the spec, DESIGN.md, or documented invariant. -->

### Actual Behavior

<!-- What actually happens. Paste relevant error output, panic message, or log lines below. -->

```
<!-- paste error output here -->
```

### Environment

| Field | Value |
|---|---|
| Platform | <!-- e.g. Windows x64 --> |
| Host OS version | |
| Rust toolchain | <!-- e.g. stable 1.78 --> |
| ogun OS version / commit | <!-- e.g. 0.1.0-alpha, commit abc1234 --> |
| Relevant crate version | |

### Logs / Telemetry

<!-- Paste relevant telemetry output, VFS log paths, or audit log excerpts. Redact operator data before pasting. -->

```
<!-- logs here -->
```

### Additional Context

<!-- Links to related issues, DESIGN.md sections, protocol specs, or architecture docs. -->

---

/label ~"type::bug"
