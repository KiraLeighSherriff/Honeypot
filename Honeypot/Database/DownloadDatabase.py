import mysql.connector
import csv
import os
from Config.db_config import db_name, db_host, db_user, db_passwd, db_port, tables_to_check

class DownloadDatabase():
    def __init__(self): 
        try: 
            self.db_connect = mysql.connector.connect(
                host=db_host,
                user=db_user,
                port=db_port,
                passwd=db_passwd
            )
            self.mycursor = self.db_connect.cursor()
        except mysql.connector.Error:
            pass
    
    # Download the database tables in CVS formate
    def Download(self, tables_to_check):
        
        username = os.getlogin() # get windows username
        download_path = f'C:\\Users\\{username}\\Downloads\\honeypot_data\\'   # file path where they will be downloaded to
        
        try:
            os.mkdir(download_path)  # Make the folder to store the download csv files
        except OSError: # for if the folder is already created
            pass
        
        # get the database content
        try:
            for table_name in tables_to_check:
                # Dont download the web account 
                if table_name != "web_account":
                    self.mycursor.execute(f"SELECT * FROM {table_name}") # execute the MySQL command
                    with open(f'{download_path}{table_name}.csv', 'w') as files: # get the folder path and create and write to the the file
                        writer = csv.writer(files) # call the writer function in csv import
                        writer.writerow([ i[0] for i in self.mycursor.description ]) # get column names 
                        writer.writerows(self.mycursor.fetchall()) # get the the data from the database command
        except mysql.connector.Error:
                pass
            
            
    def CloseConnection(self):
        try:
            self.mycursor.close()
            self.db_connect.close()
        except mysql.connector.Error:
            pass
    
if __name__ == "__main__":
    db_manager = DownloadDatabase() 
    db_manager.mycursor.execute(f"USE {db_name}")  
    db_manager.Download(tables_to_check)
    db_manager.CloseConnection
    