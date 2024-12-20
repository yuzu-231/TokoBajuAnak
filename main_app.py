import streamlit as st
import pandas as pd
from metadata.data_toko import baju_anak, accounts, vouchers
from functions.function_app import auth_user

# Inisialisasi Data
if 'df_baju_anak' not in st.session_state:
    st.session_state.df_baju_anak = pd.DataFrame(baju_anak)
if 'df_accounts' not in st.session_state:
    st.session_state.df_accounts = pd.DataFrame(accounts)
if 'df_vouchers' not in st.session_state:
    st.session_state.df_vouchers = pd.DataFrame(vouchers)
if 'keranjang' not in st.session_state:
    st.session_state.keranjang = []
if 'user' not in st.session_state:
    st.session_state.user = None

# Fungsi Registrasi Pembeli
def register_pembeli():
    st.subheader("Registrasi Pembeli")
    username = st.text_input("Masukkan username")
    password = st.text_input("Masukkan password", type="password")
    
    if st.button("Daftar"):
        if username in st.session_state.df_accounts['username'].values:
            st.error("Username sudah terdaftar. Gunakan username lain.")
        else:
            new_account = {"username": username, "password": password, "role": "pembeli"}
            st.session_state.df_accounts = st.session_state.df_accounts._append(new_account, ignore_index=True)
            st.success("Registrasi berhasil! Silakan login.")

# Fungsi Lihat Data Baju
def lihat_data_baju():
    st.subheader("Data Baju Anak")
    st.table(st.session_state.df_baju_anak)

# Fungsi Tambah Stok Baju (Admin)
def tambah_stok():
    st.subheader("Tambah Stok Baju")
    nama_baju = st.text_input("Masukkan nama baju")
    harga_baju = st.number_input("Masukkan harga baju", min_value=0, step=1000)
    ukuran_baju = st.multiselect("Pilih ukuran baju yang tersedia", ['S', 'M', 'L', 'XL'])

    if st.button("Tambah Stok"):
        if not ukuran_baju:
            st.error("Harap pilih setidaknya satu ukuran.")
        else:
            new_item = {"Nama": nama_baju, "Ukuran": ukuran_baju, "Harga": harga_baju}
            st.session_state.df_baju_anak = st.session_state.df_baju_anak._append(new_item, ignore_index=True)
            st.success(f"Berhasil menambahkan {nama_baju} dengan ukuran {ukuran_baju} dan harga Rp{harga_baju}.")


# Fungsi Tambah ke Keranjang (Pembeli)
def tambah_ke_keranjang():
    st.subheader("Tambah ke Keranjang")
    lihat_data_baju()
    index_baju = st.number_input("Pilih nomor baju (mulai dari 1)", min_value=1, max_value=len(st.session_state.df_baju_anak), step=1) - 1
    ukuran = st.selectbox("Pilih ukuran", ['S', 'M', 'L', 'XL'])

    if st.button("Tambah ke Keranjang"):
        baju = st.session_state.df_baju_anak.iloc[index_baju].to_dict()
        baju['Ukuran'] = ukuran
        st.session_state.keranjang.append(baju)
        st.success(f"Berhasil menambahkan {baju['Nama']} ukuran {ukuran} ke keranjang.")

# Fungsi Lihat Keranjang
def lihat_keranjang():
    st.subheader("Keranjang Belanja")
    if not st.session_state.keranjang:
        st.info("Keranjang Anda kosong.")
    else:
        total = sum(item['Harga'] for item in st.session_state.keranjang)
        for i, item in enumerate(st.session_state.keranjang, 1):
            st.write(f"{i}. {item['Nama']} - Ukuran {item['Ukuran']} - Rp{item['Harga']}")
        st.write(f"**Total: Rp{total}**")

# Fungsi Bayar Keranjang
def bayar_keranjang():
    lihat_keranjang()  # Menampilkan isi keranjang terlebih dahulu
    
    voucher_input = st.text_input("Masukkan kode voucher (Opsional)").strip().upper()
    total_awal = sum(item['Harga'] for item in st.session_state.keranjang)
    total_akhir = total_awal
    pesan_diskon = ""

    # Validasi voucher jika ada
    if voucher_input:
        valid_voucher = next((voucher for voucher in st.session_state.df_vouchers.to_dict(orient='records') if voucher['kode'] == voucher_input), None)
        if valid_voucher:
            diskon = valid_voucher['diskon']
            total_akhir = total_awal * (1 - diskon)
            pesan_diskon = valid_voucher['Annouce']
        else:
            st.warning("Kode voucher tidak valid.")

    # Menampilkan total setelah diskon
    st.write(f"**Total Harga Awal:** Rp{total_awal:,}")
    if voucher_input and pesan_diskon:
        st.success(pesan_diskon)
        st.write(f"**Total Setelah Diskon:** Rp{total_akhir:,}")
    else:
        st.write(f"**Total Akhir:** Rp{total_akhir:,}")

    # Tombol bayar
    if st.button("Bayar"):
        st.success("Pembayaran berhasil! Terima kasih telah berbelanja.")
        st.session_state.keranjang = []  # Mengosongkan keranjang


# Halaman Utama Streamlit
def main():
    st.title("Toko Baju Andalan")

    if st.session_state.user is None:
        menu = st.sidebar.radio("Menu", ["Login", "Register"])
        if menu == "Register":
            register_pembeli()
        elif menu == "Login":
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                login_result = auth_user(st.session_state.df_accounts, username, password)
                if login_result:
                    st.session_state.user = login_result
                    st.success(f"Login berhasil! Selamat datang, {username}.")
                    st.rerun()
                else:
                    st.error("Username atau password salah.")
    else:
        username, role = st.session_state.user
        st.sidebar.write(f"Selamat datang, **{username} ({role})**")
        if st.sidebar.button("Logout"):
            st.session_state.user = None
            st.rerun()

        if role == "admin":
            admin_menu = st.sidebar.radio("Menu Admin", ["Lihat Data Baju", "Tambah Stok"])
            if admin_menu == "Lihat Data Baju":
                lihat_data_baju()
            elif admin_menu == "Tambah Stok":
                tambah_stok()
        elif role == "pembeli":
            pembeli_menu = st.sidebar.radio("Menu Pembeli", ["Lihat Data Baju", "Tambah ke Keranjang", "Lihat Keranjang", "Bayar Keranjang"])
            if pembeli_menu == "Lihat Data Baju":
                lihat_data_baju()
            elif pembeli_menu == "Tambah ke Keranjang":
                tambah_ke_keranjang()
            elif pembeli_menu == "Lihat Keranjang":
                lihat_keranjang()
            elif pembeli_menu == "Bayar Keranjang":
                bayar_keranjang()

if __name__ == "__main__":
    main()
