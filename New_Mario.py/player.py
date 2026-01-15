# player.py - 玩家类定义
import pygame
from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 48))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # 物理属性
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        
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
        # 跳跃时给予y轴负向速度（向上）
        self.vel_y = JUMP_STRENGTH
        self.on_ground = False
    
    def move_left(self):
        self.vel_x = -PLAYER_SPEED
        
    def move_right(self):
        self.vel_x = PLAYER_SPEED
        
    def stop(self):
        self.vel_x = 0