---
name: Standard Merge Request
about: Default peer review template for all changes across the Ogun ecosystem
---

## Merge Request

### Summary

<!-- What does this MR do? One paragraph maximum. -->

### Motivation

<!-- Why is this change necessary? Link to the issue(s) it resolves. -->

Closes #___

### Change Type

- [ ] Bug fix
- [ ] New feature / capability
- [ ] Refactor (no behavior change)
- [ ] Performance improvement
- [ ] Security fix or hardening
- [ ] Documentation only
- [ ] Build / CI / tooling
- [ ] Protocol or API contract change
- [ ] Configuration or template change
- [ ] Release artifact update

---

## Affected Scope

**Repository / Workspace:**
- [ ] `ogun-runtime` (types, image-format, bootloader, kernel, session)
- [ ] `ogun-devices` (emulator, uefi, virtual hardware)
- [ ] `ogun-os` (desktop, web, mobile clients, host-server)
- [ ] `ogun-components` (drivers, modules, plugins, extensions, apps, UI)
- [ ] `ogun-sdk` (kernel-sdk, app-sdk, svc-sdk, mod-sdk, driver-sdk, etc.)
- [ ] `ogun-apps` (Tier-4 user applications)
- [ ] `ogun-cyber` (security crates and services)
- [ ] `elegua` (Elegua Protocol)
- [ ] `bula` (UI language / compiler)
- [ ] `oya` (system design platform)
- [ ] `jaku` (DevOps / build platform)
- [ ] `ogun-tools` (ogun-setup, ogun-image-tool)
- [ ] `ogun-config`, `ogun-artifacts`, `ogun-devops`, `ogun-docs`, `ogun-sites`

**Crates / files changed:** <!-- list key files or crates -->

---

## Pre-Merge Checklist

### Code Quality

- [ ] `cargo fmt --all` passes with no diffs
- [ ] `cargo clippy --all-targets -- -D warnings` passes clean
- [ ] `cargo check --workspace` passes for all affected workspaces
- [ ] `cargo test --workspace` passes (or affected test scope documented below)
- [ ] No `unwrap()` or `expect()` in production paths without documented justification
- [ ] No `unsafe` blocks added without a `// SAFETY:` comment
- [ ] Dead code removed or `#[allow(dead_code)]` justified in a comment

### Architecture & Invariants

- [ ] Layer isolation preserved — lower layers do not call into higher layers
- [ ] **Elegua Protocol**: all cross-boundary messages are typed `EleguaMessage` instances (no raw bytes at layer boundaries)
- [ ] **Elegua Protocol**: every cross-boundary communication is capability-checked
- [ ] **Ọpọn Protocol** (`SYS-001`): no change weakens cross-enterprise data isolation
- [ ] **ABI version** (`OGUN_ABI_VERSION`) unchanged, or bump is intentional and documented
- [ ] Kernel subsystem init order (1–15) unaffected, or change is explicitly justified
- [ ] Audit log remains append-only — no deletion code paths introduced
- [ ] `operator_id`, `workspace_id`, `enterprise_id`, and `trace_id` preserved on all IPC messages

### Security

- [ ] No new `unsafe` FFI boundaries without capability checks
- [ ] No capability grants added beyond minimum required (`CYBER-004`)
- [ ] Image signing and verification paths unmodified, or change is reviewed by @eatondo
- [ ] OgunNet firewall default-deny behavior unchanged (`CY-I-11`)
- [ ] No key material introduced outside `security://cyber/keys/`
- [ ] No cross-enterprise data paths introduced

### Documentation

- [ ] Public types, traits, and functions have doc comments (`///`)
- [ ] `DESIGN.md` updated if architecture changes
- [ ] `CHANGELOG.md` entry added for user-visible changes
- [ ] `ogun-docs/` updated if product spec, architecture, or execution model is affected
- [ ] README updated if component behavior, structure, or setup changes
- [ ] `TODO.md` updated if beta tasks are completed or added

### Tests

- [ ] New behavior is covered by unit tests
- [ ] Regression test added for bug fixes
- [ ] Integration tests updated if IPC, protocol, or service contracts changed
- [ ] Test coverage maintained or improved

---

## Protocol / API Contract Changes

<!-- Complete this section only if the MR modifies Elegua Protocol, Ọpọn Protocol, OgunNet, ABI, or SDK traits. -->

**Is this a breaking change?**
- [ ] No — purely additive
- [ ] Yes — describe migration path below

**ABI impact:**
- [ ] No ABI change
- [ ] `OGUN_ABI_VERSION` bump required (current → next: ___)

**New IPC channels / message kinds:** <!-- list any new `ipc://` addresses or `MessageKind` variants -->

**New capabilities declared:** <!-- list any new capability strings -->

**New namespace URIs:** <!-- list any new URI scheme additions -->

---

## Testing Notes

<!-- Describe how the change was tested. Include manual verification steps if automated tests are insufficient. -->

**Test commands run:**
```powershell
cargo test --workspace
# other commands
```

**Manual verification:**
<!-- Steps taken to verify the change works end-to-end -->

---

## Screenshots / Output

<!-- For UI changes (Bula components, desktop surfaces, Tauri windows), include before/after screenshots.
     For CLI / tooling changes, include representative terminal output. -->

---

## Reviewer Notes

<!-- Anything the reviewer should pay particular attention to, areas of uncertainty, or design decisions that need sign-off. -->

---

## Definition of Done

- [ ] All checklist items above are satisfied
- [ ] At least one approval from a project maintainer (@eatondo or designated reviewer)
- [ ] CI pipeline passes (build, lint, test)
- [ ] No unresolved reviewer threads
- [ ] Branch is up to date with `main`

---

/label ~"status::review"
