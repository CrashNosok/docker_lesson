FROM python:3.11-slim

WORKDIR /usr/src/app

COPY . .

RUN apt update && \
    apt install -y git && \
    apt install -y vim && \
    pip install --no-cache-dir -r requirements.txt


CMD [ "python", "./script_request.py" ]
