FROM ubuntu:14.10

ENV PYTHON=python3
ENV PIP=pip3
ENTRYPOINT ["make"]
CMD []
WORKDIR /utt
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends make python3-pip
COPY . /utt
