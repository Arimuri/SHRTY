# ITBS - T - Pop Rings
# Concentric rings expand on beat with pop art colors
# Knob1: ring thickness, Knob2: expansion speed, Knob3: ring count
# Knob4: foreground color, Knob5: background color
import pygame
import math

rings = []
prev_peak = 0

def setup(screen, etc):
    global rings
    rings = []

def draw(screen, etc):
    global rings, prev_peak
    w, h = screen.get_width(), screen.get_height()
    cx, cy = w // 2, h // 2

    etc.color_picker_bg(etc.knob5)

    peak = abs(etc.audio_peak) / 32768.0
    onset = peak - prev_peak
    prev_peak = peak

    thickness = int(etc.knob1 * 25) + 3
    speed = etc.knob2 * 8 + 2
    max_rings = int(etc.knob3 * 30) + 10

    # Spawn ring on beat
    if onset > 0.06:
        rings.append({
            'r': 10,
            'color_t': (etc.knob4 + len(rings) * 0.07) % 1.0,
            'thick': thickness + int(onset * 15),
            'alpha': 255,
        })

    while len(rings) > max_rings:
        rings.pop(0)

    alive = []
    for ring in rings:
        ring['r'] += speed * (1 + peak)
        ring['alpha'] -= 3
        if ring['alpha'] > 0 and ring['r'] < max(w, h):
            color = etc.color_picker(ring['color_t'])
            r = int(ring['r'])
            # Glow
            glow_surf = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*color, ring['alpha'] // 4), (cx, cy), r + 6, ring['thick'] + 6)
            screen.blit(glow_surf, (0, 0))
            # Ring
            ring_surf = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.circle(ring_surf, (*color, ring['alpha']), (cx, cy), r, ring['thick'])
            screen.blit(ring_surf, (0, 0))
            alive.append(ring)

    rings = alive
