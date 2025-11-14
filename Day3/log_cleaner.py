from pathlib import Path
import glob # alternative library
import time

# Configure your log folder and retention period
LOG_FOLDER = Path("E:/Documents/vsCodeProjects/Python/NTI Projects/Day3/test_logs") 
DAYS_TO_KEEP = 30

def clean_old_logs():
    """Delete .log files older than the given number of days."""
    current_date = time.time()
    cutoff = current_date - (DAYS_TO_KEEP * 24 * 60 * 60)

    if not LOG_FOLDER.exists():
        print(f"Folder not found: {LOG_FOLDER}")
        return

    deleted_count = 0

    for file in LOG_FOLDER.iterdir():
        # Skip anything that's not a file or not a .log
        if not file.is_file() or not file.name.endswith(".log"):
            continue

        try:
            mtime = file.stat().st_mtime
            if mtime < cutoff:
                file.unlink()  # delete it
                print(f"Deleted: {file.name}")
                deleted_count += 1
        except Exception as e:
            # Something weird happened (locked file, permissions, etc.)
            print(f"Could not delete {file.name}: {e}")

    if deleted_count == 0:
        print("No old log files found.")
    else:
        print(f"\nCleanup complete. {deleted_count} file(s) deleted.")

if __name__ == "__main__":
    clean_old_logs()
