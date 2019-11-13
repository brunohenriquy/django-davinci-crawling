FROM python:3.6.9-slim

ARG ssh_prv_key
ARG ssh_pub_key

# DB connection information
ENV DB_USER bgds
ENV DB_PASSWORD bgds
ENV DB_HOST postgres
ENV DB_PORT 5432
ENV DB_NAME bgds

# CASSANDRA connection information
ENV CASSANDRA_DB_HOST host.docker.internal
ENV CASSANDRA_DB_NAME davinci
ENV CASSANDRA_DB_USER bgds
ENV CASSANDRA_DB_PASSWORD bgds

# Install git and openssh
RUN apt-get update && \
    apt-get install -y \
        git \
        openssh-server \
        libgdal-dev \
        libev4 \
        libev-dev \
        build-essential

ENV CPLUS_INCLUDE_PATH /usr/include/gdal
ENV C_INCLUDE_PATH /usr/include/gdal

# Authorize SSH Host
RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan github.com > /root/.ssh/known_hosts

# Add the keys and set permissions
RUN echo "$ssh_prv_key" > /root/.ssh/id_rsa && \
    echo "$ssh_pub_key" > /root/.ssh/id_rsa.pub && \
    chmod 600 /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa.pub

RUN mkdir /davinci

ADD . /davinci/

RUN cd /davinci && python setup.py develop
RUN cd /davinci && pip install -r requirements.txt || echo "ignore error"
RUN cd /davinci && pip install -r requirements_tests.txt || echo "ignore error"

RUN mkdir -p /data/davinci_crawling/log

WORKDIR /davinci

VOLUME /davinci

EXPOSE 8000

CMD tail -f /dev/null