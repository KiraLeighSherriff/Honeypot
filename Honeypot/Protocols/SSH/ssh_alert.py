from datetime import date
import time

from Alert.alert import Alert
 
#This file was created to make the code more readable by have a sepreate file that will handle the alert 
# system for ssh for they the code of the main do not get to long and hard to read
 
class SSHAlert():
    def __init__(self):
        self.alert = Alert()
        # Done so the code does not have to be repeated twice in the same code 
        self.Date = date.today() # Getting the time and data of connection 
        local = time.localtime()
        self.Time = time.strftime("%H:%M:%S", local)
    
    # This will be ran when the user has entered the correct credentials for ssh 
    def SucLogin(self):
        subject = "SSH Successful Accessed"
        info = (f"""SSH was successful accessed by {self.Date} at {self.Time}. View the web application for more information""") 
        self.alert.EmailInfo(subject, info)
        
    # This will send a email was an access attempt was made on ssh.
    def AccessAttempt(self,client_addr):
        subject = "SSH Attempt Accessed"
        info = (f"""SSH was accessed by {client_addr} on {self.Date} at {self.Time}""") 
        self.alert.EmailInfo(subject, info)