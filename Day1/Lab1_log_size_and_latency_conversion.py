log_size_bytes = 12_345_678
latency_ms = 247.3
rotate_threshold_mb = 10

BYTES_IN_MB = 1024 * 1024
BYTES_IN_GB = 1024 * BYTES_IN_MB


size_mb = log_size_bytes / BYTES_IN_MB #TODO: Convert log size to MB 
size_gb = log_size_bytes / BYTES_IN_GB #TODO: Convert log size to GB
latency_s = latency_ms / 1000 #TODO: Convert latency to seconds
rotate = "True" if size_mb > rotate_threshold_mb else "False" #TODO: Determine if rotation is needed
rotate1 = size_mb > rotate_threshold_mb #TODO: Determine if rotation is needed


print(f"Log size: {size_mb} MB ({size_gb} GB)")
print(f"Latency: {latency_ms} ms ({latency_s} s)")
print(f"Rotate logs now? {rotate}")
print(f"Rotate log boolean {int(rotate1)}")
print(f"Rotate logs now? {rotate1}")








