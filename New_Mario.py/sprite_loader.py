# sprite_loader.py - 精灵加载工具
import pygame
import os

def load_sprite_sheet(sheet_path, sprite_width, sprite_height, num_sprites=None):
    """
    从精灵表中加载多个精灵帧
    :param sheet_path: 精灵表路径
    :param sprite_width: 单个精灵宽度
    :param sprite_height: 单个精灵高度
    :param num_sprites: 要加载的精灵数量，None表示加载全部
    :return: 精灵列表
    """
    if not os.path.exists(sheet_path):
        print(f"精灵表不存在: {sheet_path}")
        return []
    
    sheet = pygame.image.load(sheet_path).convert_alpha()
    sprites = []
    
    if num_sprites is None:
        num_sprites = sheet.get_width() // sprite_width
    
    for i in range(num_sprites):
        sprite = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
        sprite.blit(sheet, (0, 0), (i * sprite_width, 0, sprite_width, sprite_height))
        sprites.append(sprite)
    
    return sprites