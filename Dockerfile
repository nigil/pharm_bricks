FROM debian:stretch
MAINTAINER Aleksandr Butenko <nigillus42@gmailcom>

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y python-pip python-rdkit less python-cairocffi


RUN apt-get update -q && apt-get install -q -y \
        curl apt-transport-https apt-utils dialog

WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt