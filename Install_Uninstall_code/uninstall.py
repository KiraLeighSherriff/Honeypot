# Used to uninstall the programs when the user no longer want the honeypot on their system
import shutil
import os

# get windows username
user = os.getlogin()

# Delete the database
create_database = f'python.exe C:\\Users\\{user}\\Honeypot\Database\DeleteDatabase.py'
os.system(create_database)

# Remove the honeypots folder from the system.
shutil.rmtree("C:\\Apache24\\htdocs\\honey")
shutil.rmtree(f"C:\\Users\\{user}\\Honeypot")
