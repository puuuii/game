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

    def update_chemistry(self, value):
        self.chemistry = value

        # 材料工学
        self.mat_eng, _, _ = self.effect_other(EFFECT_BASE, [self.mat_eng])

    def update_mat_eng(self, value):
        self.mat_eng = value

        # 軍事学
        self.mil_sci, _, _ = self.effect_other(EFFECT_BASE, [self.mil_sci])

    def update_physics(self, value):
        self.physics = value

        # 軍事学、動力学
        self.mil_sci, self.dynamics, _ = self.effect_other(EFFECT_BASE, [self.mil_sci, self.dynamics])

    def update_dynamics(self, value):
        self.dynamics = value

        # なし
        _, _, _ = self.effect_other(EFFECT_BASE, [])

    def update_elc_mag(self, value):
        self.elc_mag = value

        # 軍事学、農民満足度
        self.mil_sci, self.fmr_sat, _ = self.effect_other(EFFECT_BASE, [self.mil_sci, self.fmr_sat])

    def update_mil_sci(self, value):
        self.mil_sci = value

        # 軍事力
        self.mil_pwr, _, _ = self.effect_other(EFFECT_BASE, [self.mil_pwr])

    def update_politics(self, value):
        self.politics = value

        # 政治学
        self.pli_mat, _, _ = self.effect_other(EFFECT_BASE, [self.pli_mat])

    def update_lif_sci(self, value):
        self.lif_sci = value

        # 農民満足度
        self.fmr_sat, _, _ = self.effect_other(EFFECT_BASE, [self.fmr_sat])

    def update_agriculture(self, value):
        self.agriculture = value

        # 自然、戦闘員満足度
        self.nature, self.cbt_sat, _ = self.effect_other(EFFECT_BASE, [self.nature, self.cbt_sat])

    def update_tec_art(self, value):
        self.tec_art = value

        # 生活科学、材料工学
        self.lif_sci, self.mat_eng, _ = self.effect_other(EFFECT_BASE, [self.lif_sci, self.mat_eng])

    def update_med_sci(self, value):
        self.med_sci = value

        # 医学、戦闘員満足度
        self.pub_hls, self.cbt_sat, _ = self.effect_other(EFFECT_BASE, [self.pub_hls, self.cbt_sat])

    def update_math(self, value):
        self.math = value

        # 物理学
        self.physics, _, _ = self.effect_other(EFFECT_BASE, [self.physics])

    def update_eco_pwr(self, value):
        self.eco_pwr = value

        # 軍事力
        self.mil_pwr, _, _ = self.effect_other(EFFECT_BASE, [self.mil_pwr])

    def update_mil_pwr(self, value):
        self.mil_pwr = value

        _, _, _ = self.effect_other(EFFECT_BASE, [])

    def update_edu_std(self, value):
        self.edu_std = value

        # 民度、経済力
        self.cul_lev, self.eco_pwr, _ = self.effect_other(EFFECT_BASE, [self.cul_lev, self.eco_pwr])

    def update_pli_mat(self, value):
        self.pli_mat = value

        # 教育
        self.edu_std, _, _ = self.effect_other(EFFECT_BASE, [self.edu_std])

    def update_taxrate(self, value):
        self.taxrate = value

        # 商人満足度、経済力
        self.mct_sat, self.eco_pwr, _ = self.effect_other(EFFECT_BASE, [self.mct_sat, self.eco_pwr])
        # 農民満足度（マイナス）
        self.fmr_sat, _, _ = self.effect_other(-EFFECT_BASE, [self.fmr_sat])

    def update_cul_lev(self, value):
        self.cul_lev = value

        # 政治成熟度
        self.pli_mat, _, _ = self.effect_other(EFFECT_BASE, [self.pli_mat])

    def update_fmr_sat(self, value):
        self.fmr_sat = value

        # 農林水産業、自然
        self.agriculture, self.nature, _ = self.effect_other(EFFECT_BASE, [self.agriculture, self.nature])

    def update_mct_sat(self, value):
        self.mct_sat = value

        # 経済力
        self.eco_pwr, _, _ = self.effect_other(EFFECT_BASE, [self.eco_pwr])

    def update_cbt_sat(self, value):
        self.cbt_sat = value

        # 軍事力
        self.mil_pwr, _, _ = self.effect_other(EFFECT_BASE, [self.mil_pwr])

    def update_scl_sat(self, value):
        self.scl_sat = value

        # 化学、数学、電磁気学
        self.chemistry, self.math, self.elc_mag\
            = self.effect_other(EFFECT_BASE, [self.chemistry, self.math, self.elc_mag])

    def update_crf_sat(self, value):
        self.crf_sat = value

        # 工芸
        self.tec_art, _, _ = self.effect_other(EFFECT_BASE, [self.tec_art])

    def update_dct_sat(self, value):
        self.dct_sat = value

        # 医学
        self.med_sci, _, _ = self.effect_other(EFFECT_BASE, [self.med_sci])

    def update_nature(self, value):
        self.nature = value

        # なし
        _, _, _ = self.effect_other(EFFECT_BASE, [])

    def update_pub_hls(self, value):
        self.pub_hls = value

        # 戦闘員満足度、農民満足度、医者満足度
        self.cbt_sat, self.fmr_sat, self.dct_sat\
            = self.effect_other(EFFECT_BASE, [self.cbt_sat, self.fmr_sat, self.dct_sat])

    def effect_other(self, base, params):
        """他パラメータへの影響"""

        ret = [0, 0, 0]
        for i in range(len(params)):
            validated = params[i] + (base * CORRECTION_TUPLE[i])
            ret[i] = self.validate_parameter(validated)

        return ret[0], ret[1], ret[2]

    def validate_parameter(self, param):
        """パラメータのバリデート"""

        if param < MIN_PARAMETER:
            ret = MIN_PARAMETER
        elif param > MAX_PARAMETER:
            ret = MAX_PARAMETER
        else:
            ret = param

        return ret



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