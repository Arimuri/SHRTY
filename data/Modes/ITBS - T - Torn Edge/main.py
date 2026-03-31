# ITBS - Torn Edge
# iytm-inspired gradient sky with torn paper boundaries that breathe with audio
# Knob1: boundary position, Knob2: roughness, Knob3: particle density
# Knob4: foreground color, Knob5: background color
import pygame
import random
import math

particles = []

def setup(screen, etc):
    global particles
    particles = []

def draw(screen, etc):
    global particles
    w, h = screen.get_width(), screen.get_height()

    # Gradient background (blue sky → pale)
    bg_col = etc.color_picker_bg(etc.knob5)

    # Top color (deep blue)
    r1, g1, b1 = 10, 45, 175
    # Mid color (cyan)
    r2, g2, b2 = 0, 170, 225
    # Bottom color (pale)
    r3, g3, b3 = 210, 208, 220

    for y in range(0, h, 3):
        t = y / h
        if t < 0.4:
            lt = t / 0.4
            r = int(r1 + (r2 - r1) * lt)
            g = int(g1 + (g2 - g1) * lt)
            b = int(b1 + (b2 - b1) * lt)
        else:
            lt = (t - 0.4) / 0.6
            r = int(r2 + (r3 - r2) * lt)
            g = int(g2 + (g3 - g2) * lt)
            b = int(b2 + (b3 - b2) * lt)
        pygame.draw.line(screen, (r, g, b), (0, y), (w, y))
        pygame.draw.line(screen, (r, g, b), (0, y + 1), (w, y + 1))
        pygame.draw.line(screen, (r, g, b), (0, y + 2), (w, y + 2))

    # Torn edge boundary — breathes with audio
    peak = abs(etc.audio_peak) / 32768.0
    boundary_y = etc.knob1 * h
    roughness = etc.knob2 * 60 + 10
    t_val = etc.frame_count * 0.01

    # Scatter dots along boundary (torn paper effect)
    count = int(etc.knob3 * 300) + 50
    for i in range(count):
        x = random.random() * w
        # Perlin-like variation using sin combinations
        noise_val = (math.sin(x * 0.01 + t_val) * 0.5 +
                     math.sin(x * 0.003 + t_val * 0.7) * 0.3 +
                     math.sin(x * 0.02 + t_val * 1.3) * 0.2)
        breath = peak * 40
        oy = random.gauss(0, roughness) + noise_val * roughness * 0.5 + math.sin(t_val) * breath
        y = boundary_y + oy

        # Color transition across boundary
        tt = max(0, min(1, (oy + roughness * 2) / (roughness * 4)))
        cr = int(0 + 210 * tt)
        cg = int(170 - 40 * tt)
        cb = int(225 - 25 * tt)
        alpha = random.randint(100, 240)
        sz = random.uniform(1.5, 4.0)

        dot_surf = pygame.Surface((int(sz * 2), int(sz * 2)), pygame.SRCALPHA)
        pygame.draw.circle(dot_surf, (cr, cg, cb, alpha), (int(sz), int(sz)), int(sz))
        screen.blit(dot_surf, (int(x - sz), int(y - sz)))

    # Floating particles
    density = int(etc.knob3 * 5) + 1
    for _ in range(density):
        particles.append({
            'x': random.random() * w,
            'y': random.random() * h,
            'vy': random.uniform(-0.5, -0.1),
            'size': random.uniform(1, 2.5),
            'alpha': random.randint(30, 80),
            'life': random.randint(60, 200),
            'age': 0,
        })

    while len(particles) > 400:
        particles.pop(0)

    alive = []
    for p in particles:
        p['y'] += p['vy'] * (1 + peak * 2)
        p['age'] += 1
        if p['age'] < p['life'] and p['y'] > 0:
            fade = math.sin(p['age'] / p['life'] * math.pi)
            a = int(p['alpha'] * fade)
            color = etc.color_picker(etc.knob4)
            ps = pygame.Surface((int(p['size'] * 2 + 1), int(p['size'] * 2 + 1)), pygame.SRCALPHA)
            pygame.draw.circle(ps, (*color, a), (int(p['size']), int(p['size'])), int(p['size']))
            screen.blit(ps, (int(p['x']), int(p['y'])))
            alive.append(p)
    particles = alive
