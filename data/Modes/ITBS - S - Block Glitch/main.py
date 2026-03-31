# ITBS - Block Glitch
# Audio-driven block displacement glitch (iytm style)
# Knob1: glitch intensity, Knob2: block size, Knob3: horizontal vs vertical
# Knob4: foreground color, Knob5: background color
import pygame
import random
import math

prev_peak = 0

def setup(screen, etc):
    pass

def draw(screen, etc):
    global prev_peak
    w, h = screen.get_width(), screen.get_height()

    peak = abs(etc.audio_peak) / 32768.0
    onset = peak - prev_peak
    prev_peak = peak

    # Background color from palette
    etc.color_picker_bg(etc.knob5)

    # Draw audio bars as base visual
    bar_count = 32
    bar_w = w // bar_count
    for i in range(bar_count):
        idx = int(i * 99 / bar_count)
        val = abs(etc.audio_in[idx]) / 32768.0
        bar_h = int(val * h * 0.6)

        color = etc.color_picker((i / bar_count + etc.knob4) % 1.0)
        x = i * bar_w
        y = h // 2 - bar_h // 2
        pygame.draw.rect(screen, color, (x, y, bar_w - 1, bar_h))

    # Block glitch on beat
    intensity = etc.knob1
    if onset > 0.05 and intensity > 0.02:
        block_count = int(1 + onset * 12 * intensity)
        max_block = int(etc.knob2 * 200) + 30

        for _ in range(block_count):
            bw = random.randint(20, max_block)
            bh = random.randint(10, max_block // 2)
            sx = random.randint(0, max(0, w - bw))
            sy = random.randint(0, max(0, h - bh))

            # Direction bias (knob3: 0=horizontal, 1=vertical)
            h_bias = 1.0 - etc.knob3
            v_bias = etc.knob3
            dx = int(random.uniform(-120, 120) * onset * intensity * h_bias)
            dy = int(random.uniform(-80, 80) * onset * intensity * v_bias)

            try:
                block = screen.subsurface(pygame.Rect(sx, sy, bw, bh)).copy()
                screen.blit(block, (sx + dx, sy + dy))
            except:
                pass

    # White flash on strong hit
    if onset > 0.15:
        flash = pygame.Surface((w, h), pygame.SRCALPHA)
        flash.fill((255, 255, 255, int(onset * 40)))
        screen.blit(flash, (0, 0))
