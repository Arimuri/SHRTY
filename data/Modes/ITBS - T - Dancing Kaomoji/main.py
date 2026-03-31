# T - Dancing Kaomoji
# ふざけた顔文字がオーディオトリガーで踊り出す！（軽量版）
# Silly Japanese emoticons dance to audio triggers! (Lightweight)
#
# Knob1: 出現数 (1-5個)
# Knob2: サイズ (小-大)
# Knob3: 重力 (ふわふわ-ずっしり)
# Knob4: 前景色 (パレット内でバラつき)
# Knob5: 背景色

import pygame
import random

# 顔文字コレクション
KAOMOJI = [
    "(^_^)", "(T_T)", "(o_o)", "(@_@)", "(>_<)",
    "(*_*)", "(~_~)", "(._. )", "\\(^o^)/", "d(^_^)b",
    "m(_ _)m", "(-_-)", "(^_~)", "(O_O)", "(x_x)",
    "('_')", "(;_;)", "(^o^)", "(._.)~", "(^-^)",
]

font_cache = {}
active = []
MAX_COUNT = 25

def get_font(size):
    if size not in font_cache:
        font_cache[size] = pygame.font.Font(None, size)
    return font_cache[size]

def setup(screen, eyesy):
    global active, font_cache
    font_cache = {}
    for size in [32, 48, 64, 80, 96]:
        font_cache[size] = pygame.font.Font(None, size)
    active = []

def draw(screen, eyesy):
    global active
    
    # 背景
    eyesy.color_picker_bg(eyesy.knob5)
    
    # Knob1: 出現数 (1-5)
    spawn_count = int(eyesy.knob1 * 4) + 1
    
    # Knob2: サイズ (32-96)
    base_size = int(32 + eyesy.knob2 * 64)
    size_snap = min([32, 48, 64, 80, 96], key=lambda x: abs(x - base_size))
    
    # Knob3: 重力 (0.05-0.5)
    grav = 0.05 + eyesy.knob3 * 0.45
    
    # トリガーで追加
    if eyesy.trig:
        for _ in range(min(spawn_count, MAX_COUNT - len(active))):
            active.append([
                random.randint(100, int(eyesy.xres - 100)),  # 0: x
                random.randint(50, int(eyesy.yres - 300)),   # 1: y
                random.uniform(-4, 4),                        # 2: vx
                random.uniform(-10, -5),                      # 3: vy
                random.choice(KAOMOJI),                       # 4: text
                100,                                          # 5: life
                random.uniform(-0.15, 0.15),                  # 6: color offset
            ])
    
    font = get_font(size_snap)
    
    # 更新と描画
    next_active = []
    
    for k in active:
        # 物理更新
        k[3] += grav
        k[0] += k[2]
        k[1] += k[3]
        
        # 壁反射
        if k[0] < 30 or k[0] > eyesy.xres - 30:
            k[2] *= -0.8
            k[0] = max(30, min(eyesy.xres - 30, k[0]))
        if k[1] > eyesy.yres - 30:
            k[3] *= -0.65
            k[1] = eyesy.yres - 30
        
        k[5] -= 1
        
        if k[5] > 0:
            # 毎フレームKnob4を参照して色を決定
            color_pos = (eyesy.knob4 + k[6]) % 1.0
            color = eyesy.color_picker(color_pos)
            
            surf = font.render(k[4], True, color)
            rect = surf.get_rect(center=(int(k[0]), int(k[1])))
            screen.blit(surf, rect)
            next_active.append(k)
    
    active = next_active
