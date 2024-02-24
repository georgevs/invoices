

# Refresh token

[Medium: Refresh token](https://medium.com/@developer_29635/how-to-get-a-refresh-token-for-google-apis-in-a-python-script-b68f1b6aa668)


### Install dependencies
```bash
pip3 install \
  google-api-python-client \
  install google-auth-oauthlib
```

### Generate authorization url
```python
from google_auth_oauthlib.flow import Flow
flow = Flow.from_client_secrets_file(
    './client_secret.json',
    scopes = [
      'https://www.googleapis.com/auth/photoslibrary.readonly', 
    ],
)
flow.redirect_uri = 'https://localhost:8080/auth/google/callback'
# flow.run_local_server()
authorization_url, state = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true'
)
print('Please go here to authorize the access.')
print(authorization_url)

# https://accounts.google.com/o/oauth2/auth
#   ?response_type=code
#   &client_id=1234.apps.googleusercontent.com
#   &redirect_uri=http%3A%2F%2Flocalhost%3A8080%2F
#   &scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fphotoslibrary.readonly
#   &state=LAKSbIhnYtuLLTJ9KOFfwYFNysQ0rl
#   &access_type=offline
```

### Exchange code for token
```python
# https://localhost:8080/auth/google/callback
#   ?state=rIJYBt9eiZzBx1XTXezQQ8UTedrfLX
#   &code=4%2F0AfJohXkLch7dKJThTOzMKHcEall665erwI7Igqy7UxaUww0YwBmJzzrLrxb5zBi4dsUU6A
#   &scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fphotoslibrary.readonly

authorization_response = 'https://localhost:8080/auth/google/callback?state=rIJYBt9eiZz....' 
tokens = flow.fetch_token(authorization_response=authorization_response)
print(flow.credentials.to_json())

# { "token": "ya29.a0AfB_byDxRkOeh-p..."
# , "refresh_token": "1//0gZFcredacted_0SiJ6nHA"
# , "token_uri": "https://oauth2.googleapis.com/token"
# , "client_id": "123redacted.apps.googleusercontent.com"
# , "client_secret": "redacted"
# , "scopes": ["https://www.googleapis.com/auth/photoslibrary.readonly"]
# , "expiry": "2023-10-24T16:57:18.473358Z"}
```

### Use access token
```python
async with aiohttp.ClientSession() as session:
  access_token = 'ya29.a0AfB_..._V9-hCweFHQ0171'  
  async with session.get(
            url = 'https://photoslibrary.googleapis.com/v1/mediaItems',
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
    ) as resp:
        print(f'resp.status:{resp.status}')
        data = await resp.json()
    await session.close()
```

### Refresh token
```python
async with session.post(
        url = 'https://oauth2.googleapis.com/token',
        data = {
            'grant_type': 'refresh_token',
            'client_secret': "redacted",
            'refresh_token': "1//0gZFcredacted_0SiJ6nHA",
            'client_id': "123redacted.apps.googleusercontent.com",
        },
    ) as resp:
        print( f'refresh_access_token resp.status:{resp.status}')
        data = await resp.json()
        self.access_token = data['access_token']
        self.expires_in = data['expires_in']
```