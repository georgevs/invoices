#!/usr/bin/env python3

import collections
import operator
import os
import util.json
import util.os


Attachment = collections.namedtuple('Attachment', ['contragent', 'uri'])


def load_message_attachments(messages_path):
  labels = util.json.load_json(os.path.join(messages_path, 'labels.json'))
  labels = filter(lambda it: it['type'] == 'user', labels)
  labels = map(operator.itemgetter('id', 'name'), labels)
  labels = dict(labels)

  get_label = lambda label_ids: next(filter(bool, (labels.get(id) for id in label_ids)), None)
  get_attachments = lambda message_uri: list(filter(util.os.has_ext('.pdf'), util.os.scandir(os.path.dirname(message_uri), recursive=True)))
  messages = util.os.scandir(messages_path, recursive=True)
  messages = filter(lambda it: os.path.basename(it) == 'message.json', messages)
  messages = (dict(uri=it, message=util.json.load_json(it)) for it in messages)
  messages = (dict(**it, contragent=get_label(it.get('message').get('labelIds'))) for it in messages)
  messages = (dict(**it, attachment=get_attachments(it.get('uri'))) for it in messages)
  attachments = (
    Attachment(message['contragent'], uri)
    for message in messages
    for uri in message['attachment']
  )
  return attachments


if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('--messages-path', default='./data/confidential/messages')
  args = parser.parse_args()
  attachments = load_message_attachments(**vars(args))
  attachments = map('\t'.join, attachments)
  print(*sorted(attachments), sep=os.linesep)
