from ubuntu:focal

COPY . /volume_watchdog

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        python3.7 \
        python3-pip \
        python3-setuptools \
        python3-wheel \
    && cd /volume_watchdog \
    && pip3 install -U pip \
    && pip install -e . \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/usr/local/bin/nvw"]
CMD []
