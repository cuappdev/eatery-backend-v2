FROM python:3.9

RUN mkdir /usr/app
WORKDIR /usr/app
COPY ./src .
COPY ./requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8000
