import socket
import threading
from Database.InsertData import InsertData

# Class to handle connections
class Ports1024:
    def __init__(self):
        self.insert = InsertData()

    # To open all ports in the range of 1 - 1023, also to make then threaded
    def Openall(self):
        for port in range(1, 1024):
            # To they are skipped and the correct file can created the listing port to establish the connection 
            # for the service behind the port. 
            if (port != 22) and (port != 80) and (port != 23) and (port != 21):
                honeypot_thread = threading.Thread(target=self.HoneyConnect, args=(port,))
                honeypot_thread.start() # start the thread

     
    def HoneyConnect(self, port):
        try:                              
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
            server_socket.bind(('0.0.0.0', port)) 
            server_socket.listen(250)
            
           
            while True:
                client_socket, client_addr = server_socket.accept() 
                self.insert.OtherPorts(client_addr[0], port) 
                client_socket.close()  

        except Exception:
            server_socket.close()