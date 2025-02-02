'''
Examples:
  file:           ./data/confidential/messages/1946f2799c11e6ad/attachments/0000000137766010_signed.pdf
  invoice:        ФАКТУРА ОРИГИНАЛ № 0137766010
  invoice_date:   Дата на издаване 15/01/2025
  total_due:      ОБЩА ДЪЛЖИМА СУМА           7.39 лв

  file:           ./data/confidential/messages/18ddca70d807feb5/attachments/2021-02-12-0103406574-izravnitelna.pdf
  invoice:        КРЕДИТНО ИЗВЕСТИЕ ОРИГИНАЛ № 0103406574
  invoice date:   Дата на издаване 12/02/2021
  total_due:      ОБЩА ДЪЛЖИМА СУМА         -22.03 лв
'''

import collections
import datetime
import re


Invoice = collections.namedtuple('Invoice', ['invoice_id', 'invoice_date', 'total_due'])

search_invoice_id = re.compile(r'ОРИГИНАЛ № (\d+)').search
parse_invoice_id = lambda line: (m := search_invoice_id(line)) and m.group(1)

search_invoice_date = re.compile(r'Дата на издаване (\d+)/(\d+)/(\d+)').search
parse_invoice_date = lambda line: (m := search_invoice_date(line)) and datetime.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))

search_total_due = re.compile(r'ОБЩА ДЪЛЖИМА СУМА\s+(-?[\d+\.]+)').search
parse_total_due = lambda line: (m := search_total_due(line)) and float(m.group(1))


def error(*args):
  raise Exception(*args)


def parse_invoice(lines):
  invoice_id = next(filter(bool, map(parse_invoice_id, lines)), None) or error('No invoice id')
  invoice_date = next(filter(bool, map(parse_invoice_date, lines)), None) or error('No invoice date')
  total_due = next(filter(bool, map(parse_total_due, lines)), None) or error('No total due')
  return Invoice(invoice_id, invoice_date, total_due)
