#!/bin/bash

# run django
python manage.py runserver

# run flask
cd application
python app.py

# run celery, flower
export FLOWER_UNAUTHENTICATED_API="true"
celery -A tasks worker -l INFO --pool=solo
celery -A tasks beat -l INFO
celery -A tasks flower
