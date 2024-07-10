import mysql.connector
from datetime import date
import time

from Database.Config.db_config import (db_host, db_user, db_passwd, db_name, db_port,
table_6, table_7)

class SSHInsert:   
    def __init__(self):
        self.ssh_pool = self.CreatePool()
        self.Date = date.today() 
        local = time.localtime()
        self.Time = time.strftime("%H:%M:%S", local)

    def CreatePool(self):
        connection_db = {"host": db_host,
                        "user": db_user,
                        "port": db_port,
                        "passwd": db_passwd,
                        "database" : db_name}
        # create the pool of connections with a size of 8
        ssh_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "ssh_pool",
                pool_size = 8, 
                pool_reset_session=True, 
                autocommit=True, 
                **connection_db )

        return ssh_pool
    
    # enter the username and password to the database
    def SSHLogin(self, Username, Password):
        try:
            # get a connection 
            db_connect = self.ssh_pool.get_connection()
            # make a cursor
            mycursor = db_connect.cursor()
            mycursor.execute(f"USE {db_name}")
            mycursor.execute(f"INSERT INTO {table_6} (Username, Password, Date, Time) VALUES (%s, %s, %s, %s)", (Username, Password, self.Date, self.Time))
            mycursor.close()
            db_connect.close()    
        except mysql.connector.Error:
            pass
                
            # enter the commands to teh database
    def SSHCommands(self, Command):
        try:
            db_connect = self.ssh_pool.get_connection()
            mycursor = db_connect.cursor()
            mycursor.execute(f"USE {db_name}")
            mycursor.execute(f"INSERT INTO {table_7} (Date, Time, Command) VALUES (%s, %s, %s)", (self.Date, self.Time, Command))
            mycursor.close()
            db_connect.close()
        except mysql.connector.Error:
           pass
    