from Alert.alert import Alert
 
class HTTPAlert():
    def __init__(self):
        self.alert = Alert() 
        
    # This will send a email was an access attempt was made to telnet.
    def AccessAttempt(self, address, username, password ):
        subject = "HTTP Attempt Accessed"
        info = (f"""Http was access by {address}, and entered with username {username} and password {password}""") 
        self.alert.EmailInfo(subject, info)