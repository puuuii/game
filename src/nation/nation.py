from src.consts import *
from src.parameter.parameter import NationParameter


class Nation:
    """国家クラス"""

    def __init__(self, name, coordinates=None, population=0):
        self.name = name
        self.coordinates = coordinates
        self.population = population
        self.level = NATION_LEVEL_CASTLE
        self.parameter = NationParameter()
        self.nation_converter = None

    def update(self, screen, center_point, left_top, right_bottom):
        """国家更新"""

        # 国家位置をx, yにばらして確保
        x = self.coordinates[X]
        y = self.coordinates[Y]

        # 現在描画中のセルに含まれている場合のみ描画処理続行
        if not ((left_top[X] <= x <= right_bottom[X]) and (left_top[Y] <= y <= right_bottom[Y])):
            return

        # 国家の描画スクリーン上の解像度座標算出
        x = (x - left_top[X]) * PIXCEL_OF_ONE_SIDE
        y = (y - left_top[Y]) * PIXCEL_OF_ONE_SIDE

        # 国家レベルによって画像のどの部分を中心座標とするかが異なる
        coordinates = ()
        if self.level == NATION_LEVEL_VILLAGE:
            coordinates = (x, y)
        elif self.level == NATION_LEVEL_TOWN:
            coordinates = (x - PIXCEL_OF_ONE_SIDE, y)
        elif self.level == NATION_LEVEL_CASTLE_TOWN:
            coordinates = (x - PIXCEL_OF_ONE_SIDE, y - PIXCEL_OF_ONE_SIDE)
        elif self.level == NATION_LEVEL_CASTLE:
            coordinates = (x - PIXCEL_OF_ONE_SIDE, y - PIXCEL_OF_ONE_SIDE*2)

        screen.blit(self.nation_converter[self.level], coordinates)

    def get_coordinates(self):
        return self.coordinates

    def set_converter(self, converter):
        self.nation_converter = converter