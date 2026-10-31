import turtle
import math
import random
import os
from PIL import Image, ImageDraw

# =========================================================
# PENGATURAN
# =========================================================
LEBAR, TINGGI = 800, 700
NAMA_FOTO = os.path.join("foto", "foto2.png")
NAMA_BG = os.path.join("album", "background.gif")
FILE_MUSIK = "musik.mp3"

if not os.path.exists(NAMA_FOTO):
    raise FileNotFoundError(
        f"Foto tidak ditemukan: {NAMA_FOTO}\n"
        "Simpan foto PNG kamu di folder 'foto' dengan nama 'foto2.png'."
    )

os.makedirs("album", exist_ok=True)

# =========================================================
# FUNGSI HATI MATEMATIKA - BAGIAN UTAMA PROGRAM
# =========================================================
def corazon(n):
    """Menghasilkan koordinat bentuk hati dari rumus matematika."""
    x = 15 * math.sin(n) ** 3
    y = (
        10 * math.cos(n)
        - 5 * math.cos(2 * n)
        - 2 * math.cos(3 * n)
        - math.cos(4 * n)
    )
    return x, y


def titik_hati(cx, cy, skala, jumlah=100):
    """Mengubah rumus corazon menjadi titik-titik di layar."""
    titik = []
    for i in range(jumlah + 1):
        n = (2 * math.pi * i) / jumlah
        x, y = corazon(n)
        titik.append((cx + x * skala, cy + y * skala))
    return titik


# =========================================================
# MEMBUAT BACKGROUND: HATI BESAR DI BELAKANG FOTO
# =========================================================
kanvas = Image.new("RGBA", (LEBAR, TINGGI), (255, 255, 255, 255))
gambar = ImageDraw.Draw(kanvas)


def gambar_hati_pil(draw, cx, cy, skala, warna, lebar_garis=3):
    pts = []
    for i in range(181):
        n = (2 * math.pi * i) / 180
        x, y = corazon(n)
        # Konversi koordinat Turtle (y ke atas) ke koordinat gambar (y ke bawah)
        pts.append((cx + x * skala, cy - y * skala))
    draw.line(pts, fill=warna, width=lebar_garis, joint="curve")


# Hati besar dekoratif di kiri dan kanan; semuanya berada di belakang foto.
for cx, cy, skala in [
    (100, 350, 4.8),
    (700, 350, 4.8),
    (105, 130, 2.8),
    (695, 565, 2.8),
]:
    gambar_hati_pil(gambar, cx, cy, skala, (40, 150, 255, 255), 5)
    gambar_hati_pil(gambar, cx, cy, skala * 0.88, (90, 220, 255, 255), 2)

# Foto tetap di tengah. Transparansi PNG dipertahankan agar hati di belakang
# bisa terlihat pada bagian foto yang transparan.
foto = Image.open(NAMA_FOTO).convert("RGBA")
foto.thumbnail((430, 390), Image.Resampling.LANCZOS)
pos_foto = ((LEBAR - foto.width) // 2, (TINGGI - foto.height) // 2)
kanvas.alpha_composite(foto, pos_foto)

# GIF untuk Turtle.
kanvas.convert("RGB").save(NAMA_BG, "GIF")

# =========================================================
# LAYAR TURTLE
# =========================================================
layar = turtle.Screen()
layar.setup(width=LEBAR, height=TINGGI)
layar.title("Love Animation")
layar.bgcolor("white")
layar.bgpic(NAMA_BG)
layar.tracer(0)

# =========================================================
# MUSIK OPSIONAL
# =========================================================
musik_aktif = False
try:
    import pygame
    if os.path.exists(FILE_MUSIK):
        pygame.mixer.init()
        pygame.mixer.music.load(FILE_MUSIK)
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1)
        musik_aktif = True
        print("Musik sedang diputar.")
    else:
        print("Musik tidak ditemukan; animasi tetap berjalan tanpa musik.")
except Exception as e:
    print("Musik tidak dapat diputar:", e)

# =========================================================
# HATI UTAMA BIRU - MENGGUNAKAN corazon(n)
# =========================================================
hati_utama = turtle.Turtle(visible=False)
hati_utama.speed(0)
hati_utama.pensize(2)
hati_utama.color("#087cff")
hati_utama.penup()

# Gambar beberapa lapisan hati dari rumus corazon.
# Skala dibatasi agar bentuk hati tetap terlihat di area layar.
for skala in range(1, 19):
    hati_utama.penup()
    hati_utama.goto(0, 0)
    hati_utama.pendown()
    for i in range(101):
        n = (2 * math.pi * i) / 100
        x, y = corazon(n)
        hati_utama.goto(x * skala * 0.72, y * skala * 0.72)
    hati_utama.penup()

layar.update()

# =========================================================
# HUJAN CINTA NEON
# =========================================================
hujan = turtle.Turtle(visible=False)
hujan.speed(0)
hujan.penup()
hujan_colors = ["#ff3cac", "#ff5eae", "#00d9ff", "#7d5fff", "#ff80bf"]
partikel = []

for _ in range(42):
    partikel.append({
        "x": random.randint(-380, 380),
        "y": random.randint(-330, 330),
        "speed": random.uniform(2.0, 5.5),
        "size": random.randint(8, 17),
        "color": random.choice(hujan_colors),
    })

# Animasi hujan cinta sebentar, lalu lanjut ke hati balon.
for frame in range(100):
    hujan.clear()
    for p in partikel:
        hujan.goto(p["x"], p["y"])
        hujan.color(p["color"])
        hujan.write("♥", align="center", font=("Arial", p["size"], "bold"))
        p["y"] -= p["speed"]
        if p["y"] < -350:
            p["y"] = random.randint(330, 420)
            p["x"] = random.randint(-380, 380)
    layar.update()
    layar.delay(25)

hujan.clear()
hati_utama.clear()
layar.update()

# =========================================================
# HATI BIRU BERCAHAYA BERGERAK NAIK SEPERTI BALON
# Bentuknya juga dibuat memakai fungsi corazon(n).
# Animasi ditempatkan di sisi layar agar foto tidak tertutup.
# =========================================================
anim = turtle.Turtle(visible=False)
anim.speed(0)
anim.penup()
anim.pensize(2)

balon = []
for i in range(14):
    sisi = random.choice([-1, 1])
    balon.append({
        "x": sisi * random.uniform(275, 365),
        "y": random.uniform(-370, 350),
        "skala": random.uniform(0.85, 1.45),
        "speed": random.uniform(0.7, 1.8),
        "fase": random.uniform(0, 2 * math.pi),
    })


def gambar_hati_turtle(t, cx, cy, skala, warna, lebar=2):
    pts = titik_hati(cx, cy, skala, 90)
    t.penup()
    t.goto(pts[0])
    t.pencolor(warna)
    t.pensize(lebar)
    t.pendown()
    for titik in pts[1:]:
        t.goto(titik)
    t.penup()


for frame in range(650):
    anim.clear()
    for b in balon:
        # Hati naik seperti balon dengan gerakan mendatar yang lembut.
        b["y"] += b["speed"]
        b["fase"] += 0.035
        x = b["x"] + math.sin(b["fase"]) * 10
        y = b["y"]
        if y > 390:
            b["y"] = random.uniform(-390, -300)
            b["x"] = random.choice([-1, 1]) * random.uniform(275, 365)
            b["skala"] = random.uniform(0.85, 1.45)

        s = b["skala"]
        # Beberapa lapisan warna memberi kesan neon/glow.
        gambar_hati_turtle(anim, x, y, s * 1.22, "#063fba", 5)
        gambar_hati_turtle(anim, x, y, s * 1.08, "#087cff", 3)
        gambar_hati_turtle(anim, x, y, s, "#70eaff", 1)

    layar.update()
    layar.delay(20)

# =========================================================
# PENUTUP
# =========================================================
if musik_aktif:
    try:
        import pygame
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except Exception:
        pass

layar.mainloop()
