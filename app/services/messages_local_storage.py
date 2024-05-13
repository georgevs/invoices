from util.json import save_json, load_json
from util.os import scandir
import os


class Config:
  def __init__(self, args):
    self.messages_path = args.messages_path or '__messages'


class MessagesLocalStorage:
  def __init__(self, config):
    self.config = config

  def put_message(self, message_id, message):
    file_path = os.path.join(self.config.messages_path, message_id, MessagesLocalStorage.message_file_name)
    save_json(file_path, message)
    return file_path

  def list_messages(self):
    for file_path in scandir(self.config.messages_path):
      message_id, file_name = os.path.split(os.path.relpath(file_path, self.config.messages_path))
      if file_name == MessagesLocalStorage.message_file_name:
        yield dict(id=message_id, uri=file_path)

  def get_message(self, uri):
    return load_json(uri)
  

  def put_labels(self, labels):
    file_path = os.path.join(self.config.messages_path, MessagesLocalStorage.labels_file_name)
    save_json(file_path, labels)
    return file_path

  def get_labels(self, uri):
    return load_json(uri)
  

  def put_attachment(self, message_id, filename, data):
    file_path = os.path.join(self.config.messages_path, message_id, 'attachments', filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'bw') as file:
      file.write(data)
    return file_path

  # def list_attachments(self):
  #   for file_path in scandir(self.config.messages_path):
  #     label_name, _ = os.path.split(os.path.relpath(file_path, self.config.messages_path))
  #     yield dict(label_name=label_name, uri=file_path)

  def get_attachment(self, uri):
    with open(uri, 'br') as file:
      return file.read()
  
  message_file_name = 'message.json'
  labels_file_name = 'labels.json'
