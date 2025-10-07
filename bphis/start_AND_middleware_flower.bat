@echo off

cd /d C:\Users\NS LT 1\Workspace\py-and
call env\Scripts\activate
cd /d C:\Users\NS LT 1\Workspace\py-and\bphis\application
set FLOWER_UNAUTHENTICATED_API="true"
celery -A tasks flower
timeout /t 5 /nobreak
