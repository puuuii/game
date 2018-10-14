from pygame.image import load
import pickle
import numpy as np
from src.consts import *


class Map:
    """マップクラス"""

    def __init__(self):
        self.stage = self._create_stage(ROOP_MAKING)
        self.trrain_converter = {SEA: load('../img/sea1.png').convert(),
                                 SAND: load('../img/sand1.png').convert(),
                                 GLASS: load('../img/glass1.png').convert(),
                                 FOREST: load('../img/forest1.png').convert(),
                                 MOUNTAIN: load('../img/mountain1.png').convert(),
                                 RIVER: load('../img/river1.png').convert()}

    def _create_stage(self, roop_making):
        """ステージ作成"""

        # 海と陸の作成
        stage = np.random.randint(2, size=(LENGTH_OF_ONE_SIDE, LENGTH_OF_ONE_SIDE))
        for i in range(roop_making):
            for r in range(LENGTH_OF_ONE_SIDE):
                for c in range(LENGTH_OF_ONE_SIDE):
                    stage[r][c] = self._make_terrain(stage, r, c, SAND)

        return stage

    def _make_terrain(self, stage, r, c, value):
        """周囲の地形から特定地形作成"""
        # 外周は海とする
        try:
            counter = 0
            for i in range(-1, 1, 1):
                for j in range(-1, 1, 1):
                    if i == 0 and j == 0:
                        continue
                    if stage[r+i][c+j] == value:
                        counter += 1
        except:
            return SEA

        # 要素数8のリスト要素のうちカウンターの個数だけvalueにし、そこからランダムで値を取り出す
        random_array = np.r_[np.full(counter, value), np.full(8-counter, 0)]

        return np.random.choice(random_array, 1)

    
    def update(self, screen):
        """描画更新"""
        for r in range(LENGTH_OF_ONE_SIDE):
            for c in range(LENGTH_OF_ONE_SIDE):
                terrain = self.stage[r][c]
                screen.blit(self.trrain_converter[terrain], (c*PIXCEL_OF_ONE_SIDE, r*PIXCEL_OF_ONE_SIDE))
