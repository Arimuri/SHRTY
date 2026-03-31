# ITBS - S - Helix Spin
# 二重螺旋がオーディオで膨張・収縮しながら回転する
# Double helix rotates and breathes with audio — DNA meets techno
#
# Knob1: 巻き数
# Knob2: 半径
# Knob3: 回転速度
# Knob4: foreground color
# Knob5: background color

import pygame
import math

phase = 0

def setup(screen, etc):
    pass

def draw(screen, etc):
    global phase
    w, h = screen.get_width(), screen.get_height()
    cx = w // 2

    bg = etc.color_picker_bg(etc.knob5)
    fade = pygame.Surface((w, h), pygame.SRCALPHA)
    fade.fill((*bg, 35))
    screen.blit(fade, (0, 0))

    peak = abs(etc.audio_peak) / 32768.0
    phase += etc.knob3 * 0.08 + 0.015

    coils = etc.knob1 * 6 + 2
    base_r = etc.knob2 * 180 + 40

    margin = 40
    segments = 120

    points_a = []
    points_b = []
    rungs = []

    for i in range(segments + 1):
        t = i / segments
        y = margin + t * (h - margin * 2)

        # Audio modulation
        idx = min(int(t * 99), 99)
        audio_val = etc.audio_in[idx] / 32768.0

        # Radius pulsing with audio
        r = base_r * (0.5 + abs(audio_val) * 0.8)

        # Helix angle
        angle = t * coils * math.pi * 2 + phase

        # Two strands, 180 degrees apart
        x_a = cx + math.cos(angle) * r
        x_b = cx + math.cos(angle + math.pi) * r

        points_a.append((int(x_a), int(y)))
        points_b.append((int(x_b), int(y)))

        # Rungs connecting the two strands
        if i % 6 == 0:
            # Only draw rungs when strands are "facing us" (cos > 0 for depth)
            depth = math.cos(angle)
            if abs(depth) > 0.3:
                rungs.append((points_a[-1], points_b[-1], t, abs(depth)))

    color_a = etc.color_picker(etc.knob4)
    color_b = etc.color_picker((etc.knob4 + 0.3) % 1.0)

    # Draw rungs first (behind)
    for pa, pb, t, depth in rungs:
        alpha = int(40 + depth * 120)
        rung_color = etc.color_picker((t * 0.2 + etc.knob4 + 0.15) % 1.0)
        rung_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.line(rung_surf, (*rung_color, alpha), pa, pb, 2)
        screen.blit(rung_surf, (0, 0))

    # Strand A
    if len(points_a) > 1:
        glow_a = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.lines(glow_a, (*color_a, 30), False, points_a, 8)
        screen.blit(glow_a, (0, 0))
        pygame.draw.lines(screen, color_a, False, points_a, 3)

    # Strand B
    if len(points_b) > 1:
        glow_b = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.lines(glow_b, (*color_b, 30), False, points_b, 8)
        screen.blit(glow_b, (0, 0))
        pygame.draw.lines(screen, color_b, False, points_b, 3)
