# ITBS - Scanline Melt
# Each scanline shifts horizontally based on audio, creating a melting TV effect
# Knob1: melt amount, Knob2: speed, Knob3: line thickness
# Knob4: foreground color, Knob5: background color
import pygame
import math
import random

phase = 0

def setup(screen, etc):
    pass

def draw(screen, etc):
    global phase
    w, h = screen.get_width(), screen.get_height()

    # Background color from palette
    etc.color_picker_bg(etc.knob5)

    phase += etc.knob2 * 0.08
    melt = etc.knob1 * 150 + 5
    thickness = int(etc.knob3 * 6) + 1
    peak = abs(etc.audio_peak) / 32768.0

    # Draw horizontal lines, each shifted by audio + sine wave
    line_step = thickness + 1
    for y in range(0, h, line_step):
        # Audio value for this scanline
        idx = int(y * 99 / h)
        audio_val = etc.audio_in[idx] / 32768.0

        # Horizontal offset: combination of audio and smooth wave
        wave = math.sin(y * 0.02 + phase) * melt * 0.3
        audio_shift = audio_val * melt
        offset = int(wave + audio_shift + peak * random.uniform(-20, 20))

        # Color varies per line
        t = (y / h + etc.knob4 + phase * 0.01) % 1.0
        color = etc.color_picker(t)

        # Draw the shifted line
        x_start = offset
        line_w = int(abs(audio_val) * w * 0.8 + w * 0.1)
        x_center = w // 2 + offset

        pygame.draw.line(screen, color,
                        (x_center - line_w // 2, y),
                        (x_center + line_w // 2, y),
                        thickness)

    # Occasional full-width interference
    if peak > 0.4:
        for _ in range(int(peak * 6)):
            iy = random.randint(0, h - 1)
            color = etc.color_picker(random.random())
            pygame.draw.line(screen, color, (0, iy), (w, iy), random.randint(1, 3))

    # Vertical color bars (subtle, CRT-like)
    if etc.knob1 > 0.5:
        bar_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        for x in range(0, w, 3):
            c = x % 3
            colors = [(20, 0, 0, 8), (0, 20, 0, 8), (0, 0, 20, 8)]
            pygame.draw.line(bar_surf, colors[c], (x, 0), (x, h), 1)
        screen.blit(bar_surf, (0, 0))
