# ITBS - S - Strobe Cut
# Hard geometric shapes flash and cut on beat, high contrast
# Knob1: shape count, Knob2: max size, Knob3: rotation speed
# Knob4: foreground color, Knob5: background color
import pygame
import random
import math

shapes = []
prev_peak = 0
frame_flash = 0

def setup(screen, etc):
    global shapes
    shapes = []

def draw(screen, etc):
    global shapes, prev_peak, frame_flash
    w, h = screen.get_width(), screen.get_height()

    etc.color_picker_bg(etc.knob5)

    peak = abs(etc.audio_peak) / 32768.0
    onset = peak - prev_peak
    prev_peak = peak

    count = int(etc.knob1 * 8) + 2
    max_size = int(etc.knob2 * 300) + 50
    rot_speed = etc.knob3 * 0.15

    # Spawn shapes on beat
    if onset > 0.07:
        frame_flash = 3
        for _ in range(count):
            kind = random.choice(['rect', 'tri', 'line', 'circle'])
            shapes.append({
                'kind': kind,
                'x': random.randint(0, w),
                'y': random.randint(0, h),
                'size': random.randint(30, max_size),
                'angle': random.uniform(0, math.pi * 2),
                'color_t': (etc.knob4 + random.uniform(-0.15, 0.15)) % 1.0,
                'life': random.randint(4, 15),
                'age': 0,
            })

    while len(shapes) > 80:
        shapes.pop(0)

    # Flash
    if frame_flash > 0:
        flash_alpha = frame_flash * 25
        flash = pygame.Surface((w, h), pygame.SRCALPHA)
        flash.fill((255, 255, 255, flash_alpha))
        screen.blit(flash, (0, 0))
        frame_flash -= 1

    alive = []
    for s in shapes:
        s['age'] += 1
        s['angle'] += rot_speed
        if s['age'] < s['life']:
            alpha = int(255 * (1 - s['age'] / s['life']))
            color = etc.color_picker(s['color_t'])
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            cx, cy = s['x'], s['y']
            sz = s['size']
            a = s['angle']

            if s['kind'] == 'rect':
                # Rotated rect via polygon
                corners = []
                for da in [0.25, 0.75, 1.25, 1.75]:
                    px = cx + math.cos(a + da * math.pi) * sz * 0.7
                    py = cy + math.sin(a + da * math.pi) * sz * 0.5
                    corners.append((int(px), int(py)))
                pygame.draw.polygon(surf, (*color, alpha), corners)
            elif s['kind'] == 'tri':
                pts = []
                for i in range(3):
                    px = cx + math.cos(a + i * math.pi * 2 / 3) * sz * 0.6
                    py = cy + math.sin(a + i * math.pi * 2 / 3) * sz * 0.6
                    pts.append((int(px), int(py)))
                pygame.draw.polygon(surf, (*color, alpha), pts)
            elif s['kind'] == 'circle':
                pygame.draw.circle(surf, (*color, alpha), (cx, cy), sz // 2, 4)
            elif s['kind'] == 'line':
                x1 = cx + math.cos(a) * sz
                y1 = cy + math.sin(a) * sz
                x2 = cx - math.cos(a) * sz
                y2 = cy - math.sin(a) * sz
                pygame.draw.line(surf, (*color, alpha), (int(x1), int(y1)), (int(x2), int(y2)), 5)

            screen.blit(surf, (0, 0))
            alive.append(s)

    shapes = alive
