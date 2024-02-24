from util.os import scandir
import os


class Config:
  def __init__(self, args):
    self.attachments_path = args.attachments_path or '__attachments'


class AttachmentsLocalStorage:
  def __init__(self, config):
    self.config = config

  def put_attachment(self, label_name, filename, data):
    file_path = os.path.join(self.config.attachments_path, label_name, filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'bw') as file:
      file.write(data)
    return file_path

  def list_attachments(self):
    for file_path in scandir(self.config.attachments_path):
      label_name, _ = os.path.split(os.path.relpath(file_path, self.config.attachments_path))
      yield dict(label_name=label_name, uri=file_path)

  def get_attachment(self, uri):
    with open(uri, 'br') as file:
      return file.read()
