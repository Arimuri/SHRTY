# S - Derpy Dog
# オーディオに反応するアホ犬
# A derpy dog that reacts to audio!
#
# Knob1: 犬のサイズ
# Knob2: 反応の感度
# Knob3: 揺れの強さ
# Knob4: 前景色（吐き出し要素）
# Knob5: 背景色

import pygame
import math
import random

# 状態変数
tongue_out = 0
eye_derp = 0
tail_wag = 0
shake_x = 0
shake_y = 0
pant_frame = 0
drool_drops = []
bark_particles = []
ear_momentum_l = 0
ear_momentum_r = 0
ear_angle_l = 0
ear_angle_r = 0
prev_shake_x = 0

# 犬の色（茶色固定）
DOG_COLOR = (180, 120, 60)

class DroolDrop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = 2
        self.life = 50
        self.offset = random.uniform(-0.1, 0.1)
        
    def update(self):
        self.y += self.vy
        self.vy += 0.15
        self.life -= 1
        return self.life > 0

class BarkParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(-0.5, 0.5)
        speed = random.uniform(3, 8)
        self.vx = math.cos(angle) * speed
        self.vy = -abs(math.sin(angle) * speed) - 2
        self.life = 25
        self.text = random.choice(["WOOF", "BARK", "ARF", "BORK", "WAF", "YAP"])
        self.offset = random.uniform(-0.15, 0.15)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.life -= 1
        return self.life > 0

bark_font = None
exp_font = None
title_font = None

def setup(screen, eyesy):
    global drool_drops, bark_particles, bark_font, exp_font, title_font
    global ear_momentum_l, ear_momentum_r, ear_angle_l, ear_angle_r
    bark_font = pygame.font.Font(None, 48)
    exp_font = pygame.font.Font(None, 64)
    title_font = pygame.font.Font(None, 72)
    drool_drops = []
    bark_particles = []
    ear_momentum_l = 0
    ear_momentum_r = 0
    ear_angle_l = 0
    ear_angle_r = 0

def draw(screen, eyesy):
    global tongue_out, eye_derp, tail_wag, shake_x, shake_y
    global pant_frame, drool_drops, bark_particles, prev_shake_x
    global ear_momentum_l, ear_momentum_r, ear_angle_l, ear_angle_r
    
    pant_frame += 1
    
    # 背景
    eyesy.color_picker_bg(eyesy.knob5)
    
    # Knob1: サイズ（大きく）
    dog_scale = 0.6 + eyesy.knob1 * 0.8
    
    # Knob2: 感度
    sensitivity = 0.5 + eyesy.knob2 * 1.5
    
    # Knob3: 揺れ
    shake_intensity = eyesy.knob3
    
    # オーディオレベル
    audio_level = max(abs(min(eyesy.audio_in)), abs(max(eyesy.audio_in))) / 32768.0
    audio_level = min(1.0, audio_level * sensitivity)
    
    # 中心位置
    center_x = eyesy.xres / 2 + 50
    center_y = eyesy.yres / 2
    
    # 状態更新
    tongue_out += (audio_level - tongue_out) * 0.3
    tail_wag = math.sin(pant_frame * 0.3) * (0.5 + audio_level * 0.5)
    eye_derp = audio_level * 0.5
    
    # 揺れ
    prev_shake_x = shake_x
    if audio_level > 0.4:
        shake_x = random.uniform(-15, 15) * shake_intensity * audio_level
        shake_y = random.uniform(-15, 15) * shake_intensity * audio_level
    else:
        shake_x *= 0.8
        shake_y *= 0.8
    
    # 耳の物理演算
    shake_delta = shake_x - prev_shake_x
    ear_momentum_l += -shake_delta * 0.3 + random.uniform(-0.5, 0.5) * audio_level
    ear_momentum_r += -shake_delta * 0.3 + random.uniform(-0.5, 0.5) * audio_level
    ear_momentum_l *= 0.85
    ear_momentum_r *= 0.85
    ear_angle_l += ear_momentum_l
    ear_angle_r += ear_momentum_r
    ear_angle_l *= 0.9
    ear_angle_r *= 0.9
    
    draw_x = center_x + shake_x
    draw_y = center_y + shake_y
    
    # サイズ
    head_size = int(200 * dog_scale)
    body_w = int(220 * dog_scale)
    body_h = int(150 * dog_scale)
    
    # しっぽ
    tail_x = draw_x - head_size * 0.5 - body_w * 0.8
    tail_y = draw_y + body_h * 0.2
    tail_end_x = tail_x - 60 * dog_scale + math.sin(pant_frame * 0.4) * 40 * dog_scale
    tail_end_y = tail_y - 60 * dog_scale * (1 + tail_wag)
    pygame.draw.line(screen, DOG_COLOR, 
                    (int(tail_x), int(tail_y)),
                    (int(tail_end_x), int(tail_end_y)), 
                    int(15 * dog_scale))
    
    # 体（四角）
    body_rect = pygame.Rect(
        int(draw_x - head_size * 0.5 - body_w),
        int(draw_y - body_h * 0.3),
        body_w,
        body_h
    )
    pygame.draw.rect(screen, DOG_COLOR, body_rect, border_radius=int(20 * dog_scale))
    pygame.draw.rect(screen, (0, 0, 0), body_rect, 3, border_radius=int(20 * dog_scale))
    
    # 顔（四角）
    head_rect = pygame.Rect(
        int(draw_x - head_size * 0.5),
        int(draw_y - head_size * 0.5),
        head_size,
        head_size
    )
    pygame.draw.rect(screen, DOG_COLOR, head_rect, border_radius=int(25 * dog_scale))
    pygame.draw.rect(screen, (0, 0, 0), head_rect, 3, border_radius=int(25 * dog_scale))
    
    # 耳（ぶらぶら四角）
    ear_w = int(45 * dog_scale)
    ear_h = int(90 * dog_scale)
    
    # 左耳
    ear_l_x = draw_x - head_size * 0.5 - ear_w * 0.3
    ear_l_y = draw_y - head_size * 0.3
    ear_l_surface = pygame.Surface((ear_w * 2, ear_h * 2), pygame.SRCALPHA)
    pygame.draw.rect(ear_l_surface, DOG_COLOR, (ear_w//2, 0, ear_w, ear_h), border_radius=int(10 * dog_scale))
    pygame.draw.rect(ear_l_surface, (0, 0, 0), (ear_w//2, 0, ear_w, ear_h), 3, border_radius=int(10 * dog_scale))
    ear_l_rot = pygame.transform.rotate(ear_l_surface, ear_angle_l * 3)
    ear_l_rect = ear_l_rot.get_rect(center=(int(ear_l_x), int(ear_l_y + ear_h * 0.4)))
    screen.blit(ear_l_rot, ear_l_rect)
    
    # 右耳
    ear_r_x = draw_x + head_size * 0.5 + ear_w * 0.3
    ear_r_y = draw_y - head_size * 0.3
    ear_r_surface = pygame.Surface((ear_w * 2, ear_h * 2), pygame.SRCALPHA)
    pygame.draw.rect(ear_r_surface, DOG_COLOR, (ear_w//2, 0, ear_w, ear_h), border_radius=int(10 * dog_scale))
    pygame.draw.rect(ear_r_surface, (0, 0, 0), (ear_w//2, 0, ear_w, ear_h), 3, border_radius=int(10 * dog_scale))
    ear_r_rot = pygame.transform.rotate(ear_r_surface, ear_angle_r * 3)
    ear_r_rect = ear_r_rot.get_rect(center=(int(ear_r_x), int(ear_r_y + ear_h * 0.4)))
    screen.blit(ear_r_rot, ear_r_rect)
    
    # 目（アホっぽく左右非対称）
    eye_offset_x = head_size * 0.25
    eye_offset_y = -head_size * 0.05
    eye_radius = int(head_size * 0.15)
    
    # 左目
    left_eye_x = draw_x - eye_offset_x
    left_eye_y = draw_y + eye_offset_y
    pygame.draw.circle(screen, (255, 255, 255), (int(left_eye_x), int(left_eye_y)), eye_radius)
    pygame.draw.circle(screen, (0, 0, 0), (int(left_eye_x), int(left_eye_y)), eye_radius, 2)
    pygame.draw.circle(screen, (0, 0, 0), 
                      (int(left_eye_x - eye_derp * 10), int(left_eye_y - eye_radius * 0.3)), 
                      int(eye_radius * 0.5))
    
    # 右目
    right_eye_x = draw_x + eye_offset_x
    right_eye_y = draw_y + eye_offset_y
    pygame.draw.circle(screen, (255, 255, 255), (int(right_eye_x), int(right_eye_y)), eye_radius)
    pygame.draw.circle(screen, (0, 0, 0), (int(right_eye_x), int(right_eye_y)), eye_radius, 2)
    pygame.draw.circle(screen, (0, 0, 0), 
                      (int(right_eye_x + eye_derp * 15), int(right_eye_y + eye_derp * 5)), 
                      int(eye_radius * 0.5))
    
    # 鼻
    nose_y = draw_y + head_size * 0.2
    nose_size = int(head_size * 0.12)
    pygame.draw.ellipse(screen, (30, 30, 30), 
                       (int(draw_x - nose_size), int(nose_y - nose_size * 0.5),
                        int(nose_size * 2), int(nose_size)))
    
    # 口と舌
    mouth_y = nose_y + nose_size
    mouth_width = head_size * 0.4
    
    pygame.draw.arc(screen, (0, 0, 0),
                   (int(draw_x - mouth_width/2), int(mouth_y - 15 * dog_scale),
                    int(mouth_width), int(30 * dog_scale)),
                   3.14, 0, 3)
    
    # 舌
    if tongue_out > 0.1:
        tongue_length = int(30 + tongue_out * 80) * dog_scale
        tongue_width = int(35 * dog_scale)
        tongue_x = draw_x + math.sin(pant_frame * 0.15) * 8
        
        pygame.draw.ellipse(screen, (255, 100, 120),
                           (int(tongue_x - tongue_width/2), int(mouth_y),
                            int(tongue_width), int(tongue_length)))
        pygame.draw.line(screen, (200, 80, 100),
                        (int(tongue_x), int(mouth_y + 8)),
                        (int(tongue_x), int(mouth_y + tongue_length - 10)), 2)
    
    # よだれ（パレット参照）
    if audio_level > 0.5 and random.random() > 0.7:
        drool_x = draw_x + mouth_width * 0.3 * random.choice([-1, 1])
        drool_drops.append(DroolDrop(drool_x, mouth_y + tongue_out * 35))
    
    alive_drops = []
    for drop in drool_drops:
        if drop.update():
            color_pos = (eyesy.knob4 + drop.offset) % 1.0
            drop_color = eyesy.color_picker(color_pos)
            drop_color = (min(255, drop_color[0] + 100), 
                         min(255, drop_color[1] + 100), 
                         min(255, drop_color[2] + 120))
            pygame.draw.ellipse(screen, drop_color,
                               (int(drop.x), int(drop.y), 6, 10))
            alive_drops.append(drop)
    drool_drops = alive_drops
    
    # 吠える（パレット参照）
    if eyesy.trig and audio_level > 0.3:
        for _ in range(3):
            bark_particles.append(BarkParticle(draw_x, mouth_y))
    
    alive_barks = []
    for p in bark_particles:
        if p.update():
            color_pos = (eyesy.knob4 + p.offset) % 1.0
            bark_color = eyesy.color_picker(color_pos)
            text = bark_font.render(p.text, True, bark_color)
            screen.blit(text, (int(p.x), int(p.y)))
            alive_barks.append(p)
    bark_particles = alive_barks
    
    # セリフ（犬の上）
    if audio_level > 0.8:
        expression = "BORK BORK!"
    elif audio_level > 0.5:
        expression = "*pant pant*"
    elif audio_level > 0.2:
        expression = "heck?"
    else:
        expression = "..."
    
    exp_text = exp_font.render(expression, True, (255, 255, 255))
    text_x = eyesy.xres / 2 - exp_text.get_width() / 2
    text_y = draw_y - head_size * 0.5 - 100
    screen.blit(exp_text, (int(text_x), int(text_y)))
    
    # タイトル（犬の下）
    title_text = title_font.render("Over Flow Dog", True, (255, 255, 255))
    title_x = eyesy.xres / 2 - title_text.get_width() / 2
    title_y = draw_y + head_size * 0.5 + 40
    screen.blit(title_text, (int(title_x), int(title_y)))
