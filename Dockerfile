FROM python:3.9

RUN apt-get update && apt-get -y install cron && apt-get -y install vim
RUN mkdir /usr/app
WORKDIR /usr/app
COPY ./src .
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY update_db.txt /etc/cron.d/update_db
RUN chmod 0644 /etc/cron.d/update_db
RUN chmod 0744 manage.py
RUN crontab /etc/cron.d/update_db
