FROM python:3.13-slim


RUN apt-get update && apt-get install -y \
    gcc libpq-dev && \
    pip install --upgrade pip

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
