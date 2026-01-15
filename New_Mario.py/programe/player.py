# player.py - 玩家类定义（火柴人形象）
# -*- coding: utf-8 -*-
import pygame
import os
from constants import *
import sys

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
        
        # 跳跃相关
        self.jumps_remaining = 2  # 允许跳跃次数（2段跳）
        self.max_jumps = 2  # 最大跳跃次数
        self.is_jumping = False  # 标记是否正在跳跃
        self.jump_direction = 0  # 跳跃方向：-1向左，1向右，0原地
        
        # 奔跑相关
        self.is_sprinting = False  # 是否在奔跑
        
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
        
        # 检查是否在跳跃状态
        if self.vel_y < 0:
            self.is_jumping = True
            # 根据水平速度确定跳跃方向
            if self.vel_x < 0:
                self.jump_direction = -1
            elif self.vel_x > 0:
                self.jump_direction = 1
            else:
                self.jump_direction = 0
        elif self.on_ground:
            self.is_jumping = False
            self.jump_direction = 0
        
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
            # 检查是否与带尖刺的平台碰撞
            elif hasattr(platform, 'has_spikes') and platform.has_spikes:
                # 这里不处理尖刺碰撞，由game.py处理
                continue
            # 检查是否与移动平台碰撞
            elif hasattr(platform, 'is_moving') and platform.is_moving:
                # 如果是移动平台，还要加上平台的移动速度
                self.rect.x += platform.move_speed
            
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
                    # 落地时重置跳跃次数
                    self.jumps_remaining = self.max_jumps
                    self.is_jumping = False
                    self.jump_direction = 0
                elif self.vel_y < 0:  # 上跳
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
                    # 注意：碰到天花板时不应重置跳跃次数
    
    def jump(self):
        # 检查是否还有跳跃次数
        if self.jumps_remaining > 0:
            self.vel_y = JUMP_STRENGTH
            self.jumps_remaining -= 1
            self.on_ground = False
            self.is_jumping = True  # 标记为跳跃状态
            # 根据当前面向方向设置跳跃方向
            if self.vel_x < 0:
                self.jump_direction = -1
            elif self.vel_x > 0:
                self.jump_direction = 1
            else:
                self.jump_direction = 0
    
    def move_left(self):
        speed = PLAYER_SPEED * SPRINT_MULTIPLIER if self.is_sprinting else PLAYER_SPEED
        self.vel_x = -speed
        self.facing_right = False
        # 更新奔跑状态的火柴人图像
        self.update_sprite_image()
        
    def move_right(self):
        speed = PLAYER_SPEED * SPRINT_MULTIPLIER if self.is_sprinting else PLAYER_SPEED
        self.vel_x = speed
        self.facing_right = True
        # 更新奔跑状态的火柴人图像
        self.update_sprite_image()
        
    def stop(self):
        self.vel_x = 0
    
    def set_sprint(self, sprinting):
        self.is_sprinting = sprinting
        # 更新奔跑状态的火柴人图像
        self.update_sprite_image()
    
    def update_sprite_image(self):
        """更新火柴人的图像，根据奔跑状态和跳跃状态"""
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
        
        # 根据状态绘制不同的火柴人
        if self.is_jumping:
            # 跳跃状态：根据跳跃方向显示不同动作
            # 绘制手臂（跳跃姿态，向上收起）
            arm_start = body_start
            arm_end_left = (center_x - 7, PLAYER_HEIGHT // 2 - 10)
            arm_end_right = (center_x + 7, PLAYER_HEIGHT // 2 - 10)
            pygame.draw.line(self.image, LIMB_COLOR, arm_start, arm_end_left, 2)
            pygame.draw.line(self.image, LIMB_COLOR, arm_start, arm_end_right, 2)
            
            # 绘制腿（跳跃姿态，根据方向调整姿势）
            leg_start = body_end
            
            if self.jump_direction == -1:  # 向左跳跃
                # 左腿向前（左侧）
                leg_end_left = (center_x - 12, PLAYER_HEIGHT // 2 + 10)
                # 右腿向后（右侧）
                leg_end_right = (center_x + 10, PLAYER_HEIGHT - 5)
            elif self.jump_direction == 1:  # 向右跳跃
                # 左腿向后（左侧）
                leg_end_left = (center_x - 10, PLAYER_HEIGHT - 5)
                # 右腿向前（右侧）
                leg_end_right = (center_x + 12, PLAYER_HEIGHT // 2 + 10)
            else:  # 原地跳跃
                # 左腿向上
                leg_end_left = (center_x - 8, PLAYER_HEIGHT // 2 + 5)
                # 右腿向下
                leg_end_right = (center_x + 8, PLAYER_HEIGHT - 2)
            
            pygame.draw.line(self.image, LIMB_COLOR, leg_start, leg_end_left, 2)
            pygame.draw.line(self.image, LIMB_COLOR, leg_start, leg_end_right, 2)
        elif self.is_sprinting:
            # 奔跑状态：手臂和腿部呈奔跑姿态
            # 绘制手臂（奔跑姿态，向前后摆动）
            arm_start = body_start
            # 前臂（与移动方向相反）
            if self.facing_right:
                # 向右移动时，右臂向前
                arm_end_front = (center_x + 10, PLAYER_HEIGHT // 2 - 2)
                arm_end_back = (center_x - 10, PLAYER_HEIGHT // 2)
            else:
                # 向左移动时，左臂向前
                arm_end_front = (center_x - 10, PLAYER_HEIGHT // 2 - 2)
                arm_end_back = (center_x + 10, PLAYER_HEIGHT // 2)
            pygame.draw.line(self.image, LIMB_COLOR, arm_start, arm_end_front, 2)
            pygame.draw.line(self.image, LIMB_COLOR, arm_start, arm_end_back, 2)
            
            # 绘制腿（奔跑姿态，一前一后）
            leg_start = body_end
            # 前腿（与移动方向相同）
            if self.facing_right:
                leg_end_front = (center_x + 8, PLAYER_HEIGHT - 8)
                leg_end_back = (center_x - 8, PLAYER_HEIGHT - 2)
            else:
                leg_end_front = (center_x - 8, PLAYER_HEIGHT - 8)
                leg_end_back = (center_x + 8, PLAYER_HEIGHT - 2)
            pygame.draw.line(self.image, LIMB_COLOR, leg_start, leg_end_front, 2)
            pygame.draw.line(self.image, LIMB_COLOR, leg_start, leg_end_back, 2)
        else:
            # 正常状态：手臂和腿部呈常规姿态
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