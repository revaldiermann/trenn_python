import turtle
import math
import random
import os
from PIL import Image, ImageDraw, ImageFilter

# Background putih
layar = turtle.Screen()
layar.setup(width=800, height=700)
layar.bgcolor("white")

# ==========================================
# 2. FOTO PNG TRANSPARAN DI TENGAH
# ==========================================

NAMA_FOTO = os.path.join("foto", "foto3.png")
NAMA_BG = os.path.join("album", "background.gif")

if not os.path.exists(NAMA_FOTO):
    raise FileNotFoundError(f"Foto tidak ditemukan: {NAMA_FOTO}")

os.makedirs("album", exist_ok=True)

foto = Image.open(NAMA_FOTO).convert("RGBA")
resample_method = getattr(Image, 'Resampling', Image).LANCZOS
foto.thumbnail((430, 390), resample_method)

putih = Image.new("RGBA", foto.size, "white")
putih.alpha_composite(foto)
putih.convert("RGB").save(NAMA_BG, "GIF")

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
    x = 15 * math.sin(n) ** 3
    y = (10 * math.cos(n) - 5 * math.cos(2*n) - 2 * math.cos(3*n) - math.cos(4*n))
    return x, y

t = turtle.Turtle()
t.speed(0)
t.penup()

warna_gradient = ["#FF1493", "#FF69B4", "#FFB6C1", "#FFC0CB", "#FF69B4"]

for i in range(1, 31):
    t.goto(0, 0)
    t.pendown()
    warna_idx = i % len(warna_gradient)
    t.color(warna_gradient[warna_idx])
    t.pensize(max(1, 3 - i // 10))

    for n in range(0, 100, 2):
        x, y = corazon(n / 10)
        t.goto(x * i, y * i)

    t.penup()
    t.goto(0, 0)

# ==========================================
# EFEK SPARKLE DI SEKITAR HATI
# ==========================================

sparkle = turtle.Turtle()
sparkle.hideturtle()
sparkle.speed(0)
sparkle.penup()

def gambar_sparkle(x, y, ukuran):
    sparkle.goto(x, y)
    sparkle.color(random.choice(["#FFD700", "#FFA500", "#FFFF00", "#FFFFFF"]))
    sparkle.write("✦", align="center", font=("Arial", int(8 * ukuran), "normal"))

def animasi_sparkle():
    sparkle.clear()
    for _ in range(15):
        sudut = random.uniform(0, 2 * math.pi)
        jarak = random.uniform(200, 350)
        x = jarak * math.cos(sudut)
        y = jarak * math.sin(sudut)
        ukuran = random.uniform(0.5, 1.5)
        gambar_sparkle(x, y, ukuran)
    layar.ontimer(animasi_sparkle, 300)

# ==========================================
# BALON FOTO & EFEK MELETUP (DIPERCEPAT & 98%)
# ==========================================

os.makedirs("album/balon", exist_ok=True)

daftar_foto_balon = []
for nama in ["foto6.png","foto1.png", "foto2.png", "foto3.png", "foto4.png", "foto5.png"]:
    path = os.path.join("foto", nama)
    if os.path.exists(path):
        daftar_foto_balon.append(path)

if not daftar_foto_balon:
    daftar_foto_balon = [NAMA_FOTO]

warna_balon = ["#FF69B4", "#FF1493", "#FFB6C1", "#FFC0CB", "#FF6347", "#FF7F50", "#FFA07A", "#E6E6FA", "#DDA0DD", "#EE82EE"]

def buat_balon_foto(path_foto, warna, nama_output):
    try:
        lebar_balon, tinggi_balon, tali_panjang = 100, 120, 40
        lebar_total, tinggi_total = lebar_balon + 20, tinggi_balon + tali_panjang + 20
        
        balon = Image.new("RGBA", (lebar_total, tinggi_total), (255, 255, 255, 0))
        draw = ImageDraw.Draw(balon)
        cx, cy = lebar_total // 2, tinggi_balon // 2 + 10
        
        draw.ellipse([cx - lebar_balon//2, cy - tinggi_balon//2, cx + lebar_balon//2, cy + tinggi_balon//2], fill=warna, outline="#FFFFFF", width=2)
        draw.ellipse([cx - 20, cy - 30, cx - 5, cy - 15], fill=(255, 255, 255, 180)) # Kilau
        draw.polygon([(cx - 5, cy + tinggi_balon//2 - 2), (cx + 5, cy + tinggi_balon//2 - 2), (cx, cy + tinggi_balon//2 + 5)], fill=warna)
        
        for i in range(tali_panjang):
            y_tali = cy + tinggi_balon // 2 + 5 + i
            x_tali = cx + int(3 * math.sin(i / 4))
            draw.point((x_tali, y_tali), fill="#888888")
            draw.point((x_tali + 1, y_tali), fill="#888888")
        
        foto = Image.open(path_foto).convert("RGBA").resize((50, 50), resample_method)
        mask = Image.new("L", (50, 50), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, 50, 50], fill=255)
        
        fx, fy = cx - 25, cy - 25
        balon.paste(foto, (fx, fy), mask)
        draw.ellipse([fx - 2, fy - 2, fx + 52, fy + 52], outline="#FFFFFF", width=2)
        
        balon.save(nama_output, "GIF")
        return nama_output
    except Exception as e:
        print(f"❌ Gagal membuat balon: {e}")
        return None

def buat_foto_pop(path_foto, nama_output):
    """Membuat versi foto yang lebih besar dengan efek glow untuk saat meletup."""
    try:
        ukuran = 150
        pop_img = Image.new("RGBA", (ukuran, ukuran), (255, 255, 255, 0))
        
        foto = Image.open(path_foto).convert("RGBA").resize((130, 130), resample_method)
        
        mask = Image.new("L", (130, 130), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, 130, 130], fill=255)
        
        pop_img.paste(foto, (10, 10), mask)
        
        draw = ImageDraw.Draw(pop_img)
        draw.ellipse([8, 8, 142, 142], outline="#FFFFFF", width=4)
        draw.ellipse([5, 5, 145, 145], outline="#FFB6C1", width=2) # Glow halus
        
        pop_img.save(nama_output, "GIF")
        return nama_output
    except Exception as e:
        print(f"❌ Gagal membuat foto pop: {e}")
        return None

balon_shapes = []
pop_shapes = []

for idx, path_foto in enumerate(daftar_foto_balon):
    warna = warna_balon[idx % len(warna_balon)]
    
    nama_gif = os.path.join("album", "balon", f"balon_{idx}.gif")
    hasil_gif = buat_balon_foto(path_foto, warna, nama_gif)
    if hasil_gif and os.path.exists(hasil_gif):
        layar.register_shape(hasil_gif)
        balon_shapes.append(hasil_gif)
        
    nama_pop = os.path.join("album", "balon", f"pop_{idx}.gif")
    hasil_pop = buat_foto_pop(path_foto, nama_pop)
    if hasil_pop and os.path.exists(hasil_pop):
        layar.register_shape(hasil_pop)
        pop_shapes.append(hasil_pop)

# Fallback jika hanya ada 1 foto
if len(balon_shapes) == 1:
    for i in range(1, 5):
        warna = warna_balon[i % len(warna_balon)]
        nama_gif = os.path.join("album", "balon", f"balon_extra_{i}.gif")
        hasil_gif = buat_balon_foto(daftar_foto_balon[0], warna, nama_gif)
        if hasil_gif and os.path.exists(hasil_gif):
            layar.register_shape(hasil_gif)
            balon_shapes.append(hasil_gif)
            
        nama_pop = os.path.join("album", "balon", f"pop_extra_{i}.gif")
        hasil_pop = buat_foto_pop(daftar_foto_balon[0], nama_pop)
        if hasil_pop and os.path.exists(hasil_pop):
            layar.register_shape(hasil_pop)
            pop_shapes.append(hasil_pop)

if not balon_shapes:
    balon_shapes = ["circle"]
    pop_shapes = ["circle"]

# ==========================================
# LOGIKA ANIMASI BALON & MELETUP (DIPERCEPAT)
# ==========================================

ledakan_t = turtle.Turtle()
ledakan_t.hideturtle()
ledakan_t.penup()
ledakan_t.speed(0)

jumlah_balon = 6
balon_data = []

for i in range(jumlah_balon):
    bt = turtle.Turtle()
    bt.hideturtle()
    bt.penup()
    bt.speed(0)
    
    shape_idx = i % len(balon_shapes)
    bt.shape(balon_shapes[shape_idx])
    
    x_awal = random.randint(-350, 350)
    y_awal = random.randint(-600, -300) - i * 80
    bt.goto(x_awal, y_awal)
    bt.showturtle()
    
    # Struktur data: [turtle, x, y, kecepatan, phase, amp, shape_idx, state, pop_timer]
    balon_data.append([
        bt, x_awal, y_awal,
        random.uniform(1.5, 3.0), # Kecepatan sedikit dinaikkan agar lebih dinamis
        random.uniform(0, 2 * math.pi),
        random.uniform(0.3, 0.8),
        shape_idx,
        0,  # state: 0 = melayang, 1 = meletup
        0   # pop_timer
    ])

def gambar_ledakan(x, y, frame):
    """Menggambar efek ledakan kembang api mini yang lebih cepat dan snappy."""
    ledakan_t.clear()
    
    # DURASI DIPERCEPAT: Hanya 15 frame (sekitar 0.45 detik)
    if frame < 15:
        # Transisi warna lebih cepat sesuai beat
        if frame < 5:
            warna = "#FFD700" # Emas terang
            tebal = 3
        elif frame < 10:
            warna = "#FF1493" # Deep pink
            tebal = 2
        else:
            warna = "#FFB6C1" # Light pink (memudar)
            tebal = 1
            
        ledakan_t.color(warna)
        ledakan_t.pensize(tebal)
        
        # Perhitungan panjang yang lebih eksplosif tapi cepat
        if frame < 8:
            panjang = frame * 3.5 # Fase ekspansi cepat
        else:
            panjang = (15 - frame) * 3.5 # Fase memudar cepat
            
        for i in range(8):
            sudut = (i * 45) + (frame * 5) # Rotasi lebih cepat
            rad = math.radians(sudut)
            x1 = x + math.cos(rad) * (panjang * 0.2)
            y1 = y + math.sin(rad) * (panjang * 0.2)
            x2 = x + math.cos(rad) * panjang
            y2 = y + math.sin(rad) * panjang
            
            ledakan_t.penup()
            ledakan_t.goto(x1, y1)
            ledakan_t.pendown()
            ledakan_t.goto(x2, y2)
        ledakan_t.penup()

def animasi_balon():
    for data in balon_data:
        bt, x, y, kecepatan, phase, amp, shape_idx, state, pop_timer = data
        
        if state == 0: # Melayang normal
            y += kecepatan
            phase += 0.08 # Goyangan sedikit lebih cepat
            
            x_baru = x + amp * math.sin(phase)
            x = x_baru
            
            # Cek apakah sudah di atas layar
            if y > 400: # Ambang batas sedikit diturunkan agar lebih sering terpicu
                # PERUBAHAN: Peluang meletup 98%
                if random.random() < 0.98 and len(pop_shapes) > 0:
                    state = 1
                    pop_timer = 0
                    bt.shape(pop_shapes[shape_idx]) # Tampilkan foto pop
                else:
                    # 2% sisa: reset normal tanpa meletup
                    y = random.uniform(-500, -400)
                    x = random.randint(-350, 350)
                    kecepatan = random.uniform(1.5, 3.0)
                    phase = random.uniform(0, 2 * math.pi)
                    amp = random.uniform(0.3, 0.8)
                    bt.shape(balon_shapes[shape_idx])
                    
        elif state == 1: # Sedang meletup
            pop_timer += 1
            gambar_ledakan(x, y, pop_timer)
            
            # PERUBAHAN: Reset lebih cepat (15 frame = ~0.45 detik)
            if pop_timer > 15:
                state = 0
                pop_timer = 0
                y = random.uniform(-500, -400)
                x = random.randint(-350, 350)
                kecepatan = random.uniform(1.5, 3.0)
                phase = random.uniform(0, 2 * math.pi)
                amp = random.uniform(0.3, 0.8)
                bt.shape(balon_shapes[shape_idx]) # Kembalikan ke balon normal
                ledakan_t.clear() # Bersihkan sisa ledakan segera
        
        # Update data dan posisi turtle
        data[1] = x
        data[2] = y
        data[3] = kecepatan
        data[4] = phase
        data[5] = amp
        data[7] = state
        data[8] = pop_timer
        
        bt.goto(x, y)
    
    layar.ontimer(animasi_balon, 30)

# ==========================================
# ANIMASI HUJAN LOVE KECIL ❤️
# ==========================================

layar.tracer(0)

hujan = turtle.Turtle()
hujan.hideturtle()
hujan.penup()
hujan.speed(0)

warna_love = ["red", "pink", "hot pink", "magenta", "deeppink", "light pink"]
love = []

for i in range(35):
    x = random.randint(-390, 390)
    y = random.randint(-340, 340)
    ukuran = random.uniform(0.4, 1.0)
    warna = random.choice(warna_love)
    kecepatan = random.uniform(2, 6)
    love.append([x, y, ukuran, warna, kecepatan])

def gambar_love(x, y, ukuran, warna):
    hujan.goto(x + 1, y - 1)
    hujan.color("gray")
    hujan.write("♥", align="center", font=("Arial", max(8, int(16 * ukuran)), "normal"))
    
    hujan.goto(x, y)
    hujan.color(warna)
    hujan.write("♥", align="center", font=("Arial", max(8, int(16 * ukuran)), "normal"))

def animasi_hujan():
    hujan.clear()
    for item in love:
        x, y, ukuran, warna, kecepatan = item
        gambar_love(x, y, ukuran, warna)
        item[1] -= kecepatan
        
        if item[1] < -350:
            item[0] = random.randint(-390, 390)
            item[1] = random.randint(350, 500)
            item[2] = random.uniform(0.4, 1.0)
            item[3] = random.choice(warna_love)
            item[4] = random.uniform(2, 6)

    layar.update()
    layar.ontimer(animasi_hujan, 40)

# ==========================================
# TEKS & FRAME DEKORATIF
# ==========================================

teks_turtle = turtle.Turtle()
teks_turtle.hideturtle()
teks_turtle.penup()
teks_turtle.speed(0)
teks_turtle.goto(0, -320)
teks_turtle.color("#FF1493")
teks_turtle.write("💕 Forever & Always 💕", align="center", font=("Arial", 20, "bold"))

frame = turtle.Turtle()
frame.hideturtle()
frame.speed(0)
frame.penup()
frame.color("#FFB6C1")
frame.pensize(3)

sudut_pos = [(-380, 330), (380, 330), (-380, -330), (380, -330)]
for x, y in sudut_pos:
    frame.goto(x, y)
    frame.write("♥", align="center", font=("Arial", 24, "normal"))

# Mulai semua animasi
animasi_sparkle()
animasi_balon()
animasi_hujan()

t.hideturtle()
turtle.done()
