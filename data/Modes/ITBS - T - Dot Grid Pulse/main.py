# ITBS - T - Dot Grid Pulse
# ミニマルなドットグリッドがオーディオで呼吸する
# Minimal dot grid breathes with audio — i am robot and proud vibes
#
# Knob1: グリッドサイズ
# Knob2: ドット最大半径
# Knob3: 波紋の速度
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

    etc.color_picker_bg(etc.knob5)

    peak = abs(etc.audio_peak) / 32768.0

    # Grid params
    cols = int(6 + etc.knob1 * 20)
    max_r = etc.knob2 * 20 + 4
    speed = etc.knob3 * 0.12 + 0.02

    phase += speed + peak * 0.08

    cell_w = w / cols
    cell_h = cell_w  # square cells
    rows = int(h / cell_h) + 1

    for row in range(rows):
        for col in range(cols):
            cx = cell_w * (col + 0.5)
            cy = cell_h * (row + 0.5)

            # Distance from center for ripple
            dx = (cx - w * 0.5) / w
            dy = (cy - h * 0.5) / h
            dist = math.sqrt(dx * dx + dy * dy)

            # Audio-driven ripple
            wave = math.sin(dist * 10 - phase) * 0.5 + 0.5

            # Map to audio buffer
            idx = int((col / cols) * 99)
            audio_val = abs(etc.audio_in[idx]) / 32768.0

            # Radius: mix of ripple wave and audio
            r = max_r * (0.15 + wave * 0.45 + audio_val * 0.4)
            r = max(1.5, min(r, cell_w * 0.45))

            # Color: subtle hue shift across grid
            color_t = (col / cols * 0.3 + row / rows * 0.1 + etc.knob4) % 1.0
            color = etc.color_picker(color_t)

            # Alpha based on radius
            alpha = int(80 + (r / max_r) * 175)
            alpha = min(255, alpha)

            ri = int(r)
            if ri < 2:
                pygame.draw.circle(screen, color, (int(cx), int(cy)), 1)
            else:
                dot_surf = pygame.Surface((ri * 2 + 2, ri * 2 + 2), pygame.SRCALPHA)
                pygame.draw.circle(dot_surf, (*color, alpha), (ri + 1, ri + 1), ri)
                screen.blit(dot_surf, (int(cx) - ri - 1, int(cy) - ri - 1))
