from google.attachments import Attachments
from google.authenticator import Authenticator, Config as AuthenticatorConfig
from google.gmail import Gmail
from services.attachments_local_storage import AttachmentsLocalStorage, Config as AttachmentsLocalStorageConfig
from util.logging import Config as LoggingConfig


def main(config):
  app = App(config)
  print(list(app.fetch_invoices()))


class App:
  def __init__(self, config):
    self.services = Services(config)

  def fetch_invoices(self):
    invoice_labels = self.__list_invoice_labels()
    for label in invoice_labels:
      label_name, label_id = label.get('name'), label.get('id')
      attachments = self.services.attachments.list_attachments(label_ids=[label_id])
      for attachment in attachments:
        message_id, attachment_id = attachment.get('message_id'), attachment.get('attachment_id') 
        data, size = self.services.attachments.get_attachment(attachment_id, message_id)
        filename = attachment.get('filename') 
        attachment_uri = self.services.storage.put_attachment(label_name, filename, data)
        yield dict(size=size, attachment_uri=attachment_uri)

  def __list_invoice_labels(self):
    labels = self.services.gmail.list_labels()
    is_invoice_label = (lambda it: it.get('type') == 'user' and it.get('name') in App.invoice_types)
    return filter(is_invoice_label, labels)

  invoice_types = ['electrohold', 'sofiyskavoda', 'toplofikaciya']


class Services:
  def __init__(self, config):
    self.authenticator = Authenticator(config.authenticator)
    self.gmail = Gmail(self.authenticator)
    self.attachments = Attachments(self.gmail)
    self.storage = AttachmentsLocalStorage(config.storage)


class Config:
  def __init__(self, args):
    self.authenticator = AuthenticatorConfig(args)
    self.storage = AttachmentsLocalStorageConfig(args)
    self.logging = LoggingConfig(args) if args.debug else None


if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('--attachments-path', default='__invoices')
  parser.add_argument('--bind-addr', type=str)
  parser.add_argument('--secrets-path', type=str)
  parser.add_argument('--debug', action='store_true')
  parser.add_argument('--log-file-path', type=str)
  args = parser.parse_args()

  config = Config(args)

  main(config)
