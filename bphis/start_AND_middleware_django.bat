@echo off

cd /d %USERPROFILE%\AND\py-and
call env\Scripts\activate
cd /d %USERPROFILE%\AND\py-and\bphis
python manage.py runserver
