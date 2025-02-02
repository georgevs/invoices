#!/usr/bin/env python3

'''
Run:
  app/digest_pdf.py --contragent toplofikaciya ./data/confidential/messages/1945b12c55013405/attachments/1102616307.pdf
  app/digest_pdf.py --contragent sofiyskavoda ./data/confidential/messages/1946f2799c11e6ad/attachments/0000000137766010_signed.pdf
  app/digest_pdf.py --contragent electrohold ./data/confidential/messages/1933a81ded7ae089/attachments/310285668475_0387377905_20241110.pdf
'''

import invoice.parsers.electrohold
import invoice.parsers.sofiyskavoda
import invoice.parsers.toplofikaciya
import io
import os
import sys
import util.json
import util.pdf

invoice_parser = dict(
  electrohold=invoice.parsers.electrohold.parse_invoice,
  sofiyskavoda=invoice.parsers.sofiyskavoda.parse_invoice,
  toplofikaciya=invoice.parsers.toplofikaciya.parse_invoice
)

def main(args):
  file = open(args.file_path, 'rb') if args.file_path else sys.stdin.buffer
  stream = io.BytesIO(file.read())
  pdf = util.pdf.Pdf(stream=stream)

  invoice, err = None, None
  try:
    invoice = invoice_parser[args.contragent](pdf)
  except Exception as ex:
    err = ex

  if invoice:
    file = sys.stdout
    if args.invoices_path:
      invoice_file_path = os.path.join(args.invoices_path, args.contragent, f'{invoice.invoice_date.strftime("%Y-%m-%d")}-{invoice.invoice_id}.json')
      os.makedirs(os.path.dirname(invoice_file_path), exist_ok=True)
      file = open(invoice_file_path, 'wt')
      print(args.file_path)
    invoice = dict(contragent=args.contragent, uri=args.file_path, digest=invoice._asdict())
    invoice = util.json.dump_json(invoice, indent=2)
    print(invoice, file=file)

  elif err:  
    return f'{args.file_path}\t{err}'
  

if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('--contragent', choices=['electrohold', 'sofiyskavoda', 'toplofikaciya'])
  parser.add_argument('--invoices-path', type=str, nargs='?')
  parser.add_argument('file_path', type=str, nargs='?')
  sys.exit(main(parser.parse_args()))
