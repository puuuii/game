import pickle
import numpy as np
import os
import time
from src.consts import *
from pygame.image import load
from multiprocessing import Manager, Process



class Map:
    """マップクラス"""

    def __init__(self, x, y):
        self.center_x = x
        self.center_y = y
        start_time = time.time()
        self.stage = self._create_stage()    # 地形データテーブル
        execution_time = time.time() - start_time
        print('_create_stage:', execution_time, 's')
        self.trrain_converter = {SEA: load(PATH_SEA).convert(),
                                 SAND: load(PATH_SAND).convert(),
                                 GLASS: load(PATH_GLASS).convert(),
                                 FOREST: load(PATH_FOREST).convert(),
                                 MOUNTAIN: load(PATH_MOUNTAIN).convert(),
                                 RIVER: load(PATH_RIVER).convert()}
                                                            # 地形インデックスを対応する画像オブジェクトに変換

    def _create_stage(self):
        """ステージ作成"""

        m = Manager()
        stage_dict = m.dict()

        # すでにステージが存在するならそれを返す
        if os.path.exists(PATH_STAGE):
            with open(PATH_STAGE, mode='rb') as f:
                return pickle.load(f)

        # 各種地形の作成
        jobs = [
            Process(target=self._create_stage_sand, args=(stage_dict,)),
            Process(target=self._create_stage_option, args=(GLASS, WIDTH_SURROUND_GLASS, ROOP_GLASS_MAKING, stage_dict)),
            Process(target=self._create_stage_option, args=(FOREST, WIDTH_SURROUND_FOREST, ROOP_FOREST_MAKING, stage_dict)),
            Process(target=self._create_stage_option, args=(MOUNTAIN, WIDTH_SURROUND_MOUNTAIN, ROOP_MOUNTAIN_MAKING, stage_dict)),
            Process(target=self._create_stage_river, args=(stage_dict,))
        ]
        for job in jobs:
            job.start()
        [job.join() for job in jobs]

        # 元ステージに反映
        stage = self._merge_stages(stage_dict.pop(SAND), stage_dict)

        # ステージのpkl化
        if not os.path.exists(PATH_DATA_DIR):
            os.mkdir(PATH_DATA_DIR)
        with open(PATH_STAGE, mode='wb') as f:
            pickle.dump(stage, f)

        return stage

    def _create_stage_sand(self, stage_dict):
        """砂地の作成"""

        stage = np.random.randint(2, size=(STAGE_LENGTH, STAGE_LENGTH), dtype=np.uint8)
        for i in range(ROOP_SAND_MAKING):
            for r in range(STAGE_LENGTH):
                for c in range(STAGE_LENGTH):
                    stage[r][c] = self._make_terrain(stage, r, c, SAND)

        stage_dict[SAND] = stage

    def _create_stage_option(self, terrain, width_surround, n_roop, stage_dict):
        """海&砂以外の地形地帯の作成"""

        # 海岸線から離れたところに地形作成
        stage = np.random.randint(terrain - 1, terrain + 1, size=(STAGE_LENGTH, STAGE_LENGTH), dtype=np.uint8)
        self._surround(stage, width_surround, 0)

        for i in range(n_roop):
            for r in range(STAGE_LENGTH):
                for c in range(STAGE_LENGTH):
                    stage[r][c] = self._make_terrain(stage, r, c, terrain)

        stage_dict[terrain] = stage

    def _create_stage_river(self, stage_dict):
        """川の作成"""

        stage = np.empty((STAGE_LENGTH, STAGE_LENGTH), dtype=np.int8)

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
                if (target_x == -1) or (target_x == STAGE_LENGTH) or (target_y == -1)\
                        or (target_y == STAGE_LENGTH) or (stage[target_x][target_y] == RIVER):
                    break
                stage[target_x][target_y] = RIVER

        stage_dict[RIVER] = stage

    def _surround(self, stage, witdh, terrain):
        """ステージを特定の地形で指定分だけ囲う"""
        stage[:witdh] = terrain
        stage[-witdh:] = terrain
        stage[:, :witdh] = terrain
        stage[:, -witdh:] = terrain

    def _make_terrain(self, stage, r, c, value):
        """周囲の地形から特定地形作成"""

        # 周囲8セルに特定地形が含まれる数をカウント
        surrounding = stage[r-1:r+2, c-1:c+2]
        if not surrounding.shape == (3, 3):
            return SEA
        counter = np.sum(surrounding == value)

        # 要素数9のリスト要素のうちカウンターの個数だけvalueにし、そこからランダムで値を取り出す
        random_array = ([value]*counter*2) + ([0]*(9-counter))

        return np.random.choice(random_array)

    def _merge_stages(self, original_stage, stage_dict):
        """各地形ステージを合成"""

        for terrain, stage in stage_dict.items():
            index = np.where(stage == terrain)
            original_stage[index] = terrain

        return original_stage

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

