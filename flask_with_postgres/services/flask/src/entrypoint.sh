#!/bin/sh

echo "Waiting for postgres..."

### Here postgres is service name ###
while ! nc -z postgres 5432; do
  sleep 0.1
done

echo "PostgreSQL started DOne"

gunicorn -b 0.0.0.0:5000 app:app