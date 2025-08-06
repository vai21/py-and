# Start flask as a background process
Set-Location .\application
$runflask = Start-Process python -ArgumentList "app.py" -NoNewWindow -PassThru

# Start celery
$env:FLOWER_UNAUTHENTICATED_API="true"
$runceleryworker = Start-Process celery -ArgumentList "-A tasks worker -l info --pool=solo" -NoNewWindow -PassThru
$runcelerybeat = Start-Process celery -ArgumentList "-A tasks beat -l INFO" -NoNewWindow -PassThru
$runceleryflower = Start-Process celery -ArgumentList "-A tasks flower" -NoNewWindow -PassThru


# Optional: Wait until both processes exit (if you want to ensure they complete)
Wait-Process -Id $runflask.Id

# Optionally print process IDs
Write-Host "flask running with PID: $($runflask.Id)"
