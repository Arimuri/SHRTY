# ITBS - T - Pixel Rain
# Fat retro pixels fall like rain, audio controls density and speed
# Knob1: pixel size, Knob2: speed, Knob3: density
# Knob4: foreground color, Knob5: background color
import pygame
import random

pixels = []

def setup(screen, etc):
    global pixels
    pixels = []

def draw(screen, etc):
    global pixels
    w, h = screen.get_width(), screen.get_height()

    etc.color_picker_bg(etc.knob5)

    peak = abs(etc.audio_peak) / 32768.0
    pix_size = int(etc.knob1 * 30) + 4
    speed = etc.knob2 * 15 + 2
    density = int(etc.knob3 * 8) + 1

    # Spawn
    for _ in range(density + int(peak * 10)):
        col_idx = random.randint(0, 99)
        audio_val = abs(etc.audio_in[col_idx]) / 32768.0
        x = (col_idx / 99) * w
        # Snap to grid
        x = int(x / pix_size) * pix_size
        pixels.append({
            'x': x,
            'y': -pix_size,
            'speed': speed * random.uniform(0.5, 1.5) * (0.5 + audio_val),
            'color_t': (x / w + etc.knob4) % 1.0,
            'size': pix_size,
        })

    while len(pixels) > 600:
        pixels.pop(0)

    alive = []
    for p in pixels:
        p['y'] += p['speed'] * (1 + peak * 2)
        if p['y'] < h + p['size']:
            color = etc.color_picker(p['color_t'])
            # Drop shadow
            pygame.draw.rect(screen, (0, 0, 0), (p['x'] + 2, int(p['y']) + 2, p['size'] - 1, p['size'] - 1))
            # Main pixel
            pygame.draw.rect(screen, color, (p['x'], int(p['y']), p['size'] - 1, p['size'] - 1))
            # Highlight
            pygame.draw.rect(screen, (255, 255, 255), (p['x'] + 1, int(p['y']) + 1, 2, 2))
            alive.append(p)

    pixels = alive
