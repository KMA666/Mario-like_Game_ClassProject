# script.py - 主程序入口
import pygame
import sys
from game import Game

if __name__ == "__main__":
    pygame.init()  # 在这里初始化pygame
    game = Game()
    game.run()