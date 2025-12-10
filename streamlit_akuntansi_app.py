import streamlit as st
import pandas as pd

st.title("📘 Aplikasi Akuntansi Lengkap (Debit–Kredit, Buku Besar, Laba Rugi, Neraca)")

# ==========================================
# SESSION STATE
# ==========================================
if "data" not in st.session_state:
    st.session_state.data = []

# ==========================================
# INPUT TRANSAKSI
# ==========================================
st.header("🔹 Input Transaksi")
st.write("Masukkan transaksi dan klik **Tambah Transaksi**.")

with st.form("form_transaksi"):
    akun = st.text_input("Nama Akun")
    jenis = st.selectbox("Jenis Transaksi", ["Debit", "Kredit"])
    jumlah = st.number_input("Jumlah (Rp)", min_value=0.0)
    tambah = st.form_submit_button("Tambah Transaksi")

if tambah:
    if akun.strip() == "":
        st.warning("Nama akun tidak boleh kosong.")
    else:
        st.session_state.data.append({
            "Akun": akun,
            "Jenis": jenis,
            "Jumlah": jumlah
        })
        st.success("Transaksi berhasil ditambahkan!")

# DataFrame
st.subheader("📄 Tabel Transaksi")
df = pd.DataFrame(st.session_state.data)

if df.empty:
    st.info("Belum ada transaksi.")
else:
    st.table(df)

    # ==========================================
    # PERHITUNGAN TOTAL
    # ==========================================
    total_debit = df[df["Jenis"] == "Debit"]["Jumlah"].sum()
    total_kredit = df[df["Jenis"] == "Kredit"]["Jumlah"].sum()

    st.subheader("🔢 Total")
    st.write(f"**Total Debit : Rp {total_debit:,.0f}**")
    st.write(f"**Total Kredit : Rp {total_kredit:,.0f}**")

    if total_debit == total_kredit:
        st.success("✔ Jurnal SEIMBANG")
    else:
        st.error("✘ Jurnal TIDAK seimbang")

    # ==========================================
    # BUKU BESAR
    # ==========================================
    st.header("📘 Buku Besar")

    grouped = df.groupby("Akun")

    for akun, data in grouped:
        st.subheader(f"📍 Akun: {akun}")
        st.table(data)
        total_d = data[data["Jenis"] == "Debit"]["Jumlah"].sum()
        total_k = data[data["Jenis"] == "Kredit"]["Jumlah"].sum()
        saldo = total_d - total_k

        st.write(f"**Total Debit: Rp {total_d:,.0f}**")
        st.write(f"**Total Kredit: Rp {total_k:,.0f}**")
        st.write(f"👉 **Saldo Akhir: Rp {saldo:,.0f}**")
        st.markdown("---")

    # ==========================================
    # LAPORAN LABA RUGI
    # ==========================================
    st.header("📈 Laporan Laba Rugi")

    # Tentukan akun pendapatan & beban dari input user
    pendapatan = df[(df["Akun"].str.contains("pendapatan", case=False)) & (df["Jenis"] == "Kredit")]["Jumlah"].sum()
    beban = df[(df["Akun"].str.contains("beban", case=False)) & (df["Jenis"] == "Debit")]["Jumlah"].sum()

    laba_rugi = pendapatan - beban

    st.write(f"**Total Pendapatan : Rp {pendapatan:,.0f}**")
    st.write(f"**Total Beban : Rp {beban:,.0f}**")
    st.write(f"### 👉 Laba/Rugi Bersih: **Rp {laba_rugi:,.0f}**")

    if laba_rugi >= 0:
        st.success("Perusahaan memperoleh LABA")
    else:
        st.error("Perusahaan mengalami RUGI")

    # ==========================================
    # NERACA
    # ==========================================
    st.header("📊 Neraca")

    # Akun Aktiva → debit lebih besar
    aktiva = df[(df["Jenis"] == "Debit") & ~(df["Akun"].str.contains("beban", case=False))]["Jumlah"].sum()

    # Akun Kewajiban + Ekuitas → kredit lebih besar
    pasiva = df[(df["Jenis"] == "Kredit") & ~(df["Akun"].str.contains("pendapatan", case=False))]["Jumlah"].sum()

    st.write(f"**Total Aktiva : Rp {aktiva:,.0f}**")
    st.write(f"**Total Kewajiban + Ekuitas : Rp {pasiva:,.0f}**")

    if aktiva == pasiva:
        st.success("✔ Neraca SEIMBANG")
    else:
        st.error("✘ Neraca TIDAK seimbang")
