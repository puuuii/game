import numpy as np
from src.consts import *
from multiprocessing import Manager, Process

class Map:
    """マップクラス"""

    def __init__(self, x=int(STAGE_LENGTH/2), y=int(STAGE_LENGTH/2)):
        self.center_x = x
        self.center_y = y
        self.left_top = [0, 0]
        self.right_bottom = [0, 0]
        self.stage = self._create_stage()    # 地形データテーブル
        self.terrain_converter = None        # 地形インデックスを画像オブジェクトに変換テーブル

    def _create_stage(self):
        """ステージ作成"""

        m = Manager()
        stage_dict = m.dict()

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

        return stage

    def _create_stage_sand(self, stage_dict):
        """砂地の作成"""

        stage = np.random.randint(2, size=(STAGE_LENGTH, STAGE_LENGTH))
        for i in range(ROOP_SAND_MAKING):
            for r in range(STAGE_LENGTH):
                for c in range(STAGE_LENGTH):
                    stage[r][c] = self._make_terrain(stage, r, c, SAND)

        stage_dict[SAND] = stage

    def _create_stage_option(self, terrain, width_surround, n_roop, stage_dict):
        """海&砂以外の地形地帯の作成"""

        # 海岸線から離れたところに地形作成
        stage = np.random.randint(terrain - 1, terrain + 1, size=(STAGE_LENGTH, STAGE_LENGTH))
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
            move_candidates = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if start_point[0] < half:
                move_candidates.append((-1, 0))
                move_candidates.append((-1, 0))
            else:
                move_candidates.append((1, 0))
                move_candidates.append((1, 0))
            if start_point[1] < half:
                move_candidates.append((0, -1))
                move_candidates.append((0, -1))
            else:
                move_candidates.append((0, 1))
                move_candidates.append((0, 1))

            # 川を海まで伸ばす
            stage[start_point[0]][start_point[1]] = RIVER
            target_x = start_point[0]
            target_y = start_point[1]
            while(True):
                move = np.random.permutation(move_candidates)[0]
                target_x = target_x + move[0]
                target_y = target_y + move[1]
                # 海に流れ着くと終了
                if (target_x == -1) or (target_x == STAGE_LENGTH)\
                        or (target_y == -1) or (target_y == STAGE_LENGTH):
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

        # 現在描画中のマップデータを回しつつ描画していく
        left, top = self.left_top
        right, bottom = self.right_bottom
        for r in range(top, bottom):
            for c in range(left, right):
                # ステージ外は海描画
                if self._is_outside_of_stage(c, r):
                    terrain = SEA
                else:
                    terrain = self.stage[c][r]
                x = (c - left) * PIXCEL_OF_ONE_SIDE
                y = (r - top) * PIXCEL_OF_ONE_SIDE

                screen.blit(self.terrain_converter[terrain], (x, y))

    def _is_outside_of_stage(self, c, r):
        """ステージ外かどうか判定"""
        result = not ((0 < c < STAGE_LENGTH) and (0 < r < STAGE_LENGTH))
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
        terrain = self.stage[target_x][target_y]
        if (terrain == SEA) or (terrain == RIVER):
            return False

        self.center_x = target_x
        self.center_y = target_y

        # 移動処理と同時に現在描画中のセル範囲も設定
        self.calc_limits()

        return True

    def calc_limits(self):
        """セル単位で現在描画中の座標算出"""

        self.left_top = [self.center_x - int(WIDTH_IN_CELL / 2), self.center_y - int(HEIGHT_IN_CELL / 2)]
        self.right_bottom = [self.center_x + int(WIDTH_IN_CELL / 2), self.center_y + int(HEIGHT_IN_CELL / 2)]

    def set_centers(self, x, y):
        self.center_x = x
        self.center_y = y

    def set_converter(self, converter):
        self.terrain_converter = converter

    def get_left_top(self):

        return self.left_top

    def get_right_buttom(self):

        return self.right_bottom
