# ITBS - S - Spectrum Bars
# スタイリッシュなスペクトラムバー。角丸＋グロウ＋リフレクション
# Stylish spectrum analyzer with rounded bars, glow, and reflection
#
# Knob1: バー数
# Knob2: バー幅
# Knob3: リフレクション量
# Knob4: foreground color
# Knob5: background color

import pygame
import math

smoothed = [0.0] * 100

def setup(screen, etc):
    global smoothed
    smoothed = [0.0] * 100

def draw(screen, etc):
    global smoothed
    w, h = screen.get_width(), screen.get_height()

    etc.color_picker_bg(etc.knob5)

    peak = abs(etc.audio_peak) / 32768.0

    bar_count = int(etc.knob1 * 28) + 4
    width_ratio = etc.knob2 * 0.6 + 0.3  # ratio of bar to gap
    reflection = etc.knob3

    total_w = w - 40
    bar_step = total_w / bar_count
    bar_w = max(2, int(bar_step * width_ratio))
    bar_radius = min(bar_w // 2, 6)
    base_y = int(h * 0.65)
    max_h = int(h * 0.55)

    for i in range(bar_count):
        bt = i / bar_count
        idx = min(int(bt * 99), 99)
        audio_val = abs(etc.audio_in[idx]) / 32768.0

        # Smooth
        smoothed[i] += (audio_val - smoothed[i]) * 0.35
        val = smoothed[i]

        bar_h = int(val * max_h)
        if bar_h < 2:
            bar_h = 2

        x = int(20 + i * bar_step)
        y = base_y - bar_h

        # Color gradient across bars
        color = etc.color_picker((bt * 0.4 + etc.knob4) % 1.0)

        # Glow behind bar
        if bar_h > 10:
            glow_surf = pygame.Surface((bar_w + 12, bar_h + 12), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*color, 25), (0, 0, bar_w + 12, bar_h + 12), border_radius=bar_radius + 4)
            screen.blit(glow_surf, (x - 6, y - 6))

        # Main bar
        pygame.draw.rect(screen, color, (x, y, bar_w, bar_h), border_radius=bar_radius)

        # Top highlight
        if bar_h > 6:
            highlight = (min(255, color[0] + 80), min(255, color[1] + 80), min(255, color[2] + 80))
            pygame.draw.rect(screen, highlight, (x + 1, y, bar_w - 2, 3), border_radius=bar_radius)

        # Peak dot
        pygame.draw.rect(screen, (255, 255, 255), (x, y - 4, bar_w, 2))

        # Reflection
        if reflection > 0.05 and bar_h > 4:
            ref_h = int(bar_h * reflection * 0.6)
            ref_surf = pygame.Surface((bar_w, ref_h), pygame.SRCALPHA)
            for ry in range(ref_h):
                rt = ry / ref_h
                alpha = int((1 - rt) * 60 * reflection)
                pygame.draw.line(ref_surf, (*color, alpha), (0, ry), (bar_w, ry))
            screen.blit(ref_surf, (x, base_y + 2))

    # Base line
    line_color = etc.color_picker(etc.knob4)
    pygame.draw.line(screen, line_color, (20, base_y), (w - 20, base_y), 1)
