FROM python:3.9

RUN apt-get update && apt-get -y install cron && apt-get -y install vim
RUN mkdir /usr/app
WORKDIR /usr/app
COPY ./src .
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN mv ./cron/update_db.txt /etc/cron.d/update_db
RUN mv ./cron/notify_eatery_events.txt /etc/cron.d/notify_eatery_events
RUN chmod 0766 manage.py
RUN crontab /etc/cron.d/update_db
RUN crontab /etc/cron.d/notify_eatery_events
