FROM python:3.10.9-slim-buster
# ENV http_proxy="http://172.16.20.126:3128"
# ENV https_proxy="http://172.16.20.126:3128"
RUN apt-get update  --fix-missing && \
    apt-get install -y gcc libpq-dev && \
    apt clean && \
    rm -rf /var/cache/apt/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

COPY requirements/ /tmp/requirements

RUN pip install -U pip && \
    pip install --no-cache-dir -r /tmp/requirements/dev.txt

COPY . /src
ENV PATH "$PATH:/src/scripts"

RUN useradd -m -d /src -s /bin/bash app \
    && chown -R app:app /src/* && chmod +x /src/scripts/*
RUN apt install dos2unix 
WORKDIR /src
USER root

CMD ["./scripts/start-dev.sh"]