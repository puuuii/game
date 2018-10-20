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
        self.player = Player(int(LENGTH_OF_ONE_SIDE/2), int(LENGTH_OF_ONE_SIDE/2))

    def mainroop(self):
        """メインループ"""
        clock = pygame.time.Clock()
        fullscreen_flag = False
        while True:
            clock.tick(FPS)

            # マウスハンドル
            self.handle_mouse()

            # キーハンドル
            self.handle_key()

            # マップ更新
            self.map.update(self.screen)

            # 画面描画
            pygame.display.update()

            # イベントハンドラ
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN and event.key == K_F2:
                    fullscreen_flag = not fullscreen_flag
                    if fullscreen_flag:
                        self.screen = pygame.display.set_mode(SCR_RECT.size, FULLSCREEN)
                    else:
                        self.screen = pygame.display.set_mode(SCR_RECT.size)

    def handle_mouse(self):
        """マウスハンドル"""
        mouse_pressed = pygame.mouse.get_pressed()

        # 左クリック
        if mouse_pressed[0]:
            pass

        # 右クリック
        elif mouse_pressed[1]:
            pass

    def handle_key(self):
        """キーハンドル"""
        keys_pressed = pygame.key.get_pressed()

        # 押されているキーに応じてマップ移動
        if keys_pressed[K_LEFT]:
            self.map.move(-1*SCROLL_SPEED, 0)
        if keys_pressed[K_RIGHT]:
            self.map.move(1*SCROLL_SPEED, 0)
        if keys_pressed[K_UP]:
            self.map.move(0, -1*SCROLL_SPEED)
        if keys_pressed[K_DOWN]:
            self.map.move(0, 1*SCROLL_SPEED)
