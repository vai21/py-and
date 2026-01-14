@echo off

cd /d %USERPROFILE%\AND\py-and
call env\Scripts\activate
cd /d %USERPROFILE%\AND\py-and\bphis\application
set FLOWER_UNAUTHENTICATED_API="true"
start "Celery Worker" cmd /k celery -A tasks worker -l info --pool=solo
timeout /t 10 /nobreak
start "Celery Beat" cmd /k celery -A tasks beat -l INFO
timeout /t 10 /nobreak
@REM start "Celery Flower" cmd /k celery -A tasks flower
@REM timeout /t 10 /nobreak
python app.py
