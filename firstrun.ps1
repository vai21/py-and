$installvenv = Start-Process pip -ArgumentList "install virtualenv" -NoNewWindow -PassThru
$venv = Start-Process python -ArgumentList "-m virtualenv venv" -NoNewWindow -PassThru
.\venv\Scripts\Activate
$installreq = Start-Process pip -ArgumentList "install -r requirements.txt" -NoNewWindow -PassThru

Set-Location .\application

$makemigrations = Start-Process python -ArgumentList "manage.py makemigrations" -NoNewWindow -PassThru
$migrate = Start-Process python -ArgumentList "manage.py migrate" -NoNewWindow -PassThru
$createsuperuser = Start-Process python -ArgumentList "manage.py createsuperuser" -NoNewWindow -PassThru

# Wait until both processes exit (if you want to ensure they complete)
Wait-Process -Id $installvenv.Id, $venv.Id, $installreq.Id, $makemigrations.Id, $migrate.Id, $createsuperuser.Id
