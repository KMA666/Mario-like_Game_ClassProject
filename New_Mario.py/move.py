import pygame
import os

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -12
PLAYER_SPEED = 5

# 颜色定义
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 48))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # 物理属性
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        
    def update(self, platforms):
        # 应用重力
        self.vel_y += GRAVITY
        
        # 更新位置
        self.rect.x += self.vel_x
        self.check_collisions(platforms, 'x')
        
        self.rect.y += self.vel_y
        self.check_collisions(platforms, 'y')
        
        # 限制垂直速度
        if self.vel_y > 10:
            self.vel_y = 10
            
    def check_collisions(self, platforms, direction):
        collisions = pygame.sprite.spritecollide(self, platforms, False)
        
        for platform in collisions:
            if direction == 'x':
                if self.vel_x > 0:  # 向右移动
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0:  # 向左移动
                    self.rect.left = platform.rect.right
                self.vel_x = 0
                
            elif direction == 'y':
                if self.vel_y > 0:  # 下落
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # 上跳
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
                    
    def jump(self):
        # 跳跃时给予y轴负向速度（向上）
        self.vel_y = JUMP_STRENGTH
        self.on_ground = False
    
    def move_left(self):
        self.vel_x = -PLAYER_SPEED
        
    def move_right(self):
        self.vel_x = PLAYER_SPEED
        
    def stop(self):
        self.vel_x = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Game:
    def __init__(self):
        # 创建屏幕
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("平台跳跃游戏")
        self.clock = pygame.time.Clock()
        
         # 加载背景图片
        self.background_img = None
        background_path = os.path.join("Background", "Blue.png")
        if os.path.exists(background_path):
            self.background_img = pygame.image.load(background_path).convert()
            # 缩放背景图片以适应屏幕尺寸
            self.background_img = pygame.transform.scale(
                self.background_img, 
                (SCREEN_WIDTH, SCREEN_HEIGHT)
            )

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
        # 填充背景
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