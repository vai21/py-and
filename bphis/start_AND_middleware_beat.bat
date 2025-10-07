@echo off

cd /d C:\Users\Admin\Workspace\py-and
call env\Scripts\activate
cd /d C:\Users\Admin\Workspace\py-and\bphis\application
celery -A tasks beat -l INFO
timeout /t 5 /nobreak
