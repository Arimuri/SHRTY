# ITBS - S - Arc Reactor
# 円弧が重なり合い、オーディオで弧の長さと半径が変化する
# Overlapping arcs pulse with audio — Tony Stark meets electronic music
#
# Knob1: 弧の数
# Knob2: 太さ
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
    cx, cy = w // 2, h // 2

    bg = etc.color_picker_bg(etc.knob5)
    fade = pygame.Surface((w, h), pygame.SRCALPHA)
    fade.fill((*bg, 40))
    screen.blit(fade, (0, 0))

    peak = abs(etc.audio_peak) / 32768.0
    phase += etc.knob3 * 0.08 + 0.01

    arc_count = int(etc.knob1 * 12) + 4
    thickness = int(etc.knob2 * 10) + 2
    max_r = min(w, h) * 0.44

    for i in range(arc_count):
        t = i / arc_count

        # Audio sample
        idx = min(int(t * 99), 99)
        audio_val = abs(etc.audio_in[idx]) / 32768.0

        # Radius: layered outward
        r = 20 + t * (max_r - 20)

        # Arc sweep angle driven by audio
        sweep = 0.3 + audio_val * 2.5
        sweep = min(sweep, math.pi * 1.8)

        # Start angle: rotating, each arc offset
        start = phase * (1.3 - t * 0.6) + t * math.pi * 2 / 3

        color = etc.color_picker((t * 0.35 + etc.knob4) % 1.0)

        # Draw arc as polyline
        segments = int(sweep * 15) + 8
        points = []
        for s in range(segments + 1):
            a = start + (s / segments) * sweep
            px = cx + math.cos(a) * r
            py = cy + math.sin(a) * r
            points.append((int(px), int(py)))

        if len(points) > 1:
            alpha = int(80 + audio_val * 175)
            arc_surf = pygame.Surface((w, h), pygame.SRCALPHA)

            # Glow
            pygame.draw.lines(arc_surf, (*color, alpha // 3), False, points, thickness + 6)
            screen.blit(arc_surf, (0, 0))

            # Main arc
            arc_surf2 = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.lines(arc_surf2, (*color, alpha), False, points, thickness)
            screen.blit(arc_surf2, (0, 0))

            # End caps
            for pt in [points[0], points[-1]]:
                pygame.draw.circle(screen, (255, 255, 255), pt, thickness // 2 + 1)

    # Center core
    core_r = int(8 + peak * 15)
    core_color = etc.color_picker(etc.knob4)
    pygame.draw.circle(screen, core_color, (cx, cy), core_r)
    pygame.draw.circle(screen, (255, 255, 255), (cx, cy), max(2, core_r - 4))
