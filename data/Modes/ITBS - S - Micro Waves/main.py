# ITBS - S - Micro Waves
# 極小ドットで波形を描画、オシロスコープ的だけどポップ
# Tiny dots trace waveforms — micro oscilloscope meets pop art
#
# Knob1: ドットサイズ
# Knob2: 波形の数
# Knob3: 散らし量
# Knob4: foreground color
# Knob5: background color

import pygame
import math
import random

phase = 0
trail_surfaces = None

def setup(screen, etc):
    global trail_surfaces
    trail_surfaces = None

def draw(screen, etc):
    global phase, trail_surfaces
    w, h = screen.get_width(), screen.get_height()

    # Initialize trail surface
    if trail_surfaces is None:
        trail_surfaces = pygame.Surface((w, h), pygame.SRCALPHA)

    # Fade trail
    bg = etc.color_picker_bg(etc.knob5)
    fade = pygame.Surface((w, h), pygame.SRCALPHA)
    fade.fill((*bg, 25))
    screen.blit(fade, (0, 0))

    peak = abs(etc.audio_peak) / 32768.0
    phase += 0.02 + peak * 0.03

    dot_size = int(etc.knob1 * 4) + 1
    wave_count = int(etc.knob2 * 4) + 1
    scatter = etc.knob3 * 30

    for wave in range(wave_count):
        wt = wave / wave_count
        y_base = h * (0.15 + wt * 0.7)
        color = etc.color_picker((wt * 0.35 + etc.knob4) % 1.0)

        step = dot_size * 2 + 1
        for x in range(0, w, step):
            xt = x / w
            idx = min(int(xt * 99), 99)
            audio_val = etc.audio_in[idx] / 32768.0

            y = y_base + audio_val * 120
            y += math.sin(xt * 3 + phase + wave * 2.1) * 20

            # Scatter
            if scatter > 0:
                sx = random.gauss(0, scatter * abs(audio_val) * 0.3)
                sy = random.gauss(0, scatter * abs(audio_val) * 0.3)
            else:
                sx = 0
                sy = 0

            dx = int(x + sx)
            dy = int(y + sy)

            if 0 <= dx < w and 0 <= dy < h:
                # Brightness based on audio
                brightness = 0.4 + abs(audio_val) * 0.6
                c = (int(color[0] * brightness), int(color[1] * brightness), int(color[2] * brightness))

                if dot_size <= 1:
                    screen.set_at((dx, dy), c)
                else:
                    pygame.draw.circle(screen, c, (dx, dy), dot_size)

                # White hot center on loud samples
                if abs(audio_val) > 0.4:
                    pygame.draw.circle(screen, (255, 255, 255), (dx, dy), max(1, dot_size - 1))
