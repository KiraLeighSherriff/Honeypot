import paramiko

# Import files for ssh connection to work
from .ssh_interface import SSHInterface
from .ssh_commands import SSHCommands
from .ssh_log import SSHInsert

class SSHServer(): 
    def __init__(self, server_key):
        self.server_key = server_key
        self.Command = SSHCommands()
        self.insert = SSHInsert()
    
    def ConnectSSH(self, client_socket):  
        transport_data = paramiko.Transport(client_socket)
        transport_data.add_server_key(self.server_key)  
        ssh = SSHInterface() 
        
        try: 
            transport_data.start_server(server=ssh)
        except paramiko.SSHException:
            pass
        
        channel = transport_data.accept(30)
    
        if channel is None:
            pass

        try:
            channel.send("Welcome to Ubuntu 17.04 (GNU/Linux 4.10.0.21-generic X86-64)\r\n")
            channel.send("\r\n")
            channel.send("0 Packages can be updated.\r\n")
            channel.send("0 Updates are security updates.\r\n")
            channel.send("\r\n")
            
            while True:
                channel.send("guest@ssh:/ $ ")
                commands = ""
                while not commands.endswith("\r"):
                    data = channel.recv(1024)
                    channel.send(data)
                    commands += data.decode("utf-8")

                channel.send("\r\n")
                commands = commands.rstrip().lower() 
                self.insert.SSHCommands(commands)
                
                if commands == "exit":
                    channel.send("logout guest\r\n")
                    channel.shutdown()
                    channel.close()
                else:
                    self.Command.HandleCommands(commands, channel)
        
        except Exception:
                transport_data.close()
                
if __name__ == "__main__":
    server_key = paramiko.RSAKey.from_private_key_file('RSAkeys/RSAHoney') 
    server = SSHServer(server_key)
    server.ConnectSSH()