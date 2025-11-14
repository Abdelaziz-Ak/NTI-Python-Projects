cpu_total = int(input("Enter CPU capacity: ")) #TODO: Get total CPU capacity from user input
cpu_used = int(input("Enter used CPU: ")) #TODO: Get used CPU from user input

mem_total = float(input("Enter total memory: ")) #TODO: Get total memory from user input
mem_used = float(input("Enter used memory: ")) #TODO: Get used memory from user input

cpu_util = 100*cpu_used/cpu_total #TODO: Calculate CPU utilization as a percentage
mem_util = 100*mem_used/mem_total#TODO: Calculate Memory utilization as a percentage


print(f"CPU Utilization: {cpu_util:.2f}%")
print(f"Memory Utilization: {mem_util:.2f}%")

print("\nThat's all, folks!")

