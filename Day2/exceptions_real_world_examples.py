import os
import json
import socket
import subprocess
import time


def read_config(path):
    """Simulates reading a JSON config file for deployment."""
    try:
        with open(path, "r") as file:
            data = json.load(file)
        print(f"[OK] Loaded config from {path}")
        return data

    # --- CORE EXCEPTIONS ---
    except FileNotFoundError:
        print(f"[ERROR] Config file not found: {path}")
    except PermissionError:
        print(f"[ERROR] Permission denied while accessing: {path}")
    except ValueError:
        print(f"[ERROR] Config file is not valid JSON.")
    except OSError as e:
        print(f"[ERROR] General OS error: {e}")


def connect_to_server(host, port):
    """Simulates a socket connection to a deployment server."""
    try:
        sock = socket.create_connection((host, port), timeout=3)
        print(f"[OK] Connected to {host}:{port}")
        sock.close()

    # --- NETWORK EXCEPTIONS ---
    except socket.timeout:
        print(f"[ERROR] Timeout while connecting to {host}:{port}")
    except ConnectionRefusedError:
        print(f"[ERROR] Connection refused by {host}:{port}")
    except ConnectionError:
        print(f"[ERROR] General network connection problem.")
    except TimeoutError:
        print(f"[ERROR] Operation timed out.")
    except OSError as e:
        print(f"[ERROR] Network-related OS error: {e}")


def launch_process(command):
    """Simulates running a system command like a deployment script."""
    try:
        print(f"[INFO] Running: {command}")
        result = subprocess.run(
            command, shell=True, text=True, capture_output=True, timeout=5
        )
        if result.returncode != 0:
            print(f"[ERROR] Command failed: {result.stderr.strip()}")
        else:
            print(f"[OK] Command output:\n{result.stdout.strip()}")

    # --- PROCESS & CORE EXCEPTIONS ---
    except FileNotFoundError:
        print(f"[ERROR] The command or script doesn't exist: {command}")
    except PermissionError:
        print(f"[ERROR] No permission to run the command: {command}")
    except subprocess.TimeoutExpired:
        print(f"[ERROR] Command took too long and was terminated.")
    except subprocess.SubprocessError as e:
        print(f"[ERROR] Subprocess problem: {e}")
    except OSError as e:
        print(f"[ERROR] OS-level issue: {e}")


def main():
    print("=== DEPLOYMENT CHECK SIMULATOR ===")

    # 1. File and JSON handling
    print("\n-- Step 1: Reading configuration --")
    config = read_config("deploy_config.json")

    # 2. Network test (simulate target server)
    print("\n-- Step 2: Testing network connection --")
    connect_to_server("127.0.0.1", 8080)

    # 3. Process execution (simulating a deploy command)
    print("\n-- Step 3: Launching deployment script --")
    launch_process("python fake_script.py")

    # 4. Misc everyday exception example
    print("\n-- Step 4: Everyday logic check --")
    try:
        total_requests = int(input("Enter total requests: "))
        failed = int(input("Enter failed requests: "))
        availability = 100 * (total_requests - failed) / total_requests
        print(f"[OK] Availability: {round(availability, 2)}%")
    except ZeroDivisionError:
        print("[ERROR] Total requests cannot be zero.")
    except TypeError:
        print("[ERROR] Non-numeric data type encountered.")
    except ValueError:
        print("[ERROR] Invalid input (not a number).")
    finally:
        print("Cleaning up temporary files... (pretend we did something)")


if __name__ == "__main__":
    main()
