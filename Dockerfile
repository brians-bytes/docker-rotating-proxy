FROM python:3.6-alpine3.6

MAINTAINER "Brian Rotich <brianrotych@gmail.com>"
LABEL maintainer="Brian Rotich <brianrotych@gmail.com>"

# add ha proxy
RUN apk update
RUN apk --no-cache add haproxy

COPY . /app
WORKDIR /app

# install python requirements
RUN pip install -r requirements.txt

EXPOSE 4444 8080

CMD ["python", "start.py"]
