# FoodIQ Phase 9 — Backup, Restore & Recovery Procedures

## 1. Online Backup Architecture

FoodIQ implements zero-downtime, non-locking database backups using SQLite's native C online backup API (`conn.backup()`):
- **WAL Concurrency:** Backups proceed concurrently with active read queries and transactions without blocking the server.
- **Automated Verification:** Every backup file is verified with `PRAGMA integrity_check;` before being finalized.

### Creating an Immediate Backup
```bash
python scripts/backup_db.py
```
Output archive: `data/backups/foodiq_backup_YYYYMMDD_HHMMSS.db`.

---

## 2. Restore & Disaster Recovery Procedure

To restore a database snapshot:
```bash
python scripts/restore_db.py --backup data/backups/foodiq_backup_YYYYMMDD_HHMMSS.db --target data/foodiq.db
```
### Restore Guardrails
1. **Pre-Restore Safety Snapshot:** Automatically creates `foodiq.db.pre_restore` before overwriting.
2. **Post-Restore Integrity Validation:** Verifies table integrity (`PRAGMA integrity_check`) and foreign key constraints (`PRAGMA foreign_key_check`) before confirming success.
