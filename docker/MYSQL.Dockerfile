FROM mysql:8

RUN apt-get update \
    && apt-get install -y \
    wget \
    unzip

RUN sed -i 's/NULL//g' /etc/mysql/my.cnf
