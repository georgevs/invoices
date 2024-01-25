from utils.fn import or_, pipe
from utils.parse import (
  date_from_match,
  date_of_year_month_from_match,
  float_number_comma_from_match,
  number_from_match, 
  parse_regex, 
)


parse_kin = pipe(
  or_(
    parse_regex(r'ДОГОВОРНА СМЕТКА №\s?(\d+)'), 
    parse_regex(r'КОД ПЛАТЕЦ: (\d+)'),
  ),
  number_from_match
)

parse_invoice = pipe(
  or_(
    parse_regex(r'№ (\d+) - ОРИГИНАЛ'), 
    parse_regex(r'СЪОБЩЕНИЕ КЪМ ФАКТУРА № (\d+)'),
    parse_regex(r'ФАКТУРА № (\d+) - ОРИГИНАЛ'),
  ),
  number_from_match
)

parse_invoice_date = pipe(
  parse_regex(r'Дата на данъчно събитие - (\d+)\.(\d+)\.(\d+) г\.'), 
  date_from_match
)

parse_due_date = pipe(
  or_(
    parse_regex(r'Срок за плащане (\d+)\.(\d+)\.(\d+) г.'),
    parse_regex(r'Срок за плащане на фактура № \d+ - (\d+)\.(\d+)\.(\d+) г\s?\.'),
  ),
  date_from_match
)

parse_period_start_date = or_(
  pipe(
    or_(
      parse_regex(r'Отчетен период: (\d+)\.(\d+)\.(\d+) - \d+\.\d+\.\d+ г\.'),
      parse_regex(r'Отчетен период\s?:\s?(\d+)\.(\d+)\.(\d+) г\s?\. - \d+\.\d+\.\d+ г\s?\.'),
      parse_regex(r'Топлинна енергия за период (\d+)\.(\d+)\.(\d+) - \d+\.\d+\.\d+ г\.'),
    ),
    date_from_match
  ),
  pipe(
    parse_regex(r'Общо за периода (\d+)\.(\d+) г\. - \d+\.\d+ г\.'),
    date_of_year_month_from_match
  ),
)

parse_period_end_date = or_(
  pipe(
    or_(
      parse_regex(r'Отчетен период: \d+\.\d+\.\d+ - (\d+)\.(\d+)\.(\d+) г\.'),
      parse_regex(r'Отчетен период\s?:\s?\d+\.\d+\.\d+ г\s?\. - (\d+)\.(\d+)\.(\d+) г\s?\.'),
      parse_regex(r'Топлинна енергия за период \d+\.\d+\.\d+ - (\d+)\.(\d+)\.(\d+) г\.'),
    ),
    date_from_match
  ),
  pipe(
    parse_regex(r'Общо за периода \d+\.\d+ г\. - (\d+)\.(\d+) г\.'),
    date_of_year_month_from_match
  ),
)

parse_heating_water_price = pipe(
  or_(
    parse_regex(r'за подгряване на вода ___ Мвтч ___ [\d\.]+ ___ ([\d\.]+) ___ [\d\.]+'),
    parse_regex(r'Топлинна енергия за подгряване на вода ___ М[Вв]тч ___ [\d\.,]+ ___ ([\d\.,]+) ___ [\d\.,]+'),
  ),
  float_number_comma_from_match
)

parse_heating_water_quantity = pipe(
  or_(
    parse_regex(r'за подгряване на вода ___ Мвтч ___ ([\d\.]+) ___ [\d\.]+ ___ [\d\.]+'),
    parse_regex(r'Топлинна енергия за подгряване на вода ___ М[Вв]тч ___ ([\d\.,]+) ___ [\d\.,]+ ___ [\d\.,]+'),
  ),
  float_number_comma_from_match
)

parse_heating_water_due = pipe(
  or_(
    parse_regex(r'за подгряване на вода ___ Мвтч ___ [\d\.]+ ___ [\d\.]+ ___ ([\d\.]+)'),
    parse_regex(r'Топлинна енергия за подгряване на вода ___ М[Вв]тч ___ [\d\.,]+ ___ [\d\.,]+ ___ ([\d\.,]+)'),
  ),
  float_number_comma_from_match
)

parse_heating_property_price = pipe(
  or_(
    parse_regex(r'за отопление на имот ___ Мвтч ___ [\d\.]+ ___ ([\d\.]+) ___ [\d\.]+'),
    parse_regex(r'Топлинна енергия за отопление на имот ___ М[Вв]тч ___ [\d\.,]+ ___ ([\d\.,]+) ___ [\d\.,]+'),
  ),
  float_number_comma_from_match
)

parse_heating_property_quantity = pipe(
  or_(
    parse_regex(r'за отопление на имот ___ Мвтч ___ ([\d\.]+) ___ [\d\.]+ ___ [\d\.]+'),
    parse_regex(r'Топлинна енергия за отопление на имот ___ М[Вв]тч ___ ([\d\.,]+) ___ [\d\.,]+ ___ [\d\.,]+'),
  ),
  float_number_comma_from_match
)

parse_heating_property_due = pipe(
  or_(
    parse_regex(r'за отопление на имот ___ Мвтч ___ [\d\.]+ ___ [\d\.]+ ___ ([\d\.]+)'),
    parse_regex(r'Топлинна енергия за отопление на имот ___ М[Вв]тч ___ [\d\.,]+ ___ [\d\.,]+ ___ ([\d\.,]+)'),
  ),
  float_number_comma_from_match
)

parse_heating_accounting_due = pipe(
  or_(
    parse_regex(r'\d+ ___ (?:\d+/)?\d+ ___ [\d/]+ част ___ Бр ___ [\d\.,]+ ___ [\d\.,]+ ___ ([\d\.,]+)'),
    parse_regex(r'^[\d/]+ част ___ БР ___ [\d\.,]+ ___ [\d\.,]+ ___ ([\d\.,]+)'),
    parse_regex(r'Дялово разпределение на топлинна енергия \([\d/]+ част\) ___ (?:БР|бр) ___ [\d\.,]+ ___ [\d\.,]+ ___ ([\d\.,]+)'),
  ),
  float_number_comma_from_match
)

parse_total_due = pipe(
  or_(
    parse_regex(r'(?:Всичко|ВСИЧКО)? по фактура:? ___ ([\d\.,]+)'),
    parse_regex(r'ДЪЛЖИМА СУМА ___ ([\d\.,]+)'),
    parse_regex(r'Дължима сума ___ лв\. ___ ([\d\.,]+)'),
    parse_regex(r'Дължима сума за периода по фактура ___ ([\d\.,]+) лв\.'),
  ),
  float_number_comma_from_match
)
