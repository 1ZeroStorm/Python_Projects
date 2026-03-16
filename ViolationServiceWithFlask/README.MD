# Replikasi Sistem Pelanggaran Sekolah (kategori data siswa)

# Isi HTML murid (flask)
1) Nama Murid (panjang)
2) Nomor Absen, Kelas
3) Jenis pelanggaran
4) Alasan pelanggaran

# Modul
- module 1: new database
- module 2: CRUD
- folder template

# Cara run
- buka XAMMP untuk mysql databse
- install library pada requirements.txt
- buka app.py -> run

# Checklist fitur
- sturktur aplikasi dengan flask (app.py) ✅
- routing request-response (views.py) ✅
- template html ✅
- integrasi html dengan database ✅
- CRUD ✅
- futur export dan import ✅
- terorganisir secara modular ✅
- SRP ✅

# Jawaban pertanyaan (tanpa AI)
1) Pada dasarnya dari User interface HTML, user dapat memasukkan/mengedit data melalui "Tambah Data" dan dimasukkan pada database. Konsep komunikasi dengan mysql diterapkan sama pada fitur lainnya seperti Update, Read, dan Delete. Konsep ini adalah bentuk komunikasi antara modul violation_repository dan modul views.py. Sedangkan modul violation_service merupakan tempat supaya data diciptakan (dinamai repo (singkatan repository)) dan ditampung. Apabila user ingin mengedit data melalui flask, fungsi yang dijalankan terlebih dahulu terdapat pada modul violation_service sehingga dapat berkomunikasi dengan modu violation_repository

2) Ketika user menekan export, kode views.py (bagian front end flask) mendapatkan memori data dari modul service, yang apda saat itu mengaktifkan fungsi export_to_csv,fungsi ini akan memproses dengan mendefinisikan in-memory text buffer dan dicantumkan pada csv writer sehingga dapat diisi data. Pada akhirnya ungsi memberikan string yang berisi data berupa csv. Pada saat csv di tangkap Kembali ke fungsi export pada views.py, akan dikonversi menjadi Byte. File tersebut secara automatis terdownload pada user

3) Ketika user menekan import, ia akan dibawa ke halaman import. Terdapat opsi import. Terdapat juga system pengecekan apakah user memasukkan file setelah berada pada pemilihan file import atau tidak. User harus memasukkan data berupa format csv, jika tidak maka ditolak. File tersebut kemudian dibaca yang disimpan dalam variabel csv_content dan memberitahu jumlah data yang berhasil diimpor dan yang tidak. Di sisi violation_service, data tersebut akan dibaca, kemudian kode akan membuat baris data baru dan memasukkan data sesuai dengan csv.

4) Penerapan SRP pada repository ini ialah pemisiahan class dan fungsi sesuai tugasnya masing masing. Sebagai contoh, violation_service akan mengendalikan modul lain untuk membuat objek dalam bentuk attribut dan mengatur ekpor impor yang mana membutuhkan semua baris dari seluruh data. violation_repository merupakan modul indipenden yang menyentuh secara langsung data dari MySQL termasuk CRUD. Sedangkan modul views akan menampilkan bagian User interface beserta trigger dan responsenya sehingga dapat dialurkan ke modul lain.

5) modul violation_service memiliki class ViolationService sebagaimana ia memiliki metode seperti __init__ yang membuatnya memiliki attribut repo yang berisi objek pada modul lain dan fitur create, update, delete yang secara tidak langsung memanipulasi attribut repo menurut fitur CRUD itu sendiri. Bagian violation_repository memiliki ViolationRepository yang menyentuh secara langsung dengan data MySQL sehingga mereka memiliki metode sendiri yakni CRUD dan mengorganisir Kembali ID.

6) Struktur ini penting pada penerapannya seperti
- menyetor pelanggaran murid dalam database yang terpercaya, dengan UI yang memudahkan orang awam untuk memasukkan data
- menyetor data untuk image recognition, dimana apabila terdapat data dengan skala besar, ilmuan dapat menyetor data dengan mudah dengan bantuan UI web flask. Dengan library python yang luas, ilmuan dapat mengakses koneksi MQTT dan Wifi sehingga dikoneksikan ke mikrokontroller seperti esp 32 dan menyetor data
- dengan koneksi python dengan flask dan MySQL, developer dapat mengakses library python dengan bebas seperti pygame untuk membuat game. tkinter untuk membuat UI secara lokal 




## © [2026] [YOHANES ARYA PRASETYAYUDA XIIF/15]. All rights reserved.
