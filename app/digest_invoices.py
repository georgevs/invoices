from invoice.digest import Digest
from invoice.parsers import electrohold, sofiyskavoda, toplofikaciya
from services.invoices_local_storage import InvoicesLocalStorage, Config as InvoicesLocalStorageConfig
from services.messages_local_storage import MessagesLocalStorage, Config as MessagesLocalStorageConfig
from util.json import dump_json
from util.pdf import Pdf
import io
import os


def main(config):
  app = App(config)
  print(dump_json(list(app.digest_invoices())))


class App:
  def __init__(self, config):
    self.services = Services(config)
    self.parsers = dict(
      electrohold=self.services.invoice.electrohold,
      sofiyskavoda=self.services.invoice.sofiyskavoda,
      toplofikaciya=self.services.invoice.toplofikaciya,
    )

  def digest_invoices(self):
    for attachment_info in self.services.storage.messages.list_attachments():
      yield attachment_info


  # def digest_invoices(self):
  #   for attachment in self.services.storage.list_attachments():
  #     label_name = attachment.get('label_name')
  #     if (parser := self.parsers.get(label_name)) is not None:
  #       uri = attachment.get('uri')
  #       _, ext = os.path.splitext(uri)
  #       if ext == '.pdf':
  #         data = self.services.storage.get_attachment(uri)
  #         lines = iter(Pdf(stream=io.BytesIO(data)))
  #         digest, error = parser.get_digest(lines)
  #         invoice = dict(contragent=label_name, uri=uri)
  #         if digest: 
  #           invoice.update(digest=digest)
  #         if error:
  #           invoice.update(error=error)
  #         yield invoice


class Services:
  def __init__(self, config):
    self.invoice = InvoiceServices()
    self.storage = Storage(config.storage)


class InvoiceServices:
  def __init__(self):
    self.electrohold = Digest(electrohold.Parser)
    self.sofiyskavoda = Digest(sofiyskavoda.Parser)
    self.toplofikaciya = Digest(toplofikaciya.Parser)


class Storage:
  def __init__(self, config):
    self.invoices = InvoicesLocalStorage(config.invoices)
    self.messages = MessagesLocalStorage(config.messages)


class Config:
  def __init__(self, args):
    self.storage = StorageConfig(args)


class StorageConfig:
  def __init__(self, args):
    self.invoices = InvoicesLocalStorageConfig(args)
    self.messages = MessagesLocalStorageConfig(args)


if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('--invoices-path', default='./data/confidential/invoices')
  parser.add_argument('--messages-path', default='./data/confidential/messages')
  args = parser.parse_args()

  config = Config(args)

  main(config)
