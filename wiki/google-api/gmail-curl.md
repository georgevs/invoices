# Curl playground

### Load authorization token
[jq: manual](https://jqlang.github.io/jq/manual/)  
```bash
sudo apt install jq
export TOKEN=$(jq -r .token secrets/credentials.json)
```
### List labels
```bash
curl -s https://gmail.googleapis.com/gmail/v1/users/me/labels \
  -H "Authorization: Bearer $TOKEN" 
```
### List messages
```bash
curl -s https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=5 \
  -H "Authorization: Bearer $TOKEN" | tee __messages.json

(PAGE_TOKEN=$(jq -r .nextPageToken __messages.json) ; \
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=5&pageToken=$PAGE_TOKEN" \
  -H "Authorization: Bearer $TOKEN" | tee __messages.json)
```
