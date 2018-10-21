import pygame
from pygame.image import load
from src.consts import *


class Player:
    """プレイヤークラス"""

    def __init__(self, x, y):
        self.x = x                                                  # x座標
        self.y = y                                                  # y座標
        self.img_list = {DIRECTION_UP: load(PATH_IMAGE_PLAYER_UP).convert_alpha(),
                         DIRECTION_RIGHT: load(PATH_IMAGE_PLAYER_RIGHT).convert_alpha(),
                         DIRECTION_DOWN: load(PATH_IMAGE_PLAYER_DOWN).convert_alpha(),
                         DIRECTION_LEFT: load(PATH_IMAGE_PLAYER_LEFT).convert_alpha()}
                                                                    # プレーヤー画像オブジェクト辞書
        self.direction = DIRECTION_UP

    def update(self, screen):
        """プレーヤー更新"""

        screen.blit(self.img_list[self.direction], (X_PLAYER, Y_PLAYER))

    def move(self, x, y):
        """移動処理"""

        self.x += x
        self.y += y

        return (self.x, self.y)

    def set_direction(self, direction):
        self.direction = direction