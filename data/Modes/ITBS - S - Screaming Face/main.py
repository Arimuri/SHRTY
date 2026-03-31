# S - Screaming Face
# オーディオレベルに応じて表情が変わる顔！
# A face that changes expression based on audio level!
#
# Knob1: 顔のサイズ
# Knob2: 反応の感度
# Knob3: 揺れの強さ
# Knob4: 前景色
# Knob5: 背景色

import pygame
import math
import random

# 状態変数
mouth_open = 0
eye_size = 1.0
eyebrow_angle = 0
sweat_drops = []
shake_x = 0
shake_y = 0
scream_particles = []
frame_count = 0

class SweatDrop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = 2
        self.life = 60
        
    def update(self):
        self.y += self.vy
        self.vy += 0.2
        self.life -= 1
        return self.life > 0

class ScreamParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(-math.pi * 0.8, -math.pi * 0.2)
        speed = random.uniform(5, 15)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 30
        self.char = random.choice(['!', '?', '*', '#', '@'])
        self.offset = random.uniform(-0.15, 0.15)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3
        self.life -= 1
        return self.life > 0

font = None
exp_font = None

def setup(screen, eyesy):
    global sweat_drops, scream_particles, font, exp_font
    font = pygame.font.Font(None, 36)
    exp_font = pygame.font.Font(None, 64)
    sweat_drops = []
    scream_particles = []

def draw(screen, eyesy):
    global mouth_open, eye_size, eyebrow_angle, sweat_drops, shake_x, shake_y
    global scream_particles, frame_count
    
    frame_count += 1
    
    # 背景色
    eyesy.color_picker_bg(eyesy.knob5)
    
    # 顔の色
    face_color = eyesy.color_picker(eyesy.knob4)
    
    # Knob1: 顔のサイズ
    face_scale = 0.3 + eyesy.knob1 * 0.7
    
    # Knob2: 反応の感度
    sensitivity = 0.5 + eyesy.knob2 * 1.5
    
    # Knob3: 揺れの強さ
    shake_intensity = eyesy.knob3
    
    # オーディオレベル
    audio_level = max(abs(min(eyesy.audio_in)), abs(max(eyesy.audio_in))) / 32768.0
    audio_level = min(1.0, audio_level * sensitivity)
    
    # 顔の中心位置（少し上に）
    center_x = eyesy.xres / 2
    center_y = eyesy.yres / 2 - 50
    
    # 顔の状態を更新
    mouth_open += (audio_level - mouth_open) * 0.3
    eye_size += ((1.0 + audio_level * 0.5) - eye_size) * 0.2
    eyebrow_angle += (-audio_level * 30 - eyebrow_angle) * 0.2
    
    # 画面揺れ
    if audio_level > 0.5:
        shake_x = random.uniform(-20, 20) * shake_intensity * audio_level
        shake_y = random.uniform(-20, 20) * shake_intensity * audio_level
    else:
        shake_x *= 0.8
        shake_y *= 0.8
    
    draw_x = center_x + shake_x
    draw_y = center_y + shake_y
    face_radius = int(200 * face_scale)
    
    # 顔の輪郭
    pygame.draw.circle(screen, face_color, (int(draw_x), int(draw_y)), face_radius)
    pygame.draw.circle(screen, (0, 0, 0), (int(draw_x), int(draw_y)), face_radius, 3)
    
    # 目
    eye_offset_x = face_radius * 0.35
    eye_offset_y = face_radius * 0.2
    eye_radius = int(face_radius * 0.15 * eye_size)
    
    left_eye_x = draw_x - eye_offset_x
    left_eye_y = draw_y - eye_offset_y
    right_eye_x = draw_x + eye_offset_x
    right_eye_y = draw_y - eye_offset_y
    
    # 白目
    pygame.draw.circle(screen, (255, 255, 255), (int(left_eye_x), int(left_eye_y)), eye_radius)
    pygame.draw.circle(screen, (0, 0, 0), (int(left_eye_x), int(left_eye_y)), eye_radius, 2)
    pygame.draw.circle(screen, (255, 255, 255), (int(right_eye_x), int(right_eye_y)), eye_radius)
    pygame.draw.circle(screen, (0, 0, 0), (int(right_eye_x), int(right_eye_y)), eye_radius, 2)
    
    # 瞳
    pupil_offset_x = math.sin(frame_count * 0.1) * 3
    pupil_offset_y = audio_level * -5
    pygame.draw.circle(screen, (0, 0, 0), 
                      (int(left_eye_x + pupil_offset_x), int(left_eye_y + pupil_offset_y)), 
                      int(eye_radius * 0.4))
    pygame.draw.circle(screen, (0, 0, 0), 
                      (int(right_eye_x + pupil_offset_x), int(right_eye_y + pupil_offset_y)), 
                      int(eye_radius * 0.4))
    
    # 眉毛
    eyebrow_length = face_radius * 0.25
    eyebrow_y = draw_y - eye_offset_y - eye_radius - 10
    pygame.draw.line(screen, (0, 0, 0),
                    (int(left_eye_x - eyebrow_length), int(eyebrow_y + eyebrow_angle)),
                    (int(left_eye_x + eyebrow_length), int(eyebrow_y - eyebrow_angle)), 4)
    pygame.draw.line(screen, (0, 0, 0),
                    (int(right_eye_x - eyebrow_length), int(eyebrow_y - eyebrow_angle)),
                    (int(right_eye_x + eyebrow_length), int(eyebrow_y + eyebrow_angle)), 4)
    
    # 口
    mouth_y = draw_y + face_radius * 0.3
    mouth_width = face_radius * 0.6
    mouth_height = int(face_radius * 0.4 * mouth_open)
    
    if mouth_height > 5:
        mouth_rect = pygame.Rect(
            int(draw_x - mouth_width / 2),
            int(mouth_y - mouth_height / 2),
            int(mouth_width),
            mouth_height
        )
        pygame.draw.ellipse(screen, (50, 50, 50), mouth_rect)
        pygame.draw.ellipse(screen, (0, 0, 0), mouth_rect, 3)
        
        # 口の中の波形
        if mouth_height > 20:
            wave_points = []
            for i in range(50):
                idx = int(i * len(eyesy.audio_in) / 50)
                wave_x = draw_x - mouth_width / 2 + (i / 50) * mouth_width
                wave_y = mouth_y + (eyesy.audio_in[idx] / 32768.0) * mouth_height * 0.3
                wave_points.append((wave_x, wave_y))
            if len(wave_points) > 1:
                pygame.draw.lines(screen, (255, 100, 100), False, wave_points, 2)
    else:
        pygame.draw.line(screen, (0, 0, 0),
                        (int(draw_x - mouth_width / 2), int(mouth_y)),
                        (int(draw_x + mouth_width / 2), int(mouth_y)), 3)
    
    # 汗
    if audio_level > 0.7 and random.random() > 0.7:
        sweat_drops.append(SweatDrop(draw_x + face_radius + random.randint(-10, 10),
                                      draw_y - face_radius * 0.5))
    
    alive_drops = []
    for drop in sweat_drops:
        if drop.update():
            pygame.draw.ellipse(screen, (100, 200, 255),
                               (int(drop.x), int(drop.y), 8, 12))
            alive_drops.append(drop)
    sweat_drops = alive_drops
    
    # 叫びパーティクル（パレット参照）
    if eyesy.trig and audio_level > 0.3:
        for _ in range(5):
            scream_particles.append(ScreamParticle(draw_x, mouth_y))
    
    alive_particles = []
    for p in scream_particles:
        if p.update():
            color_pos = (eyesy.knob4 + p.offset) % 1.0
            particle_color = eyesy.color_picker(color_pos)
            text = font.render(p.char, True, particle_color)
            screen.blit(text, (int(p.x), int(p.y)))
            alive_particles.append(p)
    scream_particles = alive_particles
    
    # 表情テキスト（顔の下に配置）
    if audio_level > 0.8:
        expression = "AAAAA!"
    elif audio_level > 0.5:
        expression = "whoa!"
    elif audio_level > 0.2:
        expression = "hmm"
    else:
        expression = "..."
    
    exp_text = exp_font.render(expression, True, (255, 255, 255))
    text_x = eyesy.xres / 2 - exp_text.get_width() / 2
    text_y = draw_y + face_radius + 40
    screen.blit(exp_text, (int(text_x), int(text_y)))
