#!/usr/local/bin/python3
from flask import Flask, request
from integra import IntegraClass
import datetime

app = Flask(__name__)

@app.route('/check', methods=['GET'])


def check(): # Запрос проверки существования лицевого счета
    now = datetime.datetime.now()
    data = {
        'PayerCode': request.args['PayerCode'],       # Лицевой счет, код или другой идентификатор плательщика
        'ServiceName': request.args['ServiceName'],   # Наименование услуги
        'remote_address' : request.remote_addr,       # IP адрес
#        'date': now.strftime("%Y%m%d%H%M%S"),        # Время запроса  
        'date': now,
    }

    info = IntegraClass(data.get('PayerCode'))
    info = info.check(data)
#    print(info)
    data['info'] =  info
    checklog = IntegraClass.log_check(data=data)
    return str(info)

@app.route('/pay', methods=['GET'])

def pay(): # Запрос пополнения лицевого счета
    now = datetime.datetime.now()
    details = {
    'date': now,                                   # дата запроса
    'PayerCode' : request.args['PayerCode'],       # Лицевой счет, код или другой идентификатор плательщика
    'ServiceName' : request.args['ServiceName'],   # Наименование услуги
    'NTran' : request.args['NTran'],               # Уникальный номер транзакции
    'DTran' : request.args['DTran'],               # Дата транзакции в формате ггггММддЧЧммсс
    'S' : request.args['S'],                       # Сумма платежа
    'remote_address' : request.remote_addr,        # IP адрес
     }
    print(details)
    info = IntegraClass(details.get('PayerCode'))
    print('WEB info')
    info_check = info.check(details.get('PayerCode'))
    print(info_check.get('fio'))

    details['FIO'] = info_check.get('fio')
    pay = info.pay(details)
    print('--PAY_INFO--')
    print(pay)
    details['info'] = pay

    logpay = IntegraClass.log_pay(data=details)
    print(logpay)
    return str(pay)

if __name__ == '__main__':
    app.run('127.0.0.10',6969)
