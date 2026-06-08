---
name: Security Issue
about: Report a security vulnerability, invariant bypass, or policy violation (non-sensitive issues only — see SECURITY.md for private disclosure)
labels: "type::security, priority::critical"
---

## ⚠️ Security Issue

> **For sensitive or exploitable vulnerabilities**, do NOT file a public issue.  
> Follow the private disclosure process in [`SECURITY.md`](../SECURITY.md).  
> The default embargo window is **7 days** per `CYBER-009`.

---

### Vulnerability Summary

<!-- Brief description of the security issue. Omit exploit details if this is a public filing. -->

### Affected Component

**Repository / Workspace:**
- [ ] `ogun-runtime` (bootloader, kernel, image verification)
- [ ] `ogun-cyber` (security policies, audit log, capability engine)
- [ ] `elegua` (IPC / capability enforcement)
- [ ] `ogun-sdk` (ABI, capability declarations)
- [ ] `ogun-components` (drivers, modules, plugins, extensions)
- [ ] `ogun-devices` (emulator, UEFI, virtual hardware)
- [ ] `ogunnet` / networking subsystem
- [ ] `ogun-tools` (installer, image-tool)
- [ ] Other: ___

**Specific crate or subsystem:** <!-- e.g. ogun-cyber-audit, ogun-subsystem-security -->

### Vulnerability Class

- [ ] Image signature bypass (`CYBER-001`)
- [ ] SBOM verification failure (`CYBER-002`)
- [ ] CVE in dependency — severity: High / Critical (`CYBER-003`, `CY-I-10`)
- [ ] Capability over-declaration or bypass (`CYBER-004`)
- [ ] Audit log integrity break (`CYBER-005`, `CY-I-02`)
- [ ] OgunNet firewall bypass (`CYBER-006`, `CY-I-11`)
- [ ] Unauthorized data exfiltration / DLP (`CYBER-007`)
- [ ] Unsigned extension loaded via `dlopen` (`CYBER-008`)
- [ ] Cross-enterprise data co-mingling — Ọpọn Protocol violation (`SYS-001`)
- [ ] Capability enforcement gap (Elegua Protocol)
- [ ] ABI version spoof or mismatch exploit
- [ ] Privilege escalation in kernel or OS service layer
- [ ] Supply-chain tampering
- [ ] Key material exposed outside `security://cyber/keys/`
- [ ] Other: ___

### CVSS Score (if known)

**Score:** ___  
**Vector:** ___

### Severity Assessment

- [ ] 🔴 Critical — active exploit path, data breach, boot bypass, kernel compromise
- [ ] 🟠 High — significant security boundary broken, CVE with known PoC
- [ ] 🟡 Medium — security degradation, policy weakened, audit gap
- [ ] 🟢 Low — defense-in-depth concern, theoretical bypass

### Reproduction

<!-- Minimal steps to demonstrate the issue. Omit actual exploit code from public issues. -->

1. 
2. 
3. 

### Impact

<!-- What can an attacker achieve? What data or system integrity is at risk? -->

### Proposed Mitigation

<!-- If you have a suggested fix or patch, describe it here. -->

### References

<!-- CVE IDs, advisory links, related ogun-cyber invariants (CY-I-XX), or CYBER-00X policies. -->

### Embargo

- [ ] I request private handling under the embargo policy (`CYBER-009`)
- [ ] This issue is safe to discuss publicly

---

/label ~"type::security" ~"priority::critical"
/confidential
