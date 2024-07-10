import mysql.connector
import time
from datetime import date

from Database.Config.db_config import (db_host, db_user, db_passwd, db_name, db_port,
table_2)

class HTTPInsert:   
    def __init__(self):
        self.http_pool = self.CreatePool()
        self.Date = date.today() 
        local = time.localtime()
        self.Time = time.strftime("%H:%M:%S", local)

    def CreatePool(self):
        connection_db = {"host": db_host,
                        "user": db_user,
                        "port": db_port,
                        "passwd": db_passwd,
                        "database" : db_name}
        
        http_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "http_pool",
                pool_size = 6, 
                pool_reset_session=True, 
                autocommit=True, 
                **connection_db )

        return http_pool
    
    
    def HTTPLogin(self, Client_IP, Username, Password):
        try:
            db_connect = self.http_pool.get_connection()
            mycursor = db_connect.cursor()
            mycursor.execute(f"USE {db_name}")
            mycursor.execute(f"INSERT INTO {table_2} (Client_IP, Username, Password, Date, Time) VALUES (%s, %s, %s, %s, %s)", (Client_IP, Username, Password, self.Date, self.Time))
            mycursor.close()
            db_connect.close()
        except mysql.connector.Error:
            pass
