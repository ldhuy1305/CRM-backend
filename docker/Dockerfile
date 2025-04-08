FROM python:3.12-alpine

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

COPY ../requirements.txt /

RUN pip install -r /requirements.txt

RUN mkdir /src

COPY ../src /src