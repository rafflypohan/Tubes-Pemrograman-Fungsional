import os
import sys
import csv
import pandas
from itertools import product
from multiprocessing import Process, Manager

def linear_turun(a, b, x):
    derajat_keanggotaan = (1 if x <= a else (b - x) / (b - a) if a <= x <= b else 0)
    yield derajat_keanggotaan


def linear_naik(a, b, x):
    derajat_keanggotaan = (0 if x <= a else (x - a) / (b - a) if a <= x <= b else 1)
    yield derajat_keanggotaan


def segitiga(a, b, c, x):
    derajat_keanggotaan = ((x - a) / (b - a) if a <= x <= b else (c - x) / (c - b) if b <= x <= c else 0)
    yield derajat_keanggotaan


def fungsi_keanggotaan(ipk, penghasilan, jarak, res):
    ipk_rendah = lambda x: linear_turun(1.5, 2.5, x)
    ipk_sedang = lambda x: segitiga(1.5, 2.5, 3.5, x)
    ipk_tinggi = lambda x: linear_naik(2.5, 4, x)

    penghasilan_rendah = lambda x: linear_turun(3000000, 5500000, x)
    penghasilan_sedang = lambda x: segitiga(2000000, 5500000, 9000000, x)
    penghasilan_tinggi = lambda x: linear_naik(5500000, 9000000, x)

    jarak_dekat = lambda x: linear_turun(5, 12.5, x)
    jarak_sedang = lambda x: segitiga(5, 12.5, 20, x)
    jarak_jauh = lambda x: linear_naik(12.5, 20, x)

    nilai_ipk = [next(ipk_rendah(ipk)), next(ipk_sedang(ipk)), next(ipk_tinggi(ipk))]
    nilai_penghasilan = [next(penghasilan_rendah(penghasilan)), next(penghasilan_sedang(penghasilan)),
                         next(penghasilan_tinggi(penghasilan))]
    nilai_jarak = [next(jarak_dekat(jarak)), next(jarak_sedang(jarak)), next(jarak_jauh(jarak))]

    inferensi(nilai_ipk, nilai_penghasilan, nilai_jarak, res)



def inferensi(nilai_ipk, nilai_penghasilan, nilai_jarak, res):
    x = 0
    alpha = []
    z = []
    tmp = []
    z_dapat = lambda alpha, x: (80 - 40) * alpha[x] + 40
    z_tidak_dapat = lambda alpha, x: 80 - (alpha[x]) * (80 - 40)
    for i, j, k in product(nilai_ipk, nilai_penghasilan, nilai_jarak):
        if (i and j and k) > 0:
            tmp.clear()
            tmp.extend([i, j, k])
            alpha.append(min(tmp))

            if nilai_ipk.index(i) == 2 and nilai_penghasilan.index(j) == 1 and nilai_jarak.index(k) == 2:
                z.append(z_dapat(alpha, x))
            elif nilai_ipk.index(i) == 2 and nilai_penghasilan.index(j) == 0 and nilai_jarak.index(k) == 2:
                z.append(z_dapat(alpha, x))
            elif nilai_ipk.index(i) == 2 and nilai_penghasilan.index(j) == 1 and nilai_jarak.index(k) == 1:
                z.append(z_dapat(alpha, x))
            elif nilai_ipk.index(i) == 2 and nilai_penghasilan.index(j) == 0 and nilai_jarak.index(k) == 1:
                z.append(z_dapat(alpha, x))
            elif nilai_ipk.index(i) == 2 and nilai_penghasilan.index(j) == 1 and nilai_jarak.index(k) == 0:
                z.append(z_dapat(alpha, x))
            elif nilai_ipk.index(i) == 2 and nilai_penghasilan.index(j) == 0 and nilai_jarak.index(k) == 0:
                z.append(z_dapat(alpha, x))
            else:
                z.append(z_tidak_dapat(alpha, x))
            # print(f"IF IPK = {i} AND Penghasilan = {j} AND Jarak = {k} THEN z = {z[x]} alpha = {alpha[x]} x = {x}")
            x += 1
    print("\n########### Data anda berhasil tersimpan ###########\n")

    defuzzifikasi(alpha, z, res)


def defuzzifikasi(alpha, z, res):
    # rumus centroid method
    # ((alpha1 * z1) + (alpha2 * z2) + ...) / (alpha1 + alpha2 + ...)
    jum = (a * b for a, b in zip(alpha, z))
    defuzi = sum(jum) / sum(alpha)
    res.value = round(defuzi, 2)
    # print("Hasil Defuzzifikasi = ", round(defuzi, 2), "%")


def read_csv(filename):
    try:
        print(pandas.read_csv(filename))
    except FileNotFoundError:
        print("Maaf, belum ada data")


def write_csv(filename, nama, ipk, penghasilan, jarak, peluang):
    rows = ["Nama", "IPK", "Penghasilan", "Jarak", "Peluang (%)"]
    if os.path.isfile(filename):
        with open(filename, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=rows)
            writer.writerow(
                {"Nama": nama, "IPK": ipk, "Penghasilan": penghasilan, "Jarak": jarak, "Peluang (%)": peluang})
    else:
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=rows)
            writer.writeheader()
            writer.writerow(
                {"Nama": nama, "IPK": ipk, "Penghasilan": penghasilan, "Jarak": jarak, "Peluang (%)": peluang})


def menu(filename):
    n = int(input("1. Tambah Data\n2. Tampilkan Data\n3. Keluar\nPilih Menu : "))
    print()
    if n == 1:
        main(filename)
    elif n == 2:
        read_csv(filename)
        kembali = input("Kembali ke menu utama (y/n) : ")
        (menu(filename) if kembali == "y" else sys.exit("Terima Kasih"))
    elif n == 3:
        sys.exit("Terima Kasih")
    else:
        print("Masukkan pilihan yang benar")
        menu(filename)


def main(filename):
    manager = Manager()
    res = manager.Value('d', 0)

    nama = input("Masukkan Nama: ")
    ipk = float(input("Masukkan IPK saat ini: "))
    penghasilan = int(input("Masukkan Penghasilan Orang Tua : "))
    jarak = float(input("Masukkan Jarak dari rumah anda ke Kampus/Sekolah (Km): "))

    p = Process(target=fungsi_keanggotaan, args=(ipk, penghasilan, jarak, res,))
    p.start()
    p.join()

    write_csv(filename, nama, ipk, penghasilan, jarak, res.value)

    repeat = input("Apakah anda ingin menginput data lagi?(y/n) : ")
    print()
    while repeat == "y":
        main(filename)
    menu(filename)


if __name__ == '__main__':
    filename = 'tes.csv'
    menu(filename)
