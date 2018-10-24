from src.consts import *
import random


class Nation:
    """国家クラス"""

    def __init__(self, name, coordinates=None, population=0, parameter=None):
        self.name = name
        self.coordinates = coordinates
        self.population = population
        if parameter == None:
            self.parameter = {name: value for name, value in zip(PARAMS, random.randint(1, MAX_INIT_PARAMETER))}
        else:
            self.parameter = parameter

    def get_coordinates(self):
        return self.coordinates