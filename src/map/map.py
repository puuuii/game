import pickle
import numpy as np
import os
from src.consts import *
from pygame.image import load


class Map:
    """マップクラス"""

    def __init__(self, x, y):
        self.center_x = x
        self.center_y = y
        self.stage = self._create_stage(ROOP_MAP_MAKING)    # 地形データテーブル
        self.trrain_converter = {SEA: load(PATH_SEA).convert(),
                                 SAND: load(PATH_SAND).convert(),
                                 GLASS: load(PATH_GLASS).convert(),
                                 FOREST: load(PATH_FOREST).convert(),
                                 MOUNTAIN: load(PATH_MOUNTAIN).convert(),
                                 RIVER: load(PATH_RIVER).convert()}
                                                            # 地形インデックスを対応する画像オブジェクトに変換

    def _create_stage(self, roop_making):
        """ステージ作成"""

        # すでにステージが存在するならそれを返す
        if os.path.exists(PATH_STAGE):
            with open(PATH_STAGE, mode='rb') as f:
                return pickle.load(f)

        # 海と陸の作成
        stage = np.random.randint(2, size=(STAGE_LENGTH, STAGE_LENGTH))
        for i in range(roop_making):
            for r in range(STAGE_LENGTH):
                for c in range(STAGE_LENGTH):
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

        # オフセット算出
        offset_x = self._calc_offset(self.center_x)
        offset_y = self._calc_offset(self.center_y)

        # 現在セルを基点においたセル単位で2重ループを回しつつ描画設定
        half_length_of_render_x = int(N_CELL_RENDER_X/2)
        half_length_of_render_y = int(N_CELL_RENDER_Y/2)
        for r in range(-1*half_length_of_render_y, half_length_of_render_y):
            for c in range(-1*half_length_of_render_x, half_length_of_render_x):
                # 現在処理中のセル座標がステージ外であれば地形は海
                if self._is_outside_of_stage(c, r):
                    terrain = SEA
                else:
                    idx_x = int(self.center_x + c)
                    idx_y = int(self.center_y + r)
                    terrain = self.stage[idx_x][idx_y]

                # 描画設定
                x = (half_length_of_render_x + c) * PIXCEL_OF_ONE_SIDE - offset_x
                y = (half_length_of_render_y + r) * PIXCEL_OF_ONE_SIDE - offset_y
                screen.blit(self.trrain_converter[terrain], (x, y))

    def _is_outside_of_stage(self, c, r):
        """ステージ外かどうか判定"""
        result = not ((0 < (self.center_x + c) < STAGE_LENGTH) and (0 < (self.center_y + r) < STAGE_LENGTH))
        return result

    def _calc_offset(self, value):
        """オフセット値算出"""

        offset = 1 - (value - int(value))
        if offset == 1:
            offset = 0
        return offset

    def move(self, move_value):
        """マップ移動"""

        target_x = self.center_x + move_value[0]
        target_y = self.center_y + move_value[1]

        # 水辺は移動不可
        if (self.stage[target_x][target_y] == SEA)\
                or (self.stage[target_x][target_y] == RIVER):
            return False

        self.center_x = target_x
        self.center_y = target_y

        return True

