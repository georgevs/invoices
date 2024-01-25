from utils.json import dump_json
from utils.pdf import digest_pdf
from utils.ranges import parse_number_ranges
import argparse

def main(file_path, pages):
  pages_ranges = parse_number_ranges(pages) if pages else None
  print(dump_json(digest_pdf(file_path, pages_ranges)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str, help='file path')
    parser.add_argument('--pages', type=str, help='ranges of pages to scan')
    args = parser.parse_args()
    main(**vars(args))
