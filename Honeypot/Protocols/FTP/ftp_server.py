from .ftp_log import FTPInsert
from .ftp_alert import FTPAlert

# https://en.wikipedia.org/wiki/List_of_FTP_server_return_codes for creating the correct error, or positive code when the user connects to
# make it more authentic 

class FTP:
    def __init__(self):
        self.con_insert = FTPInsert()
        self.alert = FTPAlert()
        
    def Login(self, client_socket, client_addr):
        client_socket.sendall(b'220 Welcome to the FTP!\r\n')

        username = ''
        password = ''
        
        while True: 
            data = client_socket.recv(1024).decode('utf-8')

            if not data:
                break
            
            if data.startswith('USER'):
                client_socket.sendall(b'331 Password required for user.\r\n')
                username = data.strip()  
                username = username.replace("USER", "")    
            elif data.startswith('PASS'):
                password = data.strip() 
                password = password.replace("PASS", "")
            else:
               client_socket.sendall( b'\r\n') 
          
            if username != '' and password != '':
                self.con_insert.FTPLogin(username, password)
                client_socket.sendall(b'530 Login authentication failed\r\n')
                client_socket.close() 
                self.alert.AccessAttempt(client_addr, username, password)
