"""
FoodIQ Safe Online Database Backup Tool.
Uses SQLite's online backup API (conn.backup) to create a consistent, non-corrupted snapshot
even during active reads/writes in WAL mode.
"""

import os
import sys
import sqlite3
import datetime
import argparse

def backup_database(src_path: str = "data/foodiq.db", backup_dir: str = "data/backups") -> str:
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Source database not found at {src_path}")
        
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"foodiq_backup_{timestamp}.db")
    
    src_conn = sqlite3.connect(src_path)
    dst_conn = sqlite3.connect(backup_file)
    
    print(f"Beginning safe online backup from {src_path} to {backup_file}...")
    with dst_conn:
        src_conn.backup(dst_conn, pages=100)
        
    dst_conn.close()
    src_conn.close()
    
    # Verify backup integrity
    verify_conn = sqlite3.connect(backup_file)
    integrity = verify_conn.execute("PRAGMA integrity_check;").fetchone()[0]
    verify_conn.close()
    
    if integrity != "ok":
        os.remove(backup_file)
        raise RuntimeError(f"Backup verification failed: {integrity}")
        
    size_bytes = os.path.getsize(backup_file)
    print(f"Backup verified successfully! Size: {size_bytes / 1024:.1f} KB -> {backup_file}")
    return backup_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FoodIQ Database Backup Utility")
    parser.add_argument("--src", default="data/foodiq.db", help="Path to source foodiq.db")
    parser.add_argument("--dest", default="data/backups", help="Target backup directory")
    args = parser.parse_args()
    backup_database(args.src, args.dest)
