from src.consts import *
from pygame.image import load


class ConverterBase:
    """画像変換基底クラス"""
    _instance = None

    def __new__(cls, converter=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, converter):
        self.converter = converter

    def get_converter(self):
        return self.converter


class MapImage(ConverterBase):
    """マップ画像変換クラス"""

    def __init__(self):
        converter = {SEA: load(PATH_SEA).convert(),
                     SAND: load(PATH_SAND).convert(),
                     GLASS: load(PATH_GLASS).convert(),
                     FOREST: load(PATH_FOREST).convert(),
                     MOUNTAIN: load(PATH_MOUNTAIN).convert(),
                     RIVER: load(PATH_RIVER).convert()}
        super().__init__(converter)


class PlayerImage(ConverterBase):
    """プレーヤー画像変換クラス"""

    def __init__(self):
        converter = {DIRECTION_UP: load(PATH_IMAGE_PLAYER_UP).convert_alpha(),
                     DIRECTION_RIGHT: load(PATH_IMAGE_PLAYER_RIGHT).convert_alpha(),
                     DIRECTION_DOWN: load(PATH_IMAGE_PLAYER_DOWN).convert_alpha(),
                     DIRECTION_LEFT: load(PATH_IMAGE_PLAYER_LEFT).convert_alpha()}
        super().__init__(converter)


class NationImage(ConverterBase):
    """国家画像変換クラス"""

    def __init__(self):
        converter = {NATION_LEVEL_VILLAGE: load(PATH_IMAGE_VILLAGE).convert_alpha(),
                     NATION_LEVEL_TOWN: load(PATH_IMAGE_TOWN).convert_alpha(),
                     NATION_LEVEL_CASTLE_TOWN: load(PATH_IMAGE_CASTLE_TOWN).convert_alpha(),
                     NATION_LEVEL_CASTLE: load(PATH_IMAGE_CASTLE).convert_alpha()}
        super().__init__(converter)
