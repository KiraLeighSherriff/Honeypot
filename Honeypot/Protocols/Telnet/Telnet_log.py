import mysql.connector
import time
from datetime import date

from Database.Config.db_config import (db_host, db_user, db_passwd, db_name, db_port,
table_3, table_4)

class TelnetInsert:   
    def __init__(self):
        self.telnet_pool = self.CreatePool()
        self.Date = date.today() 
        local = time.localtime()
        self.Time = time.strftime("%H:%M:%S", local)

    def CreatePool(self):
        connection_db = {"host": db_host,
                        "user": db_user,
                        "port": db_port,
                        "passwd": db_passwd,
                        "database" : db_name}
        
        telnet_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "telnet_pool",
                pool_size = 6, 
                pool_reset_session=True, 
                autocommit=True, 
                **connection_db )

        return telnet_pool
    
    # Inset data into the ssh_login table, for name and passwords tried.
    def TelnetLogin(self, Username, Password):
        try:
            db_connect = self.telnet_pool.get_connection()
            mycursor = db_connect.cursor()
            mycursor.execute(f"USE {db_name}")
            mycursor.execute(f"INSERT INTO {table_3}  (Username, Password, Date, Time) VALUES (%s, %s, %s, %s)", (Username, Password, self.Date, self.Time))
            mycursor.close()
            db_connect.close()
        except mysql.connector.Error:
            pass
            
            
    def TelnetCommands(self, Command):
        try:
            db_connect = self.telnet_pool.get_connection()
            mycursor = db_connect.cursor()
            mycursor.execute(f"USE {db_name}")
            mycursor.execute(f"INSERT INTO {table_4} (Date, Time, Command) VALUES (%s, %s, %s)", (self.Date, self.Time, Command))
            mycursor.close()
            db_connect.close() 
        except mysql.connector.Error:
            pass