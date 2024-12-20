import pandas as pd
from metadata.data_toko import baju_anak, accounts, vouchers
from functions.function import auth_user

# Simpan Pesanan di Keranjang
keranjang = []

# Fitur Registrasi Pembeli
def register_pembeli(df_accounts):
    print("\n=== Registrasi Pembeli ===")
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")

    if username in df_accounts['username'].values:
        print("Username sudah terdaftar. Gunakan username lain.")
    else:
        new_account = {"username": username, "password": password, "role": "pembeli"}
        df_accounts = df_accounts._append(new_account, ignore_index=True)
        print("Registrasi berhasil! Silakan login untuk melanjutkan.")
    return df_accounts

# Fitur Tambah Stok Baju (Admin)
def tambah_stok(df_baju_anak):
    print("\n=== Tambah Stok Baju ===")
    nama_baju = input("Masukkan nama baju: ")
    try:
        harga_baju = int(input("Masukkan harga baju: "))
        df_baju_anak = df_baju_anak._append({"Nama": nama_baju, "Harga": harga_baju}, ignore_index=True)
        print(f"Berhasil menambahkan baju: {nama_baju} dengan harga Rp{harga_baju}.")
    except ValueError:
        print("Harga baju harus berupa angka!")
    return df_baju_anak

# Fitur Lihat Data Baju
def lihat_data_baju(df_baju_anak):
    print("\n=== Data Baju Anak ===")
    print(df_baju_anak.to_string(index=False))

# Fitur Tambah ke Keranjang dengan Pilihan Ukuran
def tambah_ke_keranjang(df_baju_anak, keranjang):
    print("\n=== Tambah ke Keranjang ===")
    print(df_baju_anak.to_string(index=False))

    try:
        index_baju = int(input("Pilih nomor baju (0 untuk batal): "))
        if index_baju == 0:
            print("Batal menambahkan baju ke keranjang.")
            return keranjang

        if 0 < index_baju <= len(df_baju_anak):
            baju = df_baju_anak.iloc[index_baju - 1]

            # Menentukan ukuran baju
            ukuran = input("Pilih ukuran (S/M/L/XL): ").upper()
            if ukuran not in ['S', 'M', 'L', 'XL']:
                print("Ukuran tidak valid! Pilihan hanya S, M, L, atau XL.")
                return keranjang

            item = baju.to_dict()
            item['Ukuran'] = ukuran  # Menambahkan ukuran ke item keranjang
            keranjang.append(item)

            print(f"Berhasil menambahkan {baju['Nama']} ukuran {ukuran} ke keranjang.")
        else:
            print("Nomor baju tidak valid!")
    except ValueError:
        print("Input harus berupa angka!")

    return keranjang


# Fitur Lihat Keranjang
def lihat_keranjang(keranjang):
    print("\n=== Keranjang Belanja ===")
    if not keranjang:
        print("Keranjang Anda kosong.")
    else:
        total = sum(item['Harga'] for item in keranjang)
        for i, item in enumerate(keranjang, 1):
            print(f"{i}. {item['Nama']} - Rp{item['Harga']}")
        print(f"Total: Rp{total}")

# Fitur Pembayaran
def bayar_keranjang(keranjang, df_vouchers):
    if not keranjang:
        print("\nKeranjang Anda kosong. Pergi Ke Katalog Untuk Memilih Barang Yang Kamu Suka.")
        return keranjang

    lihat_keranjang(keranjang)
    total = sum(item['Harga'] for item in keranjang)
    kode_voucher = input("\nMasukkan kode voucher (lewati jika tidak ada): ")

    if kode_voucher:
        voucher = df_vouchers[df_vouchers['kode'] == kode_voucher]
        if not voucher.empty:
            diskon = voucher.iloc[0]['diskon']
            total *= (1 - diskon)
            print(voucher.iloc[0]['Annouce'])
        else:
            print("Kode voucher tidak valid!")

    print(f"\nTotal yang harus dibayar: Rp{total:.0f}")

    alamat_pengiriman = input("Masukkan alamat pengiriman: ")
    nomor_hp = input("Masukkan nomor HP: ")

    print("\nMetode Pembayaran:")
    print("1. Cash on Delivery (COD)")
    print("2. Transfer Bank (Virtual Account)")

    try:
        metode_pembayaran = int(input("Pilih metode pembayaran (1/2): "))

        if metode_pembayaran == 1:
            confirm = input("Konfirmasi pembayaran dengan COD? (y/n): ").lower()
            if confirm == 'y':
                print("\nPesanan Anda akan dikirimkan ke:")
                print(f"Alamat: {alamat_pengiriman}")
                print(f"Nomor HP: {nomor_hp}")
                print("Pesanan akan dibayar saat barang diterima. Terima kasih!")
                keranjang.clear()
            else:
                print("Pembayaran dibatalkan.")

        elif metode_pembayaran == 2:
            virtual_account = "3901234567890"  # Contoh nomor VA
            print("\nInstruksi Transfer:")
            print(f"1. Lakukan transfer ke nomor Virtual Account berikut: {virtual_account}")
            print("2. Total transfer: Rp{:.0f}".format(total))
            print(f"3. Pesanan Anda akan dikirimkan ke: {alamat_pengiriman}, No HP: {nomor_hp}")
            confirm = input("Konfirmasi pembayaran setelah transfer? (iya/tidak): ").lower()
            if confirm == 'iya':
                print("\nPembayaran berhasil. Terima kasih telah berbelanja!")
                keranjang.clear()
            else:
                print("Pembayaran dibatalkan.")

        else:
            print("Metode pembayaran tidak valid!")

    except ValueError:
        print("Input harus berupa angka!")

    return keranjang

# Main Program
def main():
    df_baju_anak = pd.DataFrame(baju_anak)
    df_vouchers = pd.DataFrame(vouchers)
    df_accounts = pd.DataFrame(accounts)
    keranjang = []  # Keranjang harus didefinisikan di sini

    print("\t\t SELAMAT DATANG DI TOKO BAJU ANDALAN")
    print("=" * 70)

    while True:
        print("\nMenu:")
        print("1. Register Pembeli")
        print("2. Login")
        print("3. Keluar")

        try:
            pilihan = int(input("Pilih menu: "))
            if pilihan == 1:
                df_accounts = register_pembeli(df_accounts)
            elif pilihan == 2:
                login_result = auth_user(df_accounts)  # Ganti sesuai fungsi login Anda
                if login_result is None:
                    print("Login gagal! Username atau password salah.")
                    continue  # Kembali ke menu utama jika login gagal

                username, role = login_result  # Harus mengembalikan (username, role)
                print(f"\nLogin berhasil! Selamat datang, {username} ({role}).")

                # Submenu berdasarkan role
                while True:
                    if role == "admin":
                        print("\nMenu Admin:")
                        print("1. Lihat Data Baju")
                        print("2. Tambah Stok Baju")
                        print("3. Keluar")
                    elif role == "pembeli":
                        print("\nMenu Pembeli:")
                        print("1. Lihat Data Baju")
                        print("2. Tambah ke Keranjang")
                        print("3. Lihat Keranjang")
                        print("4. Bayar Keranjang")
                        print("5. Keluar")

                    try:
                        sub_pilihan = int(input("Pilih menu: ").strip())
                        if role == "admin":
                            if sub_pilihan == 1:
                                lihat_data_baju(df_baju_anak)
                            elif sub_pilihan == 2:
                                df_baju_anak = tambah_stok(df_baju_anak)
                            elif sub_pilihan == 3:
                                print("Kembali ke menu utama.")
                                break
                            else:
                                print("Pilihan tidak valid. Coba lagi.")
                        elif role == "pembeli":
                            if sub_pilihan == 1:
                                lihat_data_baju(df_baju_anak)
                            elif sub_pilihan == 2:
                                keranjang = tambah_ke_keranjang(df_baju_anak, keranjang)
                            elif sub_pilihan == 3:
                                lihat_keranjang(keranjang)
                            elif sub_pilihan == 4:
                                keranjang = bayar_keranjang(keranjang, df_vouchers)
                            elif sub_pilihan == 5:
                                print("Kembali ke menu utama.")
                                break
                            else:
                                print("Pilihan tidak valid. Coba lagi.")
                    except ValueError:
                        print("Input harus berupa angka!")
            elif pilihan == 3:
                print("Terima kasih telah menggunakan sistem kami. Sampai jumpa!")
                break
            else:
                print("Pilihan tidak valid. Coba lagi.")
        except ValueError:
            print("Input harus berupa angka!")


if __name__ == "__main__":
    main()
