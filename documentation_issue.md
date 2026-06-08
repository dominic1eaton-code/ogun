---
name: Architecture RFC
about: Propose a structural change to protocols, kernel subsystems, SDK contracts, or system invariants
labels: "type::rfc, status::discussion"
---

## Architecture RFC — Request for Comments

### RFC Title

<!-- Short descriptive title, e.g. "Add rate-divider field to virtual CPU tick model" -->

### Status

- [ ] Draft — seeking initial feedback
- [ ] Active — discussion in progress
- [ ] Accepted — implementation tracked separately
- [ ] Rejected — see resolution notes
- [ ] Superseded by: #___

### Summary

<!-- One paragraph: what is being changed, why, and what the expected impact is. -->

### Motivation

<!-- What problem or limitation in the current architecture drives this RFC? Reference DESIGN.md, ogun-docs, or invariant IDs where applicable. -->

### Scope

**Primary impact area:**
- [ ] Boot chain / UEFI / bootloader
- [ ] Kernel core / subsystem model (1–15)
- [ ] Kernel subsystem: ___
- [ ] Driver model (host / display)
- [ ] Virtual device (emulator, virtual CPU, virtual NIC, etc.)
- [ ] Elegua Protocol (IPC, channels, bus topology, message format)
- [ ] Ọpọn Protocol (enterprise isolation, SYS-001)
- [ ] OgunNet (P2P, DHT, gossip, firewall, file transfer)
- [ ] SDK contract (`ogun-app-sdk`, `ogun-svc-sdk`, `ogun-mod-sdk`, etc.)
- [ ] Capability / permission model
- [ ] Sambara agent authority model (OBSERVE → FULL_AUTONOMY)
- [ ] VFS namespace system
- [ ] Application tier model (Tier 1–4)
- [ ] Bula language / compiler
- [ ] Oya orchestration model
- [ ] Jaku build / CI/CD pipeline
- [ ] ogun-cyber security policies or invariants
- [ ] Documentation / spec only
- [ ] Other: ___

### Proposed Design

<!-- Describe the new behavior in detail. Include:
- Data structure or API changes (Rust types, traits, enum variants)
- Protocol changes (new message kinds, IPC channels, namespace URIs)
- Invariant changes or additions
- Migration path from the current design
- Interaction with the 15-subsystem init order (if applicable) -->

```rust
// Include representative Rust types, traits, or pseudocode if helpful
```

### Design Invariants Affected

<!-- List any existing invariants from DESIGN.md or ogun-docs that this RFC modifies, adds, or removes. -->

| Invariant ID | Current rule | Proposed change |
|---|---|---|
| | | |

### Security Analysis

<!-- How does this RFC interact with:
- Ọpọn Protocol (cross-enterprise data isolation)?
- Capability enforcement?
- Audit log integrity (append-only)?
- Image signing and boot verification?
- OgunNet firewall / peer authentication? -->

### ABI / Compatibility Impact

<!-- Does this change the ABI version? Break existing components? Require SDK version bump? -->

- [ ] No ABI break — additive only
- [ ] ABI version bump required (`OGUN_ABI_VERSION`)
- [ ] Existing components must be recompiled
- [ ] Migration guide required

### Open Questions

<!-- What is still unresolved? What feedback is specifically requested? -->

1. 
2. 
3. 

### Alternatives Considered

<!-- What alternative designs were evaluated? Why was this approach chosen? -->

### Implementation Plan

<!-- If accepted: rough breakdown of implementation steps and which crates/repos are affected. -->

| Step | Crate / Repo | Owner | Milestone |
|---|---|---|---|
| | | | |

### References

<!-- DESIGN.md sections, ogun-docs paths, prior issues, external specs. -->

---

/label ~"type::rfc" ~"status::discussion"
