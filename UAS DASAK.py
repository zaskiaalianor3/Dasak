#!/usr/bin/env python
# coding: utf-8

import pandas as pd

# Struktur data transaksi
transaksi = []

# Daftar akun dasar
akun = {
    "Kas": "Aset",
    "Piutang": "Aset",
    "Perlengkapan": "Aset",
    "Modal": "Ekuitas",
    "Pendapatan": "Pendapatan",
    "Beban Gaji": "Beban",
    "Beban Listrik": "Beban"
}


def input_transaksi():
    print("=== INPUT TRANSAKSI ===")
    tanggal = input("Tanggal (YYYY-MM-DD): ")
    keterangan = input("Keterangan: ")
    akun_debit = input("Akun Debit: ")
    akun_kredit = input("Akun Kredit: ")
    jumlah = float(input("Jumlah: "))

    transaksi.append({
        "Tanggal": tanggal,
        "Keterangan": keterangan,
        "Akun Debit": akun_debit,
        "Akun Kredit": akun_kredit,
        "Jumlah": jumlah
    })

    print("\nTransaksi berhasil dicatat!\n")

# Contoh penggunaan:
# input_transaksi()


def show_transaksi():
    if len(transaksi) == 0:
        print("Belum ada transaksi.")
        return

    df = pd.DataFrame(transaksi)
    return df

# show_transaksi()


def buku_besar(nama_akun):
    data = []

    for t in transaksi:
        if t["Akun Debit"] == nama_akun:
            data.append([t["Tanggal"], t["Keterangan"], t["Jumlah"], 0])
        if t["Akun Kredit"] == nama_akun:
            data.append([t["Tanggal"], t["Keterangan"], 0, t["Jumlah"]])

    df = pd.DataFrame(data, columns=["Tanggal", "Keterangan", "Debit", "Kredit"])
    df["Saldo"] = df["Debit"] - df["Kredit"]
    df["Saldo"] = df["Saldo"].cumsum()

    return df

# buku_besar("Kas")


def neraca_saldo():
    saldo = {}

    for a in akun.keys():
        saldo[a] = 0

    for t in transaksi:
        saldo[t["Akun Debit"]] += t["Jumlah"]
        saldo[t["Akun Kredit"]] -= t["Jumlah"]

    df = pd.DataFrame(list(saldo.items()), columns=["Akun", "Saldo"])
    return df

# neraca_saldo()


def laba_rugi():
    pendapatan = 0
    beban = 0

    for t in transaksi:
        if akun.get(t["Akun Debit"]) == "Beban":
            beban += t["Jumlah"]
        if akun.get(t["Akun Kredit"]) == "Pendapatan":
            pendapatan += t["Jumlah"]

    laba = pendapatan - beban

    df = pd.DataFrame({
        "Keterangan": ["Total Pendapatan", "Total Beban", "Laba Bersih"],
        "Jumlah": [pendapatan, beban, laba]
    })

    return df

# laba_rugi()

