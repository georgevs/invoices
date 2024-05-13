from util.json import save_json, load_json
from util.os import scandir
import os


class Config:
  def __init__(self, args):
    self.invoices_path = args.invoices_path or '__invoices'


class InvoicesLocalStorage:
  def __init__(self, config):
    self.config = config

  def put_invoice(self, label_name, file_name, invoice):
    file_path = os.path.join(self.config.invoices_path, label_name, file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    save_json(file_path, invoice)
    return file_path

  def list_invoices(self):
    for file_path in scandir(self.config.invoices_path):
      label_name, _ = os.path.split(os.path.relpath(file_path, self.config.invoices_path))
      yield dict(label_name=label_name, uri=file_path)

  def get_invoice(self, uri):
    return load_json(uri)
