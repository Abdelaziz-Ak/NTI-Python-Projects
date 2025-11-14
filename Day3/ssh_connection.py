# ssh
import paramiko

# create SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # ssh my Ubuntu VM
    ssh.connect(hostname="192.168.1.37", username="neo", password="marshall")
    stdin, stdout, stderr = ssh.exec_command("df -h") # disk space check
    print ("command output: ")
    print (stdout.read().decode())
except Exception as e:
    print(f"connection or command failed : {e}")
finally:
    ssh.close()

