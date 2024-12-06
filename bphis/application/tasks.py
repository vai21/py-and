from config import create_app
from helpers import trigger_run_bluetooth, run_serial
from celery import shared_task

flask_app = create_app()
celery_app = flask_app.extensions ["celery"]

@shared_task()
def connect_to_bluetooth():
    message = trigger_run_bluetooth()
    return message

@shared_task()
def connect_to_cable():
    message = run_serial()
    return message
