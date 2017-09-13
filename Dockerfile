FROM phusion/baseimage:0.9.22
MAINTAINER Brian Rotich <brianrotych@gmail.com>

RUN apt-get update && \
    apt-get install -y haproxy

ADD haproxy.cfg /usr/local/etc/haproxy.cfg

EXPOSE 8080 4444

CMD haproxy -d -f /usr/local/etc/haproxy.cfg