# ITBS - S - Pluck String
# 弦が張られて振動する。各弦がオーディオ帯域に対応
# Vibrating strings tuned to audio bands — elegant and musical
#
# Knob1: 弦の数
# Knob2: テンション (振幅)
# Knob3: 減衰
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

    string_count = int(etc.knob1 * 10) + 3
    tension = etc.knob2 * 200 + 20
    damping = 1.0 - etc.knob3 * 0.8

    margin_x = 40
    margin_y = 60

    for s in range(string_count):
        st = s / string_count
        y_base = margin_y + st * (h - margin_y * 2)

        # Each string maps to audio band
        band_start = int(st * 80)
        band_end = min(band_start + 20, 99)

        color = etc.color_picker((st * 0.35 + etc.knob4) % 1.0)

        points = []
        segments = 80
        for seg in range(segments + 1):
            xt = seg / segments
            x = margin_x + xt * (w - margin_x * 2)

            # Audio from this string's band
            idx = min(band_start + int(xt * (band_end - band_start)), 99)
            audio_val = etc.audio_in[idx] / 32768.0

            # String physics: ends are fixed, max displacement at center
            envelope = math.sin(xt * math.pi)

            # Standing wave pattern
            mode_shape = math.sin(xt * math.pi * (1 + s % 3))

            y = y_base + audio_val * tension * envelope * damping
            y += math.sin(xt * math.pi * 2 + frame * 0.05 * (1 + st)) * 3 * envelope

            points.append((int(x), int(y)))

        if len(points) > 1:
            # Glow
            glow_surf = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.lines(glow_surf, (*color, 20), False, points, 6)
            screen.blit(glow_surf, (0, 0))

            # String
            thickness = 2 if peak < 0.3 else 3
            pygame.draw.lines(screen, color, False, points, thickness)

        # Bridge dots at ends
        dot_r = 3
        pygame.draw.circle(screen, (255, 255, 255), (margin_x, int(y_base)), dot_r)
        pygame.draw.circle(screen, (255, 255, 255), (w - margin_x, int(y_base)), dot_r)

    # Bridge lines
    bridge_color = etc.color_picker(etc.knob4)
    pygame.draw.line(screen, bridge_color, (margin_x, margin_y - 10), (margin_x, h - margin_y + 10), 2)
    pygame.draw.line(screen, bridge_color, (w - margin_x, margin_y - 10), (w - margin_x, h - margin_y + 10), 2)
