# game.py - 游戏主类定义
import pygame
import os
import random
import sys
# import io  # 注释掉这行，避免不必要的导入
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  # 注释掉这行
from constants import *
from player import Player
from brick_platform import BrickPlatform
from background_generator import generate_background
from coin import Coin
from arrow import Arrow

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
        self.coins = pygame.sprite.Group()  # 金币精灵组
        
        # 设置初始重生点在第一个安全平台上
        self.respawn_point = (250, 400)  # 第一个安全平台的位置
        
        # 设置初始得分基准高度 - 修正为正确值
        self.base_height = self.respawn_point[1]  # 以出生位置的高度为基准
        
        # 创建玩家 - 在安全平台上生成
        self.player = Player(self.respawn_point[0], self.respawn_point[1])
        self.all_sprites.add(self.player)
        
        # 平台生成控制
        self.platform_generation_threshold = 100  # 高度阈值，低于此值时生成新平台
        self.max_height_limit = -10000  # 最大高度限制（负值表示向上）
        
        # 游戏得分
        self.score = 0
        self.max_height_reached = self.respawn_point[1]  # 修正：初始高度应为玩家的y坐标
        
        # 摄像机偏移
        self.camera_offset_x = 0
        self.camera_offset_y = 0  # 添加y轴偏移以跟随玩家垂直移动
        
        # 游戏状态
        self.game_over = False
        self.restart_timer = 0  # 用于控制闪烁效果

        self.arrows = pygame.sprite.Group()
        self.all_sprites.add(self.arrows)
        self.update_camera()

        
        # 创建关卡
        self.create_level()

    
    def create_level(self):
        # 尖刺地面平台 - 扩展范围以支持左右移动，包括向左延伸
        # 将尖刺地面放置在更宽的范围内，确保摄像机向左移动时也有尖刺
        ground = BrickPlatform(-SCREEN_WIDTH, SCREEN_HEIGHT - 40, SCREEN_WIDTH * 3, 40, DEATH_GROUND)
        self.platforms.add(ground)
        self.all_sprites.add(ground)
        
        # 初始安全平台
        platform1 = BrickPlatform(200, 450, 100, 20)
        self.platforms.add(platform1)
        self.all_sprites.add(platform1)
        

        # 预生成平台直到达到最大高度限制
        self.pre_generate_platforms()

        self.pre_spawn_arrows()
    
    def pre_generate_platforms(self):
        """预先生成平台直到达到最大高度限制"""
        # 从初始平台开始向上生成
        current_highest = min(platform.rect.y for platform in self.platforms if platform != self.player)
        
        # 生成平台直到达到最大高度限制或生成指定数量
        platforms_generated = 0
        max_platforms_to_generate = 120  # 限制总生成平台数量，减少40%
        
        while current_highest > self.max_height_limit and platforms_generated < max_platforms_to_generate:
            # 计算要生成的新平台数量
            platforms_needed = min(3, max_platforms_to_generate - platforms_generated)  # 每次生成最多3个平台，减少40%
            
            for i in range(platforms_needed):
                if platforms_generated >= max_platforms_to_generate:
                    break
                    
                # 从当前最高平台向上生成，确保跳跃可达
                # 平台之间的垂直距离不能小于火柴人两倍高度
                min_vertical_distance = PLAYER_HEIGHT * 2 + 20  # 火柴人两倍高度+缓冲
                max_jump_height = abs(JUMP_STRENGTH) * 2.5  # 二段跳估算的最大高度
                
                # 确保跳跃高度不小于最小距离
                actual_max_height = max(min_vertical_distance, int(max_jump_height))
                y_pos = current_highest - random.randint(min_vertical_distance, actual_max_height)
                
                # 确保不超过最大高度限制
                if y_pos < self.max_height_limit:
                    y_pos = self.max_height_limit
                
                # 生成x坐标
                x_pos = random.randint(50, SCREEN_WIDTH - 100)
                
                # 确定是否生成带尖刺的平台 (5%概率)
                is_spike_platform = random.random() < 0.05
                
                # 确定是否生成移动平台 (10%概率，但在高度低于-1000时)
                is_moving_platform = (random.random() < 0.1 and y_pos < -1000 and not is_spike_platform)
                
                # 检查新平台是否与现有平台重叠
                overlap = True
                attempts = 0
                while overlap and attempts < 50:  # 最多重试50次
                    overlap = False
                    for platform in self.platforms:
                        # 排除玩家，只检查平台间的碰撞
                        if platform == self.player:
                            continue
                        # 检查新平台是否与现有平台重叠
                        if (abs(platform.rect.x - x_pos) < 100 and 
                            abs(platform.rect.y - y_pos) < 60):  # 减少垂直间隔
                            overlap = True
                            # 重新生成坐标
                            actual_max_height = max(min_vertical_distance, int(max_jump_height))
                            y_pos = current_highest - random.randint(min_vertical_distance, actual_max_height)
                            # 确保不超过最大高度限制
                            if y_pos < self.max_height_limit:
                                y_pos = self.max_height_limit
                            x_pos = random.randint(50, SCREEN_WIDTH - 100)
                            break
                    attempts += 1
                
                # 如果重试次数过多，仍然有重叠，强制生成
                if attempts >= 50:
                    # 采用固定间隔的方式生成平台
                    x_pos = 100 + (platforms_generated * 200) % (SCREEN_WIDTH - 200)  # 在屏幕宽度内循环
                    y_pos = current_highest - 100  # 固定垂直间隔
                
                # 创建新平台
                if is_spike_platform:
                    platform = BrickPlatform(x_pos, y_pos, 80, 15, PLATFORM, True)  # 创建带尖刺的平台
                elif is_moving_platform:
                    platform = BrickPlatform(x_pos, y_pos, 80, 15, PLATFORM, False, True)  # 创建移动平台
                else:
                    platform = BrickPlatform(x_pos, y_pos, 80, 15)
                self.platforms.add(platform)
                self.all_sprites.add(platform)
                
                # 每隔10个平台生成一个金币（约10个平台一次）
                # 这里我们使用一个计数器来追踪平台数量
                if hasattr(self, 'platform_count'):
                    self.platform_count += 1
                else:
                    self.platform_count = 1
                
                # 每10个平台生成一次金币
                if self.platform_count % 10 == 0:
                    coin_x = x_pos + random.randint(10, 60)  # 在平台上的随机位置
                    coin_y = y_pos - 20  # 在平台上方一点点
                    coin = Coin(coin_x, coin_y)
                    self.coins.add(coin)
                    self.all_sprites.add(coin)
                
                platforms_generated += 1
                if platforms_generated >= max_platforms_to_generate:
                    break
            
            # 更新当前最高平台
            if self.platforms:
                current_highest = min(platform.rect.y for platform in self.platforms if platform != self.player)
    
    def pre_spawn_arrows(self):
        """预生成一些箭矢"""
    # 不需要预生成，因为箭矢是动态生成的
    pass

    def spawn_arrow(self):
        """随机生成箭矢"""
        # 根据当前高度和时间计算箭矢生成概率
        # 随着高度增加，箭矢密度逐渐增大，最大达到40%
        height_factor = min(1.0, (self.base_height - self.player.rect.y) / 2000.0)  # 基于高度的比例
        density_factor = min(self.max_arrow_density, height_factor * self.max_arrow_density)
        
        # 根据密度因子决定是否生成箭矢
        if random.random() < density_factor:
            # 在屏幕宽度范围内随机生成箭矢
            x_pos = random.randint(0, SCREEN_WIDTH - self.arrow_width)
            # 从屏幕顶部或稍上方生成箭矢
            y_pos = random.randint(-100, -30)
            
            arrow = Arrow(x_pos, y_pos)
            self.arrows.add(arrow)
            self.all_sprites.add(arrow)

    def check_arrow_collisions(self):
        """检测箭矢与玩家的碰撞"""
        # 检测玩家与箭矢的碰撞
        arrow_collisions = pygame.sprite.spritecollide(self.player, self.arrows, False)
        for arrow in arrow_collisions:
            # 如果玩家碰到箭矢，触发死亡
            self.player_die()
            return True
        return False    
    def generate_new_platforms(self):
        """在上方随机生成新平台，确保平台间距离适中"""
        # 获取当前最高平台的大致位置
        current_highest = min(platform.rect.y for platform in self.platforms if platform != self.player)

        # 计算要生成的新平台数量
        platforms_needed = 2  # 每次生成2个新平台，减少40%

        # 估算二段跳最大距离
        # 跳跃公式: v^2 = u^2 + 2as, 其中v=0, u=JUMP_STRENGTH, a=-GRAVITY
        # 最大高度 = u^2 / (2*g) * 2 (考虑两段跳)
        # 估算二段跳最大水平距离 (考虑玩家最大移动速度)
        max_horizontal_distance = int(PLAYER_SPEED * SPRINT_MULTIPLIER * 8)  # 估算值

        # 生成新平台，确保它们之间有合理的距离
        for i in range(platforms_needed):
            # 从当前最高平台向上生成，确保跳跃可达
            # 平台之间的垂直距离不能小于火柴人两倍高度
            min_vertical_distance = PLAYER_HEIGHT * 2 + 20  # 火柴人两倍高度+缓冲
            max_jump_height = abs(JUMP_STRENGTH) * 2.5  # 二段跳估算的最大高度
            
            # 确保跳跃高度不小于最小距离
            actual_max_height = max(min_vertical_distance, int(max_jump_height))
            y_pos = current_highest - random.randint(min_vertical_distance, actual_max_height)  # 修复范围问题
            
            # 确保不超过最大高度限制
            if y_pos < self.max_height_limit:
                y_pos = self.max_height_limit
            
            # 估算玩家水平跳跃距离
            horizontal_range = min(max_horizontal_distance, SCREEN_WIDTH)
            x_pos = random.randint(50, max(50, SCREEN_WIDTH - 50 - horizontal_range))
            
            # 确定是否生成带尖刺的平台 (5%概率)
            is_spike_platform = random.random() < 0.05
            
            # 确定是否生成移动平台 (10%概率，但在高度低于-1000时)
            is_moving_platform = (random.random() < 0.1 and y_pos < -1000 and not is_spike_platform)
            
            # 检查新平台是否与现有平台重叠
            overlap = True
            attempts = 0
            while overlap and attempts < 50:  # 最多重试50次
                overlap = False
                for platform in self.platforms:
                    # 排除玩家，只检查平台间的碰撞
                    if platform == self.player:
                        continue
                    # 检查新平台是否与现有平台重叠
                    if (abs(platform.rect.x - x_pos) < 100 and 
                        abs(platform.rect.y - y_pos) < 60):  # 减少垂直间隔
                        overlap = True
                        # 重新生成坐标
                        actual_max_height = max(min_vertical_distance, int(max_jump_height))
                        y_pos = current_highest - random.randint(min_vertical_distance, actual_max_height)
                        # 确保不超过最大高度限制
                        if y_pos < self.max_height_limit:
                            y_pos = self.max_height_limit
                        x_pos = random.randint(50, max(50, SCREEN_WIDTH - 50))
                        break
                attempts += 1
            
            # 如果重试次数过多，仍然有重叠，强制生成
            if attempts >= 50:
                # 采用固定间隔的方式生成平台
                x_pos = 100 + (i * 200) % (SCREEN_WIDTH - 200)  # 在屏幕宽度内循环
                y_pos = current_highest - 100  # 固定垂直间隔
            
            # 创建新平台
            if is_spike_platform:
                platform = BrickPlatform(x_pos, y_pos, 80, 15, PLATFORM, True)  # 创建带尖刺的平台
            elif is_moving_platform:
                platform = BrickPlatform(x_pos, y_pos, 80, 15, PLATFORM, False, True)  # 创建移动平台
            else:
                platform = BrickPlatform(x_pos, y_pos, 80, 15)
            self.platforms.add(platform)
            self.all_sprites.add(platform)
            
            # 每隔10个平台生成一个金币（约10个平台一次）
            # 这里我们使用一个计数器来追踪平台数量
            if hasattr(self, 'platform_count'):
                self.platform_count += 1
            else:
                self.platform_count = 1
            
            # 每10个平台生成一次金币
            if self.platform_count % 10 == 0:
                coin_x = x_pos + random.randint(10, 60)  # 在平台上的随机位置
                coin_y = y_pos - 20  # 在平台上方一点点
                coin = Coin(coin_x, coin_y)
                self.coins.add(coin)
                self.all_sprites.add(coin)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
            # 如果游戏结束，按任意键重新开始
                if self.game_over:
                    self.restart_game()
            # 跳跃键改为 'w'
                elif event.key == pygame.K_w:
                    self.player.jump()
            # 处理Shift键
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.player.set_sprint(True)
            elif event.type == pygame.KEYUP:
            # 左右移动停止检测改为 'a' 和 'd'
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    self.player.stop()
            # 处理Shift键释放
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.player.set_sprint(False)
        return True
    
    def restart_game(self):
        """重新开始游戏"""
        self.game_over = False
        self.player.rect.x = self.respawn_point[0]
        self.player.rect.y = self.respawn_point[1]
        self.player.vel_x = 0
        self.player.vel_y = 0
        
        # 重置得分
        self.score = 0
        self.max_height_reached = self.base_height
        self.platform_count = 0  # 重置平台计数器
        
        # 清除现有平台（除了地面）
        self.platforms.empty()
        self.coins.empty()
        self.all_sprites.empty()
        

        # 清除箭矢
        self.arrows.empty()
    
        # 重置箭矢生成计时器
        self.arrow_spawn_timer = 0

        # 重新创建地面
        ground = BrickPlatform(-SCREEN_WIDTH, SCREEN_HEIGHT - 40, SCREEN_WIDTH * 3, 40, DEATH_GROUND)
        self.platforms.add(ground)
        self.all_sprites.add(ground)
        
        # 重新创建初始平台
        platform1 = BrickPlatform(200, 450, 100, 20)
        self.platforms.add(platform1)
        self.all_sprites.add(platform1)
        
        # 预生成平台直到达到最大高度限制
        self.pre_generate_platforms()
        
        # 重新添加玩家到精灵组
        self.all_sprites.add(self.player)
    
    def update(self):
        # 如果游戏结束，只更新闪烁效果计时器
        if self.game_over:
            self.restart_timer = (self.restart_timer + 1) % 60  # 每秒闪烁一次
            return
        self.arrow_spawn_timer += 1
        if self.arrow_spawn_timer >= 30:  # 每半秒尝试生成箭矢
            self.spawn_arrow()
            self.arrow_spawn_timer = 0

        keys = pygame.key.get_pressed()
        
        # 左右移动键改为 'a' 和 'd'
        if keys[pygame.K_a]:
            self.player.move_left()
        elif keys[pygame.K_d]:
            self.player.move_right()
        else:
    # 当没有按左右键时停止
            if not (keys[pygame.K_a] or keys[pygame.K_d]):
                self.player.stop()

# 奔跑键 - 检查Shift键是否按下
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.player.set_sprint(True)
        else:
            self.player.set_sprint(False)
            
        # 更新所有精灵（包括移动平台）
        for sprite in self.all_sprites:
            if isinstance(sprite, BrickPlatform) and sprite.is_moving:
                sprite.update()  # 更新移动平台
        self.all_sprites.update(self.platforms)
        # 检测箭矢碰撞
        self.check_arrow_collisions()

        # 检测金币碰撞
        coin_collisions = pygame.sprite.spritecollide(self.player, self.coins, True)
        for coin in coin_collisions:
            self.score += 30  # 拾取金币增加30分
        
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
            # 检查是否与带尖刺的平台碰撞
            elif hasattr(platform, 'has_spikes') and platform.has_spikes:
                # 如果平台有尖刺，且玩家碰撞到尖刺部分，则死亡
                # 尖刺通常在平台的顶部，所以检查玩家底部是否接触到平台顶部
                if (self.player.rect.bottom >= platform.rect.top and 
                    self.player.rect.bottom <= platform.rect.top + 10 and  # 尖刺高度大约10像素
                    self.player.rect.right > platform.rect.left and 
                    self.player.rect.left < platform.rect.right):
                    self.player_die()
                    return  # 立即返回，避免其他处理
        
        # 检查是否掉出屏幕底部
        if self.player.rect.y > SCREEN_HEIGHT:
            self.player_die()
        
        # 更新得分 - 基于玩家达到的最高高度
        self.update_score()
        
        # 如果玩家到达当前最高点上方，生成新平台
        if self.player.rect.y < self.max_height_reached - self.platform_generation_threshold:  # 当玩家向上移动超过阈值时
            self.generate_new_platforms()
            self.max_height_reached = self.player.rect.y
        
        # 摄像机跟随玩家
        self.update_camera()
    
    def update_score(self):
        """更新游戏得分"""
        # 得分计算：基于玩家达到的最高高度
        # 玩家越高（y值越小），得分越高
        # 修正：高度增益应该是基础高度减去当前最高点
        height_gained = max(0, self.base_height - self.max_height_reached)  # 确保不为负值
        self.score = height_gained // 10  # 每上升10像素得1分

    def player_die(self):
        """处理玩家死亡事件"""
        print(f"Player died! Final score: {self.score}")
        self.game_over = True
        self.restart_timer = 0  # 重置闪烁计时器
    
    def update_camera(self):
        # 计算摄像机中心应该在的位置 - 让摄像机跟随玩家
        target_x = self.player.rect.centerx - SCREEN_WIDTH // 2
        target_y = self.player.rect.centery - SCREEN_HEIGHT // 2  # 添加y轴跟随
        
        # 平滑移动摄像机，但限制其移动范围
        # 使用更快的跟踪速度，使摄像机更灵敏
        self.camera_offset_x += (target_x - self.camera_offset_x) * 0.2  # 提高跟踪速度
        self.camera_offset_y += (target_y - self.camera_offset_y) * 0.2  # 添加y轴跟踪

        # 限制摄像机不能移到关卡边界之外
        # 获取所有平台中最左和最右的边界
        min_x = float('inf')
        max_x = float('-inf')
        for platform in self.platforms:  # 只检查平台，不包括玩家和其他精灵
            min_x = min(min_x, platform.rect.left)
            max_x = max(max_x, platform.rect.right)
        
        # 限制摄像机范围
        # 由于尖刺平台非常宽，我们只需要确保摄像机在合理范围内
        min_camera_x = -(SCREEN_WIDTH // 2)  # 允许向左扩展
        max_camera_x = max_x - SCREEN_WIDTH // 2
        self.camera_offset_x = max(min_camera_x, min(self.camera_offset_x, max_camera_x))
        
        # Y轴相机限制（允许向下看，但限制向上看）
        min_camera_y = -float('inf')  # 移除上边界限制，允许无限向上
        max_camera_y = 0  # 不让相机低于起始位置太多
        self.camera_offset_y = max(min_camera_y, min(self.camera_offset_y, max_camera_y))
    
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
            if not isinstance(sprite, Arrow):
                screen_x = sprite.rect.x - self.camera_offset_x
                screen_y = sprite.rect.y - self.camera_offset_y  # 添加y轴偏移
                self.screen.blit(sprite.image, (screen_x, screen_y))
        

        # 单独绘制箭矢
        for arrow in self.arrows:
            screen_x = arrow.rect.x - self.camera_offset_x
            screen_y = arrow.rect.y - self.camera_offset_y
            self.screen.blit(arrow.image, (screen_x, screen_y))
    
        # 使用系统字体来显示中文
        # 首先尝试几种常见的中文字体
        fonts_to_try = ['simhei', 'simkai', 'simsun', 'microsoftyahei', 'arialunicode']
        font = None
        for font_name in fonts_to_try:
            try:
                font = pygame.font.Font(f"C:/Windows/Fonts/{font_name}.ttf", 24)
                break
            except FileNotFoundError:
                try:
                    font = pygame.font.SysFont(font_name, 24)
                    break
                except:
                    continue
        
        # 如果找不到中文字体，使用默认字体
        if font is None:
            font = pygame.font.SysFont(None, 24)
        
        # # 显示提示信息
        # text = font.render("使用 A/D 键移动，W 键跳跃", True, RED)
        # self.screen.blit(text, (10, 10))
        
        # 显示当前得分
        score_text = font.render(f"游戏得分: {self.score}", True, RED)
        self.screen.blit(score_text, (10, 35))
        
        # 显示当前高度
        current_height = self.base_height - self.player.rect.y  # 计算当前高度（相对于起始点）
        height_text = font.render(f"当前高度: {current_height}", True, RED)
        self.screen.blit(height_text, (10, 60))
        
        # 显示当前重生点信息
        # respawn_text = font.render(f"Respawn: ({self.respawn_point[0]}, {self.respawn_point[1]})", True, RED)
        # self.screen.blit(respawn_text, (10, 60))
        
        # 如果游戏结束，显示重新开始提示
        if self.game_over:
            large_font = None
            for font_name in fonts_to_try:
                try:
                    large_font = pygame.font.Font(f"C:/Windows/Fonts/{font_name}.ttf", 48)
                    break
                except FileNotFoundError:
                    try:
                        large_font = pygame.font.SysFont(font_name, 48)
                        break
                    except:
                        continue

            if large_font is None:
                large_font = pygame.font.SysFont(None, 48)
                
            game_over_text = large_font.render("GAME OVER!", True, RED)
            restart_text = font.render("按任意键重新开始", True, RED)
            # 添加最终得分显示
            final_score_text = font.render(f"最终得分: {self.score}", True, RED)
            
            # 居中显示文本
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
            
            # 闪烁效果：每秒闪烁一次
            if self.restart_timer < 30:  # 半秒亮半秒暗
                self.screen.blit(game_over_text, game_over_rect)
                self.screen.blit(restart_text, restart_rect)
                self.screen.blit(final_score_text, final_score_rect)
        
        pygame.display.flip()
                
                    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()