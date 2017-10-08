# -*- coding: utf-8 -*-
from mysql.connector import MySQLConnection, Error
from mysql_db_conf import read_db_config
import random, datetime, re, ipaddress

now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
def iter_row(cursor, size=10):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row

def insert_with_docs_inv(n,a,u,d): # n = max_inv , a = useradmin, u = user_UID, d = deposit
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        print('===ins docs_inv===')
        print(n)
        print(a)
        print(u)
        print(d)
        now = datetime.datetime.now()
        print(now)
        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        print(now)
        now = str(now)
        date = datetime.date.today().strftime("%Y%m%d")
        docsdate = str(date)
        print(date)

        cursor.execute('INSERT INTO docs_invoices (invoice_num, date, created, customer, phone, \
                       aid, uid, payment_id, vat, deposit, delivery_status, exchange_rate, currency) \
                       values ( '+str(n)+', '+str(docsdate)+', '+ str(now) +', "-","",'+str(a)+','+str(u)+',0, 0.00,'+ str(d)+',0,0,0) ')
        print('===end ins docs_inv ===')
        all = {}

        for row in iter_row(cursor, 10):
            all = row
            print(all)
        return all
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    if __name__ == '__main__':
        insert_with_docs_inv(n,a,u,d)

def insert_with_docs_inv_orders(inv,sum): # inv = inv_docs , sum = сумма пополнения
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        print('===ins_ord===')
        print(inv)
        print(sum)
        cursor.execute('INSERT INTO docs_invoice_orders(invoice_id, orders, counts, unit, price, fees_id) \
                        values('+ str(inv) +', "", 1, 1, '+ str(sum) +', 0) ')
        print('===end ins_ord===')

        all = {}

        for row in iter_row(cursor, 10):
            all = row
            print(all)
        return all
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    if __name__ == '__main__':
        insert_with_docs_inv_orders(inv, sum)


def update_with_deposit(uid,d,sum): # uid = userUID , sum = сумма пополнения, d = депозит до пополнения
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        print('===upd deposit===')
        print(uid)
        print(d)
        print(sum)
        sum_upd = float(d) + float(sum)
        print(sum_upd)

        cursor.execute('UPDATE bills SET deposit='+ str(sum_upd) +' WHERE uid='+ str(uid) +' ')
        print('===end upd deposit===')

        all = {}

        for row in iter_row(cursor, 10):
            all = row
            print(all)
        return all
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    if __name__ == '__main__':
        update_with_deposit(uid, d, sum)

def insert_with_payment(uid,bill_id,sum,ip,d,aid): # uid = userUID , sum = сумма пополнения, d = депозит до пополнения, ip = IPAddress
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        print('===ins payments===')
        print(uid)
        print(d)
        print(sum)
        print(ip)
        # now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        print(now)
        ip = str(ip)
        ip = int(ipaddress.IPv4Address(ip))
        print(ip)
        cursor.execute('INSERT INTO payments (uid, bill_id, date, sum, dsc, ip, last_deposit, aid, method, ext_id, \
                                    inner_describe, amount, currency) \
                        values ('+ str(uid) +', '+ str(bill_id) +', '+ str(now) +', '+ str(sum) +', "", '+str(ip)+', \
                         '+ str(d) +', '+ str(aid) +', 2,"", "", '+ str(sum) +', 0 ) ')

        print('===end ins payments===')
        all = {}

        for row in iter_row(cursor, 10):
            all = row
            print(all)
        return all
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    if __name__ == '__main__':
        insert_with_payment(uid,sum,ip,d)



def insert_with_docs_invoice2payments(inv,p,sum): # inv = invoice_id, p = payment_id, sum = сумма пополнения
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        print('===ins docs_invoice2payments===')
        print(inv)
        print(p)
        print(sum)

        cursor.execute('INSERT INTO docs_invoice2payments (invoice_id, payment_id, sum) \
                        VALUES ('+ str(inv) +', '+ str(p) +', '+ str(sum) +') ')
        print('===end ins docs_invoice2payments===')

        all = {}

        for row in iter_row(cursor, 10):
            all = row
            print(all)
        return all
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    if __name__ == '__main__':
        insert_with_docs_invoice2payments(inv, p, sum)

def ins_integra_check(data): # uid = userUID , sum = сумма пополнения, d = депозит до пополнения, ip = IPAddress
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
#        print('===ins integra_check===')
        time = data.get('date').strftime("%Y%m%d%H%M%S") # время запроса
        payer_code = str(data.get('PayerCode'))          # лицевой счет
        service_name = data.get('ServiceName')           # наименование услуги
        st = data.get('info')                            # 
        st = int(st.get('Status'))                       # статус ответа запроса
        info_conn = str(data.get('info'))                # ответ на запрос
        ip = data.get('remote_address')                  # запрос с какого ip адреса
#        ip = ipaddress.IPv4Address(str(ip))
        cursor.execute("""INSERT INTO integra_check (date,payercode,sevicename,status,info,ip) values (%s,%s,%s,%s,%s,%s)""",(time,payer_code,service_name,st,info_conn,ip))
#        print('=== end ins integra_check ===')
        all = {}

        for row in iter_row(cursor, 10):
            all = row
#            print(all)
        return all
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    if __name__ == '__main__':
        ins_integra_check(data)

def ins_integra_pay(data): # uid = userUID , sum = сумма пополнения, d = депозит до пополнения, ip = IPAddress
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        print('===ins integra_pay ===')
        print(data)
        time = data.get('date').strftime("%Y%m%d%H%M%S") # время запроса
        payer_code = str(data.get('PayerCode'))          # лицевой счет
        service_name = data.get('ServiceName')           # наименование услуги
        st = str(data.get('info'))                            # 
        st = int(data.get('Status'))                       # статус ответа запроса
        ntran = data.get('NTran')                        # уникальный номер транзакции
        dtran = data.get('DTran')                        # дата транзакции
        s = data.get('S')                                # сумма платежа
        login = data.get('login')                        # логин пользователя
        uid = data.get('uid')                            # UID пользователя
        info_conn = str(data.get('info'))                # ответ на запрос
        print('---INFO---')
        print(info_conn)
#        info_conn['login'] = str(login)
#        info_conn['uid'] = str(uid)
        ip = data.get('remote_address')                  # запрос с какого ip адреса
#        ip = ipaddress.IPv4Address(str(ip))
        cursor.execute("""INSERT INTO integra_pay (date,payercode,sevicename,status,ntran,dtran,s,info,ip,login) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(time,payer_code,service_name,st,ntran,dtran,s,info_conn,ip,login))
        print(data)
        print('=== end ins integra_pay ===')
        all = {}

        for row in iter_row(cursor, 10):
            all = row
#            print(all)
#        return all
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    if __name__ == '__main__':
         ins_integra_pay(data)
