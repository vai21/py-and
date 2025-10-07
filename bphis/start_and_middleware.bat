@echo off

cd /d C:\Users\Admin\Workspace\py-and
call env\Scripts\activate
cd /d C:\Users\Admin\Workspace\py-and\bphis\application
set FLOWER_UNAUTHENTICATED_API="true"
start "Celery Worker" cmd /k celery -A tasks worker -l info --pool=solo
timeout /t 5 /nobreak
start "Celery Beat" cmd /k celery -A tasks beat -l INFO
timeout /t 5 /nobreak
start "Celery Flower" cmd /k celery -A tasks flower
timeout /t 5 /nobreak
python app.py
