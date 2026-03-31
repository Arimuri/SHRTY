# T - Emoji Party
# 顔文字が飛び出すパーティーモード！
# ASCII emoticons explode out on trigger!
#
# Knob1: 出現数
# Knob2: サイズ
# Knob3: 重力
# Knob4: 前景色
# Knob5: 背景色

import pygame
import random
import math

# 顔文字セット
EMOJI_SETS = [
    [":)", ":D", "=)", "^_^", "\\o/", ":3", "=D", ";)", "xD", ":>"],
    [":(", ":'(", "T_T", ";_;", "D:", ":<", "=(", "._.", "-_-", ":/"],
    ["XD", ">:D", "8D", "=P", ":P", "x_x", "@_@", "O_O", "*_*", "0_0"],
    ["B)", "8)", ";)", "=]", ":]", ":}", "=}", ";]", "8]", "B]"],
    ["<3", "**", "!!", "??", "~*~", "*~*", "o/", "\\o", "\\o/", "***"],
]

SET_NAMES = ["happy", "sad", "crazy", "cool", "symbols"]

active = []
font_cache = {}
info_font = None
MAX_COUNT = 50
current_set_idx = 0

def get_font(size):
    if size not in font_cache:
        font_cache[size] = pygame.font.Font(None, size)
    return font_cache[size]

def setup(screen, eyesy):
    global active, font_cache, info_font
    font_cache = {}
    for size in [36, 48, 64, 80, 96]:
        font_cache[size] = pygame.font.Font(None, size)
    info_font = pygame.font.Font(None, 36)
    active = []

def draw(screen, eyesy):
    global active, current_set_idx
    
    # 背景
    eyesy.color_picker_bg(eyesy.knob5)
    
    # Knob1: 出現数
    spawn_count = int(1 + eyesy.knob1 * 10)
    
    # Knob2: サイズ
    base_size = int(36 + eyesy.knob2 * 60)
    size_snap = min([36, 48, 64, 80, 96], key=lambda x: abs(x - base_size))
    
    # Knob3: 重力
    gravity = eyesy.knob3 * 0.5
    
    # オーディオレベル
    audio_level = max(abs(min(eyesy.audio_in)), abs(max(eyesy.audio_in))) / 32768.0
    
    # トリガーで追加
    if eyesy.trig:
        center_x = eyesy.xres / 2
        center_y = eyesy.yres / 2
        current_set_idx = random.randint(0, len(EMOJI_SETS) - 1)
        current_set = EMOJI_SETS[current_set_idx]
        
        for _ in range(min(spawn_count, MAX_COUNT - len(active))):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(5, 15)
            
            active.append([
                center_x,                          # 0: x
                center_y,                          # 1: y
                math.cos(angle) * speed,           # 2: vx
                math.sin(angle) * speed,           # 3: vy
                random.choice(current_set),        # 4: text
                150,                               # 5: life
                random.uniform(-0.15, 0.15),       # 6: color offset
            ])
    
    font = get_font(size_snap)
    
    # 更新と描画
    next_active = []
    
    for e in active:
        # 物理更新
        e[3] += gravity
        e[0] += e[2]
        e[1] += e[3]
        
        # 壁反射
        if e[0] < 30 or e[0] > eyesy.xres - 30:
            e[2] *= -0.8
        if e[1] > eyesy.yres - 30:
            e[3] *= -0.7
            e[1] = eyesy.yres - 30
        
        # オーディオで跳ねる
        if audio_level > 0.6 and e[1] > eyesy.yres - 100:
            e[3] = -abs(e[3]) - audio_level * 5
        
        e[5] -= 1
        
        if e[5] > 0:
            # 毎フレームKnob4を参照
            color_pos = (eyesy.knob4 + e[6]) % 1.0
            color = eyesy.color_picker(color_pos)
            
            surf = font.render(e[4], True, color)
            rect = surf.get_rect(center=(int(e[0]), int(e[1])))
            screen.blit(surf, rect)
            next_active.append(e)
    
    active = next_active
    
    # 左上に情報表示
    color = eyesy.color_picker(eyesy.knob4)
    set_text = info_font.render(f"Set: {SET_NAMES[current_set_idx]}", True, (255, 255, 255))
    screen.blit(set_text, (20, 20))
    
    # オーディオバー
    bar_width = int(audio_level * 200)
    pygame.draw.rect(screen, color, (20, 60, bar_width, 20))
    pygame.draw.rect(screen, (255, 255, 255), (20, 60, 200, 20), 2)
