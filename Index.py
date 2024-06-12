import streamlit as st
import sqlite3

# Koneksi ke database SQLite
conn = sqlite3.connect('topflazid.db')
c = conn.cursor()

# Buat tabel jika belum ada
c.execute("""CREATE TABLE IF NOT EXISTS orders
             (id INTEGER PRIMARY KEY AUTOINCREMENT, game TEXT, voucher_type TEXT, amount REAL, email TEXT, payment_method TEXT, status TEXT)""")

# comit dengan perubahan
conn.commit()

# Daftar game dan nominal
games = {
    'Mobile Legend': [(10, 5.99), (20, 9.99), (50, 19.99), (100, 39.99)],
    'Valorant': [(20, 9.99), (40, 19.99), (80, 39.99)],
    'PUBG': [(10, 5.99), (25, 9.99), (50, 19.99), (100, 39.99)],
    'Roblox': [(10, 5.99), (20, 9.99), (40, 19.99), (80, 39.99)],
    'Freefire': [(10, 5.99), (20, 9.99), (50, 19.99), (100, 39.99)],
    'Genshin Impact': [(10, 5.99), (20, 9.99), (50, 19.99), (100, 39.99)]
}

# Tampilan utama
def main():
    st.title("TOPFLAZID")
    menu = ["Beli Voucher", "Daftar Pembelian"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Beli Voucher":
        st.subheader("Beli Voucher Game")

        # Pilih game
        game = st.selectbox("Pilih Game", list(games.keys()))

        # Pilih nominal voucher
        voucher_type = st.selectbox("Pilih Nominal", [f"{amount} ({price})" for amount, price in games[game]])
        amount, price = [int(x) for x in voucher_type.split(' (')[0]], float(voucher_type.split(' (')[1][:-1])

        # Input ID game dan email
        game_id = st.text_input("ID Game")
        email = st.text_input("Email")

        # Pilih metode pembayaran
        payment_method = st.selectbox("Pilih Metode Pembayaran", ["E-Wallet", "Bank"])
        if payment_method == "E-Wallet":
            payment_option = st.selectbox("Pilih E-Wallet", ["Dana", "OVO", "GoPay", "LinkAja"])
        else:
            payment_option = st.selectbox("Pilih Bank", ["Mandiri", "BCA", "BNI", "BRI", "Seabank"])

        # Konfirmasi pembelian
        if st.button("Beli"):
            confirm = st.checkbox("Konfirmasi Pembelian")
            if confirm:
                c.execute("INSERT INTO orders (game, voucher_type, amount, email, payment_method, status) VALUES (?, ?, ?, ?, ?, ?)",
                          (game, str(amount), price, email, payment_method + ": " + payment_option, "Pending"))
                conn.commit()
                st.success(f"Pembelian {voucher_type} untuk {game} berhasil! Silakan tunggu 1-2 menit.")

    elif choice == "Daftar Pembelian":
        st.subheader("Daftar Pembelian")
        c.execute("SELECT * FROM orders")
        data = c.fetchall()
        for order in data:
            st.write(f"ID: {order[0]}, Game: {order[1]}, Voucher: {order[2]} ({order[3]}), Email: {order[4]}, Pembayaran: {order[5]}, Status: {order[6]}")

if __name__ == '__main__':
    main()