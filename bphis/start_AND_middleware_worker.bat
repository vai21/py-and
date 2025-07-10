@echo off

cd /d D:\moch.rasid_aam\Documents\py-and
call venv\Scripts\activate
cd /d D:\moch.rasid_aam\Documents\py-and\bphis\application
celery -A tasks worker -l info --pool=solo
timeout /t 5 /nobreak