FROM ubuntu

# ----- Prepare -----

## PostgreSQL設定
ARG PSQLUSER=sns_user
ARG PSQLPASS=nH9Us5zw
ARG PSQLDBNAME=sns_dbname

## 設定しないとapt install中に止まる
ENV DEBIAN_FRONTEND=noninteractive
## PASSWORD入力なしでpsqlログインするのに必要
ENV PGPASSWORD=${PSQLPASS}

# ----- Install -----

RUN apt update

## PostgreSQL
RUN apt install -y python3-dev python3-pip libpq-dev postgresql postgresql-contrib sudo

# ----- Setting -----

## PostgreSQL初期設定
### SQLファイル読込で一括設定
### ユーザー作成、データベース作成
USER postgres
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER ${PSQLUSER} WITH SUPERUSER PASSWORD '${PSQLPASS}';" &&\
    createdb -O ${PSQLUSER} ${PSQLDBNAME} &&\
    psql --command "ALTER ROLE ${PSQLUSER} SET client_encoding TO 'utf8';" &&\
    psql --command "ALTER ROLE ${PSQLUSER} SET default_transaction_isolation TO 'read committed';" &&\
    psql --command "ALTER ROLE ${PSQLUSER} SET timezone TO 'Asia/Tokyo';"
RUN sed -i -e '/^local\s\+all\s\+all\s\+peer$/ s/peer/md5/g' /etc/postgresql/$(ls -1 /etc/postgresql)/main/pg_hba.conf
RUN echo "listen_addresses = '*'" >> /etc/postgresql/$(ls -1 /etc/postgresql)/main/postgresql.conf
RUN echo "host all all all md5" >> /etc/postgresql/$(ls -1 /etc/postgresql)/main/pg_hba.conf

# ----- Finally -----

WORKDIR /var/lib/postgresql
RUN >> runserver.sh echo "/usr/lib/postgresql/$(ls -1 /etc/postgresql)/bin/postgres -D /var/lib/postgresql/$(ls -1 /etc/postgresql)/main -c config_file=/etc/postgresql/$(ls -1 /etc/postgresql)/main/postgresql.conf"

CMD ["bash", "runserver.sh"]
