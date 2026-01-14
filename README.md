Cara menggunakan aplikasi ini:

Periksa versi windows, jika Windows 10 silahkan pairing di Bluetooth Settings > Add device.
Jika Windows 11 install Bluetooth LE Explorer dari Google Drive di atas.

Pastikan Python versi 3 terinstal di laptop. Jika belum terinstal, installer tersedia di Google Drive.
Tutorial instalasi python:
a. Klik installer dan ikuti petunjuk, klik next,
b. Disable max path length di windows jika ada checkbox di centang.
c. Finish
Web: How to Install Python on Your System: A Guide – Real Python 

Pastikan MySQL terinstal di laptop. Jika belum terinstal, installer tersedia di Google Drive.
Tutorial instalasi mysql:
a. Klik installer dan ikuti petunjuk, klik next,
b. Pilih instalasi mysql server, mysql workbench yang akan di install, lalu pilin next
c. untuk user root berikan password 123456, klik next
d. jika sudah selesai klik test koneksi dan finish.

Buka PowerShell lalu pindah ke directory aplikasi ini, lalu masukan command di bawah ini untuk running aplikasi bluetooth:



cd C:\Users\nama user\Downloads\py-and
pip install virtualenv
python -m virtualenv venv
cd bphis
python main.py
Untuk menginstal admin pastikan di root directory py-and, lalu



pip install -r requirements.txt
cd bphis
python manage.py migrate
python manage.py createsuperuser
Isi data user untuk admin seperti nama, email dan password .

lalu jalankan aplikasi admin dengan  mengexecute command di bawah ini:



python manage.py runserver

Untuk autostart saat startup
Buka Folder Startup:

Tekan tombol Win+R untuk membuka dialog Run.

Ketik shell:startup dan tekan Enter.

Jendela File Explorer akan terbuka ke folder Startup Anda, biasanya di jalur seperti C:\Users\NamaUser\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup.

Salin Skrip:

Salin file .vbs Anda dan tempelkan langsung ke dalam folder Startup yang baru saja Anda buka.

Alternatif: Buat shortcut dari file .vbs Anda, lalu salin/pindahkan shortcut tersebut ke folder Startup.

Selesai: Skrip .vbs sekarang akan berjalan secara otomatis setiap kali Anda masuk ke akun Windows tersebut.