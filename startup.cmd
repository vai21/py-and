PowerShell -Command "Set-ExecutionPolicy Unrestricted" >> "%TEMP%\StartupLog.txt" 2>&1
PowerShell %USERPROFILE%\Documents\py-and\venv\Scripts\Activate.ps1 >> "%TEMP%\StartupLog.txt" 2>&1
PowerShell %USERPROFILE%\Documents\py-and\bphis\runapp.ps1 >> "%TEMP%\StartupLog.txt" 2>&1
