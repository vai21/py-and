Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "C:\Users\NS LT 1\Workspace\py-and\bphis\start_AND_middleware_worker.bat" & Chr(34), 0
WshShell.Run chr(34) & "C:\Users\NS LT 1\Workspace\py-and\bphis\start_AND_middleware_beat.bat" & Chr(34), 0
WshShell.Run chr(34) & "C:\Users\NS LT 1\Workspace\py-and\bphis\start_AND_middleware_flower.bat" & Chr(34), 0
WshShell.Run chr(34) & "C:\Users\NS LT 1\Workspace\py-and\bphis\start_AND_middleware_app.bat" & Chr(34), 0
WshShell.Run chr(34) & "C:\Users\NS LT 1\Workspace\py-and\bphis\start_AND_middleware_django.bat" & Chr(34), 0
Set WshShell = Nothing
