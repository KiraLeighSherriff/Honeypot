import socket
import threading

from Database.InsertData import InsertData
from .Telnet_server import TelnetServer
from .Telnet_alert import TelnetAlert

        
class TelnetSocket():
    def __init__(self):
        self.insert = InsertData()
        self.Telnet_server = TelnetServer()
        self.Telnet_alert = TelnetAlert()

    # Create the server socket to listen for connection, bind it to the port sent by the start function loop        
    def HoneyConnect(self):
        try:                               #   IPV4               TCP
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 5) 
            server_socket.bind(('0.0.0.0', 23))
            server_socket.listen(50)
            
            # To keep the listing port open, and accept in coming connection, incoming port are sent to handle_connection 
            # so that the incoming connection get sent to the right protocol, as in port 22 to paramiko. 
            # To add the incoming connections into the database 
            while True:
                client_socket, client_addr = server_socket.accept()
                self.insert.OtherPorts(client_addr[0], 23) # Transport the info the insert function 
                self.Telnet_alert.AccessAttempt(client_addr)
                handler = threading.Thread(target=self.Telnet_server.start(client_socket, attempts), args=(client_socket))
                handler.start()
                
        # Handles error if port could not be opened
        except Exception:
            server_socket.close()