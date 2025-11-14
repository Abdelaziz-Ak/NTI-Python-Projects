
import platform
import os

# Unix systems
def osInformation():
    print("System:      ", info.sysname())
    print("Node:     ", info.nodename())
    print("Release:     ", info.release())
    print("Version:    ", info.version())
    print("Machine:    ", info.machine())


# cross platform
def platformInformation():
    print("System:      ", platform.system())
    print("Version:     ", platform.version())
    print("Release:     ", platform.release())
    print("Architecture:    ", platform.architecture())

def main():
    #osInformation()
    platformInformation()


if __name__ == "__main__":
    main()