# # platform.py - 平台类定义，游戏中的物体，玩家可以站在上面
# import pygame
# from constants import *

# class Platform(pygame.sprite.Sprite):
#     def __init__(self, x, y, width, height):
#         super().__init__()
#         self.image = pygame.Surface((width, height))
#         self.image.fill(GREEN)
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y