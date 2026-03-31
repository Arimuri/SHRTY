# ITBS - S - Bounce Line
# 波形が上下のエッジで跳ね返り続ける。残像でリボン状の軌跡
# Waveform bounces between top and bottom edges — elastic and alive
#
# Knob1: 線の数
# Knob2: 弾力
# Knob3: 残像
# Knob4: foreground color
# Knob5: background color

import pygame
import math

offsets = []
velocities = []

def setup(screen, etc):
    global offsets, velocities
    offsets = [0.5] * 100
    velocities = [0.0] * 100

def draw(screen, etc):
    global offsets, velocities
    w, h = screen.get_width(), screen.get_height()

    # Trail fade
    trail_alpha = int((1.0 - etc.knob3) * 60) + 5
    bg = etc.color_picker_bg(etc.knob5)
    fade = pygame.Surface((w, h), pygame.SRCALPHA)
    fade.fill((*bg, trail_alpha))
    screen.blit(fade, (0, 0))

    peak = abs(etc.audio_peak) / 32768.0
    bounce = etc.knob2 * 0.15 + 0.02
    line_count = int(etc.knob1 * 5) + 1

    margin = 30

    # Update physics for each column
    for i in range(100):
        audio_val = etc.audio_in[i] / 32768.0
        velocities[i] += audio_val * bounce
        velocities[i] *= 0.92  # damping
        offsets[i] += velocities[i]

        # Bounce off edges
        if offsets[i] < 0:
            offsets[i] = -offsets[i]
            velocities[i] = abs(velocities[i]) * 0.8
        elif offsets[i] > 1:
            offsets[i] = 2.0 - offsets[i]
            velocities[i] = -abs(velocities[i]) * 0.8

        offsets[i] = max(0.0, min(1.0, offsets[i]))

    for line in range(line_count):
        lt = line / line_count
        color = etc.color_picker((lt * 0.3 + etc.knob4) % 1.0)

        points = []
        for col in range(100):
            x = margin + (col / 99) * (w - margin * 2)
            # Each line uses offset data shifted
            idx = (col + int(lt * 30)) % 100
            y = margin + offsets[idx] * (h - margin * 2)
            points.append((int(x), int(y)))

        if len(points) > 1:
            # Glow
            glow = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.lines(glow, (*color, 25), False, points, 8)
            screen.blit(glow, (0, 0))

            # Main
            pygame.draw.lines(screen, color, False, points, 2)

    # Edge lines
    edge_color = etc.color_picker(etc.knob4)
    edge_surf = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.line(edge_surf, (*edge_color, 40), (margin, margin), (w - margin, margin), 1)
    pygame.draw.line(edge_surf, (*edge_color, 40), (margin, h - margin), (w - margin, h - margin), 1)
    screen.blit(edge_surf, (0, 0))
