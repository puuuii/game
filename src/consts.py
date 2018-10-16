from pygame.locals import *


# ゲーム全体系
SCR_RECT = Rect(0, 0, 1024,768)
FPS = 30

# マップ系
LENGTH_OF_ONE_SIDE = 2 ** 6#16
PIXCEL_OF_ONE_SIDE = 16
ROOP_MAP_MAKING = 10
SEA = 0
SAND = 1
GLASS = 2
FOREST = 3
MOUNTAIN = 4
RIVER = 5
PATH_STAGE = '../data/stage.pkl'
PATH_SEA = '../img/sea1.png'
PATH_SAND = '../img/sand1.png'
PATH_GLASS = '../img/glass1.png'
PATH_FOREST = '../img/forest1.png'
PATH_MOUNTAIN = '../img/mountain1.png'
PATH_RIVER = '../img/river1.png'