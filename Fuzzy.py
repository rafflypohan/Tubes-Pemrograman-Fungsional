
def ipk_rendah(ipk):
    if ipk <= 1.5:
        derajat_keanggotaan = 1
    elif 1.5 <= ipk <= 2.5:
        derajat_keanggotaan = (2.5 - ipk) / (2.5 - 1.5)
    else:
        derajat_keanggotaan = 0
    return derajat_keanggotaan


def ipk_sedang(ipk):
    if 1.5 <= ipk <= 2.5:
        derajat_keanggotaan = (ipk - 1.5) / (2.5 - 1.5)
    elif 2.5 <= ipk <= 3.5:
        derajat_keanggotaan = (3.5 - ipk) / (3.5 - 2.5)
    else:
        derajat_keanggotaan = 0
    return derajat_keanggotaan


def ipk_tinggi(ipk):
    if ipk <= 2.5:
        derajat_keanggotaan = 0
    elif 2.5 <= ipk <= 4:
        derajat_keanggotaan = (ipk - 2.5) / (4 - 2.5)
    else:
        derajat_keanggotaan = 1
    return derajat_keanggotaan


def penghasilan_rendah(penghasilan):
    if penghasilan <= 3000000:
        derajat_keanggotaan = 1
    elif 3000000 <= penghasilan <= 5500000:
        derajat_keanggotaan = (5500000 - penghasilan) / (5500000 - 3000000)
    else:
        derajat_keanggotaan = 0
    return derajat_keanggotaan


def penghasilan_sedang(penghasilan):
    if 2000000 <= penghasilan <= 5500000:
        derajat_keanggotaan = (penghasilan - 2000000) / (5500000 - 2000000)
    elif 5500000 <= penghasilan <= 9000000:
        derajat_keanggotaan = (9000000 - penghasilan) / (9000000 - 5500000)
    else:
        derajat_keanggotaan = 0
    return derajat_keanggotaan


def penghasilan_tinggi(penghasilan):
    if penghasilan <= 5500000:
        derajat_keanggotaan = 0
    elif 5500000 <= penghasilan <= 9000000:
        derajat_keanggotaan = (penghasilan - 5500000) / (9000000-5500000)
    else:
        derajat_keanggotaan = 1
    return derajat_keanggotaan


def jarak_dekat(jarak):
    if jarak <= 5:
        derajat_keanggotaan = 1
    elif 5 <= jarak <= 12.5:
        derajat_keanggotaan = (12.5 - jarak) / (12.5 - 5)
    else:
        derajat_keanggotaan = 0
    return derajat_keanggotaan


def jarak_sedang(jarak):
    if 5 <= jarak <= 12.5:
        derajat_keanggotaan = (jarak - 5) / (12.5 - 5)
    elif 12.5 <= jarak <= 20:
        derajat_keanggotaan = (20 - jarak) / (20 - 12.5)
    else:
        derajat_keanggotaan = 0


def jarak_jauh(jarak):
    if jarak <= 12.5:
        derajat_keanggotaan = 0
    elif 12.5 <= jarak <= 20:
        derajat_keanggotaan = (jarak - 12.5) / (20 - 12.5)
    else:
        derajat_keanggotaan = 1
    return derajat_keanggotaan


def inferensi(ipk, penghasilan, jarak):
    pass

print(jarak_jauh(30))
