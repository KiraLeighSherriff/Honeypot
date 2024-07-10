import os
import json
import threading

from Protocols.Telnet.Telnet_socket import TelnetSocket


# start telnet
def OpenTelnet():
    telnet = TelnetSocket()
    telnet.HoneyConnect()
    
    
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
    
    
    data['pythonpid']['telnetpid'] = main_pid
    
    # Write to the file
    with open(json_file, "w") as file_pid:
        json.dump(data, file_pid, indent=4)


# funcation to start all the threads
def main():
    telnet_thread = threading.Thread(target=OpenTelnet)
    telnet_thread.start()
    telnet_thread.join()


# Call the main funcation to start all threads
if __name__ == "__main__":
    GetProcessID()
    main()