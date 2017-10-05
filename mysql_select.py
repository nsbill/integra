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

def query_with_deposit(n):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT b.id AS bill_id, \
                            b.deposit AS deposit, \
                            u.id AS login, b.uid, b.company_id \
                        FROM bills b \
                            LEFT JOIN users u \
                            ON(u.uid = b.uid) \
                        WHERE b.id='+ str(n) +' limit 1 ')
                        # WHERE u.uid=" + str(n) + " limit 1 ")
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
        query_with_deposit(n)

def query_with_invmax():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT max(d.invoice_num), count(*) \
                        FROM docs_invoices d \
                        WHERE YEAR(date)=YEAR(now())')

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
        query_with_invmax()

def query_with_docs_inv(n):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM docs_invoices where uid='+ str(n) +' ORDER BY -invoice_num limit 1')
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
        query_with_docs_inv(n)

def query_with_payment(n):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT id,uid,last_deposit FROM payments where uid='+ str(n) +' ORDER BY -id limit 1 ')

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
        query_with_payment(n)