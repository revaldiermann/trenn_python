from __future__ import annotations

import math
import random
import sys
import pygame

# ============================================================
# LOVE IN MOTION — upgraded Pygame animation
# Controls: SPACE = particle burst | click = burst at cursor
#          R = restart animation | ESC = quit
# Edit these settings to personalize the animation.
# ============================================================
WIDTH, HEIGHT = 1280, 800
FPS = 60
CAPTION = "Love in Motion ♥"
MESSAGE = "I Love You"
SUBMESSAGE = "you make my world brighter"
BACKGROUND = (8, 5, 18)
# Dua tema bergantian: merah neon -> biru neon.
RED_THEME = {
    "accent": (255, 45, 105),
    "hot": (255, 20, 55),
    "soft": (255, 145, 180),
    "pale": (255, 225, 238),
    "ambient": (90, 10, 55),
    "petals": ((255, 65, 125), (255, 120, 165), (210, 35, 90)),
}
BLUE_THEME = {
    "accent": (45, 135, 255),
    "hot": (20, 75, 255),
    "soft": (125, 205, 255),
    "pale": (220, 245, 255),
    "ambient": (8, 35, 105),
    "petals": ((55, 130, 255), (100, 190, 255), (35, 75, 210)),
}

# Waktu tiap warna dan durasi perpindahan warna, dalam detik.
THEME_HOLD_SECONDS = 6.0
THEME_TRANSITION_SECONDS = 1.8

THEME = RED_THEME
PINK = RED_THEME["accent"]
HOT_PINK = RED_THEME["hot"]
SOFT_PINK = RED_THEME["soft"]
WHITE_PINK = RED_THEME["pale"]


def blend_color(a: tuple[int, int, int], b: tuple[int, int, int], amount: float):
    amount = clamp(amount, 0.0, 1.0)
    return tuple(int(a[i] + (b[i] - a[i]) * amount) for i in range(3))


def update_theme(time_value: float) -> None:
    """Beralih halus dari merah ke biru, lalu kembali ke merah berulang."""
    global THEME, PINK, HOT_PINK, SOFT_PINK, WHITE_PINK
    cycle = THEME_HOLD_SECONDS + THEME_TRANSITION_SECONDS
    phase = time_value % (cycle * 2)

    if phase < THEME_HOLD_SECONDS:
        red_amount = 0.0
    elif phase < cycle:
        red_amount = (phase - THEME_HOLD_SECONDS) / THEME_TRANSITION_SECONDS
    elif phase < cycle + THEME_HOLD_SECONDS:
        red_amount = 1.0
    else:
        red_amount = 1.0 - (phase - cycle - THEME_HOLD_SECONDS) / THEME_TRANSITION_SECONDS

    # red_amount 0 = merah, 1 = biru.
    THEME = {
        "accent": blend_color(RED_THEME["accent"], BLUE_THEME["accent"], red_amount),
        "hot": blend_color(RED_THEME["hot"], BLUE_THEME["hot"], red_amount),
        "soft": blend_color(RED_THEME["soft"], BLUE_THEME["soft"], red_amount),
        "pale": blend_color(RED_THEME["pale"], BLUE_THEME["pale"], red_amount),
        "ambient": blend_color(RED_THEME["ambient"], BLUE_THEME["ambient"], red_amount),
        "petals": tuple(
            blend_color(RED_THEME["petals"][i], BLUE_THEME["petals"][i], red_amount)
            for i in range(3)
        ),
    }
    PINK = THEME["accent"]
    HOT_PINK = THEME["hot"]
    SOFT_PINK = THEME["soft"]
    WHITE_PINK = THEME["pale"]


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def heart_point(t: float, scale: float, center: tuple[float, float], pulse: float = 1.0) -> tuple[float, float]:
    x = 16 * math.sin(t) ** 3
    y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
    return center[0] + x * scale * pulse, center[1] - y * scale * pulse


def make_heart_points(count: int, scale: float, center: tuple[float, float], pulse: float = 1.0):
    return [heart_point(i * math.tau / count, scale, center, pulse) for i in range(count)]


def draw_glow_circle(surface: pygame.Surface, pos: tuple[float, float], radius: int,
                      color: tuple[int, int, int], alpha: int = 255) -> None:
    x, y = int(pos[0]), int(pos[1])
    for extra, a in ((radius * 4, 12), (radius * 2.5, 22), (radius * 1.5, 45)):
        r = max(1, int(extra))
        glow = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*color, min(alpha, a)), (r + 1, r + 1), r)
        surface.blit(glow, (x - r - 1, y - r - 1), special_flags=pygame.BLEND_ADD)
    pygame.draw.circle(surface, (*color, alpha), (x, y), max(1, radius))


class Star:
    def __init__(self):
        self.x = random.randrange(WIDTH)
        self.y = random.randrange(HEIGHT)
        self.radius = random.choice((1, 1, 1, 2))
        self.phase = random.random() * math.tau
        self.speed = random.uniform(0.018, 0.055)

    def draw(self, surface: pygame.Surface, time_value: float):
        glow = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(time_value * self.speed * 60 + self.phase))
        color = (int(100 + 100 * glow), int(65 + 100 * glow), int(130 + 110 * glow))
        pygame.draw.circle(surface, color, (self.x, self.y), self.radius)


class Particle:
    def __init__(self, x: float, y: float, burst: bool = False):
        self.x, self.y = x, y
        angle = random.uniform(0, math.tau)
        speed = random.uniform(1.0, 6.0) if burst else random.uniform(0.2, 1.3)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed - (random.uniform(0.2, 2.0) if not burst else 0)
        self.life = random.randint(35, 95) if burst else random.randint(100, 230)
        self.max_life = self.life
        self.size = random.choice((2, 2, 3, 4))
        self.color = random.choice((PINK, HOT_PINK, SOFT_PINK, WHITE_PINK))
        self.phase = random.random() * math.tau

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.99
        self.vy *= 0.99
        self.life -= 1

    def draw(self, surface: pygame.Surface, time_value: float):
        if self.life <= 0:
            return
        alpha = int(255 * clamp(self.life / self.max_life, 0, 1))
        r = max(1, int(self.size * (0.7 + 0.3 * math.sin(time_value * 5 + self.phase))))
        pygame.draw.circle(surface, (*blend_color(self.color, THEME["accent"], 0.72), alpha), (int(self.x), int(self.y)), r)


class Petal:
    def __init__(self, from_top: bool = True):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(-HEIGHT, 0) if from_top else random.uniform(0, HEIGHT)
        self.speed = random.uniform(0.6, 2.0)
        self.drift = random.uniform(-0.7, 0.7)
        self.size = random.randint(5, 10)
        self.rotation = random.uniform(0, 360)
        self.spin = random.uniform(-2, 2)
        self.color = random.choice(THEME["petals"])

    def update(self):
        self.y += self.speed
        self.x += self.drift + math.sin(self.y * 0.012) * 0.7
        self.rotation += self.spin
        if self.y > HEIGHT + 20:
            self.__init__(True)
            self.y = random.uniform(-80, -10)

    def draw(self, surface: pygame.Surface):
        petal = pygame.Surface((self.size * 3, self.size * 3), pygame.SRCALPHA)
        pygame.draw.ellipse(petal, (*random.choice(THEME["petals"]), 155), (self.size // 2, self.size, self.size * 2, self.size))
        rotated = pygame.transform.rotate(petal, self.rotation)
        surface.blit(rotated, rotated.get_rect(center=(int(self.x), int(self.y))))


def draw_text_glow(surface: pygame.Surface, font: pygame.font.Font, text: str,
                   color: tuple[int, int, int], center: tuple[int, int], glow_color=PINK):
    base = font.render(text, True, color)
    glow = font.render(text, True, glow_color)
    for offset, alpha in ((8, 18), (4, 35), (2, 60)):
        layer = glow.copy()
        layer.set_alpha(alpha)
        rect = layer.get_rect(center=center)
        for dx, dy in ((offset, 0), (-offset, 0), (0, offset), (0, -offset)):
            surface.blit(layer, rect.move(dx, dy), special_flags=pygame.BLEND_ADD)
    surface.blit(base, base.get_rect(center=center))


def main():
    pygame.init()
    pygame.display.set_caption(CAPTION)
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("georgia", 58, bold=True)
    subtitle_font = pygame.font.SysFont("arial", 22)
    hint_font = pygame.font.SysFont("arial", 15)

    stars = [Star() for _ in range(150)]
    particles: list[Particle] = []
    petals = [Petal() for _ in range(28)]
    frame = 0
    heart_reveal = 0.0
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0
        frame += 1
        time_value = frame / FPS
        update_theme(time_value)
        width, height = screen.get_size()
        center = (width / 2, height / 2 - 20)
        scale = min(width / 48, height / 43) * 0.78
        pulse = 1.0 + 0.035 * math.sin(time_value * 2.8)
        heart_reveal = min(1.0, heart_reveal + dt * 0.55)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    for _ in range(120):
                        particles.append(Particle(center[0], center[1], burst=True))
                elif event.key == pygame.K_r:
                    particles.clear()
                    heart_reveal = 0.0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for _ in range(55):
                    particles.append(Particle(mx, my, burst=True))

        screen.fill(BACKGROUND)
        # Soft ambient background gradient
        ambient = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.circle(ambient, (*THEME["ambient"], 42), (int(center[0]), int(center[1])), int(min(width, height) * 0.46))
        screen.blit(ambient, (0, 0))

        for star in stars:
            star.draw(screen, time_value)
        for petal in petals:
            petal.update()
            petal.draw(screen)

        # Draw the heart progressively, with luminous dots and connecting lines.
        points = make_heart_points(190, scale, center, pulse)
        visible_count = max(2, int(len(points) * heart_reveal))
        visible = points[:visible_count]
        if len(visible) > 1:
            line_layer = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.lines(line_layer, (*THEME["accent"], 100), False, [(int(x), int(y)) for x, y in visible], 2)
            screen.blit(line_layer, (0, 0), special_flags=pygame.BLEND_ADD)
            for i, point in enumerate(visible):
                if i % 2 == 0:
                    draw_glow_circle(screen, point, 2 if i % 5 else 3, random.choice((PINK, HOT_PINK, SOFT_PINK)), 230)

        # Tiny floating heart symbols
        for i in range(12):
            orbit = time_value * 0.35 + i * math.tau / 12
            radius = scale * 1.6
            x = center[0] + math.cos(orbit) * radius
            y = center[1] + math.sin(orbit * 1.2) * radius * 0.58
            symbol = subtitle_font.render("♥", True, THEME["soft"])
            symbol.set_alpha(80 + int(70 * (0.5 + 0.5 * math.sin(time_value * 2 + i))))
            screen.blit(symbol, symbol.get_rect(center=(int(x), int(y))))

        # Main message and subtitle
        text_y = int(center[1] + scale * 0.28)
        draw_text_glow(screen, title_font, MESSAGE, WHITE_PINK, (int(center[0]), text_y))
        subtitle = subtitle_font.render(SUBMESSAGE, True, THEME["soft"])
        subtitle.set_alpha(210)
        screen.blit(subtitle, subtitle.get_rect(center=(int(center[0]), text_y + 48)))

        # Update and draw particles on top of the scene.
        particles = [p for p in particles if p.life > 0]
        for particle in particles:
            particle.update()
            particle.draw(screen, time_value)
        if len(particles) > 700:
            particles = particles[-700:]

        hint = hint_font.render("RED ♥ BLUE NEON   •   SPACE: particle explosion   •   CLICK: sparkle   •   R: restart   •   ESC: exit", True, THEME["soft"])
        screen.blit(hint, hint.get_rect(center=(width // 2, height - 28)))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
