from src.consts import *
from src.parameter.parameter import NationParameter


class Nation:
    """国家クラス"""

    def __init__(self, name, coordinates=None, population=0):
        self.name = name
        self.coordinates = coordinates
        self.population = population
        self.level = 1
        self.parameter = NationParameter()
        self.nation_converter = None

    def update(self, screen):
        """国家更新"""

        # screen.blit(self.img_list[self.direction], (X_PLAYER, Y_PLAYER))

    def get_coordinates(self):
        return self.coordinates

    def set_converter(self, converter):
        self.nation_converter = converter