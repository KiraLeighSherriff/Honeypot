import paramiko
import os
import json
import threading

from Protocols.SSH.ssh_socket import SSHSocket

        
#start SSH
def OpenSSH():
    user = os.getlogin()
    server_key = paramiko.RSAKey.from_private_key_file(f"C:\\Users\\{user}\\Honeypot\\Protocols\\SSH\\RSAKeys\\RSAHoney")
    ssh = SSHSocket(server_key)
    ssh.HoneyConnect()
    
    
# Get the pid of the file store it in a JSON file so it can be used by php to terminate the pyhton script
def GetProcessID():
    # Dynamically get path to json
    current_directory = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(current_directory, 'pids.json')

    # Open file
    with open(json_file, "r") as file_pid:
        data  = json.load(file_pid)
    
    # Get the proccess id of the file
    main_pid = (os.getpid())
    
    data['pythonpid']['sshpid'] = main_pid
    
    # Write to the file
    with open(json_file, "w") as file_pid:
        json.dump(data, file_pid, indent=4)


# funcation to start all the threads
def main():
    ssh_thread = threading.Thread(target=OpenSSH)
    ssh_thread.start()
    ssh_thread.join()

# Call the main funcation to start all threads
if __name__ == "__main__":
    GetProcessID()
    main()
