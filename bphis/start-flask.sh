#!/bin/bash

set -o errexit
set -o nounset

python manage.py migrate
python app.py -h 0.0.0.0 -p 5000
