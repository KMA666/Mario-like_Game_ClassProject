import pygame
import sys
from move import Game

if __name__ == "__main__":
    pygame.init()  # 在这里初始化pygame
    game = Game()
    game.run()
    