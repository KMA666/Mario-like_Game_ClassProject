#main.py - 主程序入口
# -*- coding: utf-8 -*-
import pygame
import sys

from start import StartScreen  # 导入开始页面
from game import Game

if __name__ == "__main__":
    pygame.init()  # 在这里初始化pygame
    
    # 先显示开始页面
    start_screen = StartScreen()
    start_screen.run()
    
    # 开始页面结束后启动游戏
    game = Game()
    game.run()