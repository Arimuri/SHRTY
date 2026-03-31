# ITBS - S - Waveform Grid
# 波形を格子状に並べて面的に展開する
# Waveform tiled in a grid — audio surface visualization
#
# Knob1: 行数
# Knob2: 振幅
# Knob3: 位相ずれ
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

    rows = int(etc.knob1 * 10) + 3
    amp = etc.knob2 * 80 + 10
    phase_shift = etc.knob3 * 0.5

    cell_h = h / rows

    for row in range(rows):
        rt = row / rows
        y_base = cell_h * (row + 0.5)
        color = etc.color_picker((rt * 0.4 + etc.knob4) % 1.0)

        points = []
        step = 4
        for x in range(0, w, step):
            xt = x / w

            # Audio sample with row-based phase shift
            idx_offset = int(row * phase_shift * 10) % 50
            idx = min(int(xt * 99), 99)
            shifted_idx = (idx + idx_offset) % 100
            audio_val = etc.audio_in[shifted_idx] / 32768.0

            y = y_base + audio_val * amp
            # Clamp to cell
            y = max(y_base - cell_h * 0.45, min(y_base + cell_h * 0.45, y))
            points.append((x, int(y)))

        if len(points) > 1:
            # Fill below wave
            fill_points = list(points) + [(w, int(y_base + cell_h * 0.45)), (0, int(y_base + cell_h * 0.45))]
            fill_surf = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.polygon(fill_surf, (*color, 25), fill_points)
            screen.blit(fill_surf, (0, 0))

            # Wave line
            pygame.draw.lines(screen, color, False, points, 2)

        # Row separator (faint)
        sep_y = int(cell_h * (row + 1))
        sep_surf = pygame.Surface((w, 1), pygame.SRCALPHA)
        sep_surf.fill((*color, 20))
        screen.blit(sep_surf, (0, sep_y))
