import pygame
from pygame.image import load
from src.consts import *


class Player:
    """プレイヤークラス"""

    def __init__(self, x, y):
        self.x = x  # x座標
        self.y = y  # y座標
        self.img_current = load(PATH_IMAGE_PLAYER).convert()

    def move(self, x, y):
        """移動処理"""

        self.x += x
        self.y += y

        return (self.x, self.y)

