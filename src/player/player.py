from src.consts import *
from src.parameter.parameter import HumanParameter


class Player:
    """プレイヤークラス"""

    def __init__(self, coordinates, nation=None):
        self.coordinates = coordinates      # 座標
        self.img_list = None                # プレーヤー画像オブジェクト辞書
        self.direction = DIRECTION_UP       # 現在の方向
        self.nation = nation                # 所属国家
        self.parameter = HumanParameter()   # パラメータ

    def update(self, screen):
        """プレーヤー更新"""

        screen.blit(self.img_list[self.direction], (X_PLAYER, Y_PLAYER))

    def move(self, move_value):
        """移動処理"""

        self.coordinates[X] += move_value[X]
        self.coordinates[Y] += move_value[Y]

    def set_direction(self, direction):
        self.direction = direction

    def set_nation(self, nation):
        self.nation = nation

    def get_coordinates(self):
        return self.coordinates

    def set_imglist(self, images):
        self.img_list = images