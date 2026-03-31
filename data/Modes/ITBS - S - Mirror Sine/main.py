# ITBS - S - Mirror Sine
# 上下左右ミラーのサイン波が万華鏡のようなシンメトリーを作る
# Mirrored sine waves create kaleidoscopic symmetry
#
# Knob1: 波の本数
# Knob2: 振幅
# Knob3: 速度
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
    hw, hh = w // 2, h // 2

    bg = etc.color_picker_bg(etc.knob5)
    fade = pygame.Surface((w, h), pygame.SRCALPHA)
    fade.fill((*bg, 30))
    screen.blit(fade, (0, 0))

    peak = abs(etc.audio_peak) / 32768.0
    phase += etc.knob3 * 0.07 + 0.015

    wave_count = int(etc.knob1 * 6) + 2
    amp = etc.knob2 * 150 + 20

    # Draw on quarter, then mirror
    quarter = pygame.Surface((hw, hh), pygame.SRCALPHA)

    for wave in range(wave_count):
        wt = wave / wave_count
        color = etc.color_picker((wt * 0.35 + etc.knob4) % 1.0)

        points = []
        step = 3
        for x in range(0, hw + step, step):
            xt = x / hw
            idx = min(int(xt * 50 + wt * 49), 99)
            audio_val = etc.audio_in[idx] / 32768.0

            y_base = hh * (0.2 + wt * 0.6)
            y = y_base
            y += math.sin(xt * (2 + wt * 3) * math.pi + phase * (1 + wt * 0.5)) * amp * 0.3
            y += audio_val * amp * 0.5

            y = max(0, min(hh - 1, y))
            points.append((x, int(y)))

        if len(points) > 1:
            # Glow
            glow = pygame.Surface((hw, hh), pygame.SRCALPHA)
            pygame.draw.lines(glow, (*color, 30), False, points, 8)
            quarter.blit(glow, (0, 0))

            # Line
            line = pygame.Surface((hw, hh), pygame.SRCALPHA)
            pygame.draw.lines(line, (*color, 200), False, points, 2)
            quarter.blit(line, (0, 0))

    # Blit 4-way mirror
    # Top-left: original
    screen.blit(quarter, (0, 0))

    # Top-right: flipped horizontal
    flipped_h = pygame.transform.flip(quarter, True, False)
    screen.blit(flipped_h, (hw, 0))

    # Bottom-left: flipped vertical
    flipped_v = pygame.transform.flip(quarter, False, True)
    screen.blit(flipped_v, (0, hh))

    # Bottom-right: flipped both
    flipped_hv = pygame.transform.flip(quarter, True, True)
    screen.blit(flipped_hv, (hw, hh))

    # Center crosshair
    alpha = int(40 + peak * 60)
    color_c = etc.color_picker(etc.knob4)
    ch_surf = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.line(ch_surf, (*color_c, alpha), (hw, 0), (hw, h), 1)
    pygame.draw.line(ch_surf, (*color_c, alpha), (0, hh), (w, hh), 1)
    screen.blit(ch_surf, (0, 0))
