from google.service import Service


class Gmail(Service):
  def __init__(self, authenticator):
    scopes = ['https://www.googleapis.com/auth/gmail.readonly']
    super().__init__(authenticator, 'gmail', 'v1', scopes)

  def list_labels(self, user_id='me'):
    # https://developers.google.com/gmail/api/reference/rest/v1/users.labels/list
    return self.service().users().labels().list(userId=user_id).execute().get('labels')

  def list_messages(self, label_ids=None, max_results=None, user_id='me'):
    # https://developers.google.com/gmail/api/reference/rest/v1/users.messages/list
    response = (self.service().users().messages()
      .list(userId=user_id, labelIds=label_ids, maxResults=max_results)
      .execute())
    page_messages, next_page_token = response.get('messages'), response.get('nextPageToken')
    if page_messages:
      yield from page_messages
      while next_page_token:
        response = (self.service().users().messages()
          .list(userId=user_id, maxResults=max_results, pageToken=next_page_token)
          .execute())
        page_messages, next_page_token = response.get('messages'), response.get('nextPageToken')
        yield from page_messages

  def get_message(self, message_id, user_id='me'):
    # https://developers.google.com/gmail/api/reference/rest/v1/users.messages/get
    return (self.service().users()
      .messages().get(id=message_id, userId=user_id)
      .execute())

  def get_attachment(self, attachment_id, message_id, user_id='me'):
    # https://developers.google.com/gmail/api/reference/rest/v1/users.messages.attachments/get
    return (self.service().users().messages()
      .attachments().get(id=attachment_id, messageId=message_id, userId=user_id)
      .execute())
