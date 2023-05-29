FROM python:3.10.4-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip 
COPY ./requirements.txt /usr/src/app
RUN apk update && \
 apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install -r requirements.txt

COPY . .