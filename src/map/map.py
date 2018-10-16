import pickle
import numpy as np
import os
from src.consts import *
from pygame.image import load


class Map:
    """マップクラス"""

    def __init__(self):
        self.stage = self._create_stage(ROOP_MAP_MAKING)
        self.trrain_converter = {SEA: load(PATH_SEA).convert(),
                                 SAND: load(PATH_SAND).convert(),
                                 GLASS: load(PATH_GLASS).convert(),
                                 FOREST: load(PATH_FOREST).convert(),
                                 MOUNTAIN: load(PATH_MOUNTAIN).convert(),
                                 RIVER: load(PATH_RIVER).convert()}

    def _create_stage(self, roop_making):
        """ステージ作成"""

        # すでにステージが存在するならそれを返す
        if os.path.exists(PATH_STAGE):
            with open(PATH_STAGE, mode='rb') as f:
                return pickle.load(f)

        # 海と陸の作成
        stage = np.random.randint(2, size=(LENGTH_OF_ONE_SIDE, LENGTH_OF_ONE_SIDE))
        for i in range(roop_making):
            for r in range(LENGTH_OF_ONE_SIDE):
                for c in range(LENGTH_OF_ONE_SIDE):
                    stage[r][c] = self._make_terrain(stage, r, c, SAND)

        # ステージのpkl化
        with open(PATH_STAGE, mode='wb') as f:
            pickle.dump(stage, f)

        return stage

    def _make_terrain(self, stage, r, c, value):
        """周囲の地形から特定地形作成"""
        # 周囲8セルに特定地形が含まれる数をカウント
        counter = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                # 自身セルは除外
                if i == 0 and j == 0:
                    continue
                # 周囲がステージ外(ステージの外枠)の場合は海
                if (r+i < 0) or (r+1 >= stage.shape[0])\
                        or (c+j < 0) or (c+j >= stage.shape[1]):
                    return SEA
                # カウント
                if stage[r+i][c+j] == value:
                    counter += 1

        # 要素数8のリスト要素のうちカウンターの個数だけvalueにし、そこからランダムで値を取り出す
        random_array = np.r_[np.full(counter*3, value), np.full((8-counter)*2, 0)]

        return np.random.choice(random_array, 1)

    
    def update(self, screen):
        """描画更新"""
        for r in range(LENGTH_OF_ONE_SIDE):
            for c in range(LENGTH_OF_ONE_SIDE):
                terrain = self.stage[r][c]
                screen.blit(self.trrain_converter[terrain], (c*PIXCEL_OF_ONE_SIDE, r*PIXCEL_OF_ONE_SIDE))
