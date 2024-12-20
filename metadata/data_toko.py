import pandas as pd 

# DATA BAJU ANAK
baju_anak = [
    {"Nama": "Baju Anak Motif Dinosaurus", "Ukuran" : ["S", "M", "L", "XL"], "Harga": 70000},
    {"Nama": "Baju Anak Motif Bunga", "Ukuran" : ["S", "M", "L", "XL"], "Harga": 70000},
    {"Nama": "Baju Anak Motif Mobil", "Ukuran" : ["S", "M", "L", "XL"], "Harga": 75000},
    {"Nama": "Baju Anak Motif Hewan", "Ukuran" : ["S", "M", "L", "XL"], "Harga": 80000},
    {"Nama": "Baju Anak Motif Buah", "Ukuran" : ["S", "M", "L", "XL"], "Harga": 95000},
    {"Nama": "Baju Anak Motif Kartun", "Ukuran" : ["S", "M", "L", "XL"], "Harga": 100000},
    {"Nama": "Baju Anak Motif Polkadot", "Ukuran" : ["S", "M", "L", "XL"], "Harga": 90000},
    {"Nama": "Baju Anak Motif Pelangi", "Ukuran" : ["S", "M", "L", "XL"], "Harga": 100000},
    {"Nama": "Baju Anak Motif Bintang", "Ukuran" : ["S", "M", "L", "XL"], "Harga": 80000},
    {"Nama": "Baju Anak Biru Polos", "Ukuran" : ["S", "M", "L", "XL"], "Harga": 60000},
    {"Nama": "Baju Anak Pink Polos", "Ukuran" : ["S", "M", "L", "XL"], "Harga": 60000},
    {"Nama": "Baju Anak Merah Polos", "Ukuran" : ["S", "M", "L", "XL"], "Harga": 60000},
    {"Nama": "Baju Anak Putih Polos", "Ukuran" : ["S", "M", "L", "XL"], "Harga": 60000},
    
]

df_baju_anak = pd.DataFrame(baju_anak)

#DATA ADMIN

accounts = [
    {
        "username": "Sabrina", 
        "password": "15240233", 
        "role" : "admin"
    },
    {
        "username": "Putra",
        "password": "15240301",
        "role":"admin"
    },
    {
        "username": "Valenvia",
        "password": "15240234",
        "role": "admin"
    },
    {
        "username": "Ahmad",
        "password": "15240440",
        "role":"admin"
    },
    {
        "username": "Fahreza",
        "password": "15240204",
        "role"  : "admin"
    },
]

df_accounts = pd.DataFrame(accounts)

vouchers = [
    {"kode": "DISC10", "diskon": 0.1, "Annouce": "Berhasil medapatkan potongan 10%!"},
    {"kode": "ANAKBSI", "diskon": 0.2, "Annouce": "Berhasil medapatkan potongan 20%!"},
    {"kode": "JUMATBERKAH", "diskon": 0.3, "Annouce": "Berhasil medapatkan potongan 30%!"},
]
df_vouchers = pd.DataFrame(vouchers)