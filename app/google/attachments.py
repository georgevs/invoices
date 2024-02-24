import base64


class Attachments:
  def __init__(self, gmail):
    self.gmail = gmail

  def list_attachments(self, label_ids=None, user_id='me'):
    messages = self.gmail.list_messages(label_ids=label_ids, user_id=user_id)
    for message in messages:
      message_id = message.get('id')
      message = self.gmail.get_message(message_id=message_id, user_id=user_id)
      for attachment in self.__get_message_attachments(message):
        attachment.update(message_id=message_id)
        yield attachment

  def get_attachment(self, attachment_id, message_id, user_id='me'):
    attachment = self.gmail.get_attachment(attachment_id, message_id, user_id)
    size = int(attachment.get('size'))
    data = base64.urlsafe_b64decode(attachment.get('data'))
    return data, size

  def __get_message_attachments(self, message):
    payload = message.get('payload')
    parts = payload.get('parts') if payload else []
    def maybe_attachment(part):
      if ((mime_type := part.get('mimeType')) and
          (filename := part.get('filename')) and 
          (body := part.get('body')) and
          (attachment_id := body.get('attachmentId')) and
          (size := body.get('size'))):
        return dict(mime_type=mime_type, filename=filename, attachment_id=attachment_id, size=int(size))
    attachments = filter(bool, map(maybe_attachment, parts)) if parts else []
    for attachment in attachments:
      yield attachment
