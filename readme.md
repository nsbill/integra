### Приложение 1
Типы запросов к субъекту платежной системы

|   Имя типа    |Описание                                     |
|---------------|---------------------------------------------|
|check          |Запрос проверки существования лицевого счета |
|pay            |Запрос пополнения лицевого счета             |
|reconciliation |Запрос на сверку взаиморасчетов              |
|cancel         |Запрос на отмену пополнения лицевого счета   |

### Приложении 2
Список параметров, передаваемых в запросах и ответах

|Наименование параметра|Описание                                              |
|----------------------|------------------------------------------------------|
|ServiceName           |Наименование услуги                                   |
|PayerCode             |Лицевой счет, код или другой идентификатор плательщика|
|NTran                 |Уникальный номер транзакции                           |
|DTran                 |Дата транзакции в формате ггггММддЧЧммсс              |
|S                     |Сумма платежа                                         |
|FIO                   |Фамилия Имя Отчество                                  |
|Adr                   |Адрес плательщика                                     |
|Status                |Результат выполнения запроса                          |
|Balance               |Баланс лицевого счета                                 |
|DStart                |Дата начала                                           |
|DStop                 |Дата окончания                                        |

### Приложении 3
Статусы результатов обработки запросов

|Статус|        Описание           |
|------|---------------------------|
|  0   | Запрос выполнен успешно   |
| 100  | Лицевой счет не найден    |
| 105  | Приём платежа запрещён    |
| 106  | Недопустимая сумма платежа|

------------------------------------------------------------------------------------------------------------------------
Запрос типа "check":

Структура GET запроса, направляемого субъекту платежной системы
```
GET &lt;path&gt;/&lt;request_type&gt;?&lt;param1=val1&amp; …&amp;paramN=valN&gt;
```
где:
`&lt;path&gt;` – URL адрес субъекта платежной системы;
`&lt;request_type&gt;` – тип запроса (перечень типов запросов и их описание определено в
приложении 1);
`&lt;param1=val1&amp;…&amp;paramN=valN&gt;` – передаваемые параметры запроса и их значения
определены в приложении 2.

Пример запроса:
http://10.10.10.10:8080/check?PayerCode=0502369&ServiceName=Интернет

```SQL
UPDATE bills SET deposit=deposit-51 WHERE id='2254'
INSERT INTO fees (uid, bill_id, date, sum, dsc, ip, last_deposit, aid, vat, inner_describe, method) 
values ('2241', '2254', now(), '51', 'Отмена платежа',INET_ATON('127.0.0.1'), '69.160000', '16','0.00', 'Integra_cancel', '6')
```
requirements.txt 
```Package                   Version               
------------------------- ----------------------
chardet                   2.3.0                 
Click                     7.0                   
command-not-found         0.3                   
configparser              3.5.0                 
connection-pool           0.0.2                 
Flask                     1.0.2                 
Flask-MySQL               1.4.0                 
get                       2018.11.19            
itsdangerous              1.1.0                 
Jinja2                    2.10                  
language-selector         0.1                   
MarkupSafe                1.1.0                 
mysql-connector-python-rf 2.2.2                 
pip                       18.1                  
post                      2018.11.20            
public                    2018.11.20            
pycurl                    7.43.0                
pygobject                 3.20.0                
PyMySQL                   0.9.3                 
pymysql-manager           0.0.2                 
python-apt                1.1.0b1+ubuntu0.16.4.2
python-debian             0.1.27                
python-systemd            231                   
query-string              2018.11.20            
request                   2018.11.20            
requests                  2.9.1                 
setuptools                20.7.0                
six                       1.10.0                
ssh-import-id             5.5                   
ufw                       0.35                  
unattended-upgrades       0.1                   
urllib3                   1.13.1                
Werkzeug                  0.14.1                
wheel                     0.29.0               
```
