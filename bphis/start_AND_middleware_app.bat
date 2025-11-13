@echo off

cd /d %USERPROFILE%\AND\py-and
call env\Scripts\activate
cd /d %USERPROFILE%\AND\py-and\bphis\application
python app.py
