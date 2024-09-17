FROM python:3.11-slim-buster

ENV CELERY_BROKER_URL amqp://guest:guest@rabbitmq:5672//
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true

WORKDIR /queue
COPY . ./queue

RUN pip install -r queue/requirements.txt




