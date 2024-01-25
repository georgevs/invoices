from electrohold.parse import parse_digest as parse_digest_full
from parse_pdf import parse_and_validate_digest_table
from sys import stderr
from utils.fn import pipe
from utils.json import dump_json
from utils.parse import validate_data
from utils.pdf import digest_pdf
import argparse


def parse_and_validate_digest(digest):
  table = { 
    'full': pipe(parse_digest_full, validate_data),
  }
  return parse_and_validate_digest_table(table, digest)


def main(file_path):
  errors, data = parse_and_validate_digest(digest_pdf(file_path))
  if errors: print(dump_json((file_path, errors)), file=stderr)
  else: print(dump_json(data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str, help='file path')
    args = parser.parse_args()
    main(**vars(args))
