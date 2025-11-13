Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & WshShell.ExpandEnvironmentStrings("%USERPROFILE%\AND\py-and\bphis\start_AND_middleware.bat") & Chr(34), 0
Set WshShell = Nothing
