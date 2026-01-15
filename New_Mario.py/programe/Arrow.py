# arrow.py - 箭矢类定义
# -*- coding: utf-8 -*-
import pygame
import random
from constants import *

class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # 箭矢尺寸
        self.arrow_width = ARROW_WIDTH
        self.arrow_height = ARROW_HEIGHT
        
        # 创建箭矢表面
        self.image = pygame.Surface((self.arrow_width, self.arrow_height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # 绘制箭矢
        self.draw_arrow()
        
        # 速度
        self.speed = random.uniform(3, 7)  # 随机下落速度
        
    def draw_arrow(self):
        """绘制箭矢"""
        # 清空表面
        self.image.fill((0, 0, 0, 0))
        
        # 箭矢颜色
        ARROW_SHAFT = (139, 69, 19)  # 棕色箭杆
        ARROW_HEAD = (105, 105, 105)  # 灰色箭头
        ARROW_FEATHER = (255, 0, 0)   # 红色羽毛
        
        # 绘制箭杆（矩形）
        shaft_rect = pygame.Rect(
            self.arrow_width // 2 - 2, 
            5, 
            4, 
            self.arrow_height - 15
        )
        pygame.draw.rect(self.image, ARROW_SHAFT, shaft_rect)
        
        # 绘制箭头（三角形）
        head_points = [
            (self.arrow_width // 2, 0),  # 顶端
            (self.arrow_width // 2 - 5, 10),  # 左下
            (self.arrow_width // 2 + 5, 10)   # 右下
        ]
        pygame.draw.polygon(self.image, ARROW_HEAD, head_points)
        
        # 绘制羽毛（底部的小三角形）
        feather_points = [
            (self.arrow_width // 2, self.arrow_height),  # 底端
            (self.arrow_width // 2 - 4, self.arrow_height - 10),  # 左上
            (self.arrow_width // 2 + 4, self.arrow_height - 10)   # 右上
        ]
        pygame.draw.polygon(self.image, ARROW_FEATHER, feather_points)
    
    def update(self, platforms=None):
        """更新箭矢状态 - 向下移动"""
        self.rect.y += self.speed
        
        # 如果箭矢移出屏幕底部，则标记为需要删除
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()  # 从所有精灵组中移除