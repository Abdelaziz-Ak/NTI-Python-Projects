
import psutil
import shutil
import time
from datetime import datetime

# Configuration
LOG_FILE = "system_health.log"
CPU_THRESHOLD = 80        # percent
DISK_THRESHOLD_GB = 5     # GB of free space minimum
CHECK_PATH = "C:\\"       # change this if needed

def check_system_health():
    """Check CPU and disk usage, return results."""
    cpu_usage = psutil.cpu_percent(interval=1)
    total, used, free = shutil.disk_usage(CHECK_PATH)
    free_gb = free / (1024 ** 3)
    return cpu_usage, free_gb

def log_health(cpu, free_gb):
    """Write a line to the log file with timestamp and status."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_line = f"[{timestamp}] CPU: {cpu:.2f}% | Free Disk: {free_gb:.2f} GB"

    # Detect warnings
    warnings = []
    if cpu > CPU_THRESHOLD:
        warnings.append("⚠ High CPU usage")
    if free_gb < DISK_THRESHOLD_GB:
        warnings.append("⚠ Low disk space")

    # Combine everything into one log line
    if warnings:
        status_line += " | " + ", ".join(warnings)

    # Write to log file
    with open(LOG_FILE, "a") as log:
        log.write(status_line + "\n")

    # Print a short summary to console
    print(status_line)

def main():
    print("System Health Monitor Started. Press Ctrl+C to stop.\n")
    for i in range(5):
        cpu_usage, free_gb = check_system_health()
        log_health(cpu_usage, free_gb)
        time.sleep(5)  # check every 5 seconds

if __name__ == "__main__":
    main()
