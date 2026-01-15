# player.py - 玩家类定义（单帧图像）
import pygame
import os
from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # 初始化位置参数
        self.start_x = x
        self.start_y = y
        
        # 物理属性
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True  # 朝向标志
        
        # 尝试加载角色图片
        self.load_character_image()
        
        # 设置初始位置
        self.rect.x = self.start_x
        self.rect.y = self.start_y
    
    def load_character_image(self):
        """尝试加载角色精灵图片"""
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 检查Ninja Frog目录中实际存在哪些文件
        ninja_frog_dir = os.path.join(current_dir, "Main Characters", "Ninja Frog")
        
        if os.path.exists(ninja_frog_dir):
            available_files = os.listdir(ninja_frog_dir)
            print(f"Ninja Frog目录中的文件: {available_files}")
        else:
            print("Ninja Frog目录不存在!")
        
        # 尝试加载Ninja Frog角色图片，使用更灵活的文件名匹配
        possible_image_names = [
            "Idle.png", "idle.png", "IDLE.png", 
            "Idle.PNG", "idle.PNG", "Character_Idle.png",
            "MainChar.png", "mainchar.png", "MainChar.PNG",
            "Run (3).png", "run (3).png", "Run.png", "run.png",
            "Jump.png", "jump.png", "Fall.png", "fall.png"
        ]
        
        char_image_path = None
        for name in possible_image_names:
            potential_path = os.path.join(current_dir, "Main Characters", "Ninja Frog", name)
            if os.path.exists(potential_path):
                char_image_path = potential_path
                break
        
        if char_image_path and os.path.exists(char_image_path):
            try:
                # 加载角色图像
                original_image = pygame.image.load(char_image_path).convert_alpha()
                
                # 获取原始图像尺寸
                orig_width, orig_height = original_image.get_size()
                
                # 按比例缩放到游戏尺寸，保持宽高比
                scale_factor = min(PLAYER_WIDTH / orig_width, PLAYER_HEIGHT / orig_height)
                new_width = int(orig_width * scale_factor)
                new_height = int(orig_height * scale_factor)
                
                # 缩放图像
                self.image = pygame.transform.scale(original_image, (new_width, new_height))
                
                print(f"成功加载角色图片: {char_image_path}, 缩放至: {new_width}x{new_height}")
            except Exception as e:
                print(f"加载角色精灵失败: {e}")
                # 备用方案：创建蓝色方块
                self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
                self.image.fill(BLUE)
        else:
            # 如果没有找到图片，使用原来的蓝色方块
            print("未找到角色图片，使用默认图形")
            self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
            self.image.fill(BLUE)
        
        # 创建rect对象
        self.rect = self.image.get_rect()
    
    def update(self, platforms):
        # 应用重力
        self.vel_y += GRAVITY
        
        # 更新位置
        self.rect.x += self.vel_x
        self.check_collisions(platforms, 'x')
        
        self.rect.y += self.vel_y
        self.check_collisions(platforms, 'y')
        
        # 限制垂直速度
        if self.vel_y > 10:
            self.vel_y = 10
    
    def check_collisions(self, platforms, direction):
        collisions = pygame.sprite.spritecollide(self, platforms, False)
        
        for platform in collisions:
            if direction == 'x':
                if self.vel_x > 0:  # 向右移动
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0:  # 向左移动
                    self.rect.left = platform.rect.right
                    self.facing_right = False
                else:
                    self.facing_right = (self.vel_x >= 0)
                self.vel_x = 0
                
            elif direction == 'y':
                if self.vel_y > 0:  # 下落
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # 上跳
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
    
    def jump(self):
        self.vel_y = JUMP_STRENGTH
        self.on_ground = False
    
    def move_left(self):
        self.vel_x = -PLAYER_SPEED
        self.facing_right = False
        
    def move_right(self):
        self.vel_x = PLAYER_SPEED
        self.facing_right = True
        
    def stop(self):
        self.vel_x = 0