# ITBS - T - Star Burst
# Stars/particles burst from center on beat, trails create kaleidoscope patterns
# Knob1: burst force, Knob2: star count, Knob3: trail length
# Knob4: foreground color, Knob5: background color
import pygame
import random
import math

stars = []
prev_peak = 0

def setup(screen, etc):
    global stars
    stars = []

def draw(screen, etc):
    global stars, prev_peak
    w, h = screen.get_width(), screen.get_height()
    cx, cy = w // 2, h // 2

    # Trail fade
    trail = int((1.0 - etc.knob3) * 50) + 3
    bg = etc.color_picker_bg(etc.knob5)
    fade = pygame.Surface((w, h), pygame.SRCALPHA)
    fade.fill((*bg, trail))
    screen.blit(fade, (0, 0))

    peak = abs(etc.audio_peak) / 32768.0
    onset = peak - prev_peak
    prev_peak = peak

    force = etc.knob1 * 20 + 5
    burst_count = int(etc.knob2 * 15) + 5

    # Burst on beat
    if onset > 0.06:
        for _ in range(burst_count):
            angle = random.uniform(0, math.pi * 2)
            speed = force * random.uniform(0.3, 1.0) * (0.5 + onset * 3)
            stars.append({
                'x': float(cx),
                'y': float(cy),
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'size': random.uniform(2, 6),
                'color_t': (etc.knob4 + random.uniform(-0.1, 0.1)) % 1.0,
                'life': random.randint(20, 60),
                'age': 0,
                'points': random.choice([4, 5, 6, 8]),
            })

    while len(stars) > 500:
        stars.pop(0)

    alive = []
    for s in stars:
        s['x'] += s['vx']
        s['y'] += s['vy']
        s['vx'] *= 0.97
        s['vy'] *= 0.97
        s['age'] += 1

        if s['age'] < s['life']:
            fade_t = 1.0 - s['age'] / s['life']
            color = etc.color_picker(s['color_t'])
            alpha = int(255 * fade_t)
            sz = s['size'] * (1 + (1 - fade_t) * 0.5)
            ix, iy = int(s['x']), int(s['y'])

            if 0 <= ix < w and 0 <= iy < h:
                # Draw star shape
                pts = s['points']
                star_pts = []
                for p in range(pts * 2):
                    a = p * math.pi / pts + s['age'] * 0.1
                    r = sz if p % 2 == 0 else sz * 0.4
                    star_pts.append((int(ix + math.cos(a) * r), int(iy + math.sin(a) * r)))

                if len(star_pts) >= 3:
                    star_surf = pygame.Surface((int(sz * 3), int(sz * 3)), pygame.SRCALPHA)
                    offset_pts = [(int(p[0] - ix + sz * 1.5), int(p[1] - iy + sz * 1.5)) for p in star_pts]
                    try:
                        pygame.draw.polygon(star_surf, (*color, alpha), offset_pts)
                        screen.blit(star_surf, (int(ix - sz * 1.5), int(iy - sz * 1.5)))
                    except:
                        pass

                alive.append(s)

    stars = alive

    # Center glow
    if peak > 0.1:
        glow_r = int(30 + peak * 50)
        glow = pygame.Surface((glow_r * 4, glow_r * 4), pygame.SRCALPHA)
        color = etc.color_picker(etc.knob4)
        pygame.draw.circle(glow, (*color, int(peak * 40)), (glow_r * 2, glow_r * 2), glow_r * 2)
        pygame.draw.circle(glow, (255, 255, 255, int(peak * 60)), (glow_r * 2, glow_r * 2), glow_r)
        screen.blit(glow, (cx - glow_r * 2, cy - glow_r * 2))
