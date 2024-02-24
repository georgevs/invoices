from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from util.json import load_json, save_json, try_load_json

import google_auth_httplib2
import httplib2
import json


class Config:
  def __init__(self, args):
    self.secrets_path = args.secrets_path or 'secrets'
    self.bind_addr = args.bind_addr or None
    self.client_secret_file_path = f'{self.secrets_path}/client_secret.json'
    self.cached_credentials_file_path = f'{self.secrets_path}/credentials.json'


class Authenticator:
  def __init__(self, config):
    self.config = config
    self.credentials = None

  def authenticate(self, scopes):
    update_credentials = False

    if not self.credentials:
      self.credentials = credentials_from_json(
        try_load_json(self.config.cached_credentials_file_path))

    if self.credentials and not set(self.credentials.scopes).issuperset(set(scopes)):
      scopes = list(set(self.credentials.scopes).union(set(scopes)))
      self.credentials = None

    if self.credentials and self.credentials.expired:
      request = google_auth_httplib2.Request(httplib2.Http())
      self.credentials.refresh(request)
      update_credentials = self.credentials.valid
      if not self.credentials.valid:
        self.credentials = None

    if not self.credentials:
      client_config = load_json(self.config.client_secret_file_path)
      self.credentials = authenticate(client_config, scopes, bind_addr=self.config.bind_addr)
      update_credentials = True

    if update_credentials:  
      save_json(self.config.cached_credentials_file_path,
                credentials_to_json(self.credentials))
              
    return self.credentials


def authenticate(client_config, scopes, bind_addr):
  flow = InstalledAppFlow.from_client_config(client_config, scopes)
  return flow.run_local_server(bind_addr=bind_addr, host='localhost', port=8080, open_browser=False, prompt='consent')


def credentials_to_json(credentials):
  return json.loads(credentials.to_json())


def credentials_from_json(credentials):
  return Credentials.from_authorized_user_info(credentials) if credentials else None
