# ITBS - S - Ring Pulse
# 波形データで同心円リングの半径が変わる、ミニマルなパルスリング
# Concentric rings whose radius follows the waveform — clean and hypnotic
#
# Knob1: リング数
# Knob2: 太さ
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
    fade.fill((*bg, 35))
    screen.blit(fade, (0, 0))

    peak = abs(etc.audio_peak) / 32768.0
    phase += etc.knob3 * 0.06 + 0.01

    ring_count = int(etc.knob1 * 10) + 3
    thickness = int(etc.knob2 * 8) + 1
    base_r = min(w, h) * 0.05

    for i in range(ring_count):
        t = i / ring_count

        # Each ring samples different part of audio buffer
        idx = min(int(t * 99), 99)
        audio_val = abs(etc.audio_in[idx]) / 32768.0

        # Radius: base + audio expansion
        r = base_r + t * min(w, h) * 0.4 + audio_val * 80

        # Subtle rotation per ring
        angle_offset = phase * (1 + t * 0.5)

        # Draw ring as series of points for waveform deformation
        color = etc.color_picker((t * 0.3 + etc.knob4) % 1.0)
        points = []
        segments = 60

        for s in range(segments + 1):
            a = (s / segments) * math.pi * 2 + angle_offset
            # Deform radius with nearby audio samples
            sub_idx = min(int((s / segments) * 99), 99)
            sub_audio = etc.audio_in[sub_idx] / 32768.0
            deform_r = r + sub_audio * 30 * (0.3 + t * 0.7)

            px = cx + math.cos(a) * deform_r
            py = cy + math.sin(a) * deform_r
            points.append((int(px), int(py)))

        if len(points) > 2:
            alpha = int(100 + (1 - t) * 155)
            ring_surf = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.lines(ring_surf, (*color, alpha), True, points, thickness)
            screen.blit(ring_surf, (0, 0))

    # Center dot
    dot_r = int(4 + peak * 10)
    pygame.draw.circle(screen, (255, 255, 255), (cx, cy), dot_r)
