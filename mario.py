import pygame
import sys

# 初始化pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 500
GRAVITY = 1
JUMP_STRENGTH = -15
MOVE_SPEED = 5

# 颜色定义
SKY_BLUE = (107, 140, 255)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("简化版马里奥游戏 - 老奶奶的游戏编程")
clock = pygame.time.Clock()

# 玩家类
class Player:
    def __init__(self):
        self.x = 100
        self.y = GROUND_HEIGHT - 50
        self.width = 40
        self.height = 50
        self.vel_y = 0
        self.jumping = False
        self.direction = 1  # 1表示向右，-1表示向左
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        
        # 边界检测
        if self.x < 0:
            self.x = 0
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            
    def apply_gravity(self):
        self.vel_y += GRAVITY
        self.move(0, self.vel_y)
        
        # 地面碰撞检测
        if self.y >= GROUND_HEIGHT - self.height:
            self.y = GROUND_HEIGHT - self.height
            self.vel_y = 0
            self.jumping = False
    
    def jump(self):
        if not self.jumping:
            self.vel_y = JUMP_STRENGTH
            self.jumping = True
    
    def draw(self, surface):
        # 绘制马里奥身体（红色矩形）
        pygame.draw.rect(surface, RED, (self.x, self.y, self.width, self.height))
        
        # 绘制马里奥帽子（红色矩形）
        pygame.draw.rect(surface, RED, (self.x-5, self.y, self.width+10, 10))
        
        # 绘制马里奥脸部（黄色矩形）
        pygame.draw.rect(surface, YELLOW, (self.x+5, self.y+10, 30, 20))
        
        # 绘制马里奥眼睛
        eye_x = self.x + 15 if self.direction == 1 else self.x + 25
        pygame.draw.circle(surface, (0, 0, 0), (eye_x, self.y+18), 3)

# 平台类
class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self, surface):
        pygame.draw.rect(surface, BROWN, (self.x, self.y, self.width, self.height))
        # 绘制平台顶部草皮
        pygame.draw.rect(surface, GREEN, (self.x, self.y, self.width, 5))

# 游戏对象
player = Player()
platforms = [
    Platform(200, 450, 100, 20),
    Platform(400, 400, 100, 20),
    Platform(600, 350, 100, 20),
]

# 游戏主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
    
    # 获取按键状态
    keys = pygame.key.get_pressed()
    dx = 0
    if keys[pygame.K_LEFT]:
        dx = -MOVE_SPEED
        player.direction = -1
    if keys[pygame.K_RIGHT]:
        dx = MOVE_SPEED
        player.direction = 1
    
    # 更新玩家位置
    player.move(dx, 0)
    player.apply_gravity()
    
    # 平台碰撞检测
    for platform in platforms:
        # 检查玩家是否落在平台上
        if (player.x + player.width > platform.x and 
            player.x < platform.x + platform.width and
            player.y + player.height <= platform.y and 
            player.y + player.height + player.vel_y >= platform.y):
            player.y = platform.y - player.height
            player.vel_y = 0
            player.jumping = False
    
    # 绘制游戏画面
    # 填充天空颜色
    screen.fill(SKY_BLUE)
    
    # 绘制地面
    pygame.draw.rect(screen, GREEN, (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
    
    # 绘制云朵
    pygame.draw.circle(screen, (255, 255, 255), (100, 80), 30)
    pygame.draw.circle(screen, (255, 255, 255), (130, 70), 35)
    pygame.draw.circle(screen, (255, 255, 255), (160, 80), 30)
    
    pygame.draw.circle(screen, (255, 255, 255), (600, 100), 40)
    pygame.draw.circle(screen, (255, 255, 255), (630, 90), 45)
    pygame.draw.circle(screen, (255, 255, 255), (660, 100), 40)
    
    # 绘制平台
    for platform in platforms:
        platform.draw(screen)
    
    # 绘制玩家
    player.draw(screen)
    
    # 显示操作提示
    font = pygame.font.SysFont(None, 30)
    text = font.render("使用方向键移动，空格键跳跃", True, (255, 255, 255))
    screen.blit(text, (10, 10))
    
    # 更新显示
    pygame.display.flip()
    
    # 控制帧率
    clock.tick(60)

# 退出游戏
pygame.quit()
sys.exit()