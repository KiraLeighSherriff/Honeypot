import socket
import threading

from Database.InsertData import InsertData
from .ssh_server import SSHServer
from .ssh_alert import SSHAlert

        
class SSHSocket():
    def __init__(self, server_key):
        self.insert = InsertData()
        self.server_key = server_key  
        self.ssh_server = SSHServer(server_key)  
        self.alert = SSHAlert()
        
    # Create the server socket to listen for connection, bind it to the port sent by the start function loop        
    def HoneyConnect(self):
        try:                               #   IPV4               TCP
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
            server_socket.bind(('0.0.0.0', 22))
            server_socket.listen(50)
            
            
            
            while True:
                client_socket, client_addr = server_socket.accept()
                self.alert.AccessAttempt(client_addr)
                self.insert.OtherPorts(client_addr[0], 22) # send so the user get an alert that an attempt to access was made
                # threaded created when user connects sent ot ConnectSSH 
                handler = threading.Thread(target=self.ssh_server.ConnectSSH, args=(client_socket,))
                handler.start()

        # Handles error if port could not be opened
        except Exception:
            server_socket.close()