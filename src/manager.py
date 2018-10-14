import pygame
from src.consts import *
from src.player.player import Player
from src.map.map import Map
from pygame.locals import *


class Manager:
    """ゲーム管理クラス"""

    def __init__(self):
        self.screen = pygame.display.set_mode(SCR_RECT.size, DOUBLEBUF | HWSURFACE)
        self.map = Map()
        self.player = Player()

    def mainroop(self):
        """メインループ"""
        clock = pygame.time.Clock()
        fullscreen_flag = False
        while True:
            clock.tick(FPS)
            self.map.update(self.screen)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN and event.key == K_F2:
                    fullscreen_flag = not fullscreen_flag
                    if fullscreen_flag:
                        self.screen = pygame.display.set_mode(SCR_RECT.size, FULLSCREEN)
                    else:
                        self.screen = pygame.display.set_mode(SCR_RECT.size)