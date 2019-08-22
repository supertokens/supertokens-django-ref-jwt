FROM ubuntu:16.04

RUN apt-get update && apt-get upgrade -y

RUN apt-get install build-essential -y

RUN apt-get install libssl-dev openssl wget -y

RUN wget https://www.python.org/ftp/python/3.5.0/Python-3.5.0.tgz

RUN tar xzvf Python-3.5.0.tgz

RUN cd Python-3.5.0 && ./configure && make && make install

RUN apt-get update

RUN apt-get install -y git-core

RUN apt-get install python-pip -y

RUN rm /usr/bin/pip

RUN ln /usr/local/bin/pip3.5 /usr/bin/pip

RUN apt-get install libsqlite3-dev

RUN wget https://www.python.org/ftp/python/3.5.0/Python-3.5.0.tar.xz

RUN tar -xf Python-3.5.0.tar.xz

RUN cd Python-3.5.0/ && ./configure --enable-loadable-sqlite-extensions && make && make install

RUN rm -rf Python-3.5.0

RUN rm Python-3.5.0.tar.xz Python-3.5.0.tgz