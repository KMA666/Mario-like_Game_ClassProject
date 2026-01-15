# sprite_sheet.py - 精灵表切割工具
import pygame
import os

class SpriteSheet:
    def __init__(self, filename):
        """加载精灵表"""
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()
    
    def get_image(self, x, y, width, height):
        """从精灵表中提取单个精灵图像"""
        # 创建一个新的透明表面
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        # 从精灵表复制指定区域到新表面
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        return image
    
    def get_strip(self, x, y, width, height, count):
        """获取一系列精灵图像（如一个动画序列）"""
        strip = []
        for i in range(count):
            img = self.get_image(x + i * width, y, width, height)
            strip.append(img)
        return strip

def split_sprite_sheet(image_path, sprite_width, sprite_height, output_dir=None):
    """
    切割精灵表并保存为单独的PNG文件
    :param image_path: 精灵表路径
    :param sprite_width: 单个精灵宽度
    :param sprite_height: 单个精灵高度
    :param output_dir: 输出目录，默认为精灵表同目录
    """
    if not os.path.exists(image_path):
        print(f"精灵表不存在: {image_path}")
        return []
    
    if output_dir is None:
        output_dir = os.path.dirname(image_path)
    
    sprite_sheet = SpriteSheet(image_path)
    sheet_width = sprite_sheet.sprite_sheet.get_width()
    sheet_height = sprite_sheet.sprite_sheet.get_height()
    
    # 计算有多少个精灵
    cols = sheet_width // sprite_width
    rows = sheet_height // sprite_height
    
    extracted_images = []
    
    for row in range(rows):
        for col in range(cols):
            x = col * sprite_width
            y = row * sprite_height
            image = sprite_sheet.get_image(x, y, sprite_width, sprite_height)
            
            # 生成文件名
            filename = f"sprite_{row}_{col}.png"
            filepath = os.path.join(output_dir, filename)
            
            # 保存图像
            pygame.image.save(image, filepath)
            extracted_images.append(filepath)
            print(f"已保存: {filepath}")
    
    return extracted_images