# ITBS - S - Laser Grid
# Perspective grid that warps with audio, synthwave/retrowave aesthetic
# Knob1: grid density, Knob2: warp amount, Knob3: scroll speed
# Knob4: foreground color, Knob5: background color
import pygame
import math

scroll = 0

def setup(screen, etc):
    pass

def draw(screen, etc):
    global scroll
    w, h = screen.get_width(), screen.get_height()

    etc.color_picker_bg(etc.knob5)

    peak = abs(etc.audio_peak) / 32768.0
    scroll += etc.knob3 * 5 + 1 + peak * 10

    grid_lines = int(etc.knob1 * 20) + 5
    warp = etc.knob2 * 100 + 10
    horizon = h * 0.35

    color = etc.color_picker(etc.knob4)
    glow = (min(255, color[0] + 60), min(255, color[1] + 60), min(255, color[2] + 60))

    # Horizontal lines (scrolling toward viewer)
    for i in range(grid_lines * 2):
        raw_y = (i * 30 + scroll) % (h * 2)
        # Perspective transform
        t = raw_y / (h * 2)
        screen_y = int(horizon + (h - horizon) * (t ** 1.5))
        if screen_y < horizon or screen_y >= h:
            continue

        depth = (screen_y - horizon) / (h - horizon)
        alpha = int(depth * 200)
        line_w = int(depth * 3) + 1

        # Audio warp
        idx = int(i % 100)
        audio_val = etc.audio_in[min(idx, 99)] / 32768.0
        wobble = int(audio_val * warp * depth)

        surf = pygame.Surface((w, 2), pygame.SRCALPHA)
        pygame.draw.line(surf, (*color, alpha), (0, 0), (w, wobble), line_w)
        screen.blit(surf, (0, screen_y))

    # Vertical lines (converging to vanishing point)
    vx = w // 2
    for i in range(grid_lines):
        t = i / grid_lines
        x_bottom = int(t * w * 1.4 - w * 0.2)

        idx = int(t * 99)
        audio_val = etc.audio_in[idx] / 32768.0
        x_shift = int(audio_val * warp * 0.3)

        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.line(surf, (*color, 150), (vx + x_shift, int(horizon)), (x_bottom, h), 1)
        screen.blit(surf, (0, 0))

    # Horizon glow line
    pygame.draw.line(screen, glow, (0, int(horizon)), (w, int(horizon)), 2)

    # Sun / circle at vanishing point
    sun_r = int(20 + peak * 40)
    sun_surf = pygame.Surface((sun_r * 4, sun_r * 4), pygame.SRCALPHA)
    pygame.draw.circle(sun_surf, (*color, 80), (sun_r * 2, sun_r * 2), sun_r * 2)
    pygame.draw.circle(sun_surf, (*glow, 150), (sun_r * 2, sun_r * 2), sun_r)
    screen.blit(sun_surf, (vx - sun_r * 2, int(horizon) - sun_r * 2))
