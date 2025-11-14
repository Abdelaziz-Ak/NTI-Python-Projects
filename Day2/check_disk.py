import shutil

def check_disk(threshold_gb, path):
    total_disk, used, free = shutil.disk_usage(path)
    free_gb = free / (1024 ** 3)
    print("Path:", path)
    print("Total Disk Space:", round((used + free) / (1024 ** 3)), 2)
    print("Free Space (GB):", round(free_gb, 2))
    print("Used Space (GB):", round(used / (1024 ** 3), 2))
    if free_gb < threshold_gb:
        print("Low Disk Space")
    else:
        print("Disk Space is Sufficient")

# Call the function *after* defining it
check_disk(50, "D:\\")




def is_server_healthy(cpu_usage):
    if cpu_usage > 80:
        return False
    else:
        return True
    
test_data = [45, 82, 67, 91]
expected_results = [True, False, True, False]

i = 0
for data in test_data:
    #print (is_server_healthy(data))
    if is_server_healthy(data) == expected_results[i]:
        print ("OK")
    else:
        print ("NO")
    i+=1

