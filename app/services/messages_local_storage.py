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
    file_path = self.get_labels_uri()
    save_json(file_path, labels)
    return file_path

  def get_labels(self):
    return load_json(self.get_labels_uri())

  def get_labels_uri(self):
    return os.path.join(self.config.messages_path, MessagesLocalStorage.labels_file_name)


  def put_attachment(self, message_id, filename, data):
    file_path = os.path.join(self.config.messages_path, message_id, MessagesLocalStorage.attachments_folder_name, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'bw') as file:
      file.write(data)
    return file_path


  def list_attachments(self):
    user_labels = { it.get('id'): it.get('name') for it in self.get_labels() if it.get('type') == 'user' }
    for message_info in self.list_messages():
      message_file_path = message_info.get('uri')
      message = self.get_message(message_file_path)
      message_label_ids = message.get('labelIds', [])
      label_name = next((label for it in message_label_ids if (label := user_labels.get(it)) is not None), None)
      if label_name:
        attachments_folder_path = os.path.join(os.path.dirname(message_file_path), MessagesLocalStorage.attachments_folder_name)
        for file_path in scandir(attachments_folder_path, recursive=False):
          yield dict(label_name=label_name, uri=file_path)


  def get_attachment(self, uri):
    with open(uri, 'br') as file:
      return file.read()
  
  message_file_name = 'message.json'
  labels_file_name = 'labels.json'
  attachments_folder_name = 'attachments'
