FROM ubuntu

# ----- Prepare -----

## 設定しないとapt install中に止まる
ENV DEBIAN_FRONTEND=noninteractive

# ----- Install -----

RUN apt update

## Python3 aptでインストール
RUN apt install -y python3-pip

## django
RUN pip3 install django
RUN pip3 install uwsgi

## nginx
RUN apt install -y nginx

## PostgreSQL
RUN pip3 install psycopg2-binary

## requirements Install
COPY requirements.txt /root/requirements.txt
RUN pip3 install -r /root/requirements.txt

# ----- Setting -----

## HOME設定
WORKDIR /root

## nginxがdjangoプロジェクトを参照する設定
ARG app_conf=/etc/nginx/conf.d/sns.conf
RUN >>"${app_conf}" echo "server {"
RUN >>"${app_conf}" echo "    listen  80;"
RUN >>"${app_conf}" echo "    server_name     127.0.0.1;"
RUN >>"${app_conf}" echo
RUN >>"${app_conf}" echo "    location /static {"
RUN >>"${app_conf}" echo "        alias /root/src/static;"
RUN >>"${app_conf}" echo "    }"
RUN >>"${app_conf}" echo ""
RUN >>"${app_conf}" echo "    location / {"
RUN >>"${app_conf}" echo "        proxy_pass http://127.0.0.1:8001;"
RUN >>"${app_conf}" echo "    }"
RUN >>"${app_conf}" echo "}"
RUN rm /etc/nginx/sites-enabled/default

## nginxのシステムユーザー設定
RUN sed -i -e "s/^user .*/user root;/g" /etc/nginx/nginx.conf

## 起動に2つのコマンドが必要なため、シェルスクリプトを作成
ARG start_shell=/root/runserver.sh
RUN >>"${start_shell}" echo "cd /root/src"
RUN >>"${start_shell}" echo "python3 manage.py makemigrations"
RUN >>"${start_shell}" echo "python3 manage.py migrate"
RUN >>"${start_shell}" echo "uwsgi --http :8001 --ini uwsgi.ini &"
RUN >>"${start_shell}" echo '/usr/sbin/nginx -g "daemon off;"'
RUN >>"${start_shell}" echo "cd -"

# 本番で不要
RUN apt update ; apt install -y vim curl
RUN echo "set -o vi" >> $HOME/.bashrc
RUN echo "alias ll='ls -la'" >> $HOME/.bashrc

# ----- Finally -----

CMD ["bash", "/root/runserver.sh"]
