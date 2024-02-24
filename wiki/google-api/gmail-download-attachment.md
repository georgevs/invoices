# Gmail: download attachment

### Dependencies
```bash
pip3 install \
  google-api-python-client \
  google-auth-oauthlib \
  pdfplumber
```
### Services
```pyhton
authenticator = Authenticator(config)
gmail = Gmail(authenticator)
```
### Fetch labels list
```python
result = (gmail.service().users()
  .labels().list(userId='me')
  .execute())
```
```json
{
  "labels": [
    {"id": "Label_4934464314942204354", "name": "toplo", "type": "user"}, 
    {"id": "Label_6647454074447976033", "name": "sofiyskavoda", "type": "user"}
  ]
}
```
### Fetch messages list
```python
result = (gmail.service().users()
  .messages().list(userId='me', maxResults=3)
  .execute())
```
```json
{
  "messages": [
    { "id": "18dcb3ba17c648e8", "threadId": "18dcb3ba17c648e8" },
    { "id": "18db2b7f8e4c8c5e", "threadId": "18db249a0526fbc5" },
    { "id": "18db2b38deab26cf", "threadId": "18db25249fc165eb" }
  ],
  "nextPageToken": "12155819075757249057",
  "resultSizeEstimate": 201
}
```
### Fetch message
```python
message = (gmail.service().users()
  .messages().get(userId='me', id='18db2b38deab26cf')
  .execute())
```
```json
{
  "id": "18db2b38deab26cf",
  "payload": {
    "parts": [
      {
        "partId": "1",
        "mimeType": "application/octet-stream",
        "filename": "1902327978.pdf",
        "headers": [
          {
            "name": "Content-Transfer-Encoding",
            "value": "base64"
          }
        ],
        "body": {
          "attachmentId": "ANGjdJ...lfz0",
          "size": 176397
        }
      }
    ]
  }
}
```
### Fetch attachment
```python
attachment = (gmail.service().users().messages().attachments().get(
    userId='me', 
    messageId='18db2b38deab26cf', 
    id='ANGjdJ...lfz0'
  ).execute())

size = int(attachment.get('size'))
data = base64.urlsafe_b64decode(attachment.get('data'))

with open('1902327978.pdf', 'bw') as file:
  file.write(data)

pdf = pdfplumber.open(io.BytesIO(data))
println(pdf.pages)
```
