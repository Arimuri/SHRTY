# ITBS - S - Ribbon Dance
# Smooth flowing ribbons that dance with audio frequency bands
# Knob1: ribbon count, Knob2: amplitude, Knob3: smoothness
# Knob4: foreground color, Knob5: background color
import pygame
import math

phase = 0

def setup(screen, etc):
    pass

def draw(screen, etc):
    global phase
    w, h = screen.get_width(), screen.get_height()

    # Fading background
    bg = etc.color_picker_bg(etc.knob5)
    fade = pygame.Surface((w, h), pygame.SRCALPHA)
    fade.fill((*bg, 30))
    screen.blit(fade, (0, 0))

    peak = abs(etc.audio_peak) / 32768.0
    phase += 0.03 + peak * 0.05

    ribbon_count = int(etc.knob1 * 6) + 2
    amp = etc.knob2 * 200 + 30
    smooth = etc.knob3 * 3 + 0.5

    for r in range(ribbon_count):
        rt = r / ribbon_count
        y_base = h * (0.15 + rt * 0.7)
        color = etc.color_picker((rt + etc.knob4) % 1.0)

        points = []
        for x in range(0, w + 4, 4):
            xt = x / w
            # Multiple sine waves for organic motion
            idx = int(xt * 99)
            audio_val = etc.audio_in[idx] / 32768.0

            y = y_base
            y += math.sin(xt * smooth * math.pi + phase + r * 1.7) * amp * 0.5
            y += math.sin(xt * smooth * 2 * math.pi + phase * 1.3 + r * 0.9) * amp * 0.25
            y += audio_val * amp * 0.6
            points.append((x, int(y)))

        if len(points) > 1:
            # Thick glow
            glow = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.lines(glow, (*color, 30), False, points, 12)
            screen.blit(glow, (0, 0))
            # Medium
            pygame.draw.lines(screen, color, False, points, 4)
            # Bright center
            pygame.draw.lines(screen, (255, 255, 255), False, points, 1)
