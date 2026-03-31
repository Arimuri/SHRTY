# ITBS - Letter Scatter
# Letters scatter on beat and rubber-band back to home (iytm style)
# Knob1: scatter force, Knob2: home pull strength, Knob3: letter size
# Knob4: foreground color, Knob5: background color
import pygame
import math
import random

letters = []
last_beat_frame = 0
beat_intensity = 0
prev_peak = 0

def setup(screen, etc):
    global letters
    w, h = screen.get_width(), screen.get_height()

    chars = [
        {'ch': 'S', 'hx': 0.30, 'hy': 0.35},
        {'ch': 'H', 'hx': 0.43, 'hy': 0.40},
        {'ch': 'R', 'hx': 0.57, 'hy': 0.38},
        {'ch': 'T', 'hx': 0.70, 'hy': 0.42},
        {'ch': 'Y', 'hx': 0.50, 'hy': 0.65},
    ]
    letters = []
    for c in chars:
        letters.append({
            'ch': c['ch'],
            'hx': c['hx'] * w, 'hy': c['hy'] * h,
            'x': c['hx'] * w, 'y': c['hy'] * h,
            'vx': 0, 'vy': 0,
            'rot': 0, 'scale': 1.0,
        })

def draw(screen, etc):
    global letters, last_beat_frame, beat_intensity, prev_peak
    if not letters:
        setup(screen, etc)

    w, h = screen.get_width(), screen.get_height()

    # Background color from palette (semi-transparent for trails)
    bg = etc.color_picker_bg(etc.knob5)
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((*bg, 25))
    screen.blit(overlay, (0, 0))

    peak = abs(etc.audio_peak) / 32768.0
    onset = peak - prev_peak
    prev_peak = peak

    # Beat detection
    beat_hit = False
    if onset > 0.08 and etc.frame_count - last_beat_frame > 3:
        beat_hit = True
        last_beat_frame = etc.frame_count
        beat_intensity = max(peak, onset * 3, 0.5)

    beat_intensity *= 0.65

    scatter_force = etc.knob1 * 400 + 50
    home_pull = etc.knob2 * 0.01 + 0.002
    font_size = int(etc.knob3 * 120) + 60
    glow_extra = 30

    font_main = pygame.font.Font(None, font_size)
    font_glow = pygame.font.Font(None, font_size + glow_extra)

    t = etc.frame_count * 0.02

    for lt in letters:
        # Rotation & scale decay
        lt['rot'] *= 0.7
        lt['scale'] += (1.0 - lt['scale']) * 0.3

        if beat_hit:
            angle = random.uniform(0, math.pi * 2)
            kick = scatter_force * beat_intensity * random.uniform(0.4, 1.3)

            if beat_intensity > 0.6:
                # Hard snap
                lt['x'] += math.cos(angle) * kick
                lt['y'] += math.sin(angle) * kick
                lt['vx'] = 0
                lt['vy'] = 0
            else:
                lt['vx'] += math.cos(angle) * kick * 0.4
                lt['vy'] += math.sin(angle) * kick * 0.4

            lt['rot'] = random.uniform(-0.5, 0.5) * beat_intensity
            lt['scale'] = 1.0 + beat_intensity * 0.6

        # Constrain
        lt['x'] = max(20, min(w - 20, lt['x']))
        lt['y'] = max(20, min(h - 20, lt['y']))

        # Rubber band home
        dx = lt['hx'] - lt['x']
        dy = lt['hy'] - lt['y']
        dist = math.sqrt(dx * dx + dy * dy)
        force = home_pull + dist * 0.00005
        lt['vx'] += dx * force
        lt['vy'] += dy * force

        # Micro orbit
        lt['vx'] += math.sin(t * 0.5 + hash(lt['ch'])) * 0.1
        lt['vy'] += math.cos(t * 0.4 + hash(lt['ch'])) * 0.08

        # Damping
        lt['vx'] *= 0.85
        lt['vy'] *= 0.85

        lt['x'] += lt['vx']
        lt['y'] += lt['vy']

        # Draw glow
        color = etc.color_picker(etc.knob4)
        glow_surf = font_glow.render(lt['ch'], True, (color[0], color[1], color[2]))
        glow_surf.set_alpha(int(40 + beat_intensity * 80))
        gr = glow_surf.get_rect(center=(int(lt['x']), int(lt['y'])))
        screen.blit(glow_surf, gr)

        # Draw letter
        main_surf = font_main.render(lt['ch'], True, (255, 255, 255))
        main_surf.set_alpha(int(200 + beat_intensity * 55))
        mr = main_surf.get_rect(center=(int(lt['x']), int(lt['y'])))
        screen.blit(main_surf, mr)

    # Dotted connections between adjacent letters
    if len(letters) >= 2:
        conn_colors = [(30, 40, 120), (210, 85, 55), (50, 180, 80), (180, 60, 180)]
        for i in range(len(letters) - 1):
            a = letters[i]
            b = letters[i + 1]
            col = conn_colors[i % len(conn_colors)]
            bright = min(255, int(col[0] + peak * 60)), min(255, int(col[1] + peak * 60)), min(255, int(col[2] + peak * 60))
            dx = b['x'] - a['x']
            dy = b['y'] - a['y']
            dist = math.sqrt(dx * dx + dy * dy)
            if dist > 0:
                steps = int(dist / 8)
                for s in range(0, steps, 2):
                    t_frac = s / max(steps, 1)
                    px = int(a['x'] + dx * t_frac)
                    py = int(a['y'] + dy * t_frac)
                    pygame.draw.circle(screen, bright, (px, py), 2)
