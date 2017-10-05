#from mysql.connector import MySQLConnection, Error
#from main.remdb.mysql_db_conf import read_db_config
from mysql_db_conf import read_db_config
import pymysql
#import MySQLError, Error
from mysql_db_conf import read_db_config

def connect():
    """ Connect to MySQL database """
    db_config = read_db_config()

    try:
        print('Connecting to MySQL database...')
        #conn = MySQLError(**db_config)
        conn = pymysql.connect(db_config.get('host'),db_config.get('user'),db_config.get('password'),db_config.get('databases'))
#        if conn.is_connected():
#            print('connection established.')
#        else:
#            print('connection failed.')
    except pymysql.err.MySQLError:
        print(conn.error())
        print('Access denied for user')

    finally:
        conn.close()
        print('Connection closed.')

if __name__ == '__main__':
    connect()
