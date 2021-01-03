def linear_turun(a, b, x):
    if x <= a:
        derajat_keanggotaan = 1
    elif a <= x <= b:
        derajat_keanggotaan = (b - x) / (b - a)
    else:
        derajat_keanggotaan = 0
    yield derajat_keanggotaan


def linear_naik(a, b, x):
    if x <= a:
        derajat_keanggotaan = 0
    elif a <= x <= b:
        derajat_keanggotaan = (x - a) / (b - a)
    else:
        derajat_keanggotaan = 1
    yield derajat_keanggotaan


def segitiga(a, b, c, x):
    if a <= x <= b:
        derajat_keanggotaan = (x - a) / (b - a)
    elif b <= x <= c:
        derajat_keanggotaan = (c - x) / (c - b)
    else:
        derajat_keanggotaan = 0
    yield derajat_keanggotaan


def ipk_rendah(x):
  yield linear_turun(1.5, 2.5, x)

def ipk_sedang(x):
  yield segitiga(1.5, 2.5, 3.5, x)

def ipk_tinggi(x):
  yield linear_naik(2.5, 4, x)

def penghasilan_rendah(x):
  yield linear_turun(3000000, 5500000, x)

def penghasilan_sedang(x):
  yield segitiga(2000000, 5500000, 9000000, x)

def penghasilan_tinggi(x):
  yield linear_naik(5500000, 9000000, x)

def jarak_dekat(x):
  yield linear_turun(5, 12.5, x)

def jarak_sedang(x):
  yield segitiga(5, 12.5, 20, x)

def jarak_jauh(x):
  yield linear_naik(12.5, 20, x)

def z_dapat(alpha, x):
  yield (80 - 40) * alpha[x] + 40

def z_tidak_dapat(alpha, x):
  yield 80 - (alpha[x]) * (80 - 40)

# * Inferensi
def inferensi(nilai_ipk, nilai_penghasilan, nilai_jarak):
  for i, ip in enumerate(nilai_ipk):
    for j, png in enumerate(nilai_penghasilan):
      for k, jrk in enumerate(nilai_jarak):
        continue


  for i in nilai_ipk:
    for j in nilai_penghasilan:
      for k in nilai_jarak:
        continue

def defuzzifikasi(alpha, z, res):
  for index in range(len(alpha)):
    jum = alpha[index] * z[index]
  defuzi = sum(jum) / sum(alpha)
  res.value = round(defuzi, 2)

if kembali == "y":
  menu(filename)
else:
  sys.exit("Terima Kasih")

