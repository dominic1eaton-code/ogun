---
name: Security Review
about: Peer review template for changes affecting security subsystems, cryptography, capability enforcement, audit logging, or protocol invariants
---

## Security Review MR

> Use this template for any MR touching: `ogun-cyber`, `ogun-subsystem-security`, capability enforcement, Ọpọn Protocol, Elegua Protocol security paths, image signing/verification, OgunNet firewall/crypto, audit logging, or key management.

### Summary

<!-- What security-relevant behavior is being changed, added, or fixed? -->

Closes #___

### Security Change Type

- [ ] New or modified capability enforcement
- [ ] Audit log change (append path, chain-hash, encryption)
- [ ] Image signing or verification path
- [ ] Ọpọn Protocol isolation rule
- [ ] Elegua Protocol capability-gating
- [ ] OgunNet firewall or peer authentication
- [ ] Cryptographic primitive addition or change
- [ ] Key lifecycle change (generation, rotation, backup, destruction)
- [ ] SBOM generation or verification
- [ ] Supply-chain integrity tooling
- [ ] Security policy engine (`CYBER-001` through `CYBER-010`)
- [ ] Hardening configuration profile
- [ ] DLP / data protection controls
- [ ] Incident response playbook
- [ ] Security documentation or spec

---

## Security Invariant Review

### Ọpọn Protocol (`SYS-001`)

- [ ] `opn-001`: No cross-enterprise data appears in any view, report, or IPC response
- [ ] `opn-002`: All enterprise data is partitioned at the kernel VFS boundary
- [ ] `opn-003`: `enterprise_id` is carried on every IPC message and validated before dispatch
- [ ] `opn-004`: No aggregation across enterprise boundaries without explicit operator consent
- [ ] `opn-005`: Enterprise partitioning cannot be configured away

### Elegua Protocol (Security Paths)

- [ ] Every cross-boundary message carries `operator_id`, `workspace_id`, and `trace_id`
- [ ] Capability checks occur at every layer boundary crossing
- [ ] No raw bytes cross layer boundaries
- [ ] No silent or unobservable communication paths introduced

### Cyber Policies (`CYBER-001` through `CYBER-010`)

<!-- Check all that are relevant to this MR. -->

- [ ] `CYBER-001`: Boot still halts on ed25519 signature failure — no fallback introduced
- [ ] `CYBER-002`: `.img` artifacts without valid signed SBOM are still rejected
- [ ] `CYBER-003`: No High/Critical CVE dependency introduced
- [ ] `CYBER-004`: Apps declare only minimum required capabilities; over-broad declarations rejected
- [ ] `CYBER-005`: Audit log chain hash verified on session open; break still halts session
- [ ] `CYBER-006`: No new inbound OgunNet peer accepted without passing firewall ruleset
- [ ] `CYBER-007`: Data export rate limiting and operator approval gate preserved
- [ ] `CYBER-008`: Extensions loaded via `dlopen` still require `cyber-signed-at` manifest field
- [ ] `CYBER-009`: Incident embargo window preserved (default 7 days)
- [ ] `CYBER-010`: Baseline hardening profile deviation still logged as MEDIUM finding

### Audit Log Invariants (`CY-I-01` through `CY-I-14`)

- [ ] `CY-I-01`: Every cyber event written to `CyberAuditWriter` **before** the operation completes or is rejected
- [ ] `CY-I-02`: Chain hash verified on session open; break transitions to incident phase `DETECTED`
- [ ] `CY-I-03`: `host_key`, `operator_id`, `enterprise_id`, `trace_id` stamped on every `CyberAuditEntry`
- [ ] `CY-I-04`: Every finding and report scoped to single `enterprise_id`
- [ ] `CY-I-06`: No private key material outside `security://cyber/keys/` or host keychain
- [ ] `CY-I-07`: Key backups encrypted under operator passphrase before disk write
- [ ] `CY-I-08`: Image signature verified on every install/update before extraction
- [ ] `CY-I-11`: OgunNet default-deny for unknown `NodeId` in Standard/Hardened/Lockdown profiles
- [ ] `CY-I-12`: IDS alert logging always active
- [ ] `CY-I-13`: `AuditLogAppend` held exclusively by `ogun-cyber-audit`
- [ ] `CY-I-14`: `FirewallWrite`, `KeyRotationExecute`, `HardeningWrite` require operator re-auth

---

## Code-Level Security Review

### Cryptography

- [ ] No home-grown cryptographic primitives — only audited crates (e.g. `ring`, `ed25519-dalek`, `aes-gcm`, `x25519-dalek`)
- [ ] RNG uses `OsRng` or equivalent cryptographically secure source
- [ ] No key material in log output, panic messages, or error strings
- [ ] Constant-time comparisons used for secrets where timing attacks apply

### Memory Safety

- [ ] No new `unsafe` blocks without `// SAFETY:` justification
- [ ] Sensitive data (keys, secrets) zeroed on drop (e.g. `zeroize` crate)
- [ ] No buffer overread/overwrite paths in parsing or deserialization

### Input Validation

- [ ] All external or untrusted inputs validated before use
- [ ] Deserialization bounded — no unbounded allocation from untrusted sources
- [ ] Namespace URIs validated before VFS or IPC dispatch

### Privilege and Capability

- [ ] No capability escalation without logged, operator-approved grant chain
- [ ] Default-deny posture preserved for new capability gates
- [ ] Sandbox isolation not weakened for plugins or extensions

---

## Pre-Merge Checklist (Security MRs)

- [ ] `cargo fmt --all` passes
- [ ] `cargo clippy --all-targets -- -D warnings` passes
- [ ] `cargo test --workspace` passes (all security-relevant test suites run)
- [ ] `cargo audit` run — no unaddressed High or Critical advisories
- [ ] SBOM updated if new dependencies introduced
- [ ] Supply-chain verification run (`ogun-cyber-supply-chain`)
- [ ] `SECURITY.md` updated if disclosure or supported-version info changes
- [ ] `CHANGELOG.md` updated with security fix or hardening note
- [ ] Reviewer with security domain knowledge has approved

---

## Threat Model Notes

<!-- Briefly describe the threat model for this change:
- Who is the adversary?
- What are they trying to achieve?
- How does this change defend against or fail to defend against that threat? -->

---

## Testing Notes

```powershell
cargo test --workspace
cargo audit
# supply-chain check if applicable:
cargo run -p ogun-cyber-supply-chain -- image --img <path>.img --sbom <path>.sbom.json
```

**Manual verification performed:**

---

## Reviewer Notes

<!-- Flag any areas of uncertainty, design tradeoffs made under time pressure, or behaviors that need extra scrutiny. -->

---

## Definition of Done

- [ ] All security invariant checkboxes confirmed or explicitly marked N/A with justification
- [ ] Approval from @eatondo (maintainer sign-off required for all security MRs)
- [ ] CI pipeline passes including `cargo audit`
- [ ] No unresolved review threads
- [ ] Branch up to date with `main`

---

/label ~"type::security" ~"status::review"
