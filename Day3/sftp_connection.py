# sftp
import paramiko

try:
    transport = paramiko.Transport(("192.168.1.37", 22))
    transport.connect(username="neo", password="marshall")

    sftp = paramiko.SFTPClient.from_transport(transport)

    # upload a file
    sftp.put("local_log.txt", "/home/neo/Downloads/ubuntu_log.txt")

    # download a file
    sftp.get("/home/neo/Downloads/ubuntu_log.txt", "transfered_file.txt")
    print("file transfer complete")

except Exception as e:
    print(f"sftp operation failed: {e}")
    
finally:
    sftp.close()
    transport.close()