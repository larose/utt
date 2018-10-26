FROM ubuntu:16.04

ENV PYTHON=python3
ENV PIP=pip3
ENTRYPOINT ["make"]
CMD []
WORKDIR /utt
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends bash-completion make python3-pip python3-setuptools
RUN pip3 install --upgrade pip
