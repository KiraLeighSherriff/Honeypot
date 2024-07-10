import mysql.connector
from Config.db_config import db_name, db_host, db_user, db_passwd, db_port, tables_to_check

class DatabaseDelete():
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
        
    # Delete the tables for the database
    def Delete(self, tables_to_check):
        try:
            for table_name in tables_to_check: # loop though tables
                if table_name != "web_account": # dont drop web account
                    self.mycursor.execute(f"DROP TABLE {table_name}")
        except mysql.connector.Error:
            pass
        
    # Recreate the table from the database 
    def Create(self, tables_to_check):
        try:
            # Remake the tables the where dropped
            for table_name in tables_to_check: 
                if table_name == 'all_connect': 
                    self.mycursor.execute(f"CREATE TABLE {table_name} (ID INT AUTO_INCREMENT PRIMARY KEY, Client_IP  VARCHAR(50), Port VARCHAR(50), Date DATE, Time TIME)")
                elif table_name == "http_login": 
                    self.mycursor.execute(f"CREATE TABLE {table_name} (ID INT AUTO_INCREMENT PRIMARY KEY, Client_IP  VARCHAR(50), Username VARCHAR(50), Password VARCHAR(255), Date DATE, Time TIME)")
                elif table_name == "ssh_command" or table_name == "telnet_command": 
                    self.mycursor.execute(f"CREATE TABLE {table_name} (ID INT AUTO_INCREMENT PRIMARY KEY, Date DATE, Time TIME, Command VARCHAR(250))")
                else: 
                    self.mycursor.execute(f"CREATE TABLE {table_name} (ID INT AUTO_INCREMENT PRIMARY KEY, Username VARCHAR(50), Password VARCHAR(50), Date DATE, Time TIME)")  
        except mysql.connector.Error:
                pass
        
    def CloseConnection(self):
        try:
            self.mycursor.close()
            self.db_connect.close()
        except mysql.connector.Error:
            pass
        
if __name__ == "__main__":
    db_manager = DatabaseDelete() 
    db_manager.mycursor.execute(f"USE {db_name}")  
    
    db_manager.Delete(tables_to_check) 
    db_manager.Create(tables_to_check)
    db_manager.CloseConnection