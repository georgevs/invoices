"""
dump_json :: obj -> json
"""

import datetime
import json

class IterEncoder(json.JSONEncoder):
  def default(self, o):
    try:
      iterable = iter(o)
    except TypeError:
      pass
    else:
      return list(iterable)

    if isinstance(o, datetime.datetime) or isinstance(o, datetime.date):
      return str(o)

    return json.JSONEncoder.default(self, o)

def dump_json(o):
  return json.dumps(o, cls=IterEncoder, ensure_ascii=False).encode('utf-8').decode()
