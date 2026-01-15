# background_generator.py - 生成游戏背景
# -*- coding: utf-8 -*-
import pygame
import random
import sys

def generate_background(screen_width, screen_height):
    """
    生成包含天空、森林和云朵的背景
    """
    # 创建背景表面
    background = pygame.Surface((screen_width, screen_height))
    
    # 定义颜色
    SKY_BLUE = (135, 206, 235)
    GRASS_GREEN = (34, 139, 34)
    TREE_BROWN = (101, 67, 33)
    TREE_GREEN = (0, 100, 0)
    CLOUD_WHITE = (250, 250, 250)
    CLOUD_LIGHT_GRAY = (230, 230, 230)
    
    # 填充天空背景
    background.fill(SKY_BLUE)
    
    # 绘制地面
    ground_height = screen_height // 5
    pygame.draw.rect(background, GRASS_GREEN, 
                     (0, screen_height - ground_height, screen_width, ground_height))
    
    # 随机生成树木
    for _ in range(15):
        # 随机位置
        tree_x = random.randint(0, screen_width)
        tree_y = screen_height - ground_height
        
        # 树干
        trunk_width = random.randint(10, 20)
        trunk_height = random.randint(30, 60)
        pygame.draw.rect(background, TREE_BROWN, 
                         (tree_x, tree_y - trunk_height, trunk_width, trunk_height))
        
        # 树冠
        crown_radius = random.randint(20, 40)
        pygame.draw.circle(background, TREE_GREEN, 
                          (tree_x + trunk_width // 2, tree_y - trunk_height - crown_radius // 2), 
                          crown_radius)
    
    # 随机生成云朵
    for _ in range(8):
        cloud_x = random.randint(0, screen_width)
        cloud_y = random.randint(20, screen_height // 3)
        
        # 云朵由几个圆形组成
        cloud_size = random.randint(20, 40)
        pygame.draw.circle(background, CLOUD_WHITE, (cloud_x, cloud_y), cloud_size)
        pygame.draw.circle(background, CLOUD_WHITE, (cloud_x + cloud_size, cloud_y - cloud_size // 2), cloud_size)
        pygame.draw.circle(background, CLOUD_WHITE, (cloud_x + cloud_size * 1.5, cloud_y), cloud_size)
        pygame.draw.circle(background, CLOUD_WHITE, (cloud_x + cloud_size * 0.75, cloud_y + cloud_size // 2), cloud_size * 0.8)
    
    # 添加一些远山效果
    for i in range(5):
        mountain_x = i * (screen_width // 4) - random.randint(50, 150)
        mountain_height = random.randint(80, 150)
        mountain_width = random.randint(150, 300)
        
        # 确保山脉在屏幕内
        if mountain_x < -mountain_width // 2:
            mountain_x = -mountain_width // 2
        elif mountain_x > screen_width + mountain_width // 2:
            mountain_x = screen_width + mountain_width // 2
        
        # 绘制山脉
        points = [
            (mountain_x - mountain_width // 2, screen_height - ground_height),
            (mountain_x, screen_height - ground_height - mountain_height),
            (mountain_x + mountain_width // 2, screen_height - ground_height)
        ]
        pygame.draw.polygon(background, (120, 120, 120), points)
    
    return background