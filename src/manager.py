import pygame
import string
import random
import os
import pickle
from src.player.player import Player
from src.map.map import Map
from src.nation.nation import Nation
from src.converter import *
from pygame.locals import *


class Manager:
    """ゲーム管理クラス"""

    def __init__(self):
        # 各種オブジェクト初期化
        self._make_data_directory()
        self.screen = pygame.display.set_mode(SCR_RECT.size, DOUBLEBUF | HWSURFACE)
        self.map = self._make_init_map()
        self.nations = self._make_init_nations()
        self.player = self._make_init_player(random.choice(self.nations))

        # マップの初期中心位置設定はプレーヤー位置と同位置
        coordinates = self.player.get_coordinates()
        self.map.set_centers(coordinates[X], coordinates[Y])
        self.map.calc_limits()

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

            # 各種更新更新
            self.map.update(self.screen)
            [nation.update(self.screen, self.player.get_coordinates(), self.map.get_left_top(), self.map.get_right_buttom())
             for nation in self.nations]
            self.player.update(self.screen)

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