def auth_user(df_accounts, username, password):
    # Cari username dan password dalam dataframe
    user_data = df_accounts[
        (df_accounts['username'] == username) & (df_accounts['password'] == password)
    ]
    if not user_data.empty:
        role = user_data.iloc[0]['role']
        return username, role
    return None  # Login gagal
