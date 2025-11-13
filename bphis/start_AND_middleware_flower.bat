@echo off

cd /d %USERPROFILE%\AND\py-and
call env\Scripts\activate
cd /d %USERPROFILE%\AND\py-and\bphis\application
set FLOWER_UNAUTHENTICATED_API="true"
celery -A tasks flower
timeout /t 5 /nobreak
