import streamlit as st
import sqlite3
import time

# Koneksi ke database SQLite3
conn = sqlite3.connect('topup.db')
c = conn.cursor()

# Buat tabel jika belum ada
c.execute('''CREATE TABLE IF NOT EXISTS topup
             (id INTEGER PRIMARY KEY AUTOINCREMENT, game TEXT, nominal TEXT, id_game TEXT, payment_method TEXT, timestamp TEXT)''')

# Daftar game dan nominal
games = {
    "Mobile Legend": [
        ("110 Diamonds", 28931),
        ("148 Diamonds", 38576),
        ("184 Diamonds", 48219),
        ("240 Diamonds", 61791),
        ("301 Diamonds", 77779),
        ("370 Diamonds", 96431),
        ("568 Diamonds", 142633)
    ],
    "Valorant": [
        ("125 Points", 15000),
        ("375 points", 42696),
        ("545 Points", 61671),
        ("700 points", 75903),
        ("1120 points", 123342),
        ("1375 points", 142317),
        ("2075 points", 218220)
    ],
    "PUBG Mobile": [
        ("60 UC", 12852),
        ("120 UC", 25704),
        ("300 + 25 Bonus UC", 64260),
        ("420 UC", 89964),
        ("600 + 60 Bonus UC", 128520),
        ("900 + 85 Bonus UC", 192780),
        ("1500 + 300 Bonus UC", 321300)
    ],
    "Roblox": [
        ("800 Robux", 147413),
        ("2000 Robux", 368533),
        ("4500 Robux", 737066),
        ("10000 Robux", 1474130)
    ],
    "CODM": [
        ("63 CP", 9642),
        ("128 CP", 19282),
        ("321 CP", 48204),
        ("645 CP", 96406),
        ("1373 CP", 192812),
        ("2750 CP", 366342),
        ("3564 CP", 482029)
    ],
    "Free Fire": [
        ("100 Diamonds", 13720),
        ("210 Diamonds", 28285),
        ("400 Diamonds", 53996),
        ("500 Diamond", 67087),
        ("720 Diamonds", 94275),
        ("1000 Diamonds", 131974),
        ("1440 Diamonds", 188523),
        ("1800 Diamonds", 237543),
        ("2000 Diamonds", 263771)
    ],
    "Genshin Impact": [
        ("60 Genesis Crystal", 11528),
        ("300 + 30 Genesis Crystal", 58704),
        ("980 + 110 Genesis Crystal", 176623),
        ("1980 + 260 Genesis Crystal", 383000),
        ("3280 + 600 Genesis Crystal", 589341),
        ("6480 + 1600 Genesis Crystal", 1179011)
    ]
}

# Tampilan utama
st.set_page_config(page_title="TOPFlazID", page_icon=":video_game:", layout="wide")
st.title("TOPFlazID - Top Up Game Termurah")

# Sidebar untuk navigasi
st.sidebar.title("Navigasi")
navigation = st.sidebar.radio("Pilih Menu", ["Top Up", "Riwayat Top Up", "Ubah Data Top Up", "Hapus Data Top Up"])

if navigation == "Top Up":
    # Pilih game
    st.header("Top Up Game")
    game = st.selectbox("Pilih Game", list(games.keys()))

    # Pilih nominal
    nominal_list = games[game]
    nominal = st.selectbox(f"Pilih Nominal {game}", [f"{n} - Rp {p:,.0f}" for n, p in nominal_list])
    nominal_value = [p for n, p in nominal_list if f"{n} - Rp {p:,.0f}" == nominal][0]

    # Input ID game
    if game == "Mobile Legend":
        user_id = st.text_input("User ID")
        zone_id = st.text_input("Zone ID")
        id_game = f"User ID: {user_id}, Zone ID: {zone_id}"
    elif game == "Valorant":
        riot_id = st.text_input("Riot ID#Tagline")
        id_game = riot_id
    elif game == "PUBG Mobile":
        uid = st.text_input("UID")
        id_game = uid
    elif game == "Roblox":
        roblox_id = st.text_input("ID Roblox")
        id_game = roblox_id
    elif game == "CODM":
        open_id = st.text_input("Open ID")
        id_game = open_id
    elif game == "Free Fire":
        uid = st.text_input("UID")
        id_game = uid
    elif game == "Genshin Impact":
        uid = st.text_input("UID")
        server = st.radio("Pilih Server", ["Server Asia", "America", "Europe", "TW_HK_MO"])
        id_game = f"UID: {uid}, Server: {server}"

    # Pilih metode pembayaran
    payment_method = st.selectbox("Pilih Metode Pembayaran", ["E-Wallet", "Bank"])

    if payment_method == "E-Wallet":
        e_wallet = st.selectbox("Pilih E-Wallet", ["DANA", "OVO", "Gopay", "LinkAja"])
    else:
        bank = st.selectbox("Pilih Bank", ["BCA", "Mandiri", "BRI", "BNI", "Seabank", "Danamon", "BSI"])

    # Konfirmasi pesanan
    if st.button("Konfirmasi Pesanan"):
        confirm = st.checkbox("Apakah pesanan Anda sudah benar?")
        if confirm:
            # Simulasikan proses top up selama 10 detik
            with st.spinner("Memproses top up..."):
                time.sleep(10)
            st.success("Top up berhasil!")

            # Simpan data ke database
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            c.execute("INSERT INTO topup (game, nominal, id_game, payment_method, timestamp) VALUES (?, ?, ?, ?, ?)",
                      (game, nominal, id_game, payment_method, timestamp))
            conn.commit()
        else:
            st.warning("Silakan periksa kembali pesanan Anda.")

elif navigation == "Riwayat Top Up":
    st.header("Riwayat Top Up")
    data = c.execute("SELECT * FROM topup").fetchall()
    st.table(data)

elif navigation == "Ubah Data Top Up":
    st.header("Ubah Data Top Up")
    data = c.execute("SELECT * FROM topup").fetchall()
    selected_row = st.selectbox("Pilih Data Top Up", data, format_func=lambda row: f"{row[1]} - {row[2]} - {row[3]} - {row[4]}")

    if selected_row:
        id_data = selected_row[0]
        game = st.selectbox("Ubah Game", list(games.keys()), index=list(games.keys()).index(selected_row[1]))
        nominal_list = games[game]
        nominal = st.selectbox(f"Ubah Nominal {game}", [f"{n} - Rp {p:,.0f}" for n, p in nominal_list])