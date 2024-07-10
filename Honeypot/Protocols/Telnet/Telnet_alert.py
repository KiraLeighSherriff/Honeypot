from datetime import date
import time

from Alert.alert import Alert
 
class TelnetAlert():
    def __init__(self):
        self.alert = Alert()
        # Done so the code does not have to be repeated twice in the same code 
        self.Date = date.today() # Getting the time and data of connection 
        local = time.localtime()
        self.Time = time.strftime("%H:%M:%S", local)
    
    # This will be ran when the user has entered the correct credentials for telnet 
    def SucLogin(self,):
        subject = "Telnet Successful Accessed"
        info = (f"""Telnet was successful accessed on {self.Date} at {self.Time}. View the web application for more information""") 
        self.alert.EmailInfo(subject, info)
        
    # This will send a email was an access attempt was made to telnet.
    def AccessAttempt(self,client_addr):
        subject = "Telnet Attempt Accessed"
        info = (f"""Telnet was accessed by {client_addr} on {self.Date} at {self.Time}""") 
        self.alert.EmailInfo(subject, info)