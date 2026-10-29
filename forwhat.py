import turtle
import math
import random
import os
from PIL import Image

# Background putih
layar = turtle.Screen()
layar.setup(width=800, height=700)
layar.bgcolor("white")

# ==========================================
# 2. FOTO PNG TRANSPARAN DI TENGAH
# ==========================================

NAMA_FOTO = os.path.join("foto", "foto2.png")
NAMA_BG = os.path.join("album", "background.gif")

if not os.path.exists(NAMA_FOTO):
    raise FileNotFoundError(
        f"Foto tidak ditemukan: {NAMA_FOTO}"
    )

os.makedirs("album", exist_ok=True)

foto = Image.open(NAMA_FOTO).convert("RGBA")
foto.thumbnail((430, 390), Image.Resampling.LANCZOS)

# Gabungkan foto transparan dengan putih.
# Hasilnya hanya sebesar foto, bukan sebesar layar.
putih = Image.new("RGBA", foto.size, "white")
putih.alpha_composite(foto)
putih.convert("RGB").save(NAMA_BG, "GIF")

# Turtle menempatkan gambar background di tengah layar.
layar.bgpic(NAMA_BG)

# ==========================================
# 3. MUSIK ROMANTIS (OPSIONAL)
# ==========================================

musik_aktif = False

try:
    import pygame
    
    file_musik = "musik.mp3"


    if os.path.exists(file_musik):
        pygame.mixer.init()
        pygame.mixer.music.load(file_musik)
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(4)
        musik_aktif = True
        print("Musik sedang diputar.")
    else:
        print("File musik tidak ditemukan:", file_musik)

except Exception as e:
    print("Musik gagal diputar:", e)
    print("Pastikan pygame terpasang dan perangkat audio aktif.")

# ==========================================
# 4. FUNGSI BENTUK HATI
# ==========================================

def corazon(n):
    x = 20 * math.sin(n) ** 3
    y = (
        8 * math.cos(n)
        - 5 * math.cos(2 * n)
        - 2 * math.cos(3 * n)
        - math.cos(4 * n)
    )
    return x, y

# _________________________________________
t = turtle.Turtle()
t.speed(0)
t.color("blue")
t.pensize(2)

def corazon(n):
    x = 15 * math.sin(n) ** 3
    y = (10 * math.cos(n)
         - 5 * math.cos(2*n)
         - 2 * math.cos(3*n)
         - math.cos(4*n))
    return x, y

t.penup()

for i in range(1, 31):
    
    
    t.goto(0, 0)
    t.pendown()

    for n in range(0, 100, 2):
        x, y = corazon(n / 10)
        t.goto(x * i, y * i)

    t.penup()
    t.goto(0, 0)



# ==========================================
# ANIMASI HUJAN LOVE KECIL ❤️
# ==========================================

layar.tracer(0)

# Turtle khusus untuk hujan love
hujan = turtle.Turtle()
hujan.hideturtle()
hujan.penup()
hujan.speed(0)

# Daftar warna love
warna_love = [
    "red", "pink", "hot pink",
    "magenta", "deeppink", "light pink"
]

# Membuat banyak love kecil
love = []

for i in range(35):
    x = random.randint(-390, 390)
    y = random.randint(-340, 340)
    ukuran = random.uniform(0.4, 1.0)
    warna = random.choice(warna_love)
    kecepatan = random.uniform(2, 6)

    love.append([x, y, ukuran, warna, kecepatan])


def gambar_love(x, y, ukuran, warna):
    """Menggambar simbol love kecil."""
    hujan.goto(x, y)
    hujan.color(warna)
    hujan.write(
        "♥",
        align="center",
        font=("Arial", max(8, int(16 * ukuran)), "normal")
    )


def animasi_hujan():
    hujan.clear()

    for item in love:
        x, y, ukuran, warna, kecepatan = item

        # Gambar love
        gambar_love(x, y, ukuran, warna)

        # Gerakkan love ke bawah
        item[1] -= kecepatan

        # Jika keluar layar, muncul lagi dari atas
        if item[1] < -350:
            item[0] = random.randint(-390, 390)
            item[1] = random.randint(350, 500)
            item[2] = random.uniform(0.4, 1.0)
            item[3] = random.choice(warna_love)
            item[4] = random.uniform(2, 6)

    layar.update()

    # Ulangi animasi
    layar.ontimer(animasi_hujan, 40)


# Mulai hujan love
animasi_hujan()

t.hideturtle()
turtle.done()




