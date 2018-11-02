import os
import pickle
import random
import string
import time
from multiprocessing import Manager, Process

import pygame

from src.converter import *
from src.map.map import Map
from src.nation.nation import Nation
from src.player.player import Player


class GameManager:
    """ゲーム管理クラス"""

    def __init__(self):
        # 各種オブジェクト初期化
        self._make_data_directory()
        self.screen = pygame.display.set_mode(SCR_RECT.size, DOUBLEBUF | HWSURFACE)
        self.map = self._make_init_map()
        self.nations = self._make_init_nations()
        self.player = self._make_init_player(random.choice(self.nations))
        m = Manager()
        self.timer = m.dict()
        self.font_time = pygame.font.Font(FONT_GOTHIC, STRING_SIZE_TIME)

        # マップの初期中心位置設定はプレーヤー位置と同位置
        coordinates = self.player.get_coordinates()
        self.map.set_centers(coordinates[X], coordinates[Y])
        self.map.calc_limits()

        # タイマー開始
        self.start_timer()

    def _make_data_directory(self):
        """dataディレクトリ作成"""

        if not os.path.exists(PATH_DATA_DIR):
            os.mkdir(PATH_DATA_DIR)

    def _make_init_map(self):
        """マップ初期化"""

        map = None
        # すでにマップが存在するならそれを返す
        if os.path.exists(PATH_STAGE):
            with open(PATH_STAGE, mode='rb') as f:
                map = pickle.load(f)
        else:
            map = Map()
        map.set_converter(MapImage().get_converter())

        # マップオブジェクトのpkl化
        with open(PATH_STAGE, mode='wb') as f:
            pickle.dump(map, f)

        return map

    def _make_init_nations(self):
        """国家初期化"""

        nations = []
        # すでに国家が存在するならそれを返す
        if os.path.exists(PATH_NATIONS):
            with open(PATH_NATIONS, mode='rb') as f:
                nations = pickle.load(f)
        else:
            for i in range(N_NATION):
                name = ''.join([random.choice(string.ascii_letters + string.digits) for j in range(N_NATION_NAME)])
                coordinates = (random.randint(0, STAGE_LENGTH), random.randint(0, STAGE_LENGTH))
                population = random.randint(1, MAX_INIT_POPULATION)
                nations.append(Nation(name, coordinates, population))
        [nation.set_converter(NationImage().get_converter()) for nation in nations]

        # pkl化
        with open(PATH_NATIONS, mode='wb') as f:
            pickle.dump(nations, f)

        return nations

    def _make_init_player(self, nation):
        """プレーヤー初期化"""

        player = None
        # すでに国家が存在するならそれを返す
        if os.path.exists(PATH_PLAYER):
            with open(PATH_PLAYER, mode='rb') as f:
                player = pickle.load(f)
        else:
            player = Player(list(nation.get_coordinates()), nation=nation)
        player.set_imglist(PlayerImage().get_converter())

        # pkl化
        with open(PATH_PLAYER, mode='wb') as f:
            pickle.dump(player, f)

        return player

    def mainroop(self):
        """メインループ"""
        clock = pygame.time.Clock()
        fullscreen_flag = False
        while True:
            clock.tick(FPS)

            # マウスハンドル
            self.handle_mouse()

            # キーハンドル
            self.handle_key()

            # 各種更新
            self.map.update(self.screen)
            [nation.update(self.screen, self.map.get_left_top(), self.map.get_right_buttom())
             for nation in self.nations]
            self.player.update(self.screen)
            self.update_time()

            # 画面描画
            pygame.display.update()

            # イベントハンドラ
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN and event.key == K_F2:
                    fullscreen_flag = not fullscreen_flag
                    if fullscreen_flag:
                        self.screen = pygame.display.set_mode(SCR_RECT.size, FULLSCREEN)
                    else:
                        self.screen = pygame.display.set_mode(SCR_RECT.size)

    def handle_mouse(self):
        """マウスハンドル"""
        mouse_pressed = pygame.mouse.get_pressed()

        # 左クリック
        if mouse_pressed[0]:
            pass

        # 右クリック
        elif mouse_pressed[1]:
            pass

    def handle_key(self):
        """キーハンドル"""
        keys_pressed = pygame.key.get_pressed()

        # 押されているキーに応じてプレーヤー方向と移動量決定
        move_value_list = []
        if keys_pressed[K_LEFT]:
            self.player.set_direction(DIRECTION_LEFT)
            move_value_list.append((-1*SCROLL_SPEED, 0))
        if keys_pressed[K_RIGHT]:
            self.player.set_direction(DIRECTION_RIGHT)
            move_value_list.append((1*SCROLL_SPEED, 0))
        if keys_pressed[K_UP]:
            self.player.set_direction(DIRECTION_UP)
            move_value_list.append((0, -1*SCROLL_SPEED))
        if keys_pressed[K_DOWN]:
            self.player.set_direction(DIRECTION_DOWN)
            move_value_list.append((0, 1*SCROLL_SPEED))

        # 移動可能な場合のみ移動処理
        for move_value in move_value_list:
            if self.map.move(move_value):
                self.player.move(move_value)

    def start_timer(self):
        """タイマー開始"""

        # すでにマップが存在するならそれを返す
        if os.path.exists(PATH_TIMER):
            with open(PATH_TIMER, mode='rb') as f:
                timer = pickle.load(f)
                self.timer[MINUTE] = timer[MINUTE]
                self.timer[HOUR] = timer[HOUR]
                self.timer[DAY] = timer[DAY]
                self.timer[MONTH] = timer[MONTH]
                self.timer[YEAR] = timer[YEAR]
        # ない場合は初期化
        else:
            self.timer[MINUTE] = 0
            self.timer[HOUR] = 6
            self.timer[DAY] = 1
            self.timer[MONTH] = APR
            self.timer[YEAR] = 1

        job = Process(target=self.count_timer)
        job.start()

    def count_timer(self):
        """時間計測"""

        while True:
            time.sleep(1)
            self.timer[MINUTE] += 1

            if self.timer[MINUTE] >= 60:
                self.timer[MINUTE] = 0
                self.timer[HOUR] += 1

            if self.timer[HOUR] >= 24:
                self.timer[HOUR] = 0
                self.timer[DAY] += 1

            if self.timer[DAY] > 28:
                self.timer[DAY] = 0
                self.timer[MONTH] += 1

            if self.timer[MONTH] > DEC:
                self.timer[MONTH] = JAN
                self.timer[YEAR] += 1

            # マップオブジェクトのpkl化
            with open(PATH_TIMER, mode='wb') as f:
                timer = {MINUTE: self.timer[MINUTE], HOUR: self.timer[HOUR], DAY: self.timer[DAY],
                         MONTH: self.timer[MONTH], YEAR: self.timer[YEAR]}
                pickle.dump(timer, f)

    def timer_to_string(self):
        """タイマー変数の内容を表示用文字列に変換"""

        string = str(self.timer[YEAR]).zfill(2) + '年目 '\
                 + str(self.timer[MONTH]).zfill(2) + '月 '\
                 + str(self.timer[DAY]).zfill(2) + '日 '\
                 + str(self.timer[HOUR]).zfill(2) + ' : '\
                 + str(self.timer[MINUTE]).zfill(2)
        return string

    def update_time(self):
        """時間表記&夕方&夜描画処理更新"""

        # 夕方&夜処理
        rect_evening = pygame.Surface((640, 480), SRCALPHA, 32)
        rect_night = pygame.Surface((640, 480), SRCALPHA, 32)
        minute = self.timer[MINUTE]
        hour = self.timer[HOUR]

        # 夕方は4時〜5時の間で濃くなる
        depth_evening = 0
        if 16 <= hour <= 17:
            # 最大値を255に補正
            depth_evening = int((((hour - 16) + (minute / 60)) / 2) * 255)
        # 夕方は6時〜9時の間で薄くなる
        elif 18 <= hour <= 21:
            # 最大値を255に補正
            depth_evening = int((((21 - hour) + (1 - (minute / 60))) / 4) * 255)
        # 夕方色を作成&設定
        color_evening = list(COLOR_ORANGE) + [int(depth_evening / 2)]
        rect_evening.fill(color_evening)
        self.screen.blit(rect_evening, (0, 0))

        # 夜は6時〜9時の間で濃くなる
        depth_night = 0
        if 18 <= hour <= 21:
            # 最大値を255に補正
            depth_night = int((((hour - 18) + (minute / 60)) / 4) * 255)
        # 夜は10時〜朝4時まで最大の濃さ
        if 22 <= hour <= 23 or 0 <= hour <= 4:
            depth_night = 255
        # 夜色を作成&設定
        color_night = list(COLOR_JET_BLACK) + [int(depth_night / 1.25)]
        rect_night.fill(color_night)
        self.screen.blit(rect_night, (0, 0))

        # 時間表記
        string_time = self.font_time.render(self.timer_to_string(), True, COLOR_TIME)
        self.screen.blit(string_time, START_POINT_STRING_TIME)