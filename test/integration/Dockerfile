FROM python:3.6.10-slim

ENTRYPOINT ["make"]
WORKDIR /utt
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    bash-completion \
    make
COPY . .
