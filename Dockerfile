FROM ubuntu:18.04

COPY . /root

RUN apt-get -y -qq update && \
    apt-get -y -qq install python3 python3-pip && \
    pip3 install -r /root/requirements.txt

