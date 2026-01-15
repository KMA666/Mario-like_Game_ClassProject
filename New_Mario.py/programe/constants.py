# constants.py - 游戏常量定义
# 游戏常量
# -*- coding: utf-8 -*-
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -12
PLAYER_SPEED = 5
SPRINT_MULTIPLIER = 1.5  # 奔跑速度倍数

# 颜色定义
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
SPIKE_COLOR = (105, 105, 105)  # 尖刺颜色

# 角色尺寸
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 48

# 死亡区域类型
DEATH_GROUND = "death_ground"
PLATFORM = "platform"

# 在 constants.py 文件末尾添加
# 箭矢尺寸
ARROW_WIDTH = 10
ARROW_HEIGHT = 30