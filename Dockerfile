FROM amd64/ubuntu:20.04

WORKDIR /app

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        libxml2-utils \
        python-is-python3 \
        pip && \
    unlink /etc/localtime && \
    ln -s /usr/share/zoneinfo/Europe/Brussels /etc/localtime

RUN apt-get install -y \
        python3-mapnik \
        fonts-noto-cjk \
        fonts-noto-hinted \
        fonts-noto-unhinted \
        fonts-hanazono \
        ttf-unifont

RUN pip install cram lxml

