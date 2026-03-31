# S - Grid Pulse
# Audio-reactive grid of rectangles
# Knob1: grid size, Knob2: color, Knob3: gap, Knob4: reactivity, Knob5: bg alpha
import pygame
import math

def setup(screen, etc):
    pass

def draw(screen, etc):
    alpha = int(etc.knob5 * 240) + 10
    s = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    s.fill((0, 0, 0, alpha))
    screen.blit(s, (0, 0))

    w = screen.get_width()
    h = screen.get_height()

    cell = int(etc.knob1 * 80) + 10
    gap = int(etc.knob3 * 10) + 1
    reactivity = etc.knob4 * 3

    cols = w // cell + 1
    rows = h // cell + 1

    for row in range(rows):
        for col in range(cols):
            # Map grid position to audio buffer
            idx = int(((row * cols + col) / (rows * cols)) * 99)
            audio_val = abs(etc.audio_in[idx]) / 32768.0

            size = int((cell - gap) * (0.2 + audio_val * reactivity))
            size = max(1, min(cell - gap, size))

            x = col * cell + (cell - size) // 2
            y = row * cell + (cell - size) // 2

            color_t = ((row * cols + col) / (rows * cols) + etc.knob2) % 1.0
            color = etc.color_picker(color_t)

            pygame.draw.rect(screen, color, (x, y, size, size))
