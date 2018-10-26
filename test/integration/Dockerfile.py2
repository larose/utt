FROM ubuntu:16.04

ENV PYTHON=python
ENV PIP=pip
ENTRYPOINT ["make"]
CMD []
WORKDIR /utt
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends bash-completion make python python-pip python-setuptools
RUN pip install --upgrade pip
