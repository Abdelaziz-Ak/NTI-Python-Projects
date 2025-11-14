# Mini tool: validate port, latency, and service name 
# Uses recursion for retries and try/except for safe conversions.

print("=== Input Validation Tool ===")


def read_port():
    s = input("Enter port: ").strip()
    if not s:
        print("❌ Port cannot be empty.")
        return read_port()
    if not s.isdigit():
        print("❌ Port must be an integer.")
        return read_port()
    port = int(s)
    if not (1 <= port <= 65535):
        print("❌ Port must be in 1–65535.")
        return read_port()
    return port

def read_latency_ms():
    s = input("Enter latency (ms): ").strip()
    if not s:
        print("❌ Latency cannot be empty.")
        return read_latency_ms()
    try:
        val = float(s)
    except ValueError:
        print("❌ Latency must be a number.")
        return read_latency_ms()
    if val < 0:
        print("❌ Latency must be non-negative.")
        return read_latency_ms()
    return val

def _valid_service_name(name: str) -> bool:
    # Alphanumeric, '_' or '-', length 3–20 (no regex, no loops)
    if not (3 <= len(name) <= 20):
        return False
    return all(ch.isalnum() or ch in "_-" for ch in name)

def read_service_name():
    name = input("Enter service name: ").strip()
    if not name:
        print("❌ Service name cannot be empty.")
        return read_service_name()
    if not _valid_service_name(name):
        print("❌ Invalid name format. Use only letters, numbers, _ or -, length 3–20.")
        return read_service_name()
    return name

def main():
    try:
        port = read_port()
        latency = read_latency_ms()
        service = read_service_name()
        print(f"✅ OK! Port={port}, Latency={latency:.2f} ms, Service='{service}'")
    except Exception as e:
        # Should rarely trigger; keeps program from crashing unexpectedly
        print("Unexpected error:", e)

if __name__ == "__main__":
    main()
