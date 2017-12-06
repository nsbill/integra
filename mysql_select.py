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

#def query_check(n):
#    try:
#        dbconfig = read_db_config()
#        conn = MySQLConnection(**dbconfig)
#        cursor = conn.cursor()
#        cursor.execute('SELECT u.uid, u.bill_id, upi.fio, u.disable \
#                        FROM users u \
#                          LEFT JOIN users_pi upi ON u.uid=upi.uid \
#                        WHERE u.bill_id=' + str(n) + ' limit 1 ')
#        u = []
#        for row in iter_row(cursor, 10):
#            u.append(row)
#
#    except Error as e:
#        print(e)
#
#    finally:
#        cursor.close()
#        conn.close()
#        return u
#    if __name__ == '__main__':
#        query_check(n)

def query_with_deposit(n):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT b.id AS bill_id, \
                            b.uid, \
                            u.id AS login, \
                            upi.fio, \
                            b.deposit AS deposit, \
                            u.disable \
                        FROM bills b \
                            LEFT JOIN users u \
                            ON (u.uid = b.uid) \
                            LEFT JOIN users_pi upi \
                            ON (u.uid=upi.uid) \
                        WHERE b.uid='+ str(n) +' limit 1 ')
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
 #       print(u)
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

def query_with_logpay(n):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
#        cursor.execute('SELECT id,payercode,status,s,DATE_FORMAT(date, "%Y%m%d%H%i%s"),info FROM integra_pay where ntran='+ str(n) +' ORDER BY -id limit 1 ')
        cursor.execute('SELECT id,payercode,status,s,DATE_FORMAT(dtran, "%Y%m%d%H%i%s"),info,ntran FROM integra_pay where ntran='+ str(n) +' ORDER BY -id limit 1 ')

        u = []
        for row in iter_row(cursor, 10):
            u.append(row)
#        print('__log_pay__')
#        print(u)
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        return u
    if __name__ == '__main__':
        query_with_logpay(n)

def query_with_logcancel(n):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute('SELECT payercode,status,DATE_FORMAT(dtran, "%Y%m%d%H%i%s"),s FROM integra_cancel where ntran='+ str(n) +' ORDER BY -id limit 1 ')

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
        query_with_logcancel(n)

def query_with_user(PayerCode):
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
#        cursor.execute('SELECT uid,id FROM users where bill_id='+ str(PayerCode) +' ORDER BY -id limit 1 ')
        cursor.execute('SELECT uid,id FROM users where uid='+ str(PayerCode) +' ORDER BY -id limit 1 ')

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
        query_with_user(PayerCode)
