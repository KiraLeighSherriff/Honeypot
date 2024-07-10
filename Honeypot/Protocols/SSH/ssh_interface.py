import os
import json
import paramiko

from .ssh_log import SSHInsert
from .ssh_alert import SSHAlert


# Creating the SSH Sever so the user can connect
# This will handel the channel, and auth for the user 
# Created following paramiko Server implementation documentation 
class SSHInterface(paramiko.ServerInterface):
    def __init__(self):
        self.insert = SSHInsert() 
        self.alert = SSHAlert()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED 
    
    def get_allowed_auths(self, username):
        return "password"
    
    def check_auth_password(self, username, password):   
        self.insert.SSHLogin(username, password)
    
        current_directory = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(current_directory, 'creds.json')

        with open(json_file) as config_file:
            config = json.load(config_file)

        ssh_login = config['ssh_login']
        json_username = ssh_login['ssh_username']
        json_password = ssh_login['ssh_password']
        
        if (username == json_username) and (password ==  json_password):    
            self.alert.SucLogin()

            return paramiko.AUTH_SUCCESSFUL 
        else:
            return paramiko.AUTH_FAILED 
        
    def check_auth_publickey(self, username, key):
        return paramiko.AUTH_FAILED  
    
    def check_channel_shell_request(self, channel): 
        return True
        
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True