'''
Examples:
  file:           ./data/confidential/messages/1945b12c55013405/attachments/1102616307.pdf
  invoice:        ФАКТУРА № 1102576833   - ОРИГИНАЛ
  invoice_date:   Дата на издаване/Дата на данъчно събитие - 30.09.2024 г.
  total_due:      ВСИЧКО по фактура:     55,78

  file:           ./data/confidential/messages/18ddc60039116e90/attachments/05-31-1301465642.pdf
  invoice:        № 1301465642 - ОРИГИНАЛ
  invoice_date:   Дата на издаване/ Дата на данъчно събитие - 31.05.2022 г.
  total_due:      ДЪЛЖИМА СУМА 1.39

  file:           ./data/confidential/messages/190ba854bbd84695/attachments/1032674463.pdf
  invoice:        № 1032674463 – Оригинал
  invoice_date:   Дата на издаване/Дата на данъчно събитие - 30.06.2024г.
  total_due:      Сума за плащане по обща фактура 164,21 лв.
'''

import collections
import datetime
import re


Invoice = collections.namedtuple('Invoice', ['invoice_id', 'invoice_date', 'total_due'])

search_invoice_id = re.compile(r'№ (\d+)\s+- ОРИГИНАЛ').search
search_invoice_id_2 = re.compile(r'№ (\d+)\s+– Оригинал').search
parse_invoice_id = lambda line: (m := search_invoice_id(line) or search_invoice_id_2(line)) and m.group(1)

search_invoice_date = re.compile(r'Дата на данъчно събитие - (\d+)\.(\d+)\.(\d+)\s*г\.').search
parse_invoice_date = lambda line: (m := search_invoice_date(line)) and datetime.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))

search_total_due = re.compile(r'ВСИЧКО по фактура:?\s+([\d\.,]+)').search
search_total_due_2 = re.compile(r'ДЪЛЖИМА СУМА\s+([\d\.,]+)').search
search_total_due_3 = re.compile(r'Всичко по фактура\s+([\d\.,]+)').search
search_total_due_4 = re.compile(r'обща фактура на стойност\s+([\d\.,]+)').search
parse_total_due = lambda line: (
  (m := search_total_due(line) or 
        search_total_due_2(line) or 
        search_total_due_3(line) or
        search_total_due_4(line)) and 
  float(m.group(1).replace(',', '.'))
)


def error(*args):
  raise Exception(*args)


def parse_invoice(lines):
  invoice_id = next(filter(bool, map(parse_invoice_id, lines)), None) or error('No invoice id')
  invoice_date = next(filter(bool, map(parse_invoice_date, lines)), None) or error('No invoice date')
  total_due = next(filter(bool, map(parse_total_due, lines)), None) or error('No total due')
  return Invoice(invoice_id, invoice_date, total_due)
