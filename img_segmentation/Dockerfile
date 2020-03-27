FROM ubuntu:18.04

COPY . /opt/ps2top

RUN apt-get -y -qq update && \
    apt-get -y -qq install python3 python3-pip && \
    pip3 install -r /opt/ps2top/requirements.txt

RUN groupadd -r extractor && useradd --no-log-init -r -g extractor extractor

COPY bin2png/entrypoint.py /opt/ps2top

USER extractor

WORKDIR /opt/ps2top

ENTRYPOINT [ "python3", "/opt/ps2top/entrypoint.py" ]
