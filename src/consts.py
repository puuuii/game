from pygame.locals import *


# ゲーム全体系
SCR_RECT = Rect(0, 0, 640, 480)
FPS = 30

# マップ系
LENGTH_OF_ONE_SIDE = 2 ** 6#16
PIXCEL_OF_ONE_SIDE = 16
ROOP_MAP_MAKING = 7
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
N_CELL_RENDER_X = round(SCR_RECT.width / PIXCEL_OF_ONE_SIDE)
N_CELL_RENDER_Y = round(SCR_RECT.height / PIXCEL_OF_ONE_SIDE)
SCROLL_SPEED = 0.5