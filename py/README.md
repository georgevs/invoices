# Digest PDF with Python

## Install dependencies
```
pip3 install -r requirements.txt
```

## Sofiyska voda

### Acquire data

Subscribe to invoice emails or download invoice PDFs from https://www.sofiyskavoda.bg

### Process invoices
```
find ./data/__confidential/sofiyskavoda -name '*.pdf' | xargs -I% bash -c 'PYTHONPATH+=./src python3 ./src/digest_pdf.py % > %-digest.json'
find ./data/__confidential/sofiyskavoda -name '*.pdf' | xargs -I% bash -c 'PYTHONPATH+=./src python3 ./src/parse_sofiyskavoda_pdf.py % > %-invoice.json'
```

## Toplofikaciya

### Acquire data

Subscribe to and download invoices from https://www.e-invoice.bg

### Process invoices
```
find ./data/__confidential/toplofikaciya -name '*.pdf' | xargs -I% bash -c 'PYTHONPATH+=./src python3 ./src/digest_pdf.py % > %-digest.json'
find ./data/__confidential/toplofikaciya -name '*.pdf' | xargs -I% bash -c 'PYTHONPATH+=./src python3 ./src/parse_toplofikaciya_pdf.py % > %-invoice.json'
```

## Electrohold

### Acquire data

Subscribe to and download invoices from https://info.electrohold.bg/webint/vok/index.php

### Process invoices
```
find ./data/__confidential/electrohold -name '*.pdf' | xargs -I% bash -c 'PYTHONPATH+=./src python3 ./src/digest_pdf.py % > %-digest.json'
find ./data/__confidential/electrohold -name '*.pdf' | xargs -I% bash -c 'PYTHONPATH+=./src python3 ./src/parse_electrohold_pdf.py % > %-invoice.json'
```


## Setup Python environment with Docker

### Create docker network
```
docker network create \
  -d bridge \
  --subnet 172.20.0.0/16 \
  --gateway 172.20.0.1 \
  bridge-dev
```

### Create docker dev image
```
DOCKER_BUILDKIT=1 \
PASSWD=$(read -s -p 'Password:' PASSWD ; echo "$USER:$PASSWD") \
docker image build \
  --no-cache \
  --secret id=PASSWD \
  --tag dev-ubuntu \
  - << EOF

  FROM ubuntu
  RUN --mount=type=secret,id=PASSWD \
    apt-get update && \
    apt-get install -y sudo && \
    useradd -m -s /bin/bash -G sudo $USER && \
    cat /run/secrets/PASSWD | chpasswd
EOF
```

### Create docker Python image
```
docker image build --no-cache --force-rm --tag dev-python - << EOF
  FROM dev-ubuntu
  RUN apt-get update && apt-get install -y tmux vim curl less python3 python3-pip libmagickwand-dev
  USER $USER
  ENV PATH "\$PATH:/home/$USER/.local/bin"
  RUN pip3 install notebook Wand
EOF
```

### Run Python container
```
docker container run -it \
  --name dev-python \
  --network bridge-dev \
  --ip 172.20.0.100 \
  --volume "$PWD:$PWD" \
  --publish 8888:8888 \
  --rm -d dev-python
```

### Start jupyter notebook (optional)
```
docker container exec -it \
  --user $USER \
  dev-python jupyter notebook --ip 0.0.0.0 --port 8888 --no-browser
```
