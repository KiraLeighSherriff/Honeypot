import smtplib
import os
import json

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# This is the alert page an alert will only be sent for http, ssh, ftp and telnet as they are the
# ports they are developed have an alert for all port could be too much information and would not 
# be worth while.

class Alert():
    def __init__(self):
        pass
    
    def EmailInfo(self, subject, info):
        
        # Get the information from the JSON file
        current_directory = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(current_directory, 'Email.json')

        # Open file
        with open(json_file) as email_file:
            email = json.load(email_file)

        address = email['EmailAddress']  
        email_address = address["user_email"]
        
        # Information to be sent to the user, this will be changed base upon which port has been accessed
        sender =  "autohoneypotalerts@gmail.com" 
        recipient = email_address # Email to be sent to make it dynamic so the user can change it from the web page
        password = "cogm qcpi bsky kvcz"
        self.Emailsend(subject, info, sender, recipient, password)
        
    def Emailsend(self, subject, info, sender, recipient, password):
        msg = MIMEMultipart() # To define the header of the email 
        msg['Subject'] = subject # add the subject 
        msg['From'] = sender # add the sender
        msg['To'] = recipient
        msg.preamble
        
        body = MIMEText(info) # To add the data to the email
        msg.attach(body)
        # try to send message if not pass
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587) # create the smtp server
            server.starttls() # to make the server tls
            server.login(sender, password) # Login into the sending account change to OAuth if possible
            server.sendmail(sender, recipient, msg.as_string()) # send the message
            server.quit()
        except:
            pass