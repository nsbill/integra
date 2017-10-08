from mysql_select import query_check, query_with_deposit, query_with_invmax, query_with_docs_inv, query_with_payment # Подключения базы данных и выборка данных о пользователе.
from mysql_insert import insert_with_docs_inv, insert_with_docs_inv_orders, update_with_deposit, insert_with_payment, insert_with_docs_invoice2payments, ins_integra_check, ins_integra_pay
import random, datetime

class IntegraClass:
    ''' Протокол информационного взаимодейсвия субъектов платёжной системы '''

    def __init__(self,n=0):
        self.numbers = n
        self.check(n)

    def log_check(data):
        ins_data = ins_integra_check(data)
#        print(data)
        return data

    def log_pay(data):
        print('---LOG_PAY---')
        ins_data = ins_integra_pay(data)
        print(ins_data)
        return ins_data

    def check(self,n):           # Запрос проверки существования лицевого счета
        self.user = query_check(self.numbers)
        self.users = dict()
        if self.user:           # Проверка пользователя
            for value in self.user:
                self.users['Status'] = 0
#                self.users['uid'] = value[0]
#                self.users['PayerCode'] = value[1]
                self.users['fio'] = value[2]

            return self.users
        else:
            self.users['Status'] = 100
#            print(self.users)
        return self.users

    def pay(self,details):             # Запрос пополнения лицевого счета
        if self.users.get('Status') == 0:
            aid = 19             # id администратора в биллинге
            deposit = query_with_deposit(n=details.get('PayerCode'))
            details['balance'] = deposit[0][1]
            details['login'] = deposit[0][2]
            details['uid'] = deposit[0][3]
            details['Status'] = 0
            details['FIO'] = details.get('FIO')
            print (deposit[0][3])
            invmax = query_with_invmax()
            print(invmax)
            print(details)
            n = invmax[0][0]
            n = n + 1
            print(n)
            ins_docs_inv = insert_with_docs_inv(n=n, a=aid, u=details.get('uid'), d=details.get('balance'))  # вставка в docs_invoices
            print(ins_docs_inv)
            doc_inv = query_with_docs_inv(n=details.get('uid'))
            print(doc_inv)
            inv = doc_inv[0][0]
            ins_docs_ord = insert_with_docs_inv_orders(inv=inv, sum=details.get('S'))
            print(ins_docs_ord)
            upd = update_with_deposit(uid=details.get('uid'), d=details.get('balance'), sum=details.get('S'))
            print(upd)
            ins_payment = insert_with_payment(uid=details.get('uid'), bill_id=details.get('PayerCode'), sum=details.get('S'), ip=details.get('remote_address'), d=details.get('balance'), aid=aid)
            print(ins_payment)
            p = query_with_payment(n=details.get('uid'))
            print(p)

            print('---details---')
            print(details)
            responce={}
            responce['Status'] = details.get('Status')
            responce['Ntran'] = details.get('NTran')
            responce['FIO'] = details.get('FIO')
            responce['Balance'] = details.get('balance')
            return responce
        else:
            details['Status'] = 100
            print('Status 100 PAY')
        print('---PAY_USERS---')
        print(self.users)
        return self.users

    def reconciliation(self):  # Запрос на сверку взаиморасчетов
        pass

    def cancel(self):          # Запрос на отмену пополнения лицевого счета
        pass

if __name__ == '__main__':
   IntegraClass()

# def mwhere(self,n):
#           if n <= 0:
#                self.where = "отсутствуют"
#           elif 0 < n < 100:
#                self.where = "малый склад"
#           else:
#                self.where = "основной склад"
#
#      def plus(self,p):
#           self.numbers = self.numbers + p
#           self.mwhere(self.numbers)
#      def minus(self,m):
#           self.numbers = self.numbers - m
#           self.mwhere(self.numbers)
#
# m1 = Building("доски", "белые",50)
# m2 = Building("доски", "коричневые", 300)
# m3 = Building("кирпичи","белые")
#
# print (m1.what,m1.color,m1.where)
# print (m2.what,m2.color,m2.where)
# print (m3.what,m3.color,m3.where)
#
# m1.plus(500)
# print (m1.numbers, m1.where)

'''
Приложение 1
Типы запросов к субъекту платежной системы
Имя типа       |    Описание
check          | Запрос проверки существования лицевого счета
pay            | Запрос пополнения лицевого счета
reconciliation | Запрос на сверку взаиморасчетов
cancel         | Запрос на отмену пополнения лицевого счета

Приложении 2
Список параметров, передаваемых в запросах и ответах

Наименование   |    Описание
 параметра     |

ServiceName    | Наименование услуги
PayerCode      | Лицевой счет, код или другой идентификатор плательщика
NTran          | Уникальный номер транзакции
DTran          | Дата транзакции в формате ггггММддЧЧммсс
S              | Сумма платежа
FIO            | Фамилия Имя Отчество
Adr            | Адрес плательщика
Status         | Результат выполнения запроса
Balance        | Баланс лицевого счета
DStart         | Дата начала
DStop          | Дата окончания

Приложении 3
Статусы результатов обработки запросов

Статус         |   Описание
0              | Запрос выполнен успешно
100            | Лицевой счет не найден
105            | Приём платежа запрещён
106            | Недопустимая сумма платежа

------------------------------------------------------------------------------------------------------------------------
Запрос типа "check":

Структура GET запроса, направляемого субъекту платежной системы
GET &lt;path&gt;/&lt;request_type&gt;?&lt;param1=val1&amp; …&amp;paramN=valN&gt;
где:
&lt;path&gt; – URL адрес субъекта платежной системы;
&lt;request_type&gt; – тип запроса (перечень типов запросов и их описание определено в
приложении 1);
&lt;param1=val1&amp;…&amp;paramN=valN&gt; – передаваемые параметры запроса и их значения
определены в приложении 2.

Пример запроса:
http://10.10.10.10:8080/check?PayerCode=0502369&ServiceName=Интернет
Пример ответа:
{
"Status": "0",
"FIO": "Иванов Иван Иванович"
}
------------------------------------------------------------------------------------------------------------------------
Запрос типа "pay":
Запрос должен включать следующие обязательные параметры: “PayerCode”,
“ServiceName”, “NTran”, “DTran”, “S” (описание параметров приведено в приложении 2)

Пример запроса:
http://10.10.10.10:8080/pay?PayerCode=0502369&ServiceName=Интернет&NTran=0000125466&DTran=20170101175859&S=100

Пример ответа:
{
"Status": "0" ;,
"NTran": "0000125466",
"FIO": "Иванов Иван Иванович"
}
------------------------------------------------------------------------------------------------------------------------
Запрос типа “cancel”:
Запрос должен включать следующие обязательные параметры: “PayerCode”,
“ServiceName”, “NTran”, “DTran”, “S” (описание параметров приведено в приложении 2).
Пример запроса:
http://10.10.10.10:8080/cancel?PayerCode=0502369&ServiceName=Интернет&NTran=0000125466&DTran=20170101175859&S=100
Пример ответа:
{
"Status": "0",
"NTran": &quot;0000125466",
"FIO": "Иванов Иван Иванович"
}
'''
