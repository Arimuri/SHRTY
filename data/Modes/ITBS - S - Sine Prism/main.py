# ITBS - S - Sine Prism
# 複数のサイン波をプリズムのように色分解して重ねる
# Layered sine waves with prismatic color separation
#
# Knob1: 波の本数
# Knob2: 振幅
# Knob3: 周波数
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

    # Soft fade instead of full clear
    bg = etc.color_picker_bg(etc.knob5)
    fade = pygame.Surface((w, h), pygame.SRCALPHA)
    fade.fill((*bg, 40))
    screen.blit(fade, (0, 0))

    peak = abs(etc.audio_peak) / 32768.0
    phase += 0.03 + peak * 0.04

    layers = int(etc.knob1 * 5) + 3
    amp = etc.knob2 * 180 + 30
    freq = etc.knob3 * 4 + 1

    for layer in range(layers):
        lt = layer / layers
        # Each layer slightly offset in phase and vertical position
        y_center = h * (0.2 + lt * 0.6)
        phase_offset = lt * 1.2

        color = etc.color_picker((lt * 0.4 + etc.knob4) % 1.0)

        points = []
        step = 3
        for x in range(0, w + step, step):
            xt = x / w
            idx = min(int(xt * 99), 99)
            audio_val = etc.audio_in[idx] / 32768.0

            y = y_center
            y += math.sin(xt * freq * math.pi + phase + phase_offset) * amp * 0.4
            y += math.sin(xt * freq * 2.3 * math.pi + phase * 1.7 + phase_offset) * amp * 0.15
            y += audio_val * amp * 0.5
            points.append((x, int(y)))

        if len(points) > 1:
            # Glow
            glow_surf = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.lines(glow_surf, (*color, 25), False, points, 10)
            screen.blit(glow_surf, (0, 0))

            # Main line
            line_surf = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.lines(line_surf, (*color, 180), False, points, 2)
            screen.blit(line_surf, (0, 0))

            # Bright center dots at peaks
            for i in range(0, len(points), 20):
                px, py = points[i]
                pygame.draw.circle(screen, (255, 255, 255), (px, py), 2)
