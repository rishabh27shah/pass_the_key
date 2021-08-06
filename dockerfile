# pull official base image
FROM python:3.9-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update &&\
    apk add postgresql-dev gcc python3-dev musl-dev

# set up django project
RUN mkdir /pass-the-key
WORKDIR /pass-the-key
ADD . /pass-the-key
RUN pip install -r requirements.txt
EXPOSE 8000

