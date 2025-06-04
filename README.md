[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

# Modkit Automod

Modkit Automod adalah sebuah proyek yang bertujuan untuk mengotomatiskan proses di website dengan dukungan modem pool GSM. Proyek ini dirancang untuk sistem MSISDN dan verifikasi OTP.

## Background

Ketika melakukan otomatisasi pembelian produk voucher dari website, dibutuhkan login dengan MSISDN dan OTP login, serta OTP pembelian saat checkout produk. Proyek ini bertujuan untuk mengotomatiskan proses tersebut dengan menggunakan modem pool GSM.

## CONCEPTUAL USER FLOW

1. **MODEMPOOL**: pengguna memasukan simcard fisik ke dalam modem pool GSM.
2. **MSISDN**: pengguna melakukan check informasi msisdn seperti balance , masa aktif , dan nomor.
3. **SAVE INFO**: pengguna menyimpan informasi msisdn ke dalam database.
4. **AUTOMATISASI**: Pengguna melakukan transaksi pembelian produk voucher dengan mengotomatiskan proses login dan checkout menggunakan MSISDN dan OTP.
5. **MONITORING**: Pengguna dapat memantau status transaksi dan informasi MSISDN melalui dashboard yang disediakan.
6. **REKAP**: Pengguna dapat melihat rekap transaksi yang telah dilakukan, termasuk informasi MSISDN dan status transaksi.

## stack

- **target OS**: windows
- **LANGUAGE**: Python >=3.12
- **PACKAGE MANAGER**: uv
- **DISTRIBUTION**: Portable Executable/Zip/Installer
- **DATABASE**: SQLite
- **GUI**: Pyside6
- **AUTOMATION**: Playwright
- **MODEMPOOL**: GSM Modem Pool

## Installation

1. Install Python 3.12 atau lebih baru.
2. double klik exe atau unzip file zip dan pilih start.bat
3. akan otomatis melakukan download yang di butuhkan :
    1. uv
    2. playwright
Jika Sudah sudah terinstall proses ini akan di lewati
4. Tunggu hingga proses selesai.
5. aplikasi siap di gunakan.

## TOS

Dengan menggunakan Modkit Automod, Anda setuju untuk mematuhi syarat dan ketentuan berikut:

1. **Penggunaan yang Sah**: Anda setuju untuk menggunakan Modkit Automod hanya untuk tujuan yang sah dan sesuai dengan hukum yang berlaku.
2. **Tanggung Jawab Pengguna**: Anda bertanggung jawab penuh atas penggunaan Modkit Automod, termasuk tetapi tidak terbatas pada penggunaan yang melanggar hak pihak ketiga atau hukum yang berlaku.
3. **Perubahan dan Pembaruan**: Modkit Automod dapat diperbarui atau diubah sewaktu-waktu tanpa pemberitahuan sebelumnya. Anda setuju untuk memeriksa pembaruan secara berkala.
4. **Batasan Tanggung Jawab**: Modkit Automod tidak bertanggung jawab atas kerusakan atau kehilangan yang timbul akibat penggunaan atau ketidakmampuan untuk menggunakan aplikasi ini.
5. **Privasi dan Keamanan**: Anda setuju untuk menjaga kerahasiaan informasi akun Anda dan tidak membagikannya kepada pihak ketiga. Modkit Automod tidak bertanggung jawab atas kebocoran informasi yang disebabkan oleh kelalaian pengguna.
6. **Segala kerugian , kerusakan, atau konsekuensi negatif yang timbul akibat penggunaan Modkit Automod adalah tanggung jawab pengguna sepenuhnya.**
