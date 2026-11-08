"""
FoodIQ Database Restore and Integrity Verification Tool.
Restores a backup into a target database destination, runs PRAGMA integrity_check,
and validates foreign keys without overwriting unless explicitly forced.
"""

import os
import sys
import sqlite3
import argparse
import shutil

def restore_database(backup_file: str, target_path: str = "data/foodiq.db", force: bool = False) -> bool:
    if not os.path.exists(backup_file):
        raise FileNotFoundError(f"Backup file not found at {backup_file}")
        
    # Check backup integrity before restoring
    src_conn = sqlite3.connect(backup_file)
    integrity = src_conn.execute("PRAGMA integrity_check;").fetchone()[0]
    src_conn.close()
    
    if integrity != "ok":
        raise ValueError(f"Cannot restore: Backup file {backup_file} is corrupted ({integrity}).")
        
    if os.path.exists(target_path) and not force:
        # Create safety copy of target before overwrite
        safety_path = f"{target_path}.pre_restore"
        shutil.copy2(target_path, safety_path)
        print(f"Safety copy of existing database preserved at {safety_path}")
        
    os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)
    
    # Restore using online backup API
    src = sqlite3.connect(backup_file)
    dst = sqlite3.connect(target_path)
    with dst:
        src.backup(dst, pages=100)
    dst.close()
    src.close()
    
    # Verify restored target
    verify_conn = sqlite3.connect(target_path)
    res_integrity = verify_conn.execute("PRAGMA integrity_check;").fetchone()[0]
    fk_check = verify_conn.execute("PRAGMA foreign_key_check;").fetchall()
    verify_conn.close()
    
    if res_integrity != "ok" or len(fk_check) > 0:
        raise RuntimeError(f"Restored target failed validation: integrity={res_integrity}, fk_violations={len(fk_check)}")
        
    print(f"Database restored and verified successfully at {target_path}!")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FoodIQ Database Restore Utility")
    parser.add_argument("--backup", required=True, help="Path to backup .db file")
    parser.add_argument("--target", default="data/foodiq.db", help="Path to restore destination")
    parser.add_argument("--force", action="store_true", help="Overwrite target without safety copy")
    args = parser.parse_args()
    restore_database(args.backup, args.target, args.force)
