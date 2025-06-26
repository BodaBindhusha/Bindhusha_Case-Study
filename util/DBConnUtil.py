# util/DBConnUtil.py
from util.DBPropertyUtil import DBPropertyUtil
import mysql.connector
class DBConnUtil:
    @staticmethod
    def getConnection():
        try:
            props = DBPropertyUtil.getPropertyDict("config.properties")
            connection = mysql.connector.connect(
                host=props['host'],
                port=int(props['port']),
                database=props['database'],
                user=props['user'],
                password=props['password']
            )
            return connection
        except mysql.connector.Error as err:
            print(f"Database connection failed: {err}")
            raise

