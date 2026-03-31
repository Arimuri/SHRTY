# ITBS - T - Hex Grid
# Hexagonal grid where each cell reacts to audio
# Knob1: hex size, Knob2: gap, Knob3: reactivity
# Knob4: foreground color, Knob5: background color
import pygame
import math

def setup(screen, etc):
    pass

def hex_corners(cx, cy, r):
    pts = []
    for i in range(6):
        angle = math.pi / 3 * i - math.pi / 6
        pts.append((int(cx + r * math.cos(angle)), int(cy + r * math.sin(angle))))
    return pts

def draw(screen, etc):
    w, h = screen.get_width(), screen.get_height()

    etc.color_picker_bg(etc.knob5)

    peak = abs(etc.audio_peak) / 32768.0
    hex_r = int(etc.knob1 * 40) + 12
    gap = int(etc.knob2 * 8) + 1
    reactivity = etc.knob3 * 2 + 0.3

    hex_w = hex_r * 2
    hex_h = int(hex_r * math.sqrt(3))
    step_x = int(hex_w * 0.75) + gap
    step_y = hex_h + gap

    col = 0
    x = 0
    while x < w + hex_r:
        row = 0
        y_offset = (hex_h // 2 + gap // 2) if col % 2 else 0
        y = y_offset
        while y < h + hex_r:
            # Map to audio
            idx = int(((col * 20 + row) % 100))
            audio_val = abs(etc.audio_in[idx]) / 32768.0

            # Size modulation
            r_mod = hex_r * (0.3 + audio_val * reactivity)
            r_mod = min(r_mod, hex_r)

            if r_mod > 2:
                color_t = ((col * 0.05 + row * 0.03 + etc.knob4) % 1.0)
                color = etc.color_picker(color_t)

                corners = hex_corners(x, y, int(r_mod))
                # Filled with slight alpha
                hex_surf = pygame.Surface((w, h), pygame.SRCALPHA)
                alpha = int(80 + audio_val * 175)
                pygame.draw.polygon(hex_surf, (*color, alpha), corners)
                pygame.draw.polygon(hex_surf, (*color, min(255, alpha + 60)), corners, 2)
                screen.blit(hex_surf, (0, 0))

            y += step_y
            row += 1
        x += step_x
        col += 1
