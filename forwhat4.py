import turtle
import math
import random
import os
import time
from PIL import Image, ImageDraw, ImageFilter

# =========================================================
# 1. PENGATURAN AWAL & DIREKTORI
# =========================================================
LEBAR, TINGGI = 900, 750
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
# 2. FUNGSI MATEMATIKA & BENTUK HATI
# =========================================================
def corazon(n):
    """Rumus matematika kurva bentuk hati yang presisi."""
    x = 16 * math.sin(n) ** 3
    y = (
        13 * math.cos(n)
        - 5 * math.cos(2 * n)
        - 2 * math.cos(3 * n)
        - math.cos(4 * n)
    )
    return x, y

def titik_hati(cx, cy, skala, jumlah=120):
    """Menghasilkan susunan koordinat titik hati."""
    titik = []
    for i in range(jumlah + 1):
        n = (2 * math.pi * i) / jumlah
        x, y = corazon(n)
        titik.append((cx + x * skala, cy + y * skala))
    return titik

# =========================================================
# 3. PEMBUATAN CANVAS BACKGROUND PRO (PIL)
# =========================================================
def buat_background_estetis():
    kanvas = Image.new("RGBA", (LEBAR, TINGGI), (10, 14, 26, 255))
    draw = ImageDraw.Draw(kanvas)

    # A. Efek Gradasi Latar Belakang Sinematik
    for y in range(TINGGI):
        r = int(8 + (28 - 8) * (y / TINGGI))
        g = int(12 + (18 - 12) * (y / TINGGI))
        b = int(24 + (55 - 24) * (y / TINGGI))
        draw.line([(0, y), (LEBAR, y)], fill=(r, g, b, 255))

    # B. Bintang & Partikel Bokeh Cahaya Halus
    random.seed(42)
    for _ in range(140):
        sx = random.randint(0, LEBAR)
        sy = random.randint(0, TINGGI)
        s_size = random.randint(1, 4)
        opacity = random.randint(80, 230)
        draw.ellipse([sx, sy, sx + s_size, sy + s_size], fill=(180, 220, 255, opacity))

    # C. Buka & Potong Foto menjadi Berbentuk Hati
    foto = Image.open(NAMA_FOTO).convert("RGBA")
    foto_size = 360
    foto = foto.resize((foto_size, foto_size), Image.Resampling.LANCZOS)

    mask = Image.new("L", (foto_size, foto_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    pts_mask = []
    cx_f, cy_f = foto_size // 2, foto_size // 2
    for i in range(180):
        n = (2 * math.pi * i) / 180
        x, y = corazon(n)
        pts_mask.append((cx_f + x * 9.5, cy_f - y * 9.5))
    mask_draw.polygon(pts_mask, fill=255)

    foto_hati = Image.new("RGBA", (foto_size, foto_size), (0, 0, 0, 0))
    foto_hati.paste(foto, (0, 0), mask)

    # D. Multi-Layer Neon Ambient Glow di Belakang Foto
    glow_layer = Image.new("RGBA", (LEBAR, TINGGI), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    cx_p, cy_p = LEBAR // 2, TINGGI // 2 - 20

    lapisan_glow = [
        (35, 30, (0, 140, 255)),
        (22, 60, (0, 210, 255)),
        (12, 110, (255, 60, 180)),
        (4, 180, (255, 255, 255))
    ]
    for r_extra, alpha, warna in lapisan_glow:
        pts_glow = []
        for i in range(180):
            n = (2 * math.pi * i) / 180
            x, y = corazon(n)
            pts_glow.append((cx_p + x * (9.5 + r_extra / 15), cy_p - y * (9.5 + r_extra / 15)))
        glow_draw.polygon(pts_glow, outline=warna + (alpha,), width=4)

    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(10))
    kanvas.alpha_composite(glow_layer)

    pos_x = cx_p - foto_size // 2
    pos_y = cy_p - foto_size // 2
    kanvas.alpha_composite(foto_hati, (pos_x, pos_y))

    kanvas.convert("RGB").save(NAMA_BG, "GIF")

buat_background_estetis()

# =========================================================
# 4. INISIALISASI TURTLE SCREEN
# =========================================================
layar = turtle.Screen()
layar.setup(width=LEBAR, height=TINGGI)
layar.title("✨ Special Love Music Sync Animation ✨")
layar.bgcolor("#0a0e1a")
layar.bgpic(NAMA_BG)
layar.tracer(0)

# =========================================================
# 5. INTEGRASI MUSIK DENGAN FADE-IN LEBIH LAMBUT
# =========================================================
durasi_musik = 30
musik_aktif = False

try:
    import pygame
    if os.path.exists(FILE_MUSIK):
        pygame.mixer.init()
        pygame.mixer.music.load(FILE_MUSIK)
        pygame.mixer.music.set_volume(0.8)
        
        sound_info = pygame.mixer.Sound(FILE_MUSIK)
        durasi_musik = int(sound_info.get_length())
        
        pygame.mixer.music.play(-1, fade_ms=3500)
        musik_aktif = True
        print(f"🎵 Musik dimainkan dengan efek Smooth Fade-in. Durasi: {durasi_musik} detik.")
    else:
        print("⚠️ File musik tidak ditemukan; Animasi tetap berjalan.")
except Exception as e:
    print("⚠️ Modul Pygame/Audio tidak aktif:", e)

# =========================================================
# 6. DRAWER HELPERS
# =========================================================
def menggambar_hati(t, cx, cy, skala, warna, lebar=2):
    pts = titik_hati(cx, cy, skala, jumlah=100)
    t.penup()
    t.goto(pts[0])
    t.pencolor(warna)
    t.pensize(lebar)
    t.pendown()
    for titik in pts[1:]:
        t.goto(titik)
    t.penup()

pen_teks = turtle.Turtle(visible=False)
pen_teks.speed(0)
pen_teks.penup()

def tampilkan_teks_glow(pesan, y_pos=-310, warna="#70eaff", intensitas_glow=False):
    pen_teks.clear()
    # Bayangan / Glow Latar Teks
    pen_teks.goto(2, y_pos - 2)
    pen_teks.color("#041c32")
    pen_teks.write(pesan, align="center", font=("Poppins", 16, "bold"))
    
    if intensitas_glow:
        pen_teks.goto(0, y_pos)
        pen_teks.color("#ff3cac")
        pen_teks.write(pesan, align="center", font=("Poppins", 16, "bold"))

    pen_teks.goto(0, y_pos)
    pen_teks.color(warna)
    pen_teks.write(pesan, align="center", font=("Poppins", 16, "bold"))

pen_intro = turtle.Turtle(visible=False)
pen_intro.speed(0)

# =========================================================
# 7. TRANSISI MASUK CINEMATIC & CINEMATIC HEART BLOOM
# =========================================================
def jalankan_transisi_masuk_halus():
    """Efek transisi masuk yang lebih lama, sinematik, dan lembut tanpa gerakan kaku."""
    total_frame = 90  # Berjalan sekitar ~3.5 detik
    
    for i in range(1, total_frame + 1):
        pen_intro.clear()
        progress = i / total_frame
        
        # Fungsi Ease-Out Quad untuk pergerakan halus melambat secara alami
        ease_out = 1 - (1 - progress) * (1 - progress)
        
        # A. Mekar Hati Utama dengan Warna Bertahap (Neon Expansion)
        skala_pembuka = ease_out * 11.5
        if skala_pembuka > 0.1:
            menggambar_hati(pen_intro, 0, 20, skala_pembuka * 1.05, "#0055ff", lebar=4)
            menggambar_hati(pen_intro, 0, 20, skala_pembuka, "#00f0ff", lebar=2)
            if skala_pembuka > 2.0:
                menggambar_hati(pen_intro, 0, 20, skala_pembuka * 0.82, "#ff3cac", lebar=1)

        layar.update()
        time.sleep(0.035)
        
    pen_intro.clear()
    layar.update()

# Jalankan transisi awal sinematik
jalankan_transisi_masuk_halus()

# =========================================================
# 8. INISIALISASI ELEMEN UTAMA
# =========================================================
pen_anim = turtle.Turtle(visible=False)
pen_anim.speed(0)

hujan_colors = ["#ff3cac", "#ff5eae", "#00d9ff", "#7d5fff", "#ff80bf", "#ffffff"]
partikel = []
for _ in range(50):
    partikel.append({
        "x": random.randint(-420, 420),
        "y": random.randint(-350, 380),
        "speed": random.uniform(2.0, 5.0),
        "size": random.randint(10, 20),
        "color": random.choice(hujan_colors),
        "char": random.choice(["♥", "❣", "✦", "✧"])
    })

balon = []
for i in range(16):
    sisi = random.choice([-1, 1])
    balon.append({
        "x": sisi * random.uniform(280, 400),
        "y": random.uniform(-380, 350),
        "skala": random.uniform(0.7, 1.3),
        "speed": random.uniform(1.0, 2.2),
        "fase": random.uniform(0, 2 * math.pi),
        "color_glow": random.choice(["#00d9ff", "#ff3cac", "#7d5fff"])
    })

kembang_api = []
def pemicu_kembang_api():
    cx = random.choice([-320, 320])
    cy = random.randint(-100, 250)
    for _ in range(18):
        sudut = random.uniform(0, 2 * math.pi)
        kecepatan = random.uniform(2, 6.5)
        kembang_api.append({
            "x": cx, "y": cy,
            "vx": math.cos(sudut) * kecepatan,
            "vy": math.sin(sudut) * kecepatan,
            "life": 1.0,
            "color": random.choice(["#00f0ff", "#ff007f", "#ffe600", "#ffffff"])
        })

# =========================================================
# 9. MAIN LOOP ANIMASI PRO
# =========================================================
waktu_mulai = time.time()
frame = 0

tampilkan_teks_glow("✨ Always In My Heart ✨", y_pos=-310, warna="#70eaff")

while True:
    waktu_berjalan = time.time() - waktu_mulai
    
    if waktu_berjalan >= durasi_musik + 3:
        break
        
    pen_anim.clear()
    frame += 1

    # --- A. Efek Beat / Multi-Layer Pulsing Neon Aura ---
    bpm_tempo = math.sin(waktu_berjalan * 4.2)
    skala_denyut = 10.0 + (bpm_tempo * 0.4)
    
    # Layering Denyut Neon Bertingkat
    menggambar_hati(pen_anim, 0, 20, skala_denyut * 1.06, "#0044aa", lebar=3)
    menggambar_hati(pen_anim, 0, 20, skala_denyut, "#00f0ff", lebar=2)
    menggambar_hati(pen_anim, 0, 20, skala_denyut * 0.94, "#ffffff", lebar=1)

    # Efek Pendar Teks Berdenyut Lembut
    if frame % 20 == 0:
        tampilkan_teks_glow("✨ Always In My Heart ✨", y_pos=-310, warna="#70eaff", intensitas_glow=(bpm_tempo > 0.5))

    # --- B. Animasi Partikel Hujan Cinta ---
    for p in partikel:
        pen_anim.goto(p["x"], p["y"])
        pen_anim.color(p["color"])
        pen_anim.write(p["char"], align="center", font=("Arial", p["size"], "bold"))
        p["y"] -= p["speed"]
        if p["y"] < -370:
            p["y"] = random.randint(360, 420)
            p["x"] = random.randint(-420, 420)

    # --- C. Animasi Balon Hati Neon Pro (Double Glow Stroke) ---
    for b in balon:
        b["y"] += b["speed"]
        b["fase"] += 0.035
        # Pergerakan melayang berayun yang lebih alami
        x = b["x"] + math.sin(b["fase"]) * 12 + math.cos(b["fase"] * 0.5) * 4
        y = b["y"]
        if y > 390:
            b["y"] = random.uniform(-390, -320)
            b["x"] = random.choice([-1, 1]) * random.uniform(280, 400)

        s = b["skala"]
        menggambar_hati(pen_anim, x, y, s * 1.20, "#041c32", lebar=5)
        menggambar_hati(pen_anim, x, y, s * 1.05, b["color_glow"], lebar=3)
        menggambar_hati(pen_anim, x, y, s * 0.88, "#ffffff", lebar=1)

    # --- D. Animasi Letupan Kembang Api dengan Spark Trails ---
    if frame % 45 == 0:
        pemicu_kembang_api()

    for ka in kembang_api[:]:
        ka["x"] += ka["vx"]
        ka["y"] += ka["vy"]
        ka["vy"] -= 0.08  # Efek gravitasi halus pada kembang api
        ka["life"] -= 0.032
        if ka["life"] <= 0:
            kembang_api.remove(ka)
        else:
            pen_anim.goto(ka["x"], ka["y"])
            pen_anim.color(ka["color"])
            ukuran_dot = int(ka["life"] * 7) + 1
            pen_anim.dot(ukuran_dot)

    layar.update()
    time.sleep(0.02)

# =========================================================
# 10. SELESAI & PENUTUP WITH FADE OUT
# =========================================================
tampilkan_teks_glow("❤️ Terima Kasih Telah Hadir ❤️", y_pos=-310, warna="#ff5eae")
layar.update()

if musik_aktif:
    try:
        pygame.mixer.music.fadeout(3000)
        time.sleep(3.0)
        pygame.mixer.quit()
    except Exception:
        pass

layar.mainloop()
