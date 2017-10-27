 UPDATE bills SET deposit=deposit-51 WHERE id='2254'
INSERT INTO fees (uid, bill_id, date, sum, dsc, ip, last_deposit, aid, vat, inner_describe, method) 
values ('2241', '2254', now(), '51', 'Отмена платежа',INET_ATON('127.0.0.1'), '69.160000', '16','0.00', 'Integra_cancel', '6')
