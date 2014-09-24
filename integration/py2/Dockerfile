FROM ubuntu:14.04

ENTRYPOINT ["make"]
WORKDIR /utt

RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends make python

ADD ./utt /utt
