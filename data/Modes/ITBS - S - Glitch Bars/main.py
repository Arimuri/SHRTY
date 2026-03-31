# ITBS - S - Glitch Bars
# 水平バーが波形データで左右にずれる。ビートで色反転＋ノイズ
# Horizontal bars shift with audio — clean digital glitch aesthetic
#
# Knob1: バー数
# Knob2: ずれ量
# Knob3: ノイズ量
# Knob4: foreground color
# Knob5: background color

import pygame
import random
import math

prev_peak = 0
invert_timer = 0

def setup(screen, etc):
    pass

def draw(screen, etc):
    global prev_peak, invert_timer
    w, h = screen.get_width(), screen.get_height()

    etc.color_picker_bg(etc.knob5)

    peak = abs(etc.audio_peak) / 32768.0
    onset = peak - prev_peak
    prev_peak = peak

    bar_count = int(etc.knob1 * 30) + 6
    shift_amount = etc.knob2 * 200 + 20
    noise = etc.knob3

    bar_h = h / bar_count

    # Beat flash
    if onset > 0.08:
        invert_timer = 3

    if invert_timer > 0:
        invert_timer -= 1

    for i in range(bar_count):
        bt = i / bar_count
        y = int(i * bar_h)
        bh = int(bar_h) + 1

        # Audio displacement
        idx = min(int(bt * 99), 99)
        audio_val = etc.audio_in[idx] / 32768.0

        x_shift = int(audio_val * shift_amount)

        # Noise jitter
        if noise > 0.05:
            x_shift += int(random.gauss(0, noise * 15 * peak))

        color = etc.color_picker((bt * 0.35 + etc.knob4) % 1.0)

        # Invert on beat
        if invert_timer > 0 and i % 2 == 0:
            color = (255 - color[0], 255 - color[1], 255 - color[2])

        # Brightness based on audio
        brightness = 0.3 + abs(audio_val) * 0.7
        c = (int(color[0] * brightness), int(color[1] * brightness), int(color[2] * brightness))

        # Main bar
        pygame.draw.rect(screen, c, (x_shift, y, w, bh))

        # Accent line at bar edge
        if abs(audio_val) > 0.3:
            pygame.draw.line(screen, (255, 255, 255), (x_shift, y), (x_shift + w, y), 1)

    # Scanline overlay
    if noise > 0.3:
        scan_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        for sy in range(0, h, 3):
            alpha = int(noise * 20)
            pygame.draw.line(scan_surf, (0, 0, 0, alpha), (0, sy), (w, sy))
        screen.blit(scan_surf, (0, 0))
