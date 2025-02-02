#!/usr/bin/env python3

'''
Run:
  app/electrohold.py ./data/confidential/messages/1933a81ded7ae089/attachments/310285668475_0387377905_20241110.pdf

Examples:
  file:           ./data/confidential/messages/1933a81ded7ae089/attachments/310285668475_0387377905_20241110.pdf
  invoice:        № 0387377905 / 10.11.2024
  invoice_date:   № 0387377905 / 10.11.2024
  total_due:      СУМА ЗА ПЛАЩАНЕ 30,49

'''

import collections
import datetime
import enum
import re
import sys
import operator


Kind = enum.Enum('Kind', ['invoice_id', 'invoice_date', 'total_due'])
Token = collections.namedtuple('Token', ['kind', 'value'])

Invoice = collections.namedtuple('Invoice', ['invoice_id', 'invoice_date', 'total_due'])

search_invoice_id = re.compile(r'№ (\d+) / (\d+)\.(\d+)\.(\d+)').search
parse_invoice_id = lambda line: (m := search_invoice_id(line)) and (Token(Kind.invoice_id, m.group(1)), Token(Kind.invoice_date, datetime.date(int(m.group(4)), int(m.group(3)), int(m.group(2)))))

search_total_due = re.compile(r'СУМА ЗА ПЛАЩАНЕ\s+([\d,]+)').search
parse_total_due = lambda line: (m := search_total_due(line)) and Token(Kind.total_due, float(m.group(1).replace(',', '.')))


def parse_invoice(lines):
  invoice_id, invoice_date = map(operator.attrgetter('value'), next(filter(bool, map(parse_invoice_id, lines))))
  total_due = next(filter(bool, map(parse_total_due, lines))).value
  return Invoice(invoice_id, invoice_date, total_due)


def maybe_parse_invoice(lines):
  try:
    return parse_invoice(lines)
  except:
    pass


if __name__ == '__main__':
  import argparse
  import util.pdf
  import os

  parser = argparse.ArgumentParser()
  parser.add_argument('file_path', type=str, nargs='?')
  args = parser.parse_args()
  pdf = util.pdf.Pdf(path_or_fp=args.file_path or sys.stdin)
  # print(*pdf, sep=os.linesep)
  invoice = maybe_parse_invoice(pdf)
  print('\t'.join(map(str, invoice)) if invoice else args.file_path or 'stdin', file=sys.stdout if invoice else sys.stderr)
