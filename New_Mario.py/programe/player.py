# player.py - 玩家类定义（火柴人形象）
# -*- coding: utf-8 -*-
import pygame
import os
from constants import *
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
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
        """绘制火柴人角色"""
        # 创建角色表面
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
        
        # 定义颜色
        HEAD_COLOR = (0, 0, 0)        # 黑色头部
        BODY_COLOR = (0, 0, 0)        # 黑色身体
        LIMB_COLOR = (0, 0, 0)        # 黑色四肢
        
        # 绘制火柴人 - 使用简单的几何图形
        center_x = PLAYER_WIDTH // 2
        head_radius = 6
        
        # 绘制头部 (圆形)
        pygame.draw.circle(self.image, HEAD_COLOR, (center_x, head_radius + 2), head_radius)
        
        # 绘制身体 (线条)
        body_start = (center_x, head_radius * 2 + 2)  # 从头部下方开始
        body_end = (center_x, PLAYER_HEIGHT // 2 + 5)  # 身体长度
        pygame.draw.line(self.image, BODY_COLOR, body_start, body_end, 2)
        
        # 绘制手臂
        arm_start = body_start
        arm_end_left = (center_x - 8, PLAYER_HEIGHT // 2 - 5)
        arm_end_right = (center_x + 8, PLAYER_HEIGHT // 2 - 5)
        pygame.draw.line(self.image, LIMB_COLOR, arm_start, arm_end_left, 2)
        pygame.draw.line(self.image, LIMB_COLOR, arm_start, arm_end_right, 2)
        
        # 绘制腿
        leg_start = body_end
        leg_end_left = (center_x - 6, PLAYER_HEIGHT - 5)
        leg_end_right = (center_x + 6, PLAYER_HEIGHT - 5)
        pygame.draw.line(self.image, LIMB_COLOR, leg_start, leg_end_left, 2)
        pygame.draw.line(self.image, LIMB_COLOR, leg_start, leg_end_right, 2)
        
        # 创建rect对象
        self.rect = self.image.get_rect()
        self.rect.x = self.start_x
        self.rect.y = self.start_y
    
    def update(self, platforms):
        # 应用重力
        self.vel_y += GRAVITY
        
        # 更新位置 - 先更新x方向
        self.rect.x += self.vel_x
        self.check_collisions(platforms, 'x')
        
        # 再更新y方向
        self.rect.y += self.vel_y
        self.check_collisions(platforms, 'y')
        
        # 限制垂直速度
        if self.vel_y > 10:
            self.vel_y = 10
    
    def check_collisions(self, platforms, direction):
        collisions = pygame.sprite.spritecollide(self, platforms, False)
        
        for platform in collisions:
            # 如果是尖刺地面，特殊处理
            if hasattr(platform, 'platform_type') and platform.platform_type == DEATH_GROUND:
                # 对于尖刺地面，我们不在这里处理碰撞，而是在game.py中处理死亡
                continue
            
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