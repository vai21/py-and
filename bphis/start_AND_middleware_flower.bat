@echo off

cd /d D:\moch.rasid_aam\Documents\py-and
call venv\Scripts\activate
cd /d D:\moch.rasid_aam\Documents\py-and\bphis\application
set FLOWER_UNAUTHENTICATED_API="true"
celery -A tasks flower
timeout /t 5 /nobreak
