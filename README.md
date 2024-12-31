
# Retail Management System

## Deskripsi Aplikasi
Aplikasi desktop sederhana untuk mengelola produk dan mencatat transaksi penjualan.

## Cara Menjalankan
1. Pastikan MySQL berjalan, dan buat database menggunakan `dump.sql`.
2. Jalankan aplikasi menggunakan file `main.py` dengan Python 3.
3. Pastikan library `mysql-connector-python` terinstal:
   ```
   pip install mysql-connector-python
   ```

## Struktur Database
### Tabel Products:
- `id`: Primary Key
- `name`: Nama Produk
- `price`: Harga Produk

### Tabel Transactions:
- `id`: Primary Key
- `product_id`: Foreign Key ke tabel Products
- `quantity`: Jumlah Produk
- `total_price`: Total Harga
- `transaction_date`: Tanggal Transaksi
