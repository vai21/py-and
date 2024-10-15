# Start main.py as a background process
$main = Start-Process python -ArgumentList "main.py" -NoNewWindow -PassThru

# Start manage.py runserver as another background process
$server = Start-Process python -ArgumentList "manage.py runserver" -NoNewWindow -PassThru

# Optional: Wait until both processes exit (if you want to ensure they complete)
Wait-Process -Id $main.Id, $server.Id

# Optionally print process IDs
Write-Host "main.py running with PID: $($main.Id)"
Write-Host "manage.py runserver running with PID: $($server.Id)"
