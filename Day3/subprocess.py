import subprocess

result = subprocess.run(
    ["cmd", "/c", "dir"], # for linux use ["ls", "-l"]
    capture_output = True, # captures stdout and stderr
    text = True,
    shell=True,
)

#result2 = subprocess.Popen()

print("Output: ")
print(result.stdout)
