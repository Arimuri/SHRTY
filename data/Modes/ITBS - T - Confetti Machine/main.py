# ITBS - T - Confetti Machine
# ビートでミニマルな幾何学コンフェティが舞う
# Geometric confetti bursts on beat — clean, playful, celebratory
#
# Knob1: パーティクル数
# Knob2: サイズ
# Knob3: 重力
# Knob4: foreground color
# Knob5: background color

import pygame
import random
import math

particles = []
prev_peak = 0

SHAPES = ['rect', 'circle', 'tri', 'diamond']

def setup(screen, etc):
    global particles
    particles = []

def draw(screen, etc):
    global particles, prev_peak
    w, h = screen.get_width(), screen.get_height()

    etc.color_picker_bg(etc.knob5)

    peak = abs(etc.audio_peak) / 32768.0
    onset = peak - prev_peak
    prev_peak = peak

    count = int(etc.knob1 * 20) + 5
    base_size = etc.knob2 * 15 + 4
    gravity = etc.knob3 * 0.4 + 0.05

    # Burst on beat
    if onset > 0.05:
        spawn = int(count * min(onset * 5, 1.0))
        for _ in range(spawn):
            # Spawn from random top positions
            sx = random.uniform(w * 0.1, w * 0.9)
            sy = random.uniform(-20, h * 0.3)
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 8) * (0.5 + onset * 3)

            particles.append({
                'x': sx,
                'y': sy,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed - 3,
                'size': base_size * random.uniform(0.5, 1.5),
                'shape': random.choice(SHAPES),
                'angle': random.uniform(0, math.pi * 2),
                'spin': random.uniform(-0.15, 0.15),
                'color_t': (etc.knob4 + random.uniform(-0.2, 0.2)) % 1.0,
                'life': random.randint(80, 160),
                'age': 0,
            })

    while len(particles) > 400:
        particles.pop(0)

    alive = []
    for p in particles:
        p['vy'] += gravity
        p['vx'] *= 0.995
        p['x'] += p['vx']
        p['y'] += p['vy']
        p['angle'] += p['spin']
        p['age'] += 1

        # Gentle flutter
        p['x'] += math.sin(p['age'] * 0.08 + p['angle']) * 0.8

        if p['age'] < p['life'] and p['y'] < h + 20:
            fade = 1.0 if p['age'] < p['life'] - 30 else (p['life'] - p['age']) / 30.0
            color = etc.color_picker(p['color_t'])
            alpha = int(230 * fade)
            sz = int(p['size'])

            if sz < 2:
                alive.append(p)
                continue

            surf = pygame.Surface((sz * 3, sz * 3), pygame.SRCALPHA)
            center = sz * 3 // 2

            if p['shape'] == 'rect':
                # Rotated rectangle
                hw, hh = sz, int(sz * 0.6)
                a = p['angle']
                corners = []
                for dx, dy in [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]:
                    rx = dx * math.cos(a) - dy * math.sin(a)
                    ry = dx * math.sin(a) + dy * math.cos(a)
                    corners.append((int(center + rx), int(center + ry)))
                pygame.draw.polygon(surf, (*color, alpha), corners)

            elif p['shape'] == 'circle':
                pygame.draw.circle(surf, (*color, alpha), (center, center), sz)

            elif p['shape'] == 'tri':
                a = p['angle']
                pts = []
                for i in range(3):
                    ta = a + i * math.pi * 2 / 3
                    pts.append((int(center + math.cos(ta) * sz), int(center + math.sin(ta) * sz)))
                pygame.draw.polygon(surf, (*color, alpha), pts)

            elif p['shape'] == 'diamond':
                a = p['angle']
                pts = []
                for i in range(4):
                    ta = a + i * math.pi * 0.5
                    r = sz if i % 2 == 0 else sz * 0.5
                    pts.append((int(center + math.cos(ta) * r), int(center + math.sin(ta) * r)))
                pygame.draw.polygon(surf, (*color, alpha), pts)

            screen.blit(surf, (int(p['x']) - center, int(p['y']) - center))
            alive.append(p)

    particles = alive
