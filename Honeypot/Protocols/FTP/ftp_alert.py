import time
from datetime import date
from Alert.alert import Alert

   
class FTPAlert():
    def __init__(self):
        self.Date = date.today() # Getting the time and data of connection 
        local = time.localtime()
        self.Time = time.strftime("%H:%M:%S", local)
        self.alert = Alert() 
   
    def AccessAttempt(self, client_addr, username, password):
        subject = "FTP Attempt Access Alert"
        # information to be sent to the body of the email
        info = (f"""FTP was accessed attempt by {client_addr} on {self.Date} at {self.Time} with the username{username} and password{password}""") 
        self.alert.EmailInfo(subject,info) # send info the the alert file