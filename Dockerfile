FROM python:3.9-slim-buster 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y install libpq-dev gcc

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt

COPY ./backless /app
EXPOSE 8000
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "backless.asgi:application"]
