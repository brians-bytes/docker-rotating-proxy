FROM python:3.6-alpine3.6
MAINTAINER "Brian Rotich <brianrotych@gmail.com>"
LABEL maintainer="Brian Rotich <brianrotych@gmail.com>"

# user account

# add ha proxy
RUN apk update \
    && apk add haproxy

COPY . /haproxy

WORKDIR /haproxy

# install python requirements
RUN pip install --upgrade pip \
    && pip install -r requirements.txt


EXPOSE 8080 4444

CMD ["python", "start.py"]
