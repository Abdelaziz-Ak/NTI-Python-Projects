
def is_ready_for_deployment(cpu, ram, disk):
    if cpu < 70 and ram < 75 and disk < 80:
        print("Server is Ready ")
        print(f"Current usage — CPU: {cpu}%, RAM: {ram}%, Disk: {disk}%")
        return True
    else:
        print("Server is NOT Ready")
        print(f"Current usage — CPU: {cpu}%, RAM: {ram}%, Disk: {disk}%")
        return False



cpu_val = int(input("Enter cpu % value: "))
ram_val = int(input("Enter ram % value: "))
disk_val = int(input("Enter disk % value: "))

print(is_ready_for_deployment(cpu_val, ram_val, disk_val))


