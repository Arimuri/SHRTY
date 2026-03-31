# S - Silly Matrix
# マトリックス風だけど、ふざけた文字が降ってくる
# Matrix rain but with silly characters instead of code!
#
# Knob1: 密度
# Knob2: 文字サイズ
# Knob3: 残像の強さ
# Knob4: 前景色
# Knob5: 背景色

import pygame
import random

# ASCII文字セット
SILLY_CHARS = [
    "(", ")", "^", "_", "o", "O", "@", "*", "-", "~",
    "1", "3", "7", "4", "0", "5", "8", "9",
    "!", "?", "#", "$", "%", "&", "+", "=",
    "x", "X", "W", "w", "M", "m", "V", "v", "Z", "z",
]

class MatrixColumn:
    def __init__(self, x, yres, char_height):
        self.x = x
        self.y = random.randint(-500, 0)
        self.yres = yres
        self.char_height = char_height
        self.speed = random.uniform(5, 15)
        self.length = random.randint(5, 25)
        self.chars = [random.choice(SILLY_CHARS) for _ in range(self.length)]
        self.change_timer = 0
        
    def update(self, audio_level):
        current_speed = self.speed * (1 + audio_level * 2)
        self.y += current_speed
        
        self.change_timer += 1
        if self.change_timer > 3:
            self.change_timer = 0
            idx = random.randint(0, len(self.chars) - 1)
            self.chars[idx] = random.choice(SILLY_CHARS)
        
        if self.y - self.length * self.char_height > self.yres:
            self.y = random.randint(-300, -50)
            self.speed = random.uniform(5, 15)
            self.length = random.randint(5, 25)
            self.chars = [random.choice(SILLY_CHARS) for _ in range(self.length)]

columns = []
font_cache = {}
initialized = False

def get_font(size):
    if size not in font_cache:
        font_cache[size] = pygame.font.Font(None, size)
    return font_cache[size]

def setup(screen, eyesy):
    global columns, font_cache, initialized
    font_cache = {}
    for size in [16, 24, 32, 40, 48]:
        font_cache[size] = pygame.font.Font(None, size)
    columns = []
    initialized = False

def draw(screen, eyesy):
    global columns, initialized
    
    # Knob1: 密度
    density = int(5 + eyesy.knob1 * 30)
    
    # Knob2: 文字サイズ
    char_size = int(16 + eyesy.knob2 * 32)
    size_snap = min([16, 24, 32, 40, 48], key=lambda x: abs(x - char_size))
    char_height = size_snap + 2
    
    # Knob3: 残像の強さ
    trail_alpha = int((1 - eyesy.knob3) * 50 + 10)
    
    # Knob4: 前景色（パレットから）
    color = eyesy.color_picker(eyesy.knob4)
    
    # 初期化
    if not initialized or len(columns) != density:
        columns = []
        spacing = eyesy.xres / density
        for i in range(density):
            x = int(i * spacing + spacing / 2)
            columns.append(MatrixColumn(x, eyesy.yres, char_height))
        initialized = True
    
    # オーディオレベル
    audio_level = max(abs(min(eyesy.audio_in)), abs(max(eyesy.audio_in))) / 32768.0
    
    # 残像効果
    overlay = pygame.Surface((int(eyesy.xres), int(eyesy.yres)))
    overlay.fill(eyesy.color_picker_bg(eyesy.knob5) or (0, 0, 0))
    overlay.set_alpha(trail_alpha)
    screen.blit(overlay, (0, 0))
    
    font = get_font(size_snap)
    
    # 描画
    for col in columns:
        col.update(audio_level)
        
        for i, char in enumerate(col.chars):
            char_y = int(col.y - i * char_height)
            
            if 0 <= char_y <= eyesy.yres:
                brightness = 1.0 - (i / col.length)
                
                if i == 0:
                    char_color = (255, 255, 255)
                else:
                    char_color = (
                        int(color[0] * brightness),
                        int(color[1] * brightness),
                        int(color[2] * brightness)
                    )
                
                text = font.render(char, True, char_color)
                screen.blit(text, (col.x, char_y))
    
    # トリガーでフラッシュ
    if eyesy.trig:
        for col in columns:
            col.chars = [random.choice(SILLY_CHARS) for _ in range(col.length)]
        flash = pygame.Surface((int(eyesy.xres), int(eyesy.yres)))
        flash.fill(color)
        flash.set_alpha(50)
        screen.blit(flash, (0, 0))
