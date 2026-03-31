# S - DVD Bounce
# あのDVDの待機画面のパロディ！コーナーにヒットすると色が変わる
# The classic DVD screensaver parody! Color changes when it hits corners!
#
# Knob1: 速度
# Knob2: ロゴサイズ
# Knob3: トレイルの長さ
# Knob4: 前景色
# Knob5: 背景色

import pygame
import random

# ロゴの状態
logo_x = 0
logo_y = 0
vel_x = 3
vel_y = 2
corner_hit_count = 0
hit_flash = 0
trail = []

font = None
big_font = None
initialized = False

def setup(screen, eyesy):
    global logo_x, logo_y, vel_x, vel_y, font, big_font, initialized, corner_hit_count
    
    logo_x = random.randint(100, int(eyesy.xres - 200))
    logo_y = random.randint(100, int(eyesy.yres - 100))
    
    font = pygame.font.Font(None, 72)
    big_font = pygame.font.Font(None, 200)
    
    corner_hit_count = 0
    initialized = True

def draw(screen, eyesy):
    global logo_x, logo_y, vel_x, vel_y, corner_hit_count, hit_flash
    global trail, font, big_font
    
    # 背景色
    eyesy.color_picker_bg(eyesy.knob5)
    
    # Knob4: 前景色
    color = eyesy.color_picker(eyesy.knob4)
    
    # Knob1: 速度
    speed = 1 + eyesy.knob1 * 8
    
    # Knob2: ロゴサイズ
    logo_scale = 0.5 + eyesy.knob2 * 1.5
    
    # Knob3: トレイルの長さ
    trail_length = int(eyesy.knob3 * 30)
    
    # オーディオで速度変動
    audio_level = max(abs(min(eyesy.audio_in)), abs(max(eyesy.audio_in))) / 32768.0
    audio_boost = 1 + audio_level * 2
    
    # ロゴテキストをレンダリング
    scaled_font = pygame.font.Font(None, int(72 * logo_scale))
    
    logo_text = "DVD"
    logo_surface = scaled_font.render(logo_text, True, color)
    logo_width = logo_surface.get_width()
    logo_height = logo_surface.get_height()
    
    # 位置を更新
    current_speed = speed * audio_boost
    logo_x += vel_x * current_speed
    logo_y += vel_y * current_speed
    
    # 壁との衝突チェック
    hit_x = False
    hit_y = False
    
    if logo_x <= 0:
        logo_x = 0
        vel_x = abs(vel_x)
        hit_x = True
    elif logo_x + logo_width >= eyesy.xres:
        logo_x = eyesy.xres - logo_width
        vel_x = -abs(vel_x)
        hit_x = True
        
    if logo_y <= 0:
        logo_y = 0
        vel_y = abs(vel_y)
        hit_y = True
    elif logo_y + logo_height >= eyesy.yres:
        logo_y = eyesy.yres - logo_height
        vel_y = -abs(vel_y)
        hit_y = True
    
    # コーナーヒット！！！
    if hit_x and hit_y:
        corner_hit_count += 1
        hit_flash = 30
    
    # トレイルを保存
    if trail_length > 0:
        trail.append((logo_x, logo_y, color))
        while len(trail) > trail_length:
            trail.pop(0)
    else:
        trail = []
    
    # トレイルを描画（薄く）
    for i, (tx, ty, tc) in enumerate(trail):
        alpha = int((i / len(trail)) * 100) if trail else 0
        faded_color = tuple(int(c * alpha / 255) for c in tc)
        trail_surface = scaled_font.render(logo_text, True, faded_color)
        screen.blit(trail_surface, (int(tx), int(ty)))
    
    # メインロゴを描画
    screen.blit(logo_surface, (int(logo_x), int(logo_y)))
    
    # コーナーヒット時のフラッシュ効果
    if hit_flash > 0:
        hit_flash -= 1
        
        flash_surface = pygame.Surface((int(eyesy.xres), int(eyesy.yres)))
        flash_alpha = min(255, hit_flash * 8)
        flash_surface.fill((255, 255, 255))
        flash_surface.set_alpha(flash_alpha)
        screen.blit(flash_surface, (0, 0))
        
        if hit_flash > 15:
            hit_text = big_font.render("CORNER!", True, (255, 255, 0))
            text_rect = hit_text.get_rect(center=(eyesy.xres/2, eyesy.yres/2))
            screen.blit(hit_text, text_rect)
    
    # ヒットカウンターを表示（右上）
    counter_text = font.render(f"Corners: {corner_hit_count}", True, color)
    screen.blit(counter_text, (int(eyesy.xres - counter_text.get_width() - 20), 20))
