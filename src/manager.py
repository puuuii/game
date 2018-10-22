import pygame
from src.consts import *
from src.player.player import Player
from src.map.map import Map
from pygame.locals import *


class Manager:
    """ゲーム管理クラス"""

    def __init__(self):
        self.screen = pygame.display.set_mode(SCR_RECT.size, DOUBLEBUF | HWSURFACE)
        self.player = Player(N_CELL_RENDER_X, N_CELL_RENDER_Y)
        self.map = Map(N_CELL_RENDER_X, N_CELL_RENDER_Y)

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

            # 各種更新更新
            self.map.update(self.screen)
            self.player.update(self.screen)

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

        # 押されているキーに応じてプレーヤー方向と移動量決定
        move_value_list = []
        if keys_pressed[K_LEFT]:
            self.player.set_direction(DIRECTION_LEFT)
            move_value_list.append((-1, 0))
        if keys_pressed[K_RIGHT]:
            self.player.set_direction(DIRECTION_RIGHT)
            move_value_list.append((1, 0))
        if keys_pressed[K_UP]:
            self.player.set_direction(DIRECTION_UP)
            move_value_list.append((0, -1))
        if keys_pressed[K_DOWN]:
            self.player.set_direction(DIRECTION_DOWN)
            move_value_list.append((0, 1))

        # 移動可能な場合のみ移動処理
        for move_value in move_value_list:
            if self.map.move(move_value):
                self.player.move(move_value)