# Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed or not added to the PATH." -ForegroundColor Red
    exit 1
}

# Check if manage.py exists in the current directory
if (-not (Test-Path "./manage.py")) {
    Write-Host "manage.py not found in the current directory. Ensure you're in the correct project folder." -ForegroundColor Yellow
    exit 1
}

# Run Bluetooth LE Receiver
Write-Host "Starting Django development server..." -ForegroundColor Green
try {
    python main.py
} catch {
    Write-Host "Failed to start the server. Check your Python/Django setup." -ForegroundColor Red
}

# Run Django server
Write-Host "Starting Django development server..." -ForegroundColor Green
try {
    python manage.py runserver
} catch {
    Write-Host "Failed to start the server. Check your Python/Django setup." -ForegroundColor Red
}
