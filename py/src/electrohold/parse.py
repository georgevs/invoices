from utils.fn import pipe
from utils.parse import (
  date_from_match,
  float_number_comma_from_match,
  number_from_match, 
  parse_regex, 
  trivial_parser,
)


parse_due_date = pipe(parse_regex(r'Срок за плащане на настоящата фактура ___ от (\d+)\.(\d+)\.(\d+) до \d+\.\d+\.\d+'), date_from_match)
parse_invoice = pipe(parse_regex(r'^№ (\d+) / \d+\.\d+\.\d+'), number_from_match)
parse_invoice_date = pipe(parse_regex(r'^№ \d+ / (\d+)\.(\d+)\.(\d+)'), date_from_match)
parse_kin = pipe(parse_regex(r'Клиентски номер : (\d+)'), number_from_match)
parse_total_due = pipe(parse_regex(r'СУМА ЗА ПЛАЩАНЕ ___ ([\d\.,]+)'), float_number_comma_from_match)

parse_period_end_date = pipe(parse_regex(r'Консумирана електрическа енергия от \d+\.\d+\.\d+ до (\d+)\.(\d+)\.(\d+)'), date_from_match)
parse_period_start_date = pipe(parse_regex(r'Консумирана електрическа енергия от (\d+)\.(\d+)\.(\d+) до \d+\.\d+\.\d+'), date_from_match)
parse_detail_meter_id = pipe(parse_regex(r'Електромер № (\d+)'), number_from_match)

parse_detail_daily_new_value = pipe(parse_regex(r'Дневна ___ (\d+) ___ \d+ ___ \d+ ___ \d+ ___ \d+'), number_from_match)
parse_detail_daily_old_value = pipe(parse_regex(r'Дневна ___ \d+ ___ (\d+) ___ \d+ ___ \d+ ___ \d+'), number_from_match)
parse_detail_daily_quantity = pipe(parse_regex(r'Дневна ___ \d+ ___ \d+ ___ (\d+) ___ \d+ ___ \d+'), number_from_match)
parse_detail_nightly_new_value = pipe(parse_regex(r'Дневна ___ (\d+) ___ \d+ ___ \d+ ___ \d+ ___ \d+'), number_from_match)
parse_detail_nightly_old_value = pipe(parse_regex(r'Нощна ___ \d+ ___ (\d+) ___ \d+ ___ \d+ ___ \d+'), number_from_match)
parse_detail_nightly_quantity = pipe(parse_regex(r'Нощна ___ \d+ ___ \d+ ___ (\d+) ___ \d+ ___ \d+'), number_from_match)

parse_supply_period_end_date = pipe(parse_regex(r'Снабдяване с електрическа енергия от (\d+)\.(\d+)\.(\d+) до \d+\.\d+\.\d+'), date_from_match)
parse_supply_period_start_date = pipe(parse_regex(r'Снабдяване с електрическа енергия от \d+\.\d+\.\d+ до (\d+)\.(\d+)\.(\d+)'), date_from_match)

parse_supply_nightly_quantity = pipe(parse_regex(r'Активна енергия Дневна ___ (\d+) ___ [\d\.,]+ ___ [\d\.,]+'), number_from_match)
parse_supply_nightly_price = pipe(parse_regex(r'Активна енергия Дневна ___ \d+ ___ ([\d\.,]+) ___ [\d\.,]+'), float_number_comma_from_match)
parse_supply_nightly_due = pipe(parse_regex(r'Активна енергия Дневна ___ \d+ ___ [\d\.,]+ ___ ([\d\.,]+)'), float_number_comma_from_match)

parse_supply_daily_quantity = pipe(parse_regex(r'Активна енергия Нощна ___ (\d+) ___ [\d\.,]+ ___ [\d\.,]+'), number_from_match)
parse_supply_daily_price = pipe(parse_regex(r'Активна енергия Нощна ___ \d+ ___ ([\d\.,]+) ___ [\d\.,]+'), float_number_comma_from_match)
parse_supply_daily_due = pipe(parse_regex(r'Активна енергия Нощна ___ \d+ ___ [\d\.,]+ ___ ([\d\.,]+)'), float_number_comma_from_match)

parse_distribution_period_end_date = pipe(parse_regex(r'Разпределение на електрическа енергия от (\d+)\.(\d+)\.(\d+) до \d+\.\d+\.\d+'), date_from_match)
parse_distribution_period_start_date = pipe(parse_regex(r'Разпределение на електрическа енергия от \d+\.\d+\.\d+ до (\d+)\.(\d+)\.(\d+)'), date_from_match)

parse_access_distribution_network_quantity = pipe(parse_regex(r'Достъп до разпределителната мрежа ___ (\d+) ___ [\d\.,]+ ___ [\d\.,]+'), number_from_match)
parse_access_distribution_network_price = pipe(parse_regex(r'Достъп до разпределителната мрежа ___ \d+ ___ ([\d\.,]+) ___ [\d\.,]+'), float_number_comma_from_match)
parse_access_distribution_network_due = pipe(parse_regex(r'Достъп до разпределителната мрежа ___ \d+ ___ [\d\.,]+ ___ ([\d\.,]+)'), float_number_comma_from_match)

parse_transfer_distribution_network_quantity = pipe(parse_regex(r'Пренос през разпределителната мрежа НН ___ (\d+) ___ [\d\.,]+ ___ [\d\.,]+'), number_from_match)
parse_transfer_distribution_network_price = pipe(parse_regex(r'Пренос през разпределителната мрежа НН ___ \d+ ___ ([\d\.,]+) ___ [\d\.,]+'), float_number_comma_from_match)
parse_transfer_distribution_network_due = pipe(parse_regex(r'Пренос през разпределителната мрежа НН ___ \d+ ___ [\d\.,]+ ___ ([\d\.,]+)'), float_number_comma_from_match)

parse_access_transportation_network_quantity = pipe(parse_regex(r'Достъп до електропреносната мрежа ___ (\d+) ___ [\d\.,]+ ___ [\d\.,]+'), number_from_match)
parse_access_transportation_network_price = pipe(parse_regex(r'Достъп до електропреносната мрежа ___ \d+ ___ ([\d\.,]+) ___ [\d\.,]+'), float_number_comma_from_match)
parse_access_transportation_network_due = pipe(parse_regex(r'Достъп до електропреносната мрежа ___ \d+ ___ [\d\.,]+ ___ ([\d\.,]+)'), float_number_comma_from_match)

parse_transfer_transportation_network_quantity = pipe(parse_regex(r'Пренос през електропреносната мрежа ___ (\d+) ___ [\d\.,]+ ___ [\d\.,]+'), number_from_match)
parse_transfer_transportation_network_price = pipe(parse_regex(r'Пренос през електропреносната мрежа ___ \d+ ___ ([\d\.,]+) ___ [\d\.,]+'), float_number_comma_from_match)
parse_transfer_transportation_network_due = pipe(parse_regex(r'Пренос през електропреносната мрежа ___ \d+ ___ [\d\.,]+ ___ ([\d\.,]+)'), float_number_comma_from_match)

parse_details_complete = pipe(parse_regex(r'СУМА ЗА ПЛАЩАНЕ ___ [\d\.,]+'), lambda match: True if match else None)


class meter_details_parser(trivial_parser):
  def __init__(self):
    super().__init__({
      'daily_new_value': parse_detail_daily_new_value,
      'daily_old_value': parse_detail_daily_old_value,
      'daily_quantity': parse_detail_daily_quantity,
      'meter_id': parse_detail_meter_id,
      'nightly_new_value': parse_detail_nightly_new_value,
      'nightly_old_value': parse_detail_nightly_old_value,
      'nightly_quantity': parse_detail_nightly_quantity,
      'period_end_date': parse_period_end_date,
      'period_start_date': parse_period_start_date,
    })


class usage_parser():
  def __init__(self):
    self.data = []
    self.parse_data = meter_details_parser().parse_line
  def parse_line(self, line):
    if (data := self.parse_data(line)):
      self.data.append(data)
      self.parse_data = meter_details_parser().parse_line
    return self.data if parse_details_complete(line) else None


class supply_nightly_details_parser(trivial_parser):
  def __init__(self):
    super().__init__({
      'due': parse_supply_nightly_due,
      'price': parse_supply_nightly_price,
      'quantity': parse_supply_nightly_quantity,
    })
    

class all_supply_nightly_details_parser():
  def __init__(self):
    self.data = []
    self.parse_data = supply_nightly_details_parser().parse_line
  def parse_line(self, line):
    if (data := self.parse_data(line)):
      self.data.append(data)
      self.parse_data = supply_nightly_details_parser().parse_line
    return self.data if parse_details_complete(line) else None


class supply_daily_details_parser(trivial_parser):
  def __init__(self):
    super().__init__({
      'due': parse_supply_daily_due,
      'price': parse_supply_daily_price,
      'quantity': parse_supply_daily_quantity,
    })
    

class all_supply_daily_details_parser():
  def __init__(self):
    self.data = []
    self.parse_data = supply_daily_details_parser().parse_line
  def parse_line(self, line):
    if (data := self.parse_data(line)):
      self.data.append(data)
      self.parse_data = supply_daily_details_parser().parse_line
    return self.data if parse_details_complete(line) else None


class provision_parser(trivial_parser):
  def __init__(self):
    super().__init__({
      'daily': all_supply_daily_details_parser().parse_line,
      'nightly': all_supply_nightly_details_parser().parse_line,
      'period_end_date': parse_supply_period_end_date,
      'period_start_date': parse_supply_period_start_date,
    })


class access_distribution_network_details_parser(trivial_parser):
  def __init__(self):
    super().__init__({
      'due': parse_access_distribution_network_due,
      'price': parse_access_distribution_network_price,
      'quantity': parse_access_distribution_network_quantity,
    })
    

class all_access_distribution_network_details_parser():
  def __init__(self):
    self.data = []
    self.parse_data = access_distribution_network_details_parser().parse_line
  def parse_line(self, line):
    if (data := self.parse_data(line)):
      self.data.append(data)
      self.parse_data = access_distribution_network_details_parser().parse_line
    return self.data if parse_details_complete(line) else None


class transfer_distribution_network_details_parser(trivial_parser):
  def __init__(self):
    super().__init__({
      'due': parse_transfer_distribution_network_due,
      'price': parse_transfer_distribution_network_price,
      'quantity': parse_transfer_distribution_network_quantity,
    })
    

class all_transfer_distribution_network_details_parser():
  def __init__(self):
    self.data = []
    self.parse_data = transfer_distribution_network_details_parser().parse_line
  def parse_line(self, line):
    if (data := self.parse_data(line)):
      self.data.append(data)
      self.parse_data = transfer_distribution_network_details_parser().parse_line
    return self.data if parse_details_complete(line) else None


class access_transportation_network_details_parser(trivial_parser):
  def __init__(self):
    super().__init__({
      'due': parse_access_transportation_network_due,
      'price': parse_access_transportation_network_price,
      'quantity': parse_access_transportation_network_quantity,
    })
    

class all_access_transportation_network_details_parser():
  def __init__(self):
    self.data = []
    self.parse_data = access_transportation_network_details_parser().parse_line
  def parse_line(self, line):
    if (data := self.parse_data(line)):
      self.data.append(data)
      self.parse_data = access_transportation_network_details_parser().parse_line
    return self.data if parse_details_complete(line) else None


class transfer_transportation_network_details_parser(trivial_parser):
  def __init__(self):
    super().__init__({
      'due': parse_transfer_transportation_network_due,
      'price': parse_transfer_transportation_network_price,
      'quantity': parse_transfer_transportation_network_quantity,
    })
    

class all_transfer_transportation_network_details_parser():
  def __init__(self):
    self.data = []
    self.parse_data = transfer_transportation_network_details_parser().parse_line
  def parse_line(self, line):
    if (data := self.parse_data(line)):
      self.data.append(data)
      self.parse_data = transfer_transportation_network_details_parser().parse_line
    return self.data if parse_details_complete(line) else None


class distribution_parser(trivial_parser):
  def __init__(self):
    super().__init__({
      'access_distribution_network': all_access_distribution_network_details_parser().parse_line,
      'access_transportation_network': all_access_transportation_network_details_parser().parse_line,
      'period_end_date': parse_distribution_period_end_date,
      'period_start_date': parse_distribution_period_start_date,
      'transfer_distribution_network': all_transfer_distribution_network_details_parser().parse_line,
      'transfer_transportation_network': all_transfer_transportation_network_details_parser().parse_line,
    })


class digest_parser(trivial_parser):
  def __init__(self):
    super().__init__({
      'distribution': distribution_parser().parse_line,
      'due_date': parse_due_date,
      'invoice_date': parse_invoice_date,
      'invoice': parse_invoice,
      'kin': parse_kin,
      'provision': provision_parser().parse_line,
      'total_due': parse_total_due,
      'usage': usage_parser().parse_line,
    })


def parse_digest(digest):
  parser = digest_parser()
  for line in digest:
    if parser.parse_line(line) is not None:
      break
  return parser.data
  