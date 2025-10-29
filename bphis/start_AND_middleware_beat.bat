@echo off

cd /d C:\Users\User.KM\AND\py-and
call env\Scripts\activate
cd /d C:\Users\User.KM\AND\py-and\bphis\application
celery -A tasks beat -l INFO
timeout /t 5 /nobreak
