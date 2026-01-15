# game.py - 游戏主类定义
import pygame
import os
from constants import *
from player import Player
from platform import Platform

class Game:
    def __init__(self):
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"当前脚本目录: {current_dir}")  # 调试信息
        
        # 创建屏幕
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("平台跳跃游戏")
        self.clock = pygame.time.Clock()
        
        # 加载背景图片 - 使用更全面的方法
        self.background_img = None
        
        # 搜索背景图片的各种可能位置
        search_dirs = [
            os.path.join(current_dir, "Background"),
            os.path.join(current_dir, "background"),
            os.path.join(current_dir, "BG"),
            os.path.join(current_dir, "bg"),
            current_dir  # 也搜索当前目录
        ]
        
        # 支持的图片格式
        image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
        
        for search_dir in search_dirs:
            if os.path.exists(search_dir):
                print(f"正在搜索目录: {search_dir}")  # 调试信息
                files_in_dir = os.listdir(search_dir)
                
                # 查找所有图片文件
                for file in files_in_dir:
                    name, ext = os.path.splitext(file.lower())
                    if ext in image_extensions and ('blue' in name or 'background' in name or 'bg' in name):
                        background_path = os.path.join(search_dir, file)
                        print(f"发现可能的背景文件: {background_path}")  # 调试信息
                        
                        try:
                            self.background_img = pygame.image.load(background_path).convert()
                            # 缩放背景图片以适应屏幕尺寸
                            self.background_img = pygame.transform.scale(
                                self.background_img, 
                                (SCREEN_WIDTH, SCREEN_HEIGHT)
                            )
                            print(f"成功加载背景图片: {background_path}")  # 成功信息
                            break
                        except pygame.error as e:
                            print(f"无法加载图片 {background_path}: {e}")
                
                if self.background_img is not None:  # 如果已找到并加载图片，则退出循环
                    break
            else:
                print(f"目录不存在: {search_dir}")  # 调试信息
        
        if self.background_img is None:
            print("未找到合适的背景图片文件")  # 提示信息

        # 创建精灵组
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        
        # 创建玩家
        self.player = Player(100, 300)
        self.all_sprites.add(self.player)
        
        # 创建平台
        self.create_level()
        
        # 摄像机偏移
        self.camera_offset_x = 0
        
    def create_level(self):
        # 地面平台
        ground = Platform(-100, SCREEN_HEIGHT - 40, SCREEN_WIDTH + 200, 40)
        self.platforms.add(ground)
        self.all_sprites.add(ground)
        
        # 其他平台
        platform1 = Platform(200, 450, 100, 20)
        self.platforms.add(platform1)
        self.all_sprites.add(platform1)
        
        platform2 = Platform(400, 350, 100, 20)
        self.platforms.add(platform2)
        self.all_sprites.add(platform2)
        
        platform3 = Platform(600, 250, 100, 20)
        self.platforms.add(platform3)
        self.all_sprites.add(platform3)
        
        # 更多平台
        platform4 = Platform(100, 200, 100, 20)
        self.platforms.add(platform4)
        self.all_sprites.add(platform4)
        
        platform5 = Platform(350, 150, 100, 20)
        self.platforms.add(platform5)
        self.all_sprites.add(platform5)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                # 跳跃键改为 'w'
                if event.key == pygame.K_w:
                    self.player.jump()
            elif event.type == pygame.KEYUP:
                # 左右移动停止检测改为 'a' 和 'd'
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    self.player.stop()
        return True
    
    def update(self):
        keys = pygame.key.get_pressed()
        
        # 左右移动键改为 'a' 和 'd'
        if keys[pygame.K_a]:
            self.player.move_left()
        elif keys[pygame.K_d]:
            self.player.move_right()
            
        # 更新所有精灵
        self.all_sprites.update(self.platforms)
        
        # 重置地面状态
        self.player.on_ground = False
        
        # 检查是否掉出屏幕
        if self.player.rect.y > SCREEN_HEIGHT:
            self.player.rect.x = 100
            self.player.rect.y = 300
            self.player.vel_x = 0
            self.player.vel_y = 0
        
        # 摄像机跟随玩家
        self.update_camera()
    
    def update_camera(self):
        # 计算摄像机中心应该在的位置
        target_x = self.player.rect.centerx - SCREEN_WIDTH // 2
        # 平滑移动摄像机
        self.camera_offset_x += (target_x - self.camera_offset_x) * 0.1
    
    def draw(self):
        # 绘制背景
        if self.background_img:
            # 如果有背景图片则绘制图片
            self.screen.blit(self.background_img, (0, 0))
        else:
            # 否则填充默认颜色
            self.screen.fill(WHITE)
        
        # 绘制所有精灵
        for sprite in self.all_sprites:
            screen_x = sprite.rect.x - self.camera_offset_x
            self.screen.blit(sprite.image, (screen_x, sprite.rect.y))
        
        # 显示提示信息
        font = pygame.font.SysFont(None, 24)
        text = font.render("使用 A/D 移动，W 键跳跃", True, RED)
        self.screen.blit(text, (10, 10))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()