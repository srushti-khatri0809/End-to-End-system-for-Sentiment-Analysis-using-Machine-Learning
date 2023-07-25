FROM python:3.7-slim

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev-is-python3

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app
