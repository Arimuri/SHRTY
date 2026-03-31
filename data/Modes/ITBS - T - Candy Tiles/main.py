# ITBS - T - Candy Tiles
# カラフルな角丸タイルがオーディオでフリップ・スケールする
# Rounded candy tiles scale and shift with audio — playful grid
#
# Knob1: グリッドサイズ
# Knob2: 角丸の丸み
# Knob3: リアクション強度
# Knob4: foreground color
# Knob5: background color

import pygame
import math

frame = 0

def setup(screen, etc):
    pass

def draw(screen, etc):
    global frame
    frame += 1
    w, h = screen.get_width(), screen.get_height()

    etc.color_picker_bg(etc.knob5)

    peak = abs(etc.audio_peak) / 32768.0

    cols = int(4 + etc.knob1 * 12)
    border_radius = int(etc.knob2 * 20) + 2
    react = etc.knob3 * 1.5 + 0.3

    cell_w = w / cols
    cell_h = cell_w
    rows = int(h / cell_h) + 1
    gap = 3

    for row in range(rows):
        for col in range(cols):
            x = col * cell_w
            y = row * cell_h

            # Audio mapping
            idx = min(int((col + row * cols) % 100), 99)
            audio_val = abs(etc.audio_in[idx]) / 32768.0

            # Scale: shrink/grow with audio
            scale = 0.5 + audio_val * react * 0.5
            scale = min(1.0, max(0.1, scale))

            # Checkerboard-ish color offset
            checker = (col + row) % 2
            color_t = (col / cols * 0.3 + row / rows * 0.15 + checker * 0.08 + etc.knob4) % 1.0
            color = etc.color_picker(color_t)

            # Brightness boost on loud tiles
            if audio_val > 0.5:
                color = (min(255, color[0] + 40), min(255, color[1] + 40), min(255, color[2] + 40))

            # Tile size with scale
            tw = int(cell_w * scale) - gap * 2
            th = int(cell_h * scale) - gap * 2
            if tw < 2 or th < 2:
                continue

            tx = int(x + (cell_w - tw) * 0.5)
            ty = int(y + (cell_h - th) * 0.5)

            br = min(border_radius, tw // 2, th // 2)

            # Alpha based on scale
            alpha = int(120 + scale * 135)
            tile_surf = pygame.Surface((tw, th), pygame.SRCALPHA)
            pygame.draw.rect(tile_surf, (*color, alpha), (0, 0, tw, th), border_radius=br)

            # Subtle inner highlight (top-left)
            if tw > 8 and th > 8:
                highlight = (min(255, color[0] + 70), min(255, color[1] + 70), min(255, color[2] + 70))
                pygame.draw.rect(tile_surf, (*highlight, 40), (2, 2, tw - 4, th // 3), border_radius=br)

            screen.blit(tile_surf, (tx, ty))
