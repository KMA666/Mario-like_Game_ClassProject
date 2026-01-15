# game.py - 游戏主类定义
import pygame
import os
from constants import *
from player import Player
from brick_platform import BrickPlatform
from background_generator import generate_background

class Game:
    def __init__(self):
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"当前脚本目录: {current_dir}")  # 调试信息
        
        # 创建屏幕
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("平台跳跃游戏")
        self.clock = pygame.time.Clock()
        
        # 生成背景图片
        self.background_img = generate_background(SCREEN_WIDTH, SCREEN_HEIGHT)

        # 创建精灵组
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        
        # 设置初始重生点在第一个安全平台上
        self.respawn_point = (250, 400)  # 第一个安全平台的位置
        
        # 创建玩家 - 在安全平台上生成
        self.player = Player(self.respawn_point[0], self.respawn_point[1])  # 在安全平台位置生成玩家
        self.all_sprites.add(self.player)
        
        # 创建关卡
        self.create_level()
        
        # 摄像机偏移
        self.camera_offset_x = 0
        
    def create_level(self):
        # 尖刺地面平台 - 扩展范围以支持左右移动，包括向左延伸
        # 将尖刺地面放置在更宽的范围内，确保摄像机向左移动时也有尖刺
        ground = BrickPlatform(-SCREEN_WIDTH, SCREEN_HEIGHT - 40, SCREEN_WIDTH * 3, 40, DEATH_GROUND)
        self.platforms.add(ground)
        self.all_sprites.add(ground)
        
        # 其他安全砖块平台作为重生点
        platform1 = BrickPlatform(200, 450, 100, 20)
        self.platforms.add(platform1)
        self.all_sprites.add(platform1)
        
        platform2 = BrickPlatform(400, 350, 100, 20)
        self.platforms.add(platform2)
        self.all_sprites.add(platform2)
        
        platform3 = BrickPlatform(600, 250, 100, 20)
        self.platforms.add(platform3)
        self.all_sprites.add(platform3)
        
        # 更多安全平台
        platform4 = BrickPlatform(100, 200, 100, 20)
        self.platforms.add(platform4)
        self.all_sprites.add(platform4)
        
        platform5 = BrickPlatform(350, 150, 100, 20)
        self.platforms.add(platform5)
        self.all_sprites.add(platform5)
        
        # 额外的安全平台
        platform6 = BrickPlatform(550, 400, 80, 15)
        self.platforms.add(platform6)
        self.all_sprites.add(platform6)
        
        platform7 = BrickPlatform(150, 350, 120, 15)
        self.platforms.add(platform7)
        self.all_sprites.add(platform7)
    
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
        
        # 检测碰撞并判断死亡 - 这里是关键修改部分
        collisions = pygame.sprite.spritecollide(self.player, self.platforms, False)
        for platform in collisions:
            # 检查是否与尖刺地面碰撞
            if hasattr(platform, 'platform_type') and platform.platform_type == DEATH_GROUND:
                # 如果与尖刺地面碰撞，立即死亡
                if (self.player.rect.bottom >= platform.rect.top and 
                    self.player.rect.top <= platform.rect.bottom and
                    self.player.rect.right > platform.rect.left and 
                    self.player.rect.left < platform.rect.right):
                    self.player_die()
                    return  # 立即返回，避免其他处理
        
        # 检查是否掉出屏幕底部
        if self.player.rect.y > SCREEN_HEIGHT:
            self.player_die()
        
        # 摄像机跟随玩家
        self.update_camera()
    
    def player_die(self):
        """处理玩家死亡事件"""
        print("玩家死亡！重生在安全平台")
        
        # 重置玩家位置到安全平台
        self.player.rect.x = self.respawn_point[0]
        self.player.rect.y = self.respawn_point[1]
        self.player.vel_x = 0
        self.player.vel_y = 0
        
        # 确保玩家不会立即再次死亡
        # 检查重生点是否安全
        collisions = pygame.sprite.spritecollide(self.player, self.platforms, False)
        for platform in collisions:
            if hasattr(platform, 'platform_type') and platform.platform_type == DEATH_GROUND:
                # 如果重生点不安全，稍微调整位置
                self.player.rect.y = self.respawn_point[1] - 50  # 往上一点
    
    def update_camera(self):
        # 计算摄像机中心应该在的位置 - 让摄像机跟随玩家
        target_x = self.player.rect.centerx - SCREEN_WIDTH // 2
        
        # 平滑移动摄像机，但限制其移动范围
        # 使用更快的跟踪速度，使摄像机更灵敏
        self.camera_offset_x += (target_x - self.camera_offset_x) * 0.2  # 提高跟踪速度

        # 限制摄像机不能移到关卡边界之外
        # 获取所有平台中最左和最右的边界
        min_x = float('inf')
        max_x = float('-inf')
        for platform in self.all_sprites:
            min_x = min(min_x, platform.rect.left)
            max_x = max(max_x, platform.rect.right)
        
        # 限制摄像机范围
        # 由于尖刺平台非常宽，我们只需要确保摄像机在合理范围内
        min_camera_x = -(SCREEN_WIDTH // 2)  # 允许向左扩展
        max_camera_x = max_x - SCREEN_WIDTH // 2
        self.camera_offset_x = max(min_camera_x, min(self.camera_offset_x, max_camera_x))
    
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
        text = font.render("使用 A/D 移动，W 键跳跃 - 注意避开尖刺地面！", True, RED)
        self.screen.blit(text, (10, 10))
        
        # 显示当前重生点信息
        respawn_text = font.render(f"重生点: ({self.respawn_point[0]}, {self.respawn_point[1]})", True, RED)
        self.screen.blit(respawn_text, (10, 35))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()