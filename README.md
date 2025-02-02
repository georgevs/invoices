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

cd ~/ws/DEV/projects/invoices
pip3 install -r requirements.txt 
```

### Fetch messages from Gmail
The client machine where authentication runs in the browser must PROXY `8080:172.20.0.220:8080` into the machine where Docker runs `172.20.0.220` container
```bash
app/fetch_messages.py --bind-addr 172.20.0.220 | tee ./data/confidential/messages.log
```

### Parse toplofikaciya
```
app/messages_db.py | grep toplofikaciya | cut -f2 | tee data/confidential/toplofikaciya.lst

cat data/confidential/toplofikaciya.lst | cut -f1 \
| xargs -I {} app/digest_pdf.py --contragent toplofikaciya --invoices-path ./data/confidential/invoices '{}' \
2>data/confidential/toplofikaciya.err.lst ; mv data/confidential/toplofikaciya.err.lst data/confidential/toplofikaciya.lst 

find ./data/confidential/invoices -type f -name '*.json' | grep toplofikaciya | sort
```

### Parse sofiyskavoda
```
app/messages_db.py | grep sofiyskavoda | cut -f2 | tee data/confidential/sofiyskavoda.lst

cat data/confidential/sofiyskavoda.lst | cut -f1 \
| xargs -I {} app/digest_pdf.py --contragent sofiyskavoda --invoices-path ./data/confidential/invoices '{}' \
2>data/confidential/sofiyskavoda.err.lst ; mv data/confidential/sofiyskavoda.err.lst data/confidential/sofiyskavoda.lst 

find ./data/confidential/invoices -type f -name '*.json' | grep sofiyskavoda | sort
```

### Parse electrohold
```
app/messages_db.py | grep electrohold | cut -f2 | tee data/confidential/electrohold.lst

cat data/confidential/electrohold.lst | cut -f1 \
| xargs -I {} app/digest_pdf.py --contragent electrohold --invoices-path ./data/confidential/invoices '{}' \
2>data/confidential/electrohold.err.lst ; mv data/confidential/electrohold.err.lst data/confidential/electrohold.lst 

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
