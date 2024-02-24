from googleapiclient.discovery import build as build_service

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
      self.authenticated_service = build_service(self.name, self.version, credentials=credentials)
    return self.authenticated_service
