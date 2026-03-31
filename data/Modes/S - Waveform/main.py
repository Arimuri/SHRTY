# S - Waveform
# Classic oscilloscope-style waveform display
# Knob1: amplitude, Knob2: color, Knob3: thickness, Knob4: y-position, Knob5: mirror
import pygame

def setup(screen, etc):
    pass

def draw(screen, etc):
    screen.fill(etc.bg_color)

    w = screen.get_width()
    h = screen.get_height()
    amp = etc.knob1 * 3 + 0.5
    thickness = int(etc.knob3 * 8) + 1
    y_center = int(etc.knob4 * h)

    color = etc.color_picker(etc.knob2)

    # Draw waveform from audio buffer
    points = []
    buf_len = len(etc.audio_in)
    for i in range(w):
        buf_idx = int(i * buf_len / w)
        if buf_idx >= buf_len:
            buf_idx = buf_len - 1
        val = etc.audio_in[buf_idx] / 32768.0
        y = int(y_center + val * h * 0.4 * amp)
        y = max(0, min(h - 1, y))
        points.append((i, y))

    if len(points) > 1:
        pygame.draw.lines(screen, color, False, points, thickness)

    # Mirror
    if etc.knob5 > 0.5:
        points_mirror = [(x, 2 * y_center - y) for x, y in points]
        color2 = etc.color_picker(etc.knob2 + 0.5)
        if len(points_mirror) > 1:
            pygame.draw.lines(screen, color2, False, points_mirror, thickness)
