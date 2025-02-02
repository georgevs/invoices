#!/usr/bin/env python3

import collections
import itertools
import operator
import util.json
import util.os


Invoice = collections.namedtuple('Invoice', ['contragent', 'uri'])


def load_invoices(invoices_path):
  invoices = util.os.scandir(invoices_path, recursive=True)
  invoices = filter(util.os.has_ext('.json'), invoices)
  invoices = map(util.json.load_json, invoices)
  invoices = map(operator.itemgetter(*Invoice._fields), invoices)
  invoices = itertools.starmap(Invoice, invoices)
  return invoices


if __name__ == '__main__':
  import argparse
  import os
  parser = argparse.ArgumentParser()
  parser.add_argument('--invoices-path', default='./data/confidential/invoices')
  args = parser.parse_args()
  print(*sorted(load_invoices(**vars(args))), sep=os.linesep)
