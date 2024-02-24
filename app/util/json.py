import datetime
import json
import os


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
    if isinstance(o, Exception):
      return str(o)

    return json.JSONEncoder.default(self, o)


def dump_json(o):
  return json.dumps(o, cls=IterEncoder, ensure_ascii=False).encode('utf-8').decode()


def try_load_json(file_path):
  try:
    return load_json(file_path)
  except:
    pass


def load_json(file_path):
  with open(file_path, 'r') as file:
    return json.load(file)


def save_json(file_path, x):
  os.makedirs(os.path.dirname(file_path), exist_ok=True)
  with open(file_path, 'wt') as file:
    json.dump(x, file, indent=2)
