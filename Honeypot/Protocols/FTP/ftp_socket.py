import threading
import socket
from Database.InsertData import InsertData
from .ftp_server import FTP

class FTPServer:
    def __init__(self):
        self.insert = InsertData()
        self.ftp_server = FTP() 
        
    def HoneyConnect(self):
        try:                               #   IPV4               TCP
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
            server_socket.bind(('0.0.0.0', 21))
            server_socket.listen(50)
            
            # To keep the listing port open, and accept incoming connection, incoming ports are sent to handle_connection 
            while True:
                client_socket, client_addr = server_socket.accept()
                self.insert.OtherPorts(client_addr[0], 21)
                # start the thread transport to FTP server script
                handler = threading.Thread(target=self.ftp_server.Login, args=(client_socket,client_addr))
                handler.start()

        # Handles error if port could not be opened
        except Exception:
            server_socket.close()