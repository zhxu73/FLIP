FROM ubuntu:18.04

# bin2png, img_segmentation, fluorescence_aggregation
ARG STEP

# copy source code
COPY . /opt/ps2top

# install dependency
RUN apt-get -y -qq update && \
    apt-get -y -qq install python3 python3-pip && \
    pip3 install -r /opt/ps2top/requirements.txt

# add non-root user
RUN groupadd -r extractor && useradd --no-log-init -r -g extractor extractor

# copy entrypoint
COPY $STEP/entrypoint.py /opt/ps2top

USER extractor

WORKDIR /opt/ps2top

ENTRYPOINT [ "python3", "/opt/ps2top/entrypoint.py" ]