import mysql.connector
from Config.db_config import db_name, db_host, db_user, db_passwd, db_port, tables_to_check

class DatabaseManager():
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

    def CreateDatabase(self, db_name):
        try:
            # runs the database command
            self.mycursor.execute("SHOW DATABASES")
            # get the all teh results
            database = self.mycursor.fetchall()
            # if the database name "honeypot" is within the fetch results pass else create the table
            if db_name in database:
                pass
            else:
                # execute the create database mysql command
                self.mycursor.execute(f"CREATE DATABASE {db_name}")
        except mysql.connector.Error:
           pass

    def TableCreate(self, tables_to_check):
        
        
        try:
            # loop through all the tables in the table_to_check table list
            for table_name in tables_to_check:
                # get all the tables
                self.mycursor.execute(f"USE {db_name}") 
                self.mycursor.execute(f"SHOW TABLES")
                # fetch the results 
                table_exists = self.mycursor.fetchall()
                # if the exists then pass else the table should be created
                if tables_to_check in table_exists:
                    pass
                elif table_name == 'all_connect':
                        self.mycursor.execute(f"CREATE TABLE {table_name} (ID INT AUTO_INCREMENT PRIMARY KEY, Client_IP  VARCHAR(50), Port VARCHAR(50), Date DATE, Time TIME)")
                elif table_name == "http_login": 
                    self.mycursor.execute(f"CREATE TABLE {table_name} (ID INT AUTO_INCREMENT PRIMARY KEY, Client_IP  VARCHAR(50), Username VARCHAR(50), Password VARCHAR(255), Date DATE, Time TIME)")
                elif table_name == "web_account": 
                    self.mycursor.execute(f"CREATE TABLE {table_name} (ID INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50), password VARCHAR(255))")
                elif table_name == "ssh_command" or table_name == "telnet_command": 
                    self.mycursor.execute(f"CREATE TABLE {table_name} (ID INT AUTO_INCREMENT PRIMARY KEY, Date DATE, Time TIME, Command VARCHAR(250))")
                else: 
                    self.mycursor.execute(f"CREATE TABLE {table_name} (ID INT AUTO_INCREMENT PRIMARY KEY, Username VARCHAR(50), Password VARCHAR(50), Date DATE, Time TIME)")  
        except mysql.connector.Error:
            pass
    
    # close the connection once all everything is done
    def CloseConnection(self):
        try:
            self.mycursor.close()
            self.db_connect.close()
        except mysql.connector.Error:
            pass
        
manager = DatabaseManager() 
manager.CreateDatabase(f"{db_name}") 
manager.TableCreate(tables_to_check) 
manager.CloseConnection()