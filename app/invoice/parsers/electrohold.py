import datetime
import re
from invoice.parsers.common import (
  date_from_match,
  float_comma_from_match,
  int_from_match,
  MissingPropertiesError,
)


match_invoice_and_date = re.compile(r'№ (\d+) / (\d+)\.(\d+)\.(\d+)').search
match_total_due = re.compile(r'СУМА ЗА ПЛАЩАНЕ ([\d,]+)').search


class Parser:
  def __init__(self):
    self.invoice = None
    self.invoice_date = None
    self.total_due = None

  def parse_line(self, line):
    if self.invoice is None and (match := match_invoice_and_date(line)):
      self.invoice = int_from_match(match)
      self.invoice_date = datetime.date(int(match.group(4)), int(match.group(3)), int(match.group(2)))
    elif self.total_due is None and (match := match_total_due(line)):
      self.total_due = float_comma_from_match(match)

  def is_complete(self):
    return (
      self.invoice is not None and 
      self.invoice_date is not None and
      self.total_due is not None
    )
  
  def get_digest(self):
    digest = dict(
      invoice=self.invoice,
      invoice_date=self.invoice_date,
      total_due=self.total_due,
    )
    missing_properties = list(map(lambda it: it[0], filter(lambda it: it[1] is None, digest.items())))
    if missing_properties:
      raise MissingPropertiesError(','.join(missing_properties))

    return digest
