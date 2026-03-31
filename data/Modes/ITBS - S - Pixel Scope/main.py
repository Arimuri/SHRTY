# ITBS - S - Pixel Scope
# 太ピクセルで波形を描画するレトロポップなオシロスコープ
# Chunky pixel waveform display — retro meets pop
#
# Knob1: ピクセルサイズ
# Knob2: 波形の高さ
# Knob3: ミラー (左右対称度)
# Knob4: foreground color
# Knob5: background color

import pygame
import math

def setup(screen, etc):
    pass

def draw(screen, etc):
    w, h = screen.get_width(), screen.get_height()

    etc.color_picker_bg(etc.knob5)

    peak = abs(etc.audio_peak) / 32768.0
    pix = int(etc.knob1 * 24) + 4
    amp = etc.knob2 * 250 + 50
    mirror = etc.knob3

    cols = w // pix

    for col in range(cols):
        ct = col / cols
        idx = min(int(ct * 99), 99)
        audio_val = etc.audio_in[idx] / 32768.0

        # Color: gradient across width
        color = etc.color_picker((ct * 0.3 + etc.knob4) % 1.0)

        # Bar height from audio
        bar_h = abs(audio_val) * amp

        x = col * pix
        cy = h // 2

        # Main bar (center-out)
        top = int(cy - bar_h * 0.5)
        bot = int(cy + bar_h * 0.5)
        rect_h = max(pix, bot - top)

        pygame.draw.rect(screen, color, (x, top, pix - 1, rect_h))

        # Highlight on top pixel
        if rect_h > pix:
            pygame.draw.rect(screen, (255, 255, 255), (x, top, pix - 1, pix))

        # Mirror: draw flipped copy with fade
        if mirror > 0.1:
            alpha = int(mirror * 120)
            mirror_surf = pygame.Surface((pix - 1, rect_h), pygame.SRCALPHA)
            mirror_surf.fill((*color, alpha))

            # Top mirror
            screen.blit(mirror_surf, (x, top - rect_h - 4))
            # Bottom mirror
            screen.blit(mirror_surf, (x, bot + 4))

    # Center line
    line_alpha = int(60 + peak * 80)
    line_surf = pygame.Surface((w, 2), pygame.SRCALPHA)
    line_surf.fill((*etc.color_picker(etc.knob4), line_alpha))
    screen.blit(line_surf, (0, h // 2 - 1))
