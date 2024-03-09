FROM python:3.11.5-slim
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get -y install gcc
RUN /usr/local/bin/python -m pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN mkdir -p /src
COPY . /src
WORKDIR /src