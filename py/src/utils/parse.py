from re import compile as compile_regex
from utils.fn import branch, iflatten, pipe
import datetime


parse_regex = lambda regex: compile_regex(regex).search

date_from_match = lambda match: datetime.date(int(match.group(3)), int(match.group(2)), int(match.group(1))) if match else None
date_of_year_month_from_match  = lambda match: datetime.date(int(match.group(2)), int(match.group(1)), 1) if match else None
number_from_match = lambda match: int(match.group(1)) if match else None
float_number_from_match = lambda match: float(match.group(1)) if match else None
float_number_comma_from_match = lambda match: float(match.group(1).replace(',', '.')) if match else None

init_data = lambda ks: { k: None for k in ks }
valid_data = lambda data: data if all(value is not None for _, value in data.items()) else None
missing_data = lambda data: [key for key,value in data.items() if value is None]
validate_data = lambda data: (None, data) if len(error := missing_data(data)) == 0 else ({ 'error': error }, None)
  
parse_field = lambda field, parse_line: lambda line: [(field, data)] if (data := parse_line(line)) is not None else []
parse_table = lambda field_parse_table: pipe(
  branch(*[parse_field(field, once(parse_line)) for field, parse_line in field_parse_table.items()]),
  iflatten
)


class once():
  def __init__(self, fn):
    self.fn = fn
  def __call__(self, x):
    r = self.fn(x) if self.fn else None
    if r is not None: self.fn = None
    return r


class trivial_parser():
  def __init__(self, parse_field_table):
    self.data = init_data(parse_field_table.keys())
    self.parse_data = parse_table(parse_field_table)
  def parse_line(self, line):
    self.data.update(self.parse_data(line))
    return valid_data(self.data)
