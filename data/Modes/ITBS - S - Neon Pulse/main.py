# ITBS - S - Neon Pulse
# Thick neon lines pulse outward from center with audio
# Knob1: line count, Knob2: thickness, Knob3: speed
# Knob4: foreground color, Knob5: background color
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
    phase += (etc.knob3 * 0.1 + 0.01) * (1 + peak * 2)

    line_count = int(etc.knob1 * 12) + 3
    thickness = int(etc.knob2 * 20) + 2

    for i in range(line_count):
        t = i / line_count
        angle = t * math.pi * 2 + phase

        # Audio drives radius
        idx = int(t * 99)
        audio_val = abs(etc.audio_in[idx]) / 32768.0
        radius = 50 + audio_val * min(w, h) * 0.4

        x1 = cx + math.cos(angle) * 30
        y1 = cy + math.sin(angle) * 30
        x2 = cx + math.cos(angle) * radius
        y2 = cy + math.sin(angle) * radius

        # Glow layer
        color = etc.color_picker((t + etc.knob4) % 1.0)
        glow_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.line(glow_surf, (*color, 40), (int(x1), int(y1)), (int(x2), int(y2)), thickness + 8)
        screen.blit(glow_surf, (0, 0))

        # Main line
        pygame.draw.line(screen, color, (int(x1), int(y1)), (int(x2), int(y2)), thickness)

        # Tip circle
        pygame.draw.circle(screen, (255, 255, 255), (int(x2), int(y2)), thickness // 2 + 1)
