#!/usr/local/bin/python3
from flask import Flask, request
from integra import IntegraClass
import datetime

app = Flask(__name__)

@app.route('/check', methods=['GET'])


def check():
    ''' Запрос проверки существования лицевого счета '''
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
    data['info'] =  info
    checklog = IntegraClass.log_check(data=data)      # Логирование запроса и ответа
    return str(info)

@app.route('/pay', methods=['GET'])

def pay():
    ''' Запрос пополнения лицевого счета '''
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
    aboninfo = info.aboninfo(details.get('PayerCode'))
    status={
    'Status' : aboninfo.get('Status'),
    'NTran' : details.get('NTran'),
    'FIO' : aboninfo.get('FIO'),
    'sum' : 'Недопустимая сумма платежа. Пополнения от 50 до 5000 руб',
    }
    if int(aboninfo.get('Status')) == 0:
        if float(details.get('S')) < 50:
            print('Low')
#            aboninfo['Status'] = 106
            status['Status'] = 106
            logpay = IntegraClass.log_pay(data=details,info=status)
            print(logpay)
        elif 50 <= float(details.get('S')) <= 5000:
            pay = info.pay(details)
            print('--PAY_INFO--')
            print(pay)
            details['info'] = pay
            status['Status'] = 0
            status['Balance'] = float(pay.get('Balance'))+float(details.get('S'))
            status['sum'] = 'Успешно пополнен'
            logpay = IntegraClass.log_pay(data=details,info=status)
            print(logpay)
            print('Mid')
#        return str(pay)
        else:
            print('High')
            status['Status'] = 106
            logpay = IntegraClass.log_pay(data=details,info=status)
            print(logpay)
    elif int(aboninfo.get('Status')) == 100:
        status['Status'] = 100
        status['sum'] = 'Лицевой счет не найден !!!'
        logpay = IntegraClass.log_pay(data=details,info=status)
        print(logpay)
    elif int(aboninfo.get('Status')) == 105:
        status['Status'] = 105
        status['sum'] = 'Прием платежей запрещен !!!'
        logpay = IntegraClass.log_pay(data=details,info=status)
        print(logpay)
    else:
        status['Status'] = 106
        status['sum'] = 'Недопустимая сумма платежа !!!'
        logpay = IntegraClass.log_pay(data=details,info=status)
        print(logpay)
    return str(status)

if __name__ == '__main__':
    app.run('127.0.0.10',6969)
