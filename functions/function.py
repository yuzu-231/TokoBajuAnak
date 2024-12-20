def auth_user(df_accounts):
    print("\nSilakan login sebagai admin:")
    username = input("Masukkan username: ").strip()
    password = input("Masukkan password: ").strip()

    # Cari username dan password dalam dataframe
    admin_data = df_accounts[(df_accounts['username'] == username) & (df_accounts['password'] == password)]
    if not admin_data.empty and admin_data.iloc[0]['role'] == 'admin':
        return username, 'admin'
    elif not admin_data.empty and admin_data.iloc[0]['role'] == 'pembeli':
        return username, 'pembeli'
    else:
        return None  # Login gagal
