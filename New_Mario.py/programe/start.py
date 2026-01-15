# start.py - 游戏开始页面
# -*- coding: utf-8 -*-
import pygame
import sys
from constants import *

class StartScreen:
    def __init__(self):
        # 初始化屏幕
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("平台跳跃游戏 - 开始")
        self.clock = pygame.time.Clock()
        
        # 字体设置 - 优先使用系统字体，兼容中文
        self.title_font = self.get_chinese_font(72)
        self.instruction_font = self.get_chinese_font(36)
        
        # 火柴人大小设置
        self.stickman_scale = 2  # 火柴人放大倍数
    
    def get_chinese_font(self, size):
        """获取支持中文的字体"""
        # 尝试多种中文字体
        chinese_fonts = [
            'SimHei',           # 黑体
            'Microsoft YaHei',  # 微软雅黑
            'SimSun',           # 宋体
            'KaiTi',            # 楷体
            'FangSong',         # 仿宋
        ]
        
        for font_name in chinese_fonts:
            try:
                return pygame.font.SysFont(font_name, size)
            except:
                continue
        
        # 如果没有找到合适的中文字体，使用默认字体
        return pygame.font.SysFont(None, size)
    
    def draw_charming_stickman(self, x, y):
        """
        绘制一个侧趴姿势的火柴人
        """
        # 计算火柴人各部分尺寸（基于原始尺寸放大）
        head_radius = 6 * self.stickman_scale
        body_length = (PLAYER_HEIGHT // 10 + 5) * self.stickman_scale
        limb_length = 12 * self.stickman_scale
        
        # 绘制头部（椭圆形，模拟侧趴视角）
        pygame.draw.ellipse(self.screen, (44, 34, 100), 
                           (x - head_radius, y - head_radius, 
                            head_radius * 2, head_radius * 1.5))
        
        # 绘制身体（弯曲的身体，展现侧趴姿势）
        body_curve = 9* self.stickman_scale  # 身体弯曲程度
        
        # 身体起点
        body_start_x = x + head_radius
        body_start_y = y - head_radius // 2
        # 身体终点
        body_end_x = x + body_length
        body_end_y = y + body_curve
        
        # 绘制弯曲的身体
        pygame.draw.line(self.screen, (2, 0, 0), 
                        (body_start_x, body_start_y), 
                        (body_end_x, body_end_y), 
                        int(2 * self.stickman_scale))
        
        # 绘制手臂（支撑地面的姿势）
        # 左手臂（前肢）
        left_arm_start_x = x + head_radius + 5 * self.stickman_scale
        left_arm_start_y = y - 3 * self.stickman_scale
        left_arm_end_x = left_arm_start_x + 557 * self.stickman_scale
        left_arm_end_y = left_arm_start_y + 8 * self.stickman_scale
        
        # 右手臂（后肢）
        right_arm_start_x = x + head_radius + 10 * self.stickman_scale
        right_arm_start_y = y
        right_arm_end_x = right_arm_start_x - 802 * self.stickman_scale
        right_arm_end_y = right_arm_start_y + 10 * self.stickman_scale
        
        pygame.draw.line(self.screen, (0, 0, 0), 
                        (left_arm_start_x, left_arm_start_y), 
                        (left_arm_end_x, left_arm_end_y), 
                        int(2 * self.stickman_scale))
        pygame.draw.line(self.screen, (0, 0, 0), 
                        (right_arm_start_x, right_arm_start_y), 
                        (right_arm_end_x, right_arm_end_y), 
                        int(2 * self.stickman_scale))
        
        # 绘制腿（弯曲的腿部，增加动态感）
        # 左腿
        left_leg_start_x = body_end_x - 5 * self.stickman_scale
        left_leg_start_y = body_end_y - 2 * self.stickman_scale
        left_leg_knee_x = left_leg_start_x + 8 * self.stickman_scale
        left_leg_knee_y = left_leg_start_y + 6 * self.stickman_scale
        left_leg_end_x = left_leg_knee_x + 6 * self.stickman_scale
        left_leg_end_y = left_leg_knee_y + 4 * self.stickman_scale
        
        pygame.draw.line(self.screen, (0, 0, 0), 
                        (left_leg_start_x, left_leg_start_y), 
                        (left_leg_knee_x, left_leg_knee_y), 
                        int(2 * self.stickman_scale))
        pygame.draw.line(self.screen, (0, 0, 0), 
                        (left_leg_knee_x, left_leg_knee_y), 
                        (left_leg_end_x, left_leg_end_y), 
                        int(2 * self.stickman_scale))
        
        # 右腿
        right_leg_start_x = body_end_x - 2 * self.stickman_scale
        right_leg_start_y = body_end_y
        right_leg_knee_x = right_leg_start_x + 10 * self.stickman_scale
        right_leg_knee_y = right_leg_start_y + 4 * self.stickman_scale
        right_leg_end_x = right_leg_knee_x + 8 * self.stickman_scale
        right_leg_end_y = right_leg_knee_y + 6 * self.stickman_scale
        
        pygame.draw.line(self.screen, (0, 0, 0), 
                        (right_leg_start_x, right_leg_start_y), 
                        (right_leg_knee_x, right_leg_knee_y), 
                        int(2 * self.stickman_scale))
        pygame.draw.line(self.screen, (0, 0, 0), 
                        (right_leg_knee_x, right_leg_knee_y), 
                        (right_leg_end_x, right_leg_end_y), 
                        int(2 * self.stickman_scale))

    def draw(self):
        # 白色背景
        self.screen.fill(WHITE)
        
        # 绘制大型侧趴火柴人
        stickman_x = SCREEN_WIDTH // 2 - 50  # 调整位置，给文字留出空间
        stickman_y = SCREEN_HEIGHT // 8 + 30  # 火柴人在屏幕上方三分之一处
        self.draw_charming_stickman(stickman_x, stickman_y)
        
        # 绘制标题文字
        title_text = self.title_font.render("往上跳！", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 80))
        self.screen.blit(title_text, title_rect)
        
        # 绘制开始提示文字
        start_text = self.instruction_font.render("按任意键开始游戏", True, (0, 3, 100))
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2-15, SCREEN_HEIGHT//1.5 - 20))
        self.screen.blit(start_text, start_rect)
        
        # 绘制操作说明
        controls_text = self.instruction_font.render("A/D键移动，W键跳跃，Shift键加速奔跑", True, (23, 30, 50))
        controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//1.2 + 30))
        self.screen.blit(controls_text, controls_rect)
        
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                    # 按任意键继续
                    running = False
            
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    pygame.init()
    start_screen = StartScreen()
    start_screen.run()