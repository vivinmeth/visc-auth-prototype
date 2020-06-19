FROM python:3.8-buster
MAINTAINER VIVINMETH

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /authapp
WORKDIR /authapp
COPY ./authapp /authapp
