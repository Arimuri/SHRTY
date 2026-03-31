# ITBS - T - Iso Blocks
# アイソメトリックブロックがビートで積み上がる
# Isometric blocks stack up on beat — clean geometric pop
#
# Knob1: ブロックサイズ
# Knob2: 列数
# Knob3: 落下速度
# Knob4: foreground color
# Knob5: background color

import pygame
import math
import random

blocks = []
prev_peak = 0

def setup(screen, etc):
    global blocks
    blocks = []

def iso_block(screen, cx, cy, size, color, height):
    """Draw an isometric block at cx, cy."""
    s = size
    hs = s * 0.5
    # Height offset
    top_y = cy - height

    # Top face
    top = [
        (cx, top_y - hs),
        (cx + s, top_y),
        (cx, top_y + hs),
        (cx - s, top_y),
    ]
    # Right face
    right = [
        (cx, top_y + hs),
        (cx + s, top_y),
        (cx + s, top_y + height),
        (cx, top_y + hs + height),
    ]
    # Left face
    left = [
        (cx, top_y + hs),
        (cx - s, top_y),
        (cx - s, top_y + height),
        (cx, top_y + hs + height),
    ]

    # Shade colors
    r, g, b = color
    dark = (max(0, r - 60), max(0, g - 60), max(0, b - 60))
    mid = (max(0, r - 30), max(0, g - 30), max(0, b - 30))

    pygame.draw.polygon(screen, dark, [(int(p[0]), int(p[1])) for p in left])
    pygame.draw.polygon(screen, mid, [(int(p[0]), int(p[1])) for p in right])
    pygame.draw.polygon(screen, color, [(int(p[0]), int(p[1])) for p in top])

    # Outlines
    for face in [top, right, left]:
        pts = [(int(p[0]), int(p[1])) for p in face]
        pygame.draw.polygon(screen, (255, 255, 255), pts, 1)

def draw(screen, etc):
    global blocks, prev_peak
    w, h = screen.get_width(), screen.get_height()

    etc.color_picker_bg(etc.knob5)

    peak = abs(etc.audio_peak) / 32768.0
    onset = peak - prev_peak
    prev_peak = peak

    block_size = int(etc.knob1 * 40) + 15
    cols = int(etc.knob2 * 8) + 3
    fall_speed = etc.knob3 * 6 + 2

    # Spawn on beat
    if onset > 0.05:
        col = random.randint(0, cols - 1)
        col_t = col / cols
        # Isometric grid position
        cx = w * 0.2 + col * block_size * 1.8
        block_h = int(10 + onset * 60)
        blocks.append({
            'cx': cx,
            'cy': -block_size,
            'target_y': h * 0.7 - random.randint(0, 3) * block_size * 0.5,
            'size': block_size,
            'height': block_h,
            'color_t': (col_t * 0.5 + etc.knob4) % 1.0,
            'vy': 0,
            'landed': False,
            'life': 180,
        })

    while len(blocks) > 60:
        blocks.pop(0)

    alive = []
    # Sort by y for depth
    blocks.sort(key=lambda b: b['cy'])

    for b in blocks:
        if not b['landed']:
            b['vy'] += 0.3
            b['cy'] += b['vy'] + fall_speed * 0.3
            if b['cy'] >= b['target_y']:
                b['cy'] = b['target_y']
                b['landed'] = True
                b['vy'] = 0
        else:
            b['life'] -= 1
            # Subtle bounce on audio
            b['cy'] = b['target_y'] - peak * 8

        if b['life'] > 0:
            color = etc.color_picker(b['color_t'])
            alpha_mult = min(1.0, b['life'] / 30.0)
            c = (int(color[0] * alpha_mult), int(color[1] * alpha_mult), int(color[2] * alpha_mult))
            iso_block(screen, b['cx'], b['cy'], b['size'], c, b['height'])
            alive.append(b)

    blocks = alive
