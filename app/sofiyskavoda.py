#!/usr/bin/env python3

'''
Run:
  app/sofiyskavoda.py ./data/confidential/messages/1946f2799c11e6ad/attachments/0000000137766010_signed.pdf

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
import enum
import re
import sys


Kind = enum.Enum('Kind', ['invoice_id', 'invoice_date', 'total_due'])
Token = collections.namedtuple('Token', ['kind', 'value'])

Invoice = collections.namedtuple('Invoice', ['invoice_id', 'invoice_date', 'total_due'])

search_invoice_id = re.compile(r'ОРИГИНАЛ № (\d+)').search
parse_invoice_id = lambda line: (m := search_invoice_id(line)) and Token(Kind.invoice_id, m.group(1))

search_invoice_date = re.compile(r'Дата на издаване (\d+)/(\d+)/(\d+)').search
parse_invoice_date = lambda line: (m := search_invoice_date(line)) and Token(Kind.invoice_date, datetime.date(int(m.group(3)), int(m.group(2)), int(m.group(1))))

search_total_due = re.compile(r'ОБЩА ДЪЛЖИМА СУМА\s+(-?[\d+\.]+)').search
parse_total_due = lambda line: (m := search_total_due(line)) and Token(Kind.total_due, float(m.group(1)))


def parse_invoice(lines):
  invoice_id = next(filter(bool, map(parse_invoice_id, lines))).value
  invoice_date = next(filter(bool, map(parse_invoice_date, lines))).value
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
