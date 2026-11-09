# FoodIQ v1.1 — Security, Reliability & Compliance Manual
**Document Reference:** DOC-V11-12  
**Classification:** Cybersecurity & Infrastructure Hardening  

---

## 1. Defensive Engineering Principles

FoodIQ is built to institutional compliance standards:
1. **Parameterized Queries:** All SQL calls use standard DB-API parameter placeholders (`?`). String formatting or raw concatenation is banned.
2. **Path Sanitization:** File endpoints sanitize user-provided file names using strict path resolution and whitelist validation. Directory traversal sequences (`..`) raise HTTP 400.
3. **No Credential Persistence:** The repository contains zero API keys, database credentials, or secret keys.
4. **Resilience & Backups:** Scheduled snapshots preserve the canonical database in `data/backups/`.
