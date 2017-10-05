from mysql_select import query_check query_with_deposit query_with_invmax query_with_docs_inv query_with_payment # Подключения базы данных и выборка данных о пользователе.
from mysql_insert import insert_with_docs_inv insert_with_docs_inv_orders update_with_deposit insert_with_payment insert_with_docs_invoice2payments
import random, datetime

class IntegraClass:
    ''' Протокол информационного взаимодейсвия субъектов платёжной системы '''

    def __init__(self,n=0):
        self.numbers = n
        self.check(n)
#        return print(self.check(n))

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

    def pay(self,p):             # Запрос пополнения лицевого счета
        if self.users.get('Status') == 0:
            self.PayerCode = p
            aid = 19             # id администратора в биллинге
            self.check(p)
            print(self.check(p))
            print(self.PayerCode)
            print('Status 0')
            print('--- dict pay ---')
            self.users['ServiceName'] = 'Internet'
            self.users['PayerCode'] = self.numbers
            print('--- dict end pay ---')
            print(self.users)
        else:
            print('Status 100')

    def reconciliation(self):  # Запрос на сверку взаиморасчетов
        pass

    def cancel(self):          # Запрос на отмену пополнения лицевого счета
        pass

if __name__ == '__main__':
   IntegraClass()

#    def pay(self,p):             # Запрос пополнения лицевого счета
#        if self.users.get('Status') == 0:
#            now = datetime.datetime.now()
#            #print(self.users)
#            #print(p)
#            print('Status 0')
#            print('--- dict pay ---')
#            self.users['ServiceName'] = 'Internet'
#            self.users['PayerCode'] = self.numbers
#            l = list('123456789')
#            random.shuffle(l)
#            psw = ''.join([random.choice(l) for x in range(10)])
#            self.users['NTran'] = psw
#            self.users['DTran'] = now.strftime("%Y%m%d%H%M%S")
#            self.users['S'] = p
#            print('--- dict end pay ---')
#            print(self.users)
#        else:
#            print('Status 100')
#        #print(self.users)
#        #self.numbers = self.numbers + p
#        #self.s = self.check(p)
#        #print(self.s)
#
 
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
