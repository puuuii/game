import sys
from pygame.locals import *


# ゲーム全体系
SCR_RECT = Rect(0, 0, 640, 480)
FPS = 30
X = 0
Y = 1

# マップ系
STAGE_LENGTH = 2 ** 9
PIXCEL_OF_ONE_SIDE = 16
ROOP_SAND_MAKING = 5
ROOP_GLASS_MAKING = 3
ROOP_FOREST_MAKING = 3
ROOP_MOUNTAIN_MAKING = 5
WIDTH_SURROUND_GLASS = 10
WIDTH_SURROUND_FOREST = 50
WIDTH_SURROUND_MOUNTAIN = 100
N_RIVER = 12
SEA = 0
SAND = 1
GLASS = 2
FOREST = 3
MOUNTAIN = 4
RIVER = 5
PATH_DATA_DIR = '../data'
PATH_STAGE = '../data/map.pkl'
PATH_NATIONS = '../data/nations.pkl'
PATH_PLAYER = '../data/player.pkl'
PATH_SEA = '../img/sea1.png'
PATH_SAND = '../img/sand1.png'
PATH_GLASS = '../img/glass1.png'
PATH_FOREST = '../img/forest1.png'
PATH_MOUNTAIN = '../img/mountain1.png'
PATH_RIVER = '../img/river1.png'
PATH_VILLAGE = '../img/village.png'
PATH_TOWN = '../img/town.png'
PATH_CASTLE_TOWN = '../img/castle_town.png'
PATH_CASTLE = '../img/castle.png'
N_CELL_RENDER_X = round(SCR_RECT.width / PIXCEL_OF_ONE_SIDE)
N_CELL_RENDER_Y = round(SCR_RECT.height / PIXCEL_OF_ONE_SIDE)
SCROLL_SPEED = 1
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

# 国家系
N_NATION = 10
N_NATION_NAME = 5
MAX_INIT_POPULATION = 10
MAX_POPULATION = 65535
MAX_INIT_PARAMETER = 5
MAX_PARAMETER = 65535
CHEMISTRY = 'chemistry'
MAT_ENG = 'materials_engineering'
PHYSICS = 'physics'
DYNAMICS = 'dynamics'
ELC_MAG = 'electromagnetism'
MIL_SCI = 'military_science'
POLITUCS = 'politics'
LIF_SCI = 'life_sciences'
AGRICULTURE = 'agriculture'
TEC_ART = 'technical_art'
MED_SCI = 'medical_science'
MATH = 'mathematics'
ECO_POW = 'economic_power'
MIL_POW = 'military_power'
EDU_STD = 'educational_standard'
POL_MAT = 'political_maturation'
TAXRATE = 'tax_rate'
CUL_LEV = 'cultural_level'
FAR_SAT = 'farmer_satisfaction'
MER_SAT = 'merchant_satisfaction'
COM_SAT = 'combatant_satisfaction'
SCH_SAT = 'scholar_satisfaction'
CRA_SAT = 'craftsman_satisfaction'
DOC_SAT = 'doctor_satisfaction'
NATURE = 'nature'
PUB_HLS = 'public_health'
PARAMS = [CHEMISTRY, MAT_ENG, PHYSICS, DYNAMICS, ELC_MAG, MIL_SCI, POLITUCS, LIF_SCI,
          AGRICULTURE, TEC_ART, MED_SCI, MATH,ECO_POW, MIL_POW, EDU_STD, POL_MAT, TAXRATE,
          CUL_LEV, FAR_SAT, MER_SAT, COM_SAT, SCH_SAT, CRA_SAT, DOC_SAT, NATURE, PUB_HLS]