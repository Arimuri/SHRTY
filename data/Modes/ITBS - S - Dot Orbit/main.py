# ITBS - S - Dot Orbit
# ドットが軌道上を周回、オーディオで軌道半径が脈動する
# Dots orbit the center, radius pulsing with audio — playful and clean
#
# Knob1: 軌道数
# Knob2: ドット数/軌道
# Knob3: 速度
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

    etc.color_picker_bg(etc.knob5)

    peak = abs(etc.audio_peak) / 32768.0
    phase += etc.knob3 * 0.08 + 0.015

    orbit_count = int(etc.knob1 * 6) + 2
    dots_per_orbit = int(etc.knob2 * 8) + 3
    max_r = min(w, h) * 0.42

    for orb in range(orbit_count):
        ot = orb / orbit_count
        base_r = 30 + ot * (max_r - 30)

        # Audio modulation of radius
        idx = min(int(ot * 99), 99)
        audio_val = abs(etc.audio_in[idx]) / 32768.0
        r = base_r + audio_val * 60

        # Orbit color
        color = etc.color_picker((ot * 0.4 + etc.knob4) % 1.0)

        # Draw faint orbit path
        orbit_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.circle(orbit_surf, (*color, 25), (cx, cy), int(r), 1)
        screen.blit(orbit_surf, (0, 0))

        # Speed: inner orbits faster
        speed = phase * (1.5 - ot * 0.8)

        for d in range(dots_per_orbit):
            dt = d / dots_per_orbit
            angle = dt * math.pi * 2 + speed

            # Per-dot audio wiggle
            dot_idx = min(int((dt + ot * 0.3) * 99) % 100, 99)
            dot_audio = abs(etc.audio_in[dot_idx]) / 32768.0
            dot_r_offset = dot_audio * 20

            px = cx + math.cos(angle) * (r + dot_r_offset)
            py = cy + math.sin(angle) * (r + dot_r_offset)

            # Dot size: bigger when loud
            dot_size = int(3 + dot_audio * 6 + ot * 2)

            # Glow
            glow_surf = pygame.Surface((dot_size * 6, dot_size * 6), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*color, 30), (dot_size * 3, dot_size * 3), dot_size * 3)
            screen.blit(glow_surf, (int(px) - dot_size * 3, int(py) - dot_size * 3))

            # Dot
            pygame.draw.circle(screen, color, (int(px), int(py)), dot_size)

            # Bright center
            if dot_audio > 0.3:
                pygame.draw.circle(screen, (255, 255, 255), (int(px), int(py)), max(1, dot_size - 2))

    # Center
    center_r = int(5 + peak * 8)
    color_c = etc.color_picker(etc.knob4)
    pygame.draw.circle(screen, color_c, (cx, cy), center_r)
    pygame.draw.circle(screen, (255, 255, 255), (cx, cy), max(2, center_r - 3))
