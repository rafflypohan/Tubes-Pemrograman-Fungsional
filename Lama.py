import os
import sys
import csv
import itertools
import multiprocessing as mp
import pandas


def linear_turun(a, b, x):
    if x <= a:
        derajat_keanggotaan = 1
    elif a <= x <= b:
        derajat_keanggotaan = (b - x) / (b - a)
    else:
        derajat_keanggotaan = 0
    return derajat_keanggotaan


def linear_naik(a, b, x):
    if x <= a:
        derajat_keanggotaan = 0
    elif a <= x <= b:
        derajat_keanggotaan = (x - a) / (b - a)
    else:
        derajat_keanggotaan = 1
    return derajat_keanggotaan


def segitiga(a, b, c, x):
    if a <= x <= b:
        derajat_keanggotaan = (x - a) / (b - a)
    elif b <= x <= c:
        derajat_keanggotaan = (c - x) / (c - b)
    else:
        derajat_keanggotaan = 0
    return derajat_keanggotaan


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

    nilai_ipk = [ipk_rendah(ipk), ipk_sedang(ipk), ipk_tinggi(ipk)]
    nilai_penghasilan = [penghasilan_rendah(penghasilan), penghasilan_sedang(penghasilan),
                         penghasilan_tinggi(penghasilan)]
    nilai_jarak = [jarak_dekat(jarak), jarak_sedang(jarak), jarak_jauh(jarak)]

    inferensi(nilai_ipk, nilai_penghasilan, nilai_jarak, res)


def inferensi(nilai_ipk, nilai_penghasilan, nilai_jarak, res):
    x = 0
    alpha = []
    z = []
    ls = []
    z_dapat = lambda alpha, x: (80 - 40) * alpha[x] + 40
    z_tidak_dapat = lambda alpha, x: 80 - (alpha[x]) * (80 - 40)
    for i, j, k in itertools.product(nilai_ipk, nilai_penghasilan, nilai_jarak):
        if (next(i) and next(j) and next(k)) > 0:
            ls.clear()
            ls.extend([i, j, k])
            alpha.append(min(ls))

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
            print(f"IF IPK = {i} AND Penghasilan = {j} AND Jarak = {k} THEN z = {z[x]} alpha = {alpha[x]} x = {x}")
            x += 1

    defuzzifikasi(alpha, z, res)


def defuzzifikasi(alpha, z, res):
    # rumus centroid method
    # ((alpha1 * z1) + (alpha2 * z2) + ...) / (alpha1 + alpha2 + ...)
    # global res
    jum = (a * b for a, b in zip(alpha, z))
    defuzi = sum(jum) / sum(alpha)
    res.value = round(defuzi, 2)
    print("Hasil Defuzzifikasi = ", round(defuzi, 2), "%")


def read_csv(filename):
    print(pandas.read_csv(filename))


def write_csv(filename, nama, ipk, penghasilan, jarak, peluang):
    rows = ["Nama", "IPK", "Penghasilan", "Jarak", "Peluang (%)"]
    if os.path.isfile(filename):
        with open(filename, 'a', newline='') as f:
            w = csv.DictWriter(f, fieldnames=rows)
            w.writerow({"Nama": nama, "IPK": ipk, "Penghasilan": penghasilan, "Jarak": jarak, "Peluang (%)": peluang})
    else:
        with open(filename, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=rows)
            w.writeheader()
            w.writerow({"Nama": nama, "IPK": ipk, "Penghasilan": penghasilan, "Jarak": jarak, "Peluang (%)": peluang})


def menu(filename):
    print("1. Tambah Data\n2. Tampilkan Data\n3. Keluar")
    n = int(input("Pilih Menu : "))
    if n == 1:
        main(filename)
    elif n == 2:
        read_csv(filename)
        m = input("Kembali ke menu utama (y) : ")
        (menu(filename) if m == "y" else sys.exit("Terima Kasih"))
    elif n == 3:
        sys.exit("Terima Kasih")
    else:
        menu(filename)


def main(filename):
    manager = mp.Manager()
    res = manager.Value('d', 0)

    nama = input("Masukkan Nama: ")
    ipk = float(input("Masukkan IPK saat ini: "))
    penghasilan = int(input("Masukkan Penghasilan Orang Tua : "))
    jarak = float(input("Masukkan Jarak dari rumah anda ke Kampus/Sekolah (Km): "))

    p = mp.Process(target=fungsi_keanggotaan, args=(ipk, penghasilan, jarak, res,))
    p.start()
    p.join()

    write_csv(filename, nama, ipk, penghasilan, jarak, res.value)

    repeat = input("Apakah anda ingin menginput data lagi?(y/n) : ")
    while repeat == "y":
        main(filename)
    menu(filename)


if __name__ == '__main__':
    filename = 'tes.csv'
    menu(filename)
    # read_csv('tes.csv')
