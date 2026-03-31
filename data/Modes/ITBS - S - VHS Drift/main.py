# ITBS - VHS Drift
# Lo-fi VHS aesthetic: scanlines, chromatic aberration, film grain, color drift
# Knob1: scanline intensity, Knob2: chroma shift, Knob3: grain amount
# Knob4: foreground color, Knob5: background color
import pygame
import random
import math

scanline_offset = 0

def setup(screen, etc):
    pass

def draw(screen, etc):
    global scanline_offset
    w, h = screen.get_width(), screen.get_height()

    # Background color from palette
    etc.color_picker_bg(etc.knob5)

    peak = abs(etc.audio_peak) / 32768.0

    # Audio waveform with chromatic aberration
    chroma = int(etc.knob2 * 15 + peak * 10)
    points_r = []
    points_g = []
    points_b = []
    for x in range(0, w, 3):
        idx = int(x * 99 / w)
        val = etc.audio_in[idx] / 32768.0
        y_base = h // 2 + int(val * h * 0.35)
        points_r.append((x - chroma, y_base))
        points_g.append((x, y_base))
        points_b.append((x + chroma, y_base))

    # Foreground color from palette
    color = etc.color_picker(etc.knob4)
    r, g, b = color

    if len(points_r) > 1:
        pygame.draw.lines(screen, (r, 0, 0), False, points_r, 2)
        pygame.draw.lines(screen, (0, g, 0), False, points_g, 2)
        pygame.draw.lines(screen, (0, 0, b), False, points_b, 2)

    # Scanlines
    scanline_offset = (scanline_offset + 0.5 + peak * 3) % 4
    scan_alpha = int(etc.knob1 * 40) + 10
    for y in range(int(scanline_offset), h, 4):
        pygame.draw.line(screen, (0, 0, 0), (0, y), (w, y), 1)

    # Interference lines on beat
    if peak > 0.3:
        for _ in range(int(peak * 4)):
            iy = random.randint(0, h - 1)
            ih = random.randint(1, int(3 + peak * 8))
            pygame.draw.rect(screen, (255, 255, 255), (0, iy, w, ih))

    # Film grain
    grain = int(etc.knob3 * 30) + 2
    for _ in range(grain * 20):
        gx = random.randint(0, w - 1)
        gy = random.randint(0, h - 1)
        gv = random.randint(-grain * 3, grain * 3)
        c = max(0, min(255, 128 + gv))
        screen.set_at((gx, gy), (c, c, c))
