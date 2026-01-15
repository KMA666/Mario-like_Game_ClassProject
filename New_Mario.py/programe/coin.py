# coin.py - 金币类定义
import pygame
import math
from constants import *

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # 创建金币表面 - 改为40x40（原来20x20）
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # 绘制金币
        self.draw_coin()
        
        # 旋转动画参数
        self.angle = 0
        self.rotation_speed = 2  # 旋转速度
    
    def draw_coin(self):
        """绘制金币"""
        # 清空表面
        self.image.fill((0, 0, 0, 0))
        
        # 金币颜色
        GOLD_OUTER = (255, 215, 0)      # 金色外圈
        GOLD_INNER = (255, 255, 100)    # 金色内圈
        GOLD_HIGHLIGHT = (255, 255, 200) # 金色高光
        
        # 绘制金币主体
        center_x = self.rect.width // 2
        center_y = self.rect.height // 2
        radius = 16  # 原来是8，现在翻倍
        
        # 绘制外圆
        pygame.draw.circle(self.image, GOLD_OUTER, (center_x, center_y), radius)
        
        # 绘制内圆
        pygame.draw.circle(self.image, GOLD_INNER, (center_x, center_y), radius - 4)
        
        # 绘制高光
        highlight_pos = (center_x - 4, center_y - 4)
        pygame.draw.circle(self.image, GOLD_HIGHLIGHT, highlight_pos, 4)
    
    def update(self, platforms=None):
        """更新金币状态"""
        # 旋转动画
        self.angle = (self.angle + self.rotation_speed) % 360
        
        # 重新绘制金币以反映旋转效果（这里简化处理，只是定期更新外观）
        # 实际上，真正的旋转需要创建旋转后的图像
        pass