# ITBS - S - Polar Flower
# 波形を極座標で描画し、花のようなパターンを生成
# Waveform in polar coordinates creates floral audio patterns
#
# Knob1: 花弁数
# Knob2: 半径
# Knob3: 回転速度
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
    cx, cy = w // 2, h // 2

    bg = etc.color_picker_bg(etc.knob5)
    fade = pygame.Surface((w, h), pygame.SRCALPHA)
    fade.fill((*bg, 30))
    screen.blit(fade, (0, 0))

    peak = abs(etc.audio_peak) / 32768.0
    phase += etc.knob3 * 0.05 + 0.008

    petals = int(etc.knob1 * 8) + 2
    base_r = etc.knob2 * 200 + 60
    segments = 180

    # Draw multiple layers
    layers = 3
    for layer in range(layers):
        lt = layer / layers
        color = etc.color_picker((lt * 0.2 + etc.knob4) % 1.0)
        layer_phase = phase + lt * 0.5

        points = []
        for i in range(segments + 1):
            t = i / segments
            angle = t * math.pi * 2 + layer_phase

            # Audio modulation
            idx = min(int(t * 99), 99)
            audio_val = abs(etc.audio_in[idx]) / 32768.0

            # Rose curve: r = cos(petals * theta)
            rose = abs(math.cos(petals * angle * 0.5))
            r = base_r * (0.2 + rose * 0.5 + audio_val * 0.5) * (0.6 + lt * 0.4)

            px = cx + math.cos(angle) * r
            py = cy + math.sin(angle) * r
            points.append((int(px), int(py)))

        if len(points) > 2:
            # Fill
            fill_surf = pygame.Surface((w, h), pygame.SRCALPHA)
            alpha_fill = int(15 + lt * 20)
            pygame.draw.polygon(fill_surf, (*color, alpha_fill), points)
            screen.blit(fill_surf, (0, 0))

            # Outline
            alpha_line = int(100 + lt * 100)
            line_surf = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.lines(line_surf, (*color, alpha_line), True, points, 2)
            screen.blit(line_surf, (0, 0))

    # Center
    center_r = int(5 + peak * 12)
    pygame.draw.circle(screen, (255, 255, 255), (cx, cy), center_r)
