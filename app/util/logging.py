import logging
import os
import sys


class Config:
  def __init__(self, args):
    self.log_file_path = args.log_file_path or Config.__get_log_file_path()
    os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)
    logging.basicConfig(filename=self.log_file_path, encoding='utf-8', level=logging.DEBUG)

  def __get_log_file_path():
    script_file_path = sys.argv[0]
    script_file_name, _ = os.path.splitext(os.path.basename(script_file_path))
    return os.path.join('__logs', f'{script_file_name}.log')
