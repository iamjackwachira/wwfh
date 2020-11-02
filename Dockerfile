FROM ubuntu:bionic

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update --fix-missing && apt-get install -y --no-install-recommends \
    wget gpg dirmngr gpg-agent build-essential checkinstall tk-dev \
    libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev \
    libc6-dev libbz2-dev python3-pip python3-dev libpq-dev \
    postgresql postgresql-contrib

WORKDIR /code
COPY ./requirements/* /code/requirements/
RUN pip3 install cython && pip3 install setuptools
RUN pip3 install -r requirements/production.txt --no-cache-dir

COPY . /code

EXPOSE 8080

ENTRYPOINT ["bash", "/code/docker-entrypoint.sh"]
