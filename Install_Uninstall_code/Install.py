# This script is used to "install" the code on to the system, it will take each of the file and put then in the correct path
# for the program to work correctly, this script must be launched. For better used experience the python file has been change to a 
# windows executable. It will also create the database.   

import shutil
import os
import json
import subprocess

# get the username for the windows account
user = os.getlogin()

# put the username into a json, file that is in teh web application 
# this was done, as PHP has no function that can find who the windows user is
# only how owns the scripts or the hostname of the machine
directory = 'honey'
json_file = os.path.join(directory, 'username.json')

# Open file
with open(json_file, "r") as file_user:
    data  = json.load(file_user)

# Get the proccess id of the file
data['username']['user'] = user
with open(json_file, "w") as file_user:
    json.dump(data, file_user)

# Create the database
create_database = 'python.exe Honeypot\Database\CreateDatabase.py'
os.system(create_database)

# # Move the honeypot file
protocols = shutil.move('Honeypot', f'C:\\Users\\{user}\\')
print(protocols)


# # move the web application into Xammp
webapp = shutil.move('honey', "C:\\Apache24\\htdocs")
print(webapp)

Python_setup = subprocess.run(f"cd C:\\ && cd \\Users\\{user}\\Honeypot && pip install -e. ", shell=True)

