@echo off

cd /d C:\Users\Admin\Workspace\py-and
call env\Scripts\activate
cd /d C:\Users\Admin\Workspace\py-and\bphis\application
celery -A tasks worker -l info --pool=solo
timeout /t 5 /nobreak
