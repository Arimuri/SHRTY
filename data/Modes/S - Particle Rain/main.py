# S - Particle Rain
# Particles fall and react to audio
# Knob1: speed, Knob2: color, Knob3: density, Knob4: size, Knob5: bg alpha
import pygame
import random
import math

particles = []

def setup(screen, etc):
    global particles
    particles = []

def draw(screen, etc):
    global particles

    alpha = int(etc.knob5 * 200) + 20
    s = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    s.fill((0, 0, 0, alpha))
    screen.blit(s, (0, 0))

    w = screen.get_width()
    h = screen.get_height()

    speed = etc.knob1 * 10 + 1
    density = int(etc.knob3 * 10) + 1
    base_size = etc.knob4 * 15 + 2

    # Audio peak drives burst
    peak = abs(etc.audio_peak) / 32768.0

    # Spawn particles
    for _ in range(density):
        particles.append({
            'x': random.randint(0, w),
            'y': random.randint(-20, 0),
            'vx': random.uniform(-1, 1) + peak * random.uniform(-3, 3),
            'vy': random.uniform(1, 3) * speed * (0.5 + peak),
            'size': random.uniform(1, base_size),
            'color_t': random.random(),
            'life': random.randint(30, 120),
            'age': 0,
        })

    # Cap
    while len(particles) > 500:
        particles.pop(0)

    # Update and draw
    alive = []
    for p in particles:
        p['x'] += p['vx']
        p['y'] += p['vy']
        p['vy'] += 0.1  # gravity
        p['age'] += 1

        if p['age'] < p['life'] and 0 <= p['x'] <= w and p['y'] <= h:
            fade = 1.0 - (p['age'] / p['life'])
            color = etc.color_picker((p['color_t'] + etc.knob2) % 1.0)
            r = max(1, int(p['size'] * fade))
            pygame.draw.circle(screen, color, (int(p['x']), int(p['y'])), r)
            alive.append(p)

    particles = alive
