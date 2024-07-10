
import paramiko
import json
import threading
import os

from Protocols.tcp_app import Ports1024
from Protocols.SSH.ssh_socket import SSHSocket
from Protocols.Telnet.Telnet_socket import TelnetSocket
from Protocols.FTP.ftp_socket import FTPServer

# open all ports
def Open1024():
    open_ports = Ports1024()
    open_ports.Openall()
    
# open ssh
def OpenSSH():
    username = os.getlogin()
    server_key = paramiko.RSAKey.from_private_key_file(f"C:\\Users\\{username}\\Honeypot\\Protocols\\SSH\\RSAKeys\\RSAHoney")
    ssh = SSHSocket(server_key)
    ssh.HoneyConnect()
    
# open telnet 
def OpenTelnet():
    telnet = TelnetSocket()
    telnet.HoneyConnect()
      
# open ftp
def OpenFTP():
    ftp = FTPServer()
    ftp.HoneyConnect()
    
# open http
def OpenHTTP():
    from Protocols.HTTP.app import app 
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)
    
# Get the PID of the script once it starts
def GetProcessID():
    # Path to json file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(current_directory, 'pids.json')

    with open(json_file, "r") as file_pid:
        data  = json.load(file_pid)
    
    # edit the data
    main_pid = (os.getpid())
    data['pythonpid']['allpid'] = main_pid
    
    with open(json_file, "w") as file_pid:
        json.dump(data, file_pid, indent=4)


def main():
    
    # creating target to start the threads
    port_thread = threading.Thread(target=Open1024)
    ssh_thread = threading.Thread(target=OpenSSH)
    telnet_thread = threading.Thread(target=OpenTelnet)
    http_thread = threading.Thread(target=OpenHTTP)
    ftp_thread = threading.Thread(target=OpenFTP)
    
    # start the thread for the functions and the scripts that they call
    port_thread.start()
    ssh_thread.start()
    telnet_thread.start()
    http_thread.start()
    ftp_thread.start()
    
    port_thread.join()
    ssh_thread.join()
    telnet_thread.join()
    http_thread.join()
    ftp_thread.join

if __name__ == "__main__":
    GetProcessID()
    main()