# brick_platform.py - 砖块平台类定义
import pygame
from constants import *

class BrickPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, platform_type=PLATFORM):
        super().__init__()
        
        self.platform_type = platform_type
        
        # 创建平台表面 - 对于尖刺地面，创建更大的表面以实现无限延伸效果
        if self.platform_type == DEATH_GROUND:
            # 为尖刺地面创建一个比实际显示区域大得多的表面
            extended_width = width + 600  # 在左右方向各扩展300个单位，总共600个单位
            self.image = pygame.Surface((extended_width, height), pygame.SRCALPHA)
        else:
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # 根据类型绘制不同纹理
        if self.platform_type == DEATH_GROUND:
            self.draw_spike_texture(extended_width, height)
        else:
            self.draw_brick_texture(width, height)
    
    def draw_brick_texture(self, width, height):
        """绘制砖块纹理"""
        # 砖块颜色定义
        BRICK_RED = (178, 34, 34)  # 砖红色
        BRICK_DARK_RED = (139, 0, 0)  # 深砖红
        BRICK_BORDER = (105, 105, 105)  # 砖块边缘灰
        
        # 填充背景
        self.image.fill(BRICK_DARK_RED)
        
        # 计算砖块尺寸
        brick_width = 40
        brick_height = 20
        mortar_thickness = 2  # 灰缝厚度
        
        # 绘制砖块网格
        for row in range(0, height, brick_height + mortar_thickness):
            for col in range(0, width, brick_width + mortar_thickness):
                # 交错砖块（类似真实砖墙）
                offset = 0
                if (row // (brick_height + mortar_thickness)) % 2 == 1:
                    offset = brick_width // 2
                
                # 检查是否超出边界
                if col + offset + brick_width <= width and row + brick_height <= height:
                    # 绘制砖块
                    brick_rect = pygame.Rect(col + offset, row, brick_width, brick_height)
                    pygame.draw.rect(self.image, BRICK_RED, brick_rect)
                    
                    # 绘制砖块边框
                    pygame.draw.rect(self.image, BRICK_BORDER, brick_rect, 1)
        
        # 绘制平台整体边框
        border_rect = pygame.Rect(0, 0, width, height)
        pygame.draw.rect(self.image, BRICK_BORDER, border_rect, 2)
    
    def draw_spike_texture(self, width, height):
        """绘制尖刺地面纹理 - 无限延伸效果"""
        # 尖刺颜色定义
        SPIKE_TOP = (50, 50, 50)      # 尖刺顶部深色
        SPIKE_MIDDLE = (80, 80, 80)   # 尖刺中间颜色
        SPIKE_BOTTOM = (100, 100, 100)  # 尖刺底部浅色
        
        # 透明化整个表面
        self.image.fill((0, 0, 0, 0))
        
        # 计算三角形尺寸 - 使尖刺更大更突出
        triangle_width = 15
        triangle_height = 40  # 增加高度，让尖刺更突出
        
        # 绘制连续的三角形，形成无限延伸的尖刺效果
        # 从负600位置开始绘制，确保从屏幕左边无缝进入
        x_pos = -600  # 从负600位置开始，确保左侧扩展
        while x_pos < width + 300:  # 直到超过右侧300个单位
            # 绘制一个向上指的三角形（尖刺）
            triangle_points = [
                (x_pos, height),                           # 左下角（底部）
                (x_pos + triangle_width, height),          # 右下角
                (x_pos + triangle_width // 2, height - triangle_height)  # 顶点
            ]
            
            # 绘制三角形尖刺
            pygame.draw.polygon(self.image, SPIKE_TOP, triangle_points)
            pygame.draw.polygon(self.image, SPIKE_MIDDLE, [
                (x_pos + 2, height),
                (x_pos + triangle_width - 2, height),
                (x_pos + triangle_width // 2, height - triangle_height)
            ])
            pygame.draw.polygon(self.image, SPIKE_BOTTOM, triangle_points, 1)  # 边框
            
            x_pos += triangle_width