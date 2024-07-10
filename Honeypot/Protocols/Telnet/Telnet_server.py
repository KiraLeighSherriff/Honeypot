import os
import json

from .Telnet_log import TelnetInsert
from .Telnet_commands import TelnetCommands
from .Telnet_alert import TelnetAlert

# Getting password and username form those who try to login into telnet

class TelnetServer():
    def __init__(self):
        self.insert = TelnetInsert()
        self.commands = TelnetCommands()
        self.alert = TelnetAlert()
        self.attempts = 0
        
    def AuthCreds(self, username, password, client_socket):
        
        current_directory = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(current_directory, 'creds.json')

        with open(json_file) as config_file:
            config = json.load(config_file)

        telnet_login = config['telnet_login']
        json_username = telnet_login['telnet_username']
        json_password = telnet_login['telnet_password']
        
        if (username == json_username) and (password == json_password):
            client_socket.send(b"Welcome to Ubuntu 17.04 (GNU/Linux 4.10.0.21-generic X86-64)\r\n") 
            self.GetCommand(client_socket)     
            self.alert.SucLogin()
            self.attempts = 5 
        else:
            client_socket.send(b"\n\rIncorrect Login\n\r")


    def Username(self, client_socket):
        username = ""
        client_socket.send(b"Login: ")
        while True:
            data = client_socket.recv(1024)
            if not data or data == b'\r\n':
                    break
            username += data.decode("utf-8") 
        return username.strip() 

            
    def password(self, client_socket):
                        
        password = ""
        client_socket.send(b"Password: ")
        while True:
            data = client_socket.recv(1024)
            if not data or data == b'\r\n':
                    break
            password += data.decode("utf-8") 
        return password.strip() 
    
    def GetCommand(self, client_socket):
    
        while True:
          
            command = ""
            client_socket.send(b"guest@telnet: $> ")
           
            while not command.endswith("\n"):
                data = client_socket.recv(1024)

                if not data or data == b'\r\n':
                    command = command.lower().strip()          
                    self.insert.TelnetCommands(command)

                    if command == 'exit':
                        data = ''
                        return False 
                    else:
                        self.commands.HandleCommands(command, client_socket)

                command += data.decode("utf-8")
        

    def start(self, client_socket):
            
            while self.attempts < 3:
              
                username = self.Username(client_socket)
                password = self.password(client_socket)
                self.insert.TelnetLogin(username,password)
                self.AuthCreds(username, password, client_socket)
                self.attempts += 1 
            else:
                client_socket.send(b"Connection Close")           
                client_socket.close()  