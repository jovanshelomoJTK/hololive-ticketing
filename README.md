# Tugas Besar Sistem Terdistribusi - Aplikasi Pembelian Tiket Konser VTuber Berbasis Sistem Terdistribusi

## Pendahuluan
Aplikasi ini bertujuan untuk mengatasi tantangan dalam mengelola penjualan tiket konser VTuber dengan jumlah penggemar yang besar dan permintaan yang tinggi.

## Teknologi yang Digunakan

Berikut adalah daftar teknologi yang digunakan dalam pengembangan aplikasi:

| No. | Nama Teknologi   | Deskripsi                                                                                                                                                                                                                                              |
| --- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | Python           | Python merupakan bahasa pemrograman komputer yang biasa dipakai untuk membangun situs, software/aplikasi, mengotomatiskan tugas, dan melakukan analisis data. Python memiliki fitur threading yang memungkinkan pemrosesan secara paralel untuk menangani banyak tugas secara sekaligus. |
| 2   | Visual Studio Code | Visual Studio Code merupakan aplikasi code editor yang dikembangkan oleh Microsoft. Dalam konteks pengembangan aplikasi pembelian tiket konser VTuber berbasis sistem terdistribusi, Visual Studio Code digunakan untuk menulis, mengedit, dan mengelola kode sumber aplikasi. |
| 3   | Tailwind CSS     | Tailwind CSS merupakan framework CSS yang berbasis utility untuk membuat UI atau tampilan dari aplikasi web. Berbasis utility artinya Tailwind hanya terdiri dari 100% utility class dan tidak ada class komponen seperti Navbar, Button, Card, Modal, dll.   |
| 4   | React            | React adalah library JavaScript populer buatan Facebook yang digunakan dalam pengembangan aplikasi mobile dan web. React berisi kumpulan snippet kode JavaScript (komponen) yang bisa digunakan berulang kali untuk mendesain antarmuka pengguna.               |
| 5   | TypeScript       | TypeScript adalah bahasa pemrograman berbasis JavaScript yang menambahkan fitur strong-typing & konsep pemrograman OOP klasik (class, interface). TypeScript disebut sebagai superset dari JavaScript, menawarkan class, module, dan interface untuk mengembangkan aplikasi kompleks dengan lebih mudah. |
| 6   | Vite             | Vite adalah framework JavaScript open-source yang digunakan untuk membangun aplikasi frontend yang cepat dan efisien. Vite berfokus pada performa yang cepat dan pengembangan yang mudah, serta mendukung hot-reloading untuk melihat perubahan pada kode secara langsung.   |
| 7   | Node.js          | Node.js adalah runtime environment untuk JavaScript yang bersifat open-source dan cross-platform. Node.js menjalankan V8 JavaScript engine di luar browser, memungkinkan penggunaan JavaScript di berbagai lingkungan, termasuk pengembangan aplikasi web.         |

## Pembagian Tugas dan Tanggung Jawab Anggota Kelompok

Berikut adalah pembagian tugas dan tanggung jawab masing-masing anggota tim dalam pengembangan aplikasi:

| No. | Nama Anggota          | Tugas dan Tanggung Jawab                                                                                                                                     |
| --- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Jovan Shelomo         | - Pemilik Repository <br> - Dokumentasi Laporan <br> - Programmer                                                                                           |
| 2   | Muhammad Rafi Farhan  | - Dokumentasi Laporan <br> - Programmer                                                                                                                       |
| 3   | Rachmat Purwa Saputra | - Ketua <br> - Dokumentasi Laporan <br> - Programmer                                                                                                          |
| 4   | Reihan Hadi Fauzan    | - Dokumentasi Laporan <br> - Programmer                                                                                                                       |

## Analisis Alasan Pemilihan Tema dan Solusi

Aplikasi ini dipilih sebagai solusi untuk mengatasi tantangan dalam mengelola penjualan tiket konser VTuber karena kebutuhan akan sistem yang dapat mengelola lalu lintas pengguna yang tinggi, ketersediaan tiket secara real-time, dan mencegah kesalahan dalam pembelian tiket. Solusi ini juga memungkinkan penggemar untuk mengakses acara-acara tersebut dengan lebih mudah.

## Arsitektur Sistem dan Jaringan

### 1.Arsitektur Sistem:

Kami merancang aplikasi ini dengan sistem terdistribusi yang mengadopsi arsitektur berbasis client-server.

**Client Side:**
- **Komponen:** Web Browser / HTTP Client.
- **Proses:**
  - **Permintaan HTTP:** Klien mengirimkan permintaan HTTP ke server, bisa berupa GET untuk mendapatkan data (seperti daftar stage atau tiket) atau POST untuk membeli tiket.
  - **Pengolahan Respons:** Klien menerima respons HTTP dari server dalam format JSON untuk diolah atau ditampilkan.

**Server Side:**
- **Komponen:** ThreadingHTTPServer, Handler, Handlers Functions.
- **Proses:**
  - **Penerimaan Permintaan:** Server menerima permintaan dari klien dan menggunakan Handler untuk menentukan tindakan yang tepat.
  - **Pengolahan Data:** Berdasarkan jenis permintaan, server membaca atau menulis ke database menggunakan semaphore untuk menjaga integritas data.
  - **Pengiriman Respons:** Setelah permintaan diproses, server mengirimkan respons dalam format JSON kembali ke klien.

### 2. Arsitektur Jaringan:

**Client Network:**
- **Komponen:** Jaringan yang digunakan oleh klien untuk mengirim permintaan HTTP ke server, bisa LAN atau internet.
- **Komunikasi:** Klien mengirimkan permintaan melalui protokol HTTP ke alamat IP dan port server.

**Server Network:**
- **Komponen:** Jaringan tempat server berada, bisa lokal atau terhubung ke internet.
- **Komunikasi:** Server mendengarkan permintaan pada alamat IP tertentu dan port tertentu.

### 3. Alur Proses Aplikasi

**Permintaan Untuk Mendaftar Stage (GET /stages):**
- Klien mengirimkan permintaan GET untuk mendapatkan daftar stage.
- Server memproses permintaan dan mengirim respons berisi daftar stage kembali ke klien.

**Permintaan Untuk Mendapatkan Tiket (GET /my-tickets):**
- Klien mengirimkan permintaan GET untuk mendapatkan daftar tiket milik pengguna tertentu.
- Server memproses permintaan dan mengirim respons berisi daftar tiket kembali ke klien.

**Klien Mengirim Permintaan Untuk Membeli Tiket (POST /buy-tickets):**
- Klien mengirimkan permintaan POST untuk membeli tiket dengan data JSON.
- Server memproses permintaan dan mengirim respons berisi informasi tiket yang berhasil dibeli kembali ke klien.

### 4. Penanganan Kesalahan

**Permintaan dengan Parameter Tidak Lengkap atau Tidak Valid:**
- Jika permintaan tidak menyertakan parameter yang diperlukan atau parameter tidak valid, server mengirimkan respons kesalahan yang sesuai ke klien.

**Kesalahan Akses Berkas:**
- Jika terjadi kesalahan saat membaca atau menulis berkas, server mengirimkan respons kesalahan internal server ke klien.

## Prerequisite

- Node.js 20
- Python 3.12

## How to run

1. Clone repository ini ke dalam perangkat lokal Anda dengan menjalankan perintah berikut pada terminal atau command prompt:
    ```bash
    git clone https://github.com/jovanshelomoJTK/hololive-ticketing.git
    ```

2. Setelah proses cloning selesai, buka folder proyek ini pada Visual Studio Code.
   
3. Jalankan perintah berikut pada terminal atau command prompt untuk menginstall dependencies yang diperlukan:
    ```bash
    npm install
    ```
    
4. Tunggu hingga proses instalasi dependencies selesai dan sukses. Setelah itu, proyek siap untuk dijalankan dengan perintah berikut:
    ```bash
    npm run dev
    ```
