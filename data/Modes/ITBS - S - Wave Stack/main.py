# ITBS - S - Wave Stack
# Stacked waveforms with parallax depth, each band a different frequency range
# Knob1: wave count, Knob2: amplitude, Knob3: spacing
# Knob4: foreground color, Knob5: background color
import pygame
import math

def setup(screen, etc):
    pass

def draw(screen, etc):
    w, h = screen.get_width(), screen.get_height()

    etc.color_picker_bg(etc.knob5)

    peak = abs(etc.audio_peak) / 32768.0
    wave_count = int(etc.knob1 * 8) + 3
    amp = etc.knob2 * 150 + 20
    spacing = etc.knob3 * 0.7 + 0.3
    t = etc.frame_count * 0.02

    for i in range(wave_count):
        layer_t = i / wave_count
        y_base = int(h * (0.1 + layer_t * spacing * 0.9))

        # Color gradient across layers
        color = etc.color_picker((layer_t + etc.knob4) % 1.0)

        # Each layer samples different part of audio buffer
        buf_start = int(layer_t * 60)

        points_top = []
        points_fill = []
        for x in range(0, w + 4, 4):
            xt = x / w
            idx = min(buf_start + int(xt * 30), 99)
            audio_val = etc.audio_in[idx] / 32768.0

            # Depth: back layers move slower
            depth = 0.3 + layer_t * 0.7
            y = y_base + audio_val * amp * depth
            y += math.sin(xt * 3 + t * (1 + layer_t)) * 15 * depth
            points_top.append((x, int(y)))

        # Fill area below wave
        if len(points_top) > 1:
            fill_points = list(points_top) + [(w, h), (0, h)]
            fill_surf = pygame.Surface((w, h), pygame.SRCALPHA)
            alpha = int(40 + (1 - layer_t) * 60)
            pygame.draw.polygon(fill_surf, (*color, alpha), fill_points)
            screen.blit(fill_surf, (0, 0))

            # Wave line
            line_alpha = int(150 + (1 - layer_t) * 105)
            line_surf = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.lines(line_surf, (*color, line_alpha), False, points_top, 3)
            screen.blit(line_surf, (0, 0))

            # Bright edge on front waves
            if layer_t > 0.5:
                pygame.draw.lines(screen, (255, 255, 255), False, points_top, 1)
