# -*- coding: utf-8 -*-
from mysql.connector import MySQLConnection, Error
from mysql_db_conf import read_db_config
#from django.shortcuts import render

def iter_row(cursor, size=10):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row

def query_check(n):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT u.uid, u.bill_id, upi.fio \
                        FROM users u \
                          LEFT JOIN users_pi upi ON u.uid=upi.uid \
                        WHERE u.bill_id=' + str(n) + ' limit 1 ')
        u = []
        for row in iter_row(cursor, 10):
            u.append(row)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return u
if __name__ == '__main__':
    query_check(n)
