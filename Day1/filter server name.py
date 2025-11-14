server_name = input("Enter Server Name: ")

filtered_name = ""
for char in server_name:
    if char.isdigit() or char in "@#-":
        continue
    filtered_name += char

print(f"Filtered name is: {filtered_name}")
