import random
from src.consts import *


class Nation:
    """国家クラス"""

    def __init__(self, name, coordinates=None, population=0, parameter=None):
        self.name = name
        self.coordinates = coordinates
        self.population = population
        self.level = 1
        if parameter == None:
            self.parameter = {name: value for name, value in zip(PARAMS, random.randint(1, MAX_INIT_PARAMETER))}
        else:
            self.parameter = parameter
        self.nation_converter = None

    def update(self, screen):
        """国家更新"""

        # screen.blit(self.img_list[self.direction], (X_PLAYER, Y_PLAYER))

    def get_coordinates(self):
        return self.coordinates

    def set_converter(self, converter):
        self.nation_converter = converter