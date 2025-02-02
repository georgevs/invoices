#!/usr/bin/env python3

from google.attachments import Attachments
from google.authenticator import Authenticator, Config as AuthenticatorConfig
from google.gmail import Gmail
from itertools import chain
from services.messages_local_storage import MessagesLocalStorage, Config as MessagesLocalStorageConfig
from util.logging import Config as LoggingConfig


def main(config):
  app = App(config)
  target_labels = ['electrohold', 'sofiyskavoda', 'toplofikaciya']
  for message in app.fetch_messages(target_labels=target_labels):
    print(message)


class App:
  def __init__(self, config):
    self.services = Services(config)

  def fetch_messages(self, target_labels):
    labels = list(self.services.gmail.list_labels())
    self.services.storage.put_labels(labels)
    is_target_label = (lambda it: it.get('type') == 'user' and it.get('name') in target_labels)
    target_labels_iter = (it for it in labels if is_target_label(it))
    message_infos_iter = chain.from_iterable(self.services.gmail.list_messages(label_ids=[it.get('id')]) for it in target_labels_iter)
    messages_iter = (self.services.gmail.get_message(it.get('id')) for it in message_infos_iter)
    
    for message in messages_iter:
      yield self.fetch_message(message)


  def fetch_message(self, message):
    message_id = message.get('id')
    message_uri = self.services.storage.put_message(message_id, message)
    
    for attachment_info in self.services.attachments.get_message_attachments(message):
      attachment_id = attachment_info.get('attachment_id') 
      data, _ = self.services.attachments.get_attachment(attachment_id, message_id)
      file_name = attachment_info.get('file_name') 
      self.services.storage.put_attachment(message_id, file_name, data)

    return dict(message_id=message_id, message_uri=message_uri)


class Services:
  def __init__(self, config):
    self.authenticator = Authenticator(config.authenticator)
    self.gmail = Gmail(self.authenticator)
    self.attachments = Attachments(self.gmail)
    self.storage = MessagesLocalStorage(config.storage)

class Config:
  def __init__(self, args):
    self.authenticator = AuthenticatorConfig(args)
    self.storage = MessagesLocalStorageConfig(args)
    self.logging = LoggingConfig(args) if args.debug else None


if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('--bind-addr', type=str)
  parser.add_argument('--debug', action='store_true')
  parser.add_argument('--log-file-path', type=str, default='./__logs/fetch_invoice_messages.log')
  parser.add_argument('--messages-path', default='./data/confidential/messages')
  parser.add_argument('--secrets-path', type=str, default='./secrets')
  args = parser.parse_args()

  config = Config(args)

  main(config)
