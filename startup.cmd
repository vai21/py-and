PowerShell -Command "Set-ExecutionPolicy Unrestricted" >> "%TEMP%\StartupLog.txt" 2>&1
PowerShell %USERPROFILE%\AND\py-and\env\Scripts\Activate.ps1 >> "%TEMP%\StartupLog.txt" 2>&1
PowerShell %USERPROFILE%\AND\py-and\bphis\runapp.ps1 >> "%TEMP%\StartupLog.txt" 2>&1
