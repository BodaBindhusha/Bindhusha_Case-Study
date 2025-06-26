# util/DBPropertyUtil.py
import configparser
class DBPropertyUtil:
    @staticmethod
    def getPropertyDict(file_name):
        config = configparser.ConfigParser()
        config.read(file_name)

        if 'mysql' not in config:
            raise Exception("Missing [mysql] section in config file.")

        return {
            'host': config.get('mysql', 'host'),
            'port': config.get('mysql', 'port'),
            'database': config.get('mysql', 'database'),
            'user': config.get('mysql', 'user'),
            'password': config.get('mysql', 'password')
        }





                