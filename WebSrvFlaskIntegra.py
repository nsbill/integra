#!/usr/local/bin/python3
from flask import Flask, request
from integra import IntegraClass
import datetime
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)


@app.route('/')
def foo():
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    app.logger.info('Info')
    return "foo"

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
    print('__Check_DATA__')
    if data.get('PayerCode'):
        info = IntegraClass(data.get('PayerCode'))
        info = info.check(data)
        data['info'] =  info
        checklog = IntegraClass.log_check(data=data)      # Логирование запроса и ответа
        app.logger.warning('[ %s ] CHECK  %s' % (now, data))
#        app.logger.error('An error occurred')
#        app.logger.info('Info')
        return str(info)
    else:
        info = '{\'Status\': 105 }'
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
    app.logger.warning('[ %s ] PAY  %s' % (now, details))
    if details.get('PayerCode') and details.get('NTran') and details.get('DTran') and details.get('S'):
        print('__NONE__')
        info = IntegraClass(details.get('PayerCode'))  #  Выборка данных об абоненте
        aboninfo = info.aboninfo(details.get('PayerCode')) # создаем словарь 
        status={
        'Status' : aboninfo.get('Status'),
        'NTran' : details.get('NTran'),
        'FIO' : aboninfo.get('FIO'),
#    'sum' : 'Недопустимая сумма платежа. Пополнения от 50 до 5000 руб',
        }

        if int(aboninfo.get('Status')) == 0:  # проверяем статус 
            if float(details.get('S')) < 50:  # если сумма платежа меньше 50 руб.
#            print('Low')
                status['Status'] = 106
                details['Login'] = aboninfo.get('Login')
                logpay = IntegraClass.log_pay(data=details,info=status)  # логирование запроса и ответа
#            print(logpay)
            elif 50 <= float(details.get('S')) <= 5000:  #
                pay = info.pay(details)
                if int(pay.get('Status'))==105:
                    print('__pay_W__')
                    print(pay)
                    details['info'] = pay
                    status['Status'] = 0
                    status['DSC'] = pay.get('DSC')
                    details['Login'] = aboninfo.get('Login')
                    logpay = IntegraClass.log_pay(data=details,info=status)
                else:
                    details['info'] = pay
                    status['Status'] = 0
                    status['Balance'] = float(pay.get('Balance'))+float(details.get('S'))
                    status['DSC'] = 'Успешно пополнен'
                    details['Login'] = aboninfo.get('Login')
                    logpay = IntegraClass.log_pay(data=details,info=status)
#            print(logpay)
            else:
                status['Status'] = 106
                details['Login'] = aboninfo.get('Login')
                logpay = IntegraClass.log_pay(data=details,info=status)
#            print(logpay)
        elif int(aboninfo.get('Status')) == 100:
            status['Status'] = 100
            status['DSC'] = 'Лицевой счет не найден !!!'
            logpay = IntegraClass.log_pay(data=details,info=status)
            print(logpay)
        elif int(aboninfo.get('Status')) == 105:
            status['Status'] = 105
            status['DSC'] = 'Прием платежей запрещен !!!'
            logpay = IntegraClass.log_pay(data=details,info=status)
            print(logpay)
        else:
            status['Status'] = 106
            status['DSC'] = 'Недопустимая сумма платежа !!!'
            logpay = IntegraClass.log_pay(data=details,info=status)
            print(logpay)
        return str(status)
    else:
        info = '{\'Status\': 105 }'
        return str(info)


@app.route('/cancel', methods=['GET'])

def cancel():
    ''' Запрос на отмену транзакции
    http://10.10.10.10:8080/cancel?PayerCode=0502369&ServiceName=Интернет&NTran=0000125466&DTran=20170101175859&S=100
    '''
    now = datetime.datetime.now()
    data = {
        'PayerCode': request.args['PayerCode'],       # Лицевой счет, код или другой идентификатор плательщика
        'ServiceName': request.args['ServiceName'],   # Наименование услуги
        'remote_address' : request.remote_addr,       # IP адрес
        'NTran': request.args['NTran'],               # Уникальный номер транзакции
        'DTran': request.args['DTran'],               # Дата транзакции в формате ггггММддЧЧммсс
        'S': request.args['S'],                       # Сумма которую нужно отменить 
#        'date': now.strftime("%Y%m%d%H%M%S"),        # Время запроса  
        'date': now,
    }
    app.logger.warning('[ %s ] CANCEL  %s' % (now, data))
    print('__Cancel__query__')
    print(data)

    if data.get('PayerCode') and data.get('NTran') and data.get('DTran') and data.get('S'):
#    info = IntegraClass(data.get('PayerCode'))
        info = IntegraClass()
        print('__IntegraClass_Web__')
        print(info)
        info = info.cancel(data.get('NTran'),data)
        data['info'] =  info
        print('__INFO_CANCEL__')
        print(info)
#    checklog = IntegraClass.log_check(data=data)      # Логирование запроса и ответа
        return str(info)
    else:
        info = '{\'Status\': 105 }'
        return str(info)

if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run('127.0.0.10',6969)
