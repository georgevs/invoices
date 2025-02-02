'''
Examples:
  file:           ./data/confidential/messages/1933a81ded7ae089/attachments/310285668475_0387377905_20241110.pdf
  invoice:        № 0387377905 / 10.11.2024
  invoice_date:   № 0387377905 / 10.11.2024
  total_due:      СУМА ЗА ПЛАЩАНЕ 30,49
'''

import collections
import datetime
import re


Invoice = collections.namedtuple('Invoice', ['invoice_id', 'invoice_date', 'total_due'])

search_invoice_id = re.compile(r'№ (\d+) / (\d+)\.(\d+)\.(\d+)').search
parse_invoice_id = lambda line: (m := search_invoice_id(line)) and (m.group(1), datetime.date(int(m.group(4)), int(m.group(3)), int(m.group(2))))

search_total_due = re.compile(r'СУМА ЗА ПЛАЩАНЕ\s+([\d,]+)').search
parse_total_due = lambda line: (m := search_total_due(line)) and float(m.group(1).replace(',', '.'))


def error(*args):
  raise Exception(*args)


def parse_invoice(lines):
  invoice_id, invoice_date = next(filter(bool, map(parse_invoice_id, lines)), None) or error('No invoice id/date')
  total_due = next(filter(bool, map(parse_total_due, lines)), None) or error('No total due')
  return Invoice(invoice_id, invoice_date, total_due)
