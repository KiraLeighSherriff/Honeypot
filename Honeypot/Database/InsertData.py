import mysql.connector
from datetime import date
import time

from .Config.db_config import db_host, db_user, db_passwd, db_name, db_port, table_1

class InsertData:   
    def __init__(self):
        self.honeypot_pool = self.CreatePool()
        self.Date = date.today() 
        local = time.localtime()
        self.Time = time.strftime("%H:%M:%S", local)
       # Create a pool of connections, better efficiency of database 
    # After use all connects are close so they can be brought back to the pool
    # to be reused
    
    def CreatePool(self):
        connection_db = {"host": db_host,
                        "user": db_user,
                        "port": db_port,
                        "passwd": db_passwd,
                        "database" : db_name}
        
        # Create a pool of connections to help with the flow of fast insertion 
        honeypot_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name = "honey_pool",
                pool_size = 18, 
                pool_reset_session=True, 
                autocommit=True, 
                **connection_db )

        return honeypot_pool
    
        # Logs port that have had an access attempt    
    def OtherPorts(self, Client_IP, Port):
        try:
            con = self.honeypot_pool.get_connection()
            mycursor = con.cursor()
            mycursor.execute(f"USE {db_name}")
            mycursor.execute(f"INSERT INTO {table_1} (Client_IP, Port, Date, Time) VALUES (%s, %s, %s, %s)", (Client_IP, Port, self.Date, self.Time))
            mycursor.close()
            con.close()     
        except mysql.connector.Error:
            pass
    
                  
