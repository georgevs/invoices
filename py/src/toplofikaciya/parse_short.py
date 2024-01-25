from toplofikaciya.parse import (
  parse_due_date,
  parse_heating_accounting_due,
  parse_invoice_date,
  parse_invoice,
  parse_kin,
  parse_period_end_date,
  parse_period_start_date,
  parse_total_due,
)
from utils.parse import trivial_parser


class digest_parser(trivial_parser):
  def __init__(self):
    super().__init__({
      'due_date': parse_due_date,
      'heating_accounting_due': parse_heating_accounting_due,
      'invoice_date': parse_invoice_date,
      'invoice': parse_invoice,
      'kin': parse_kin,
      'period_end_date': parse_period_end_date,
      'period_start_date': parse_period_start_date,
      'total_due': parse_total_due,
    })


def parse_digest(digest):
  parser = digest_parser()
  for line in digest:
    if parser.parse_line(line) is not None:
      break
  return parser.data
  