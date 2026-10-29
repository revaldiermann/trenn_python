import turtle
import math
import random
import os
from PIL import Image

# ==================================================
# PENGATURAN
# ==================================================
LEBAR, TINGGI = 1000, 800
FOTO_PATH = os.path.join("foto", "foto1.png")
MUSIK_PATH = os.path.join("musik.mp3")
ALBUM_DIR = "album"

# Folder album hanya untuk menyimpan hasil olahan foto.
os.makedirs(ALBUM_DIR, exist_ok=True)

if not os.path.isfile(FOTO_PATH):
    raise FileNotFoundError(
        f"Foto tidak ditemukan: {FOTO_PATH}\n"
        "Pastikan file foto1.png berada di folder foto."
    )

# ==================================================
# FOTO PNG TRANSPARAN DI ATAS LATAR PUTIH
# ==================================================
# PNG transparan tidak dipakai sebagai bgpic secara langsung.
# Kita gabungkan alpha dengan putih, lalu tempatkan sebagai background GIF.
foto = Image.open(FOTO_PATH).convert("RGBA")
foto.thumbnail((430, 390), Image.Resampling.LANCZOS)

latar_foto = Image.new("RGBA", foto.size, (255, 255, 255, 255))
latar_foto.alpha_composite(foto)
bg_path = os.path.join(ALBUM_DIR, "background.gif")
latar_foto.convert("RGB").save(bg_path, "GIF")

# ==================================================
# LAYAR TURTLE
# ==================================================
layar = turtle.Screen()
layar.setup(width=LEBAR, height=TINGGI)
layar.title("I Love You Forever")
layar.bgcolor("white")
layar.bgpic(bg_path)
layar.tracer(0)

# ==================================================
# MUSIK OPSIONAL
# ==================================================
try:
    import pygame
    if os.path.isfile(MUSIK_PATH):
        pygame.mixer.init()
        pygame.mixer.music.load(MUSIK_PATH)
        pygame.mixer.music.set_volume(0.45)
        pygame.mixer.music.play(-1)
        print("Musik sedang diputar.")
    else:
        print(f"Musik tidak ditemukan: {MUSIK_PATH} (musik dilewati)")
except Exception as exc:
    print(f"Musik tidak aktif: {exc}")
    print("Jika ingin musik, pasang pygame dan pastikan file musik tersedia.")

# ==================================================
# FUNGSI BENTUK HATI
# ==================================================
def corazon(n):
    x = 16 * math.sin(n) ** 3
    y = (
        13 * math.cos(n)
        - 5 * math.cos(2 * n)
        - 2 * math.cos(3 * n)
        - math.cos(4 * n)
    )
    return x, y

# Setiap efek memakai turtle terpisah agar clear() tidak menghapus efek lain.
neon = turtle.Turtle(visible=False)
neon.speed(0)
neon.penup()

bintang = turtle.Turtle(visible=False)
bintang.speed(0)
bintang.penup()

hujan = turtle.Turtle(visible=False)
hujan.speed(0)
hujan.penup()

teks = turtle.Turtle(visible=False)
teks.speed(0)
teks.penup()

# ==================================================
# GAMBAR SATU GARIS HATI
# ==================================================
def gambar_hati(pen, scale, warna, tebal, titik=42):
    pen.color(warna)
    pen.pensize(tebal)
    pen.penup()

    for j in range(titik + 1):
        n = 2 * math.pi * j / titik
        x, y = corazon(n)
        x *= scale
        y *= scale

        if j == 0:
            pen.goto(x, y)
            pen.pendown()
        else:
            pen.goto(x, y)

    pen.penup()

# ==================================================
# BINTANG BERKILAU
# ==================================================
daftar_bintang = [
    {
        "x": random.randint(-475, 475),
        "y": random.randint(-370, 370),
        "ukuran": random.randint(2, 5),
        "fase": random.random() * 2 * math.pi,
    }
    for _ in range(32)
]

def gambar_bintang(waktu):
    bintang.clear()
    for s in daftar_bintang:
        terang = math.sin(waktu * 3 + s["fase"])
        if terang > -0.05:
            bintang.goto(s["x"], s["y"])
            warna = "#69BFFF" if terang > 0.65 else "#D2EEFF"
            bintang.dot(s["ukuran"] + (2 if terang > 0.65 else 0), warna)

# ==================================================
# HUJAN HATI KECIL
# ==================================================
daftar_hati = [
    {
        "x": random.randint(-480, 480),
        "y": random.randint(-390, 390),
        "v": random.uniform(1.2, 2.8),
        "ukuran": random.uniform(0.12, 0.22),
        "fase": random.random() * 2 * math.pi,
    }
    for _ in range(16)
]

def gambar_hati_kecil(x, y, ukuran):
    hujan.color("#78BDFF")
    titik = 14
    hujan.penup()
    for j in range(titik + 1):
        n = 2 * math.pi * j / titik
        hx, hy = corazon(n)
        pos = (x + hx * ukuran, y + hy * ukuran)
        if j == 0:
            hujan.goto(*pos)
            hujan.pendown()
        else:
            hujan.goto(*pos)
    hujan.penup()

def animasi_hujan(waktu):
    hujan.clear()
    for h in daftar_hati:
        gambar_hati_kecil(h["x"], h["y"], h["ukuran"])
        h["y"] -= h["v"]
        h["x"] += math.sin(waktu + h["fase"]) * 0.35
        if h["y"] < -410:
            h["y"] = 410
            h["x"] = random.randint(-480, 480)

# ==================================================
# TULISAN MUNCUL PER HURUF
# ==================================================
PESAN = "I Love You Forever"

def gambar_teks(jumlah):
    teks.clear()
    teks.goto(0, -345)
    teks.color("#087BFF")
    teks.write(PESAN[:jumlah], align="center", font=("Arial", 26, "bold"))

    if jumlah >= len(PESAN):
        teks.goto(0, -380)
        teks.color("#409EFF")
        teks.write("Forever & Always", align="center",
                   font=("Arial", 14, "italic"))

# ==================================================
# ANIMASI: HATI DIGAMBAR BERLAPIS, KEMUDIAN BERDETAK
# ==================================================
waktu = 0.0
frame = 0
jumlah_huruf = 0
JUMLAH_LAPISAN = 24
FASE_AWAL = 24  # sekitar 1,2 detik pertama untuk efek gambar masuk

def animasi():
    global waktu, frame, jumlah_huruf

    waktu += 0.12
    frame += 1

    # Awalnya lapisan bertambah satu per frame.
    # Setelah semua terbentuk, seluruh hati berdetak bersama.
    if frame <= FASE_AWAL:
        lapisan_aktif = max(1, int(JUMLAH_LAPISAN * frame / FASE_AWAL))
        detak = 1.0
    else:
        lapisan_aktif = JUMLAH_LAPISAN
        detak = 1 + 0.055 * math.sin(waktu * 2.5)

    neon.clear()

    # Gambar lapisan besar ke kecil supaya garis inti tampak jelas.
    for i in range(lapisan_aktif, 0, -1):
        scale = i * 0.88 * detak
        gambar_hati(neon, scale, "#BFEFFF", 4, 42)
        gambar_hati(neon, scale, "#087BFF", 1.5, 42)

    gambar_bintang(waktu)
    animasi_hujan(waktu)

    # Tampilkan tulisan perlahan setelah hati mulai terbentuk.
    if frame > FASE_AWAL and frame % 4 == 0:
        if jumlah_huruf < len(PESAN):
            jumlah_huruf += 1
    gambar_teks(jumlah_huruf)

    layar.update()
    layar.ontimer(animasi, 50)

animasi()
turtle.done()
