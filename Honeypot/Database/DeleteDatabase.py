# This is different from the flush database as that is to remove all data by deleting the table them remake, them
# this file is part of the uninstall process when the user no longer want to have the honeypot on their system

from Database.Config.db_config import db_name, db_host, db_user, db_passwd, db_port
import mysql.connector

class DeleteDatabase():
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
    
    def Delete(self):
        try:
            # Drop the database
            self.mycursor.execute(f"DROP DATABASE {db_name}")
        except mysql.connector.Error:
            pass
        
        # close the connection
    def CloseConnection(self):
        self.mycursor.close()
        self.db_connect.close()

if __name__ == "__main__":
    start = DeleteDatabase()
    start.Delete()
    start.CloseConnection()
