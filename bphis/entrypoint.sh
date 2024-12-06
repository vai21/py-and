#!/bin/sh

# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# exits if any of your variables is not set
set -o nounset

echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# python manage.py flush --no-input
# python manage.py migrate

exec "$@"
