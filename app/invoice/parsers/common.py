import datetime


int_from_match = lambda match: int(match.group(1))
float_from_match = lambda match: float(match.group(1))
float_comma_from_match = lambda match: float(match.group(1).replace(',','.'))
date_from_match = lambda match: datetime.date(int(match.group(3)), int(match.group(2)), int(match.group(1)))


class ParseError(Exception): ...
class MissingPropertiesError(ParseError): ...
