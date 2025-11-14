try:
    value = int(input("Enter a natural number "))
    print("the reciprocal of ", value, "is ", 1/value)
except ZeroDivisionError:
    print("can't divide by zero mf")
except ValueError:
    print(" I don't know what to do!")
except:
    print(" I don't know what to do!")

def handleExceptions():
    try:
        total_requests = int(input("Enter total requests number: "))
        failed_requests = int(input("Enter failed requests number: "))
        availability = 100 * (total_requests - failed_requests) / total_requests
        print(f"Availability: {round(availability, 2)}%")
    except ValueError:
        print("you entered non-integer values.")
    except ZeroDivisionError:
        print("total requests can't be zero.")
    except TypeError:
        print("somethin unexpected was passed to tha fun.")
    print("Done")


# ZeroDivisionError
# ValueError
# TypeError
# AttributeError
# SyntaxError

# RuntimeError
# RuntimeWarning
# ReferenceError
# RecursionError
# ResourceWarning
# TimeoutError
# TabError
# UnicodeError
# ImportError
# OverflowError
# PermissionError
# ProcessLookupError
# ArithmeticError
# WindowsError
# FileNotFoundError
# FloatingPointError
# KeyError
# LookupError
# ConnectionError
# ChildProcessError
# BufferError
# NotADirectoryError
# NotImplementedError
# MemoryError


# 1. Everyday Core Errors (you’ll actually meet these)
# ZeroDivisionError

# When you divide by zero.
# Happens in math ops, metrics, or monitoring scripts.

# cpu_ratio = used / total  # total = 0 -> boom


# Handle it when dealing with unpredictable inputs, logs, or scraped values.

# #######################################################################################

# ValueError

# When you pass the right type but the wrong value.

# int("Neo")  # Type is str, but not a valid number


# Common in automation scripts parsing user input, CLI args, or API strings.

# #######################################################################################

# TypeError

# Wrong data type used.

# "5" + 5  # You mixed types


# You’ll meet this while juggling environment variables (they’re strings) and integers.

# #######################################################################################

# AttributeError

# When you try to access something that doesn’t exist.

# server = None
# print(server.status)  # server is None


# Classic when calling .json() on a failed API response or working with dynamic objects.

# #######################################################################################

# KeyError

# When a dictionary key isn’t found.

# data = {"status": "ok"}
# print(data["result"])  # KeyError


# Constant companion when dealing with JSON, YAML, or configs from hell.

# #######################################################################################

# IndexError

# You accessed a list position that doesn’t exist.

# servers = []
# print(servers[0])  # Empty


# Useful to handle loops and queue processing gracefully.

# #######################################################################################

# FileNotFoundError

# When you try to open or read a missing file.

# open("/etc/missing.conf")


# Extremely common in DevOps scripts handling logs, configs, or backups.

# #######################################################################################

# PermissionError

# No access to what you’re touching.

# open("/root/secure.key", "w")


# You’ll run into this when automating with elevated privileges, copying files, or writing logs in system dirs.

# #######################################################################################

# ImportError / ModuleNotFoundError

# You import something that isn’t installed or visible.

# import not_real_lib


# Happens when your environment isn’t properly isolated — a Python venv fix usually saves you.

# #######################################################################################

# ConnectionError (and subtypes)

# Network issues — connection refused, reset, or dropped.

# requests.get("http://server:8080")  # Server is dead


# In DevOps, this one’s gold. Wrap your network/API calls with it.

# #######################################################################################

# TimeoutError

# When something takes too long — especially network or subprocess calls.

# subprocess.run(["ping", "server"], timeout=5)


# You’ll see it in health checks, API polls, and async jobs.

# #######################################################################################

# OSError

# Generic “OS messed up” bucket.
# Covers file system, process, and I/O failures.

# os.rename("a.txt", "b.txt")  # fails if file is locked


# Useful when you can’t predict whether the OS will cooperate (and it usually won’t).

# #######################################################################################


# MemoryError

# Ran out of RAM.
# Happens with large file reads, giant JSONs, or carelessly looping through logs from 2017.
# You don’t “handle” it much — you just avoid it by streaming or chunking data.

# #######################################################################################

# RuntimeError

# The “I don’t know what went wrong but something did” error.
# Raised manually by certain libraries when a condition fails at runtime.
# Usually a catch-all fallback.

# #######################################################################################

# 2. Secondary Tier (you’ll meet them sometimes)
# LookupError

# Parent of IndexError and KeyError.
# You’ll rarely catch it directly, but good to know it exists.

# #######################################################################################

# NotADirectoryError

# When a path you thought was a directory is actually a file.

# os.listdir("file.txt")


# Happens when your paths come from config or user input. Good for safety checks.

# #######################################################################################

# IsADirectoryError

# The reverse — you try to open a directory like a file.

# open("/var/log")


# Seen often in file cleanup scripts.

# #######################################################################################

# ProcessLookupError

# You tried to kill or manage a process that doesn’t exist.

# os.kill(999999, 9)


# Relevant when you’re automating service restarts.

# #######################################################################################

# ChildProcessError

# Parent process tries to interact with a dead subprocess.
# Happens when subprocess calls fail mid-pipeline.

# #######################################################################################

# ConnectionRefusedError / ConnectionResetError / BrokenPipeError

# All network-related — server down, connection dropped, etc.
# Catch them when using requests, sockets, or subprocesses that rely on connections.

# #######################################################################################

# ArithmeticError

# Parent of ZeroDivisionError and OverflowError.
# Rare to catch directly.

# #######################################################################################

# OverflowError

# Number too big for Python’s floating-point brain.
# You won’t see this often unless you’re crunching massive metrics.
# Usually, if you see it, you’ve lost control of your loop.

# #######################################################################################

# UnicodeError

# Encoding/decoding gone wrong.
# Common when reading logs or config files with weird characters.
# Use encoding="utf-8" and your life improves.

# #######################################################################################

# RecursionError

# Your function called itself into oblivion.
# Doesn’t happen in DevOps unless you mess with recursive config traversal.

# #######################################################################################

# ImportWarning / ResourceWarning / RuntimeWarning

# Not fatal. Python’s passive-aggressive notes.

# #######################################################################################

# ResourceWarning happens if you forget to close files or sockets.

# 3. Rare, But Mentionable (the “meh” zone)
# TabError / IndentationError / SyntaxError

# You’ll fix these before code runs.
# Not runtime issues, so you don’t “handle” them — you avoid them.

# #######################################################################################

# BufferError / FloatingPointError / WindowsError

# Low-level, rare. Usually from ancient C extensions or system-level APIs.

# #######################################################################################

# NotImplementedError

# Raised when you leave a function unimplemented.
# Good placeholder in skeletons or abstract classes.

# #######################################################################################

# ReferenceError

# Python’s garbage collector doesn’t like your dangling reference.
# If you see it, something exotic is happening with weakref.

# #######################################################################################

# ResourceWarning

# Python reminding you you’re leaking file handles.
# Take it as “close your damn files.”

# #######################################################################################