@echo off

cd /d %USERPROFILE%\AND\py-and
call env\Scripts\activate
cd /d %USERPROFILE%\AND\py-and\bphis\application
celery -A tasks worker -l info --pool=solo
timeout /t 5 /nobreak
