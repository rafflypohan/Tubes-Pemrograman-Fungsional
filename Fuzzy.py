import multiprocessing as mp
import itertools


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


def z_dapat(alpha, x):
    return (80 - 40) * alpha[x] + 40


def z_tidak_dapat(alpha, x):
    return 80 - (alpha[x]) * (80 - 40)


def fungsi_keanggotaan(ipk, penghasilan, jarak):
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

    inferensi(nilai_ipk, nilai_penghasilan, nilai_jarak)


def inferensi(nilai_ipk, nilai_penghasilan, nilai_jarak):
    x = 0
    alpha = []
    z = []
    ls = []

    for i, j, k in itertools.product(nilai_ipk, nilai_penghasilan, nilai_jarak):
        if (i > 0) and (j > 0) and (k > 0):
            ls.clear()
            ls.extend([i, j, k])
            alpha.append(min(ls))
            # print(alpha)
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

    defuzzifikasi(alpha, z)


def defuzzifikasi(alpha, z):
    # rumus centroid method
    # ((alpha1 * z1) + (alpha2 * z2) + ...) / (alpha1 + alpha2 + ...)
    jum = (a * b for a, b in zip(alpha, z))
    defuzi = sum(jum) / sum(alpha)
    print("Defuzzifikasi = " + "{:.2f}".format(defuzi) + "%")


if __name__ == '__main__':
    p = mp.Process(target=fungsi_keanggotaan, args=(3.3, 50000, 60))
    p.start()
    p.join()
