import re
from invoice.parsers.common import (
  date_from_match,
  float_from_match,
  int_from_match,
  MissingPropertiesError,
)


match_invoice = re.compile(r'ФАКТУРА ОРИГИНАЛ № (\d+)').search
match_invoice_date = re.compile(r'Дата на издаване (\d+)/(\d+)/(\d+)').search
# match_total_due = re.compile(r'ОБЩА ДЪЛЖИМА СУМА \s*([\d\.]+) лв').search
match_invoice_due = re.compile(f'Сума по фактура: \s*([\d\.]+) лв').search


class Parser:
  def __init__(self):
    self.invoice = None
    self.invoice_date = None
    self.invoice_due = None

  def parse_line(self, line):
    if self.invoice is None and (match := match_invoice(line)):
      self.invoice = int_from_match(match)
    elif self.invoice_date is None and (match := match_invoice_date(line)):
      self.invoice_date = date_from_match(match)
    elif self.invoice_due is None and (match := match_invoice_due(line)):
      self.invoice_due = float_from_match(match)

  def is_complete(self):
    return (
      self.invoice is not None and 
      self.invoice_date is not None and
      self.invoice_due is not None
    )
  
  def get_digest(self):
    digest = dict(
      invoice=self.invoice,
      invoice_date=self.invoice_date,
      invoice_due=self.invoice_due,
    )
    missing_properties = list(map(lambda it: it[0], filter(lambda it: it[1] is None, digest.items())))
    if missing_properties:
      raise MissingPropertiesError(','.join(missing_properties))

    return digest
   