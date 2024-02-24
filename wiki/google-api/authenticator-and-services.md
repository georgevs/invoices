# Google Identity Service and API

### References
[Google: Server side web app authorization](https://developers.google.com/identity/protocols/oauth2/web-server#python_1)  

### Dependencies
```bash
pip3 install \
  google-api-python-client
  google-auth-oauthlib
```

### Authenticator
```python
def authenticate(client_config, scopes, bind_addr):
  flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_config(client_config, scopes)
  return flow.run_local_server(bind_addr=bind_addr, host='localhost', port=8080,        
                               open_browser=False, prompt='consent')

def credentials_to_json(credentials):
  return json.loads(credentials.to_json())

def credentials_from_json(credentials):
  return google.oauth2.credentials.Credentials.from_authorized_user_info(credentials) if credentials else None


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
```

### Services
```python
class Service:
  def __init__(self, authenticator, name, version, scopes):
    self.authenticator = authenticator
    self.scopes = scopes
    self.name = name
    self.version = version
    self.authenticated_service = None

  def service(self):
    if not self.authenticated_service:
      credentials = self.authenticator.authenticate(self.scopes)
      self.authenticated_service = googleapiclient.discovery.build(
        self.name, self.version, credentials=credentials)
    return self.authenticated_service


# https://developers.google.com/gmail/api/reference/rest
class Gmail(Service):
  def __init__(self, authenticator):
    scopes = ['https://www.googleapis.com/auth/gmail.readonly']
    super().__init__(authenticator, 'gmail', 'v1', scopes)


# https://developers.google.com/sheets/api/reference/rest
class Spreadsheets(Service):
  def __init__(self, authenticator):
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    super().__init__(authenticator, 'sheets', 'v4', scopes)


# https://developers.google.com/drive/api/reference/rest
class Drive(Service):
  def __init__(self, authenticator):
    scopes = ['https://www.googleapis.com/auth/drive.readonly']
    super().__init__(authenticator, 'drive', 'v3', scopes)
```
