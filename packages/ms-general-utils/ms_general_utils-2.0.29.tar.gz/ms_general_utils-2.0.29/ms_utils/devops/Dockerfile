FROM python:3.11.5-bullseye
ARG EXPORT_PORT
ENV port $EXPORT_PORT
ARG DIRECTORY_BASE
ENV directory $DIRECTORY_BASE
RUN apt update &&\
    apt install -y \
    ca-certificates openssl python3-dev default-libmysqlclient-dev build-essential libssl-dev libffi-dev python3-setuptools && \
    rm -rf /var/lib/apt/lists/*

ADD http://cdn.vacolba.inet/cfssl/vacolba_ca.crt /usr/local/share/ca-certificates/vacolba_ca.crt

RUN update-ca-certificates

ENV REQUESTS_CA_BUNDLE /etc/ssl/certs/ca-certificates.crt

WORKDIR /usr/app

COPY $directory ./

ADD http://cdn.vacolba.inet/cfssl/vacolba_ca.crt ./certs/

COPY deploy/app/run.sh ./

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE $EXPORT_PORT

RUN ["chmod", "+x", "./run.sh"]

RUN sed 's/\r$//' ./run.sh > ./parse_script.sh

RUN echo "/bin/bash /usr/app/parse_script.sh $port" > /tmp.sh

RUN ["chmod", "+x", "/tmp.sh"]

ENTRYPOINT ["/bin/bash", "/tmp.sh"]