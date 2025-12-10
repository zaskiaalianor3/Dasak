import streamlit as st
import pandas as pd

st.title("Aplikasi Akuntansi Sederhana (Debit – Kredit)")

# ==============================
# SESSION STATE untuk menyimpan data
# ==============================
if "data" not in st.session_state:
    st.session_state.data = []

st.write("Masukkan transaksi lalu klik **Tambah Transaksi**.")

# ==============================
# FORM INPUT
# ==============================
with st.form("input_transaksi"):
    akun = st.text_input("Nama Akun")
    jenis = st.selectbox("Jenis Transaksi", ["Debit", "Kredit"])
    jumlah = st.number_input("Jumlah (Rp)", min_value=0.0)
    tambah = st.form_submit_button("Tambah Transaksi")

# Saat tombol diklik → simpan
if tambah:
    if akun == "":
        st.warning("Nama akun tidak boleh kosong.")
    else:
        st.session_state.data.append({
            "Akun": akun,
            "Jenis": jenis,
            "Jumlah": jumlah
        })
        st.success("Transaksi berhasil ditambahkan!")

# ==============================
# TABEL OUTPUT
# ==============================
df = pd.DataFrame(st.session_state.data)

if not df.empty:
    st.subheader("📄 Tabel Transaksi")
    st.table(df)

    # Hitung debit dan kredit
    total_debit = df[df["Jenis"] == "Debit"]["Jumlah"].sum()
    total_kredit = df[df["Jenis"] == "Kredit"]["Jumlah"].sum()

    st.write("### 🔢 Total")
    st.write(f"**Total Debit  : Rp {total_debit:,.0f}**")
    st.write(f"**Total Kredit : Rp {total_kredit:,.0f}**")

    # Status Balance
    st.write("### 📌 Status Jurnal")
    if total_debit == total_kredit:
        st.success("✔ Jurnal SEIMBANG")
    else:
        st.error("✘ Jurnal TIDAK seimbang")
else:
    st.info("Belum ada transaksi yang dimasukkan.")
