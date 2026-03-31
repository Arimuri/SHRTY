# ITBS - T - Bubble Pop
# Colorful bubbles rise and pop on beat
# Knob1: bubble size, Knob2: rise speed, Knob3: density
# Knob4: foreground color, Knob5: background color
import pygame
import random
import math

bubbles = []
prev_peak = 0

def setup(screen, etc):
    global bubbles
    bubbles = []

def draw(screen, etc):
    global bubbles, prev_peak
    w, h = screen.get_width(), screen.get_height()

    etc.color_picker_bg(etc.knob5)

    peak = abs(etc.audio_peak) / 32768.0
    onset = peak - prev_peak
    prev_peak = peak

    base_size = etc.knob1 * 60 + 10
    speed = etc.knob2 * 5 + 1
    density = int(etc.knob3 * 5) + 1

    # Spawn bubbles from bottom
    for _ in range(density):
        size = base_size * random.uniform(0.3, 1.5)
        bubbles.append({
            'x': random.uniform(size, w - size),
            'y': h + size,
            'size': size,
            'vx': random.uniform(-0.5, 0.5),
            'vy': -speed * random.uniform(0.5, 1.5),
            'wobble_phase': random.uniform(0, math.pi * 2),
            'color_t': (random.random() * 0.3 + etc.knob4) % 1.0,
            'popped': False,
            'pop_frame': 0,
        })

    while len(bubbles) > 300:
        bubbles.pop(0)

    # Pop bubbles on strong beat
    if onset > 0.1:
        for b in bubbles:
            if not b['popped'] and random.random() < onset * 2:
                b['popped'] = True
                b['pop_frame'] = 0

    alive = []
    for b in bubbles:
        if b['popped']:
            # Pop animation: expanding ring
            b['pop_frame'] += 1
            if b['pop_frame'] < 10:
                color = etc.color_picker(b['color_t'])
                r = int(b['size'] + b['pop_frame'] * 5)
                alpha = int(255 * (1 - b['pop_frame'] / 10))
                pop_surf = pygame.Surface((r * 2 + 4, r * 2 + 4), pygame.SRCALPHA)
                pygame.draw.circle(pop_surf, (*color, alpha), (r + 2, r + 2), r, 3)
                screen.blit(pop_surf, (int(b['x'] - r - 2), int(b['y'] - r - 2)))
                alive.append(b)
        else:
            b['wobble_phase'] += 0.1
            b['x'] += b['vx'] + math.sin(b['wobble_phase']) * 1.5
            b['y'] += b['vy'] * (1 + peak)

            if b['y'] > -b['size']:
                color = etc.color_picker(b['color_t'])
                r = int(b['size'])
                cx, cy = int(b['x']), int(b['y'])

                # Bubble body
                bubble_surf = pygame.Surface((r * 2 + 4, r * 2 + 4), pygame.SRCALPHA)
                pygame.draw.circle(bubble_surf, (*color, 60), (r + 2, r + 2), r)
                pygame.draw.circle(bubble_surf, (*color, 150), (r + 2, r + 2), r, 2)
                # Highlight
                hl_x = r + 2 - int(r * 0.3)
                hl_y = r + 2 - int(r * 0.3)
                hl_r = max(2, int(r * 0.25))
                pygame.draw.circle(bubble_surf, (255, 255, 255, 120), (hl_x, hl_y), hl_r)
                screen.blit(bubble_surf, (cx - r - 2, cy - r - 2))
                alive.append(b)

    bubbles = alive
