from random import randint
from src.consts import *


class ParameterBase:
    """パラメータベースクラス"""

    pass


class NationParameter(ParameterBase):
    """国家パラメータクラス"""

    def __init__(self):
        self.chemistry = randint(1, MAX_INIT_PARAMETER)
        self.mat_eng = randint(1, MAX_INIT_PARAMETER)
        self.physics = randint(1, MAX_INIT_PARAMETER)
        self.dynamics = randint(1, MAX_INIT_PARAMETER)
        self.elc_mag = randint(1, MAX_INIT_PARAMETER)
        self.mil_sci = randint(1, MAX_INIT_PARAMETER)
        self.politics = randint(1, MAX_INIT_PARAMETER)
        self.lif_sci = randint(1, MAX_INIT_PARAMETER)
        self.agriculture = randint(1, MAX_INIT_PARAMETER)
        self.tec_art = randint(1, MAX_INIT_PARAMETER)
        self.med_sci = randint(1, MAX_INIT_PARAMETER)
        self.math = randint(1, MAX_INIT_PARAMETER)
        self.eco_pwr = randint(1, MAX_INIT_PARAMETER)
        self.mil_pwr = randint(1, MAX_INIT_PARAMETER)
        self.edu_std = randint(1, MAX_INIT_PARAMETER)
        self.pli_mat = randint(1, MAX_INIT_PARAMETER)
        self.taxrate = randint(1, MAX_INIT_PARAMETER)
        self.cul_lev = randint(1, MAX_INIT_PARAMETER)
        self.fmr_sat = randint(1, MAX_INIT_PARAMETER)
        self.mct_sat = randint(1, MAX_INIT_PARAMETER)
        self.cbt_sat = randint(1, MAX_INIT_PARAMETER)
        self.scl_sat = randint(1, MAX_INIT_PARAMETER)
        self.crf_sat = randint(1, MAX_INIT_PARAMETER)
        self.dct_sat = randint(1, MAX_INIT_PARAMETER)
        self.nature = randint(1, MAX_INIT_PARAMETER)
        self.pub_hls = randint(1, MAX_INIT_PARAMETER)


class HumanParameter(ParameterBase):
    """人（プレーヤー含む）パラメータクラス"""

    def __init__(self):
        self.life = MAX_PARAMETER
        self.hunger = MAX_PARAMETER
        self.thirst = MAX_PARAMETER
        self.body_temperture = NORMAL_BODY_TEMPERTURE
        self.tiredness = MAX_PARAMETER
        self.mental_fatigue = MAX_PARAMETER
        self.patriotism = 0
        self.craft_skill = randint(1, MAX_INIT_PARAMETER)
        self.merchant_skill = randint(1, MAX_INIT_PARAMETER)
        self.combat_skill = randint(1, MAX_INIT_PARAMETER)
        self.farming_skill = randint(1, MAX_INIT_PARAMETER)
        self.intelligence = randint(1, MAX_INIT_PARAMETER)