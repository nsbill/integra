#!/usr/local/bin/python3
from flask import Flask, request
#from mysql_select import query_check
from integra import IntegraClass 

app = Flask(__name__)

@app.route('/check', methods=['GET'])


def check(): # Запрос проверки существования лицевого счета
    PayerCode = request.args['PayerCode']       # Лицевой счет, код или другой идентификатор плательщика
    ServiceName= request.args['ServiceName']    # Наименование услуги

    info = IntegraClass(PayerCode)
    info = info.check(PayerCode)
    return str(info)

@app.route('/pay', methods=['GET'])

def pay(): # Запрос пополнения лицевого счета
    PayerCode = request.args['PayerCode']       # Лицевой счет, код или другой идентификатор плательщика
    ServiceName = request.args['ServiceName']   # Наименование услуги
    NTran = request.args['NTran']               # Уникальный номер транзакции
    DTran = request.args['DTran']               # Дата транзакции в формате ггггММддЧЧммсс
    S = request.args['S']                       # Сумма платежа

    info = IntegraClass(PayerCode)
    print(info)
    pay = info.pay(PayerCode)
    print(pay)
    return str(pay)

if __name__ == '__main__':
    app.run('127.0.0.10',6969)
