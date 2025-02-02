# Google GMail
[Google: overview](https://developers.google.com/gmail/api)  
[Google: reference](https://developers.google.com/gmail/api/reference/rest)  
[Google: discovery](https://sheets.googleapis.com/$discovery/rest?version=v4)  

[Google: quickstart](https://developers.google.com/gmail/api/quickstart/python)  

### Manage secrets
Push secrets:
```
tar czv secrets | openssl enc -aes-128-cbc -pbkdf2 -salt -out ~/ws-archive/secrets.hacct-script.tar.gz.enc
```
Fetch secrets:
```
openssl enc -d -aes-128-cbc -pb kdf2 -salt -in ~/ws-archive/secrets.hacct-script.tar.gz.enc | tar xzv
```
### Run docker container
```bash
sudo apt install docker.io docker-buildx

DOCKER_BUILDKIT=1 \
PASSWD=$(read -s -p 'Password:' PASSWD ; echo "$USER:$PASSWD") \
docker image build --no-cache --secret id=PASSWD --tag dev-jupyter - << EOF
  FROM ubuntu
  RUN --mount=type=secret,id=PASSWD \
    apt-get update && apt-get install -y sudo tmux vim curl python3 python3-pip && \
    useradd -m -s /bin/bash -G sudo $USER && \
    cat /run/secrets/PASSWD | chpasswd
    USER $USER
    ENV PATH "\$PATH:/home/$USER/.local/bin"
    RUN pip3 install notebook
EOF

docker network create \
  -d bridge \
  --subnet 172.20.0.0/16 \
  --gateway 172.20.0.1 \
  bridge-dev

docker container run -it \
  --name dev-jupyter \
  --network bridge-dev \
  --ip 172.20.0.220 \
  --publish 8888:8888 \
  --publish 8080:8080 \
  --volume "/home/$USER/ws/DEV:/home/$USER/ws/DEV" \
  --volume "/home/$USER/ws/NOTES/wiki:/home/$USER/ws/NOTES/wiki" \
  -d dev-jupyter

docker container inspect dev-jupyter | jq -r '.[].NetworkSettings.Networks["bridge-dev"].IPAddress'
docker container start -ia --detach-keys='ctrl-x' dev-jupyter
docker container attach --detach-keys='ctrl-x' dev-jupyter

~/.local/bin/jupyter notebook --ip 0.0.0.0 --port 8888 --no-browser
```

### Run scripts
The client machine where authentication runs in the browser must PROXY `8080:172.20.0.220:8080` into the machine where Docker runs `172.20.0.220` container
```bash
docker container start -ia --detach-keys='ctrl-x' dev-jupyter
cd ~/ws/DEV/projects/invoices
pip3 install -r requirements.txt 
app/fetch_messages.py --bind-addr 172.20.0.220 | tee ./data/confidential/messages.log
app/digest_invoices.py | tee ./data/confidential/invoices.log
app/get_missing_invoices.py
```

### Parse toplofikaciya
```
app/messages_db.py | grep toplofikaciya | cut -f2 | tee __toplofikaciya.lst
cat __toplofikaciya.lst | xargs -I {} app/toplofikaciya.py '{}' 2>__toplofikaciya.err.lst ; mv __toplofikaciya.err.lst __toplofikaciya.lst 
find ./data/confidential/invoices -type f -name '*.json' | grep toplofikaciya | sort
```

### Parse sofiyskavoda
```
app/messages_db.py | grep sofiyskavoda | cut -f2 | tee __sofiyskavoda.lst
cat __sofiyskavoda.lst | xargs -I {} app/sofiyskavoda.py '{}' 2>__sofiyskavoda.err.lst ; mv __sofiyskavoda.err.lst __sofiyskavoda.lst 
find ./data/confidential/invoices -type f -name '*.json' | grep sofiyskavoda | sort
```

### Parse electrohold
```
app/messages_db.py | grep electrohold | cut -f2 | tee __electrohold.lst
cat __electrohold.lst | xargs -I {} app/electrohold.py '{}' 2>__electrohold.err.lst ; mv __electrohold.err.lst __electrohold.lst 
find ./data/confidential/invoices -type f -name '*.json' | grep electrohold | sort
```

### Check for missing invoices
```
app/get_missing_invoices.py
```

### Pull fetched messages
```bash
mkdir -p ~/ws/DEV/projects/invoices/data/confidential
ssh xps tar -czC '~/ws/DEV/projects/invoices/data/confidential' messages | tar -xzvC ~/ws/DEV/projects/invoices/data/confidential
```
