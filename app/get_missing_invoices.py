#!/usr/bin/env python3

import operator
import messages_db
import invoices_db


def get_missing_invoices(invoices_path, messages_path):
  invoices = invoices_db.load_invoices(invoices_path)
  attachments = messages_db.load_message_attachments(messages_path)
  invoice_uris = set(map(operator.attrgetter('uri'), invoices))
  return (it for it in attachments if it.uri not in invoice_uris)


if __name__ == '__main__':
  import argparse
  import os
  parser = argparse.ArgumentParser()
  parser.add_argument('--invoices-path', default='./data/confidential/invoices')
  parser.add_argument('--messages-path', default='./data/confidential/messages')
  args = parser.parse_args()
  print(*sorted(get_missing_invoices(**vars(args))), sep=os.linesep)
