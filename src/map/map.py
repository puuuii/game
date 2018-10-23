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
        self.stage = self._create_stage()    # 地形データテーブル
        self.trrain_converter = {SEA: load(PATH_SEA).convert(),
                                 SAND: load(PATH_SAND).convert(),
                                 GLASS: load(PATH_GLASS).convert(),
                                 FOREST: load(PATH_FOREST).convert(),
                                 MOUNTAIN: load(PATH_MOUNTAIN).convert(),
                                 RIVER: load(PATH_RIVER).convert()}
                                                            # 地形インデックスを対応する画像オブジェクトに変換

    def _create_stage(self):
        """ステージ作成"""

        # すでにステージが存在するならそれを返す
        if os.path.exists(PATH_STAGE):
            with open(PATH_STAGE, mode='rb') as f:
                return pickle.load(f)

        # 海と陸の作成
        stage = self._create_stage_sand()

        # 草原の作成
        stage = self._create_stage_option(stage, GLASS, WIDTH_SURROUND_GLASS, ROOP_GLASS_MAKING)
        
        # 森の作成
        stage = self._create_stage_option(stage, FOREST, WIDTH_SURROUND_FOREST, ROOP_FOREST_MAKING)

        # 山の作成
        stage = self._create_stage_option(stage, MOUNTAIN, WIDTH_SURROUND_MOUNTAIN, ROOP_MOUNTAIN_MAKING)

        # 川の作成
        stage = self._create_stage_river(stage)

        # ステージのpkl化
        with open(PATH_STAGE, mode='wb') as f:
            pickle.dump(stage, f)

        return stage

    def _create_stage_sand(self):
        """砂地の作成"""

        stage = np.random.randint(2, size=(STAGE_LENGTH, STAGE_LENGTH), dtype=np.uint8)
        for i in range(ROOP_SAND_MAKING):
            for r in range(STAGE_LENGTH):
                for c in range(STAGE_LENGTH):
                    stage[r][c] = self._make_terrain(stage, r, c, SAND)

        return stage

    def _create_stage_option(self, stage, terrain, width_surround, n_roop):
        """海&砂以外の地形地帯の作成"""

        # 海岸線から離れたところに地形作成
        stage_option = np.random.randint(terrain - 1, terrain + 1, size=(STAGE_LENGTH, STAGE_LENGTH), dtype=np.uint8)
        self._surround(stage_option, width_surround, 0)
        
        for i in range(n_roop):
            for r in range(STAGE_LENGTH):
                for c in range(STAGE_LENGTH):
                    stage_option[r][c] = self._make_terrain(stage_option, r, c, terrain)
        # 草原をステージに反映
        index = np.where(stage_option == terrain)
        stage[index] = terrain

        return stage

    def _create_stage_river(self, stage):
        """川の作成"""

        # それぞれの川の開始地点を取得
        the_first_quartile = int(STAGE_LENGTH / 4)
        half = int(STAGE_LENGTH / 2)
        candidates =  range(the_first_quartile, the_first_quartile + half)
        starts_x = np.random.choice(candidates, N_RIVER, replace=False)
        starts_y = np.random.choice(candidates, N_RIVER, replace=False)
        start_points = [(x, y) for x, y in zip(starts_x, starts_y)]

        # 開始地点から最も近い海岸に向かって川を伸ばす
        for start_point in start_points:
            # 開始地点の位置によってどの方向に川を伸ばすか決定
            move_candidates = []
            if start_point[0] < half:
                move_candidates.append((-1, 0))
            else:
                move_candidates.append((1, 0))
            if start_point[1] < half:
                move_candidates.append((0, -1))
            else:
                move_candidates.append((0, 1))

            # 川を海まで伸ばす
            stage[start_point[0]][start_point[1]] = RIVER
            target_x = start_point[0]
            target_y = start_point[1]
            while(True):
                move = np.random.permutation(move_candidates)[0]
                target_x = target_x + move[0]
                target_y = target_y + move[1]
                # 海に流れ着くか他の川に合流した場合は終了
                if (stage[target_x][target_y] == SEA) or (stage[target_x][target_y] == SEA):
                    break
                stage[target_x][target_y] = RIVER

        return stage

    def _surround(self, stage, witdh, terrain):
        """ステージを特定の地形で指定分だけ囲う"""
        stage[:witdh] = terrain
        stage[-witdh:] = terrain
        stage[:, :witdh] = terrain
        stage[:, -witdh:] = terrain

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

