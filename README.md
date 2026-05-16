#  KELOMPOK-5_E-Commerce Order Management & Recommendation Engine 
   TOPIK 3 E-Commerce Order Management & Recommendation Engine 

   ## ANGGOTA
      1.Dandy Faisal Bimasena      (25051030062)
      2.Dewangga Dai Prabawa       (25051030058)
      3.Muhammad Fathir Al Malik   (25051030067)
      4.Muhammad Raykhan Faddillah (25051030057)

   ## MATA KULIAH
   Algoritma dan Struktur Data  
S1 Teknik Elektro  
Universitas Negeri Yogyakarta

   ## STRUKTUR DATA YANG DIGUNAKAN 
projek kali ini kita menggunakan beberapa stuktur data yaitu

- Linked list
  - Digunakan sebagai dasar pembuatan node melalui class LLNode. Setiap node menyimpan data dan pointer ke node berikutnya (next). Struktur ini menjadi fondasi untuk Queue dan Stack.

- Queue (Antrian / FIFO)
  - Diimplementasikan pada class Queue menggunakan linked list. Queue bekerja dengan prinsip First In First Out, yaitu data yang masuk lebih dulu akan diproses lebih dulu. Pada program ini queue digunakan untuk menyimpan antrian pesanan pelanggan berdasarkan tier (Premium, Regular, Economy).
- Stack (Tumpukan / LIFO)
  - Diimplementasikan pada class Stack menggunakan linked list. Stack bekerja dengan prinsip Last In First Out, yaitu data terakhir yang masuk akan keluar lebih dulu. Pada program ini stack digunakan untuk menyimpan riwayat transaksi pelanggan.

- Binary Search Tree (BST)
  - Diimplementasikan pada class BSTNode dan BSTKatalog. BST digunakan untuk menyimpan data katalog produk berdasarkan kode produk, sehingga proses pencarian produk, update stok, dan penampilan data secara terurut menjadi lebih efisien.

- Graph
  - Diimplementasikan pada class GraphRekomendasi menggunakan adjacency list (Dictionary + List). Graph digunakan untuk menyimpan hubungan antar produk berdasarkan pembelian bersamaan (co-purchase), sehingga sistem dapat memberikan rekomendasi produk terkait.

- Dictionary (Hash Table)
  - Digunakan pada beberapa bagian seperti TIER, queues, cust_stacks, dan adj. Struktur ini memungkinkan akses data berdasarkan key secara cepat, seperti tier pelanggan, data pelanggan, dan hubungan produk.

- List (Array Dinamis)
  - Digunakan untuk menyimpan kumpulan data, seperti daftar produk pada generate_produk(), hasil traversal BST, dan daftar rekomendasi produk.
   
   ## FITUR DARI PROJEK
- Manajemen Order Pelanggan
- Pemrosesan Pesanan
- Pembatalan Order Terakhir
- Pencarian Produk
- Update Stok Produk
- Rekomendasi Produk
- Riwayat Order Pelanggan
- Laporan Harian
- Bantuan Sistem
