FROM ubuntu:16.04

RUN apt-get update && apt-get upgrade -y

RUN apt-get install build-essential -y

RUN apt-get install libssl-dev openssl wget -y

RUN apt-get update

RUN apt-get install -y git-core

RUN apt-get install libsqlite3-dev

RUN wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz

RUN tar xzvf Python-3.7.0.tgz

RUN cd Python-3.7.0/ && ./configure --enable-loadable-sqlite-extensions

RUN cd Python-3.7.0/ && make 

RUN apt-get install libffi-dev

RUN cd Python-3.7.0/ && make install

RUN rm -rf Python-3.7.0

RUN rm Python-3.7.0.tgz

RUN apt-get install python-pip -y

RUN rm /usr/bin/pip

RUN ln /usr/local/bin/pip3.7 /usr/bin/pip