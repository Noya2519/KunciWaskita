# KunciWaskita
# Persyaratan dan Instalasi Aplikasi Enkripsi GUI

## 1. Persyaratan Sistem
Aplikasi ini membutuhkan beberapa dependensi Python serta alat tambahan agar dapat berjalan dengan baik.

### a. Versi Python
- **Python 3.8 - 3.12** (Disarankan menggunakan versi stabil terbaru)

### b. Modul Python yang Dibutuhkan
Berikut adalah daftar modul yang digunakan dalam aplikasi ini:
- **`customtkinter`** → Untuk GUI modern berbasis Tkinter
- **`pycryptodome`** → Untuk enkripsi AES
- **`hashlib`** → Untuk hashing kunci enkripsi
- **`base64`** → Untuk encoding teks hasil XOR
- **`tkinter`** → Untuk dialog pemilihan file
- **`pyinstaller`** → Untuk membuat executable (.exe)

## 2. Cara Menginstal Dependensi
Jalankan perintah berikut di terminal atau command prompt:
```sh
pip install customtkinter pycryptodome pyinstaller
```
Jika ada error saat import **`customtkinter`**, coba perbarui dengan:
```sh
pip install --upgrade customtkinter
```

## 3. Konversi ke File .exe dengan PyInstaller
Setelah semua dependensi diinstal, jalankan perintah berikut untuk membuat file **KUNCI WASKITA.exe**:
```sh
pyinstaller --noconsole --onefile --icon=icon.ico "KUNCI WASKITA.py"
```
Penjelasan opsi yang digunakan:
- **`--noconsole`** → Menjalankan tanpa jendela CMD (untuk aplikasi GUI)
- **`--onefile`** → Membuat satu file `.exe` tanpa folder tambahan
- **`--icon=icon.ico`** → Menggunakan ikon khusus (opsional)

Jika tidak memiliki file `icon.ico`, cukup jalankan:
```sh
pyinstaller --noconsole --onefile "KUNCI WASKITA.py"
```

## 4. File yang Harus Disertakan
Setelah proses konversi berhasil, file executable dapat ditemukan di dalam folder `dist/`. Pastikan untuk menyertakan **icon.ico** jika diperlukan.

Cek executable yang berhasil dibuat dengan menjalankan:
```sh
dist/KUNCI WASKITA.exe
```

## 5. Troubleshooting
Jika aplikasi tidak berjalan setelah dikonversi ke `.exe`, coba langkah berikut:
- Pastikan semua dependensi telah terinstal dengan benar.
- Jalankan ulang perintah **PyInstaller**.
- Jika ada error spesifik, coba jalankan aplikasi dalam mode debug dengan:
  ```sh
  pyinstaller --onefile --windowed "KUNCI WASKITA.py"
  ```

Dengan mengikuti langkah-langkah ini, aplikasi enkripsi GUI akan dapat berjalan dengan baik dan dapat digunakan di berbagai komputer tanpa perlu menginstal Python secara terpisah.
kalau tidak bisa install dari github klik https://drive.google.com/file/d/1UubwbpbHMa4Kth_IYwM7F7YJzUKaTV0V/view?usp=sharing
