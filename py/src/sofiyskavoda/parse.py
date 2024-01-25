from utils.fn import pipe
from utils.parse import (
  date_from_match,
  float_number_from_match,
  number_from_match, 
  parse_regex, 
  trivial_parser,
)


parse_kin = pipe(parse_regex(r'КЛИЕНТСКИ НОМЕР:(\d+)'), number_from_match)
parse_invoice = pipe(parse_regex(r'ФАКТУРА ОРИГИНАЛ № (\d+)'), number_from_match)
parse_invoice_date = pipe(parse_regex(r'Дата на издаване (\d+)/(\d+)/(\d+)'), date_from_match)
parse_due_date = pipe(parse_regex(r'Краен срок за плащане (\d+)/(\d+)/(\d+)'), date_from_match)
parse_period_start_date = pipe(parse_regex(r'Период на фактуриране от (\d+)/(\d+)/(\d+) до \d+/\d+/\d+'), date_from_match)
parse_period_end_date = pipe(parse_regex(r'Период на фактуриране от \d+/\d+/\d+ до (\d+)/(\d+)/(\d+)'), date_from_match)
parse_next_report_date = pipe(parse_regex(r'Следващият реален отчет на вашите водомери ще бъде в периода от: (\d+)\.(\d+)\.(\d+) до \d+\.\d+\.\d+'), date_from_match)
parse_supply_price = pipe(parse_regex(r'Доставяне на питейна вода ___ ([\d\.]+) ___ [\d\.]+ ___ [\d\.]+ лв'), float_number_from_match)
parse_supply_quantity = pipe(parse_regex(r'Доставяне на питейна вода ___ [\d\.]+ ___ ([\d\.]+) ___ [\d\.]+ лв'), float_number_from_match)
parse_supply_due = pipe(parse_regex(r'Доставяне на питейна вода ___ [\d\.]+ ___ [\d\.]+ ___ ([\d\.]+) лв'), float_number_from_match)
parse_drain_price = pipe(parse_regex(r'Отвеждане на отпадъчни води ___ ([\d\.]+) ___ [\d\.]+ ___ [\d\.]+ лв'), float_number_from_match)
parse_drain_quantity = pipe(parse_regex(r'Отвеждане на отпадъчни води ___ [\d\.]+ ___ ([\d\.]+) ___ [\d\.]+ лв'), float_number_from_match)
parse_drain_due = pipe(parse_regex(r'Отвеждане на отпадъчни води ___ [\d\.]+ ___ [\d\.]+ ___ ([\d\.]+) лв'), float_number_from_match)
parse_filter_price = pipe(parse_regex(r'Пречистване на отпадъчни води ___ ([\d\.]+) ___ [\d\.]+ ___ [\d\.]+ лв'), float_number_from_match)
parse_filter_quantity = pipe(parse_regex(r'Пречистване на отпадъчни води ___ [\d\.]+ ___ ([\d\.]+) ___ [\d\.]+ лв'), float_number_from_match)
parse_filter_due = pipe(parse_regex(r'Пречистване на отпадъчни води ___ [\d\.]+ ___ [\d\.]+ ___ ([\d\.]+) лв'), float_number_from_match)
parse_due = pipe(parse_regex(r'Сума по сделката: ___ ([\d\.]+) лв'), float_number_from_match)
parse_tax_rate = pipe(parse_regex(r'ДДС  (\d+)% от [\d\.]+ лв: ___ [\d\.]+ лв'), float_number_from_match)
parse_tax_due = pipe(parse_regex(r'ДДС  \d+% от [\d\.]+ лв: ___ ([\d\.]+) лв'), float_number_from_match)
parse_past_due = pipe(parse_regex(r'Старо салдо ___ (-?[\d\.]+) лв'), float_number_from_match)
parse_total_due = pipe(parse_regex(r'ОБЩА ДЪЛЖИМА СУМА ___ (-?[\d\.]+) лв'), float_number_from_match)
parse_account = pipe(parse_regex(r'договорна сметка: (\d+)'), number_from_match)
parse_detail_meter_id = pipe(parse_regex(r'(\d+) ___ [\d\.]+ ___ \d+/\d+/\d+ ___ .+ ___ [\d\.]+ ___ \d+/\d+/\d+ ___ .+ ___ [\d\.]+ \s*m3'), number_from_match)
parse_detail_old_value = pipe(parse_regex(r'\d+ ___ ([\d\.]+) ___ \d+/\d+/\d+ ___ .+ ___ [\d\.]+ ___ \d+/\d+/\d+ ___ .+ ___ [\d\.]+ \s*m3'), float_number_from_match)
parse_detail_old_date = pipe(parse_regex(r'\d+ ___ [\d\.]+ ___ (\d+)/(\d+)/(\d+) ___ .+ ___ [\d\.]+ ___ \d+/\d+/\d+ ___ .+ ___ [\d\.]+ \s*m3'), date_from_match)
parse_detail_new_value = pipe(parse_regex(r'\d+ ___ [\d\.]+ ___ \d+/\d+/\d+ ___ .+ ___ ([\d\.]+) ___ \d+/\d+/\d+ ___ .+ ___ [\d\.]+ \s*m3'), float_number_from_match)
parse_detail_new_date = pipe(parse_regex(r'\d+ ___ [\d\.]+ ___ \d+/\d+/\d+ ___ .+ ___ [\d\.]+ ___ (\d+)/(\d+)/(\d+) ___ .+ ___ [\d\.]+ \s*m3'), date_from_match)
parse_details_complete = pipe(parse_regex(r'ОБЩО ЗА АДРЕС НА КОНСУМАЦИЯ ___ [\d\.]+ m3'), lambda match: True if match else None)


class meter_details_parser(trivial_parser):
  def __init__(self):
    super().__init__({
      'meter_id': parse_detail_meter_id,
      'new_date': parse_detail_new_date,
      'new_value': parse_detail_new_value,
      'old_date': parse_detail_old_date,
      'old_value': parse_detail_old_value,
    })


class details_parser():
  def __init__(self):
    self.data = []
    self.parse_data = meter_details_parser().parse_line
    
  def parse_line(self, line):
    if (data := self.parse_data(line)):
      self.data.append(data)
      self.parse_data = meter_details_parser().parse_line
    return self.data if parse_details_complete(line) else None


class digest_parser(trivial_parser):
  def __init__(self):
    super().__init__({
      'account': parse_account,
      'details': details_parser().parse_line,
      'drain_due': parse_drain_due,
      'drain_price': parse_drain_price,
      'drain_quantity': parse_drain_quantity,
      'due_date': parse_due_date,
      'due': parse_due,
      'filter_due': parse_filter_due,
      'filter_price': parse_filter_price,
      'filter_quantity': parse_filter_quantity,
      'invoice_date': parse_invoice_date,
      'invoice': parse_invoice,
      'kin': parse_kin,
      'next_report_date': parse_next_report_date,
      'past_due': parse_past_due,
      'period_end_date': parse_period_end_date,
      'period_start_date': parse_period_start_date,
      'supply_due': parse_supply_due,
      'supply_price': parse_supply_price,
      'supply_quantity': parse_supply_quantity,
      'tax_due': parse_tax_due,
      'tax_rate': parse_tax_rate,
      'total_due': parse_total_due,
    })


def parse_digest(digest):
  parser = digest_parser()
  for line in digest:
    if parser.parse_line(line) is not None:
      break
  return parser.data
  