from pygame.locals import *


# ゲーム全体系
SCR_RECT = Rect(0, 0, 640, 480)
FPS = 30

# マップ系
STAGE_LENGTH = 2 ** 6#16
PIXCEL_OF_ONE_SIDE = 16
ROOP_SAND_MAKING = 7
ROOP_GLASS_MAKING = 3
BEACH_AREA = 10
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
SCROLL_SPEED = 1.0
LIMIT_RIGHT_IN_PIXEL = (STAGE_LENGTH * PIXCEL_OF_ONE_SIDE) - (SCR_RECT.width / 2)
LIMIT_LEFT_IN_CELL = SCR_RECT.width / 2 / PIXCEL_OF_ONE_SIDE
LIMIT_TOP_IN_CELL = SCR_RECT.height / 2 / PIXCEL_OF_ONE_SIDE
LIMIT_RIGHT_IN_CELLS = STAGE_LENGTH - ((SCR_RECT.width / 2) / PIXCEL_OF_ONE_SIDE)
LIMIT_BOTTOM_IN_CELLS = STAGE_LENGTH - ((SCR_RECT.height / 2) / PIXCEL_OF_ONE_SIDE)

# プレーヤー系
PATH_IMAGE_PLAYER_UP = '../img/player_up.png'
PATH_IMAGE_PLAYER_RIGHT = '../img/player_right.png'
PATH_IMAGE_PLAYER_DOWN = '../img/player_down.png'
PATH_IMAGE_PLAYER_LEFT = '../img/player_left.png'
X_PLAYER = SCR_RECT.width / 2
Y_PLAYER = SCR_RECT.height / 2
DIRECTION_UP = 0
DIRECTION_RIGHT = 1
DIRECTION_DOWN = 2
DIRECTION_LEFT   = 3
