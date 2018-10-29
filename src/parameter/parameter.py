from random import randint

from src.consts import *


class ParameterBase:
    """パラメータベースクラス"""

    def effect_other(self, base, params):
        """他パラメータへの影響"""

        ret = [0, 0, 0]
        for i in range(len(params)):
            validated = params[i] + (base * CORRECTION_TUPLE[i])
            ret[i] = self.validate_parameter(validated)

        return ret[0], ret[1], ret[2]

    def validate_parameter(self, param, max=MAX_PARAMETER, min=MIN_PARAMETER):
        """パラメータのバリデート"""

        if param < min:
            ret = min
        elif param > max:
            ret = max
        else:
            ret = param

        return ret


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
        validated = self.chemistry + value
        self.chemistry = self.validate_parameter(validated)

        # 材料工学
        self.mat_eng, _, _ = self.effect_other(EFFECT_BASE, [self.mat_eng])

    def update_mat_eng(self, value):
        validated = self.mat_eng + value
        self.mat_eng = self.validate_parameter(validated)

        # 軍事学
        self.mil_sci, _, _ = self.effect_other(EFFECT_BASE, [self.mil_sci])

    def update_physics(self, value):
        validated = self.physics + value
        self.physics = self.validate_parameter(validated)

        # 軍事学、動力学
        self.mil_sci, self.dynamics, _ = self.effect_other(EFFECT_BASE, [self.mil_sci, self.dynamics])

    def update_dynamics(self, value):
        validated = self.dynamics + value
        self.dynamics = self.validate_parameter(validated)

        # なし
        _, _, _ = self.effect_other(EFFECT_BASE, [])

    def update_elc_mag(self, value):
        validated = self.elc_mag + value
        self.elc_mag = self.validate_parameter(validated)

        # 軍事学、農民満足度
        self.mil_sci, self.fmr_sat, _ = self.effect_other(EFFECT_BASE, [self.mil_sci, self.fmr_sat])

    def update_mil_sci(self, value):
        validated = self.mil_sci + value
        self.mil_sci = self.validate_parameter(validated)

        # 軍事力
        self.mil_pwr, _, _ = self.effect_other(EFFECT_BASE, [self.mil_pwr])

    def update_politics(self, value):
        validated = self.politics + value
        self.politics = self.validate_parameter(validated)

        # 政治学
        self.pli_mat, _, _ = self.effect_other(EFFECT_BASE, [self.pli_mat])

    def update_lif_sci(self, value):
        validated = self.lif_sci + value
        self.lif_sci = self.validate_parameter(validated)

        # 農民満足度
        self.fmr_sat, _, _ = self.effect_other(EFFECT_BASE, [self.fmr_sat])

    def update_agriculture(self, value):
        validated = self.agriculture + value
        self.agriculture = self.validate_parameter(validated)

        # 自然、戦闘員満足度
        self.nature, self.cbt_sat, _ = self.effect_other(EFFECT_BASE, [self.nature, self.cbt_sat])

    def update_tec_art(self, value):
        validated = self.tec_art + value
        self.tec_art = self.validate_parameter(validated)

        # 生活科学、材料工学
        self.lif_sci, self.mat_eng, _ = self.effect_other(EFFECT_BASE, [self.lif_sci, self.mat_eng])

    def update_med_sci(self, value):
        validated = self.med_sci + value
        self.med_sci = self.validate_parameter(validated)

        # 医学、戦闘員満足度
        self.pub_hls, self.cbt_sat, _ = self.effect_other(EFFECT_BASE, [self.pub_hls, self.cbt_sat])

    def update_math(self, value):
        validated = self.math + value
        self.math = self.validate_parameter(validated)

        # 物理学
        self.physics, _, _ = self.effect_other(EFFECT_BASE, [self.physics])

    def update_eco_pwr(self, value):
        validated = self.eco_pwr + value
        self.eco_pwr = self.validate_parameter(validated)

        # 軍事力
        self.mil_pwr, _, _ = self.effect_other(EFFECT_BASE, [self.mil_pwr])

    def update_mil_pwr(self, value):
        validated = self.mil_pwr + value
        self.mil_pwr = self.validate_parameter(validated)

        _, _, _ = self.effect_other(EFFECT_BASE, [])

    def update_edu_std(self, value):
        validated = self.edu_std + value
        self.edu_std = self.validate_parameter(validated)

        # 民度、経済力
        self.cul_lev, self.eco_pwr, _ = self.effect_other(EFFECT_BASE, [self.cul_lev, self.eco_pwr])

    def update_pli_mat(self, value):
        validated = self.pli_mat + value
        self.pli_mat = self.validate_parameter(validated)

        # 教育
        self.edu_std, _, _ = self.effect_other(EFFECT_BASE, [self.edu_std])

    def update_taxrate(self, value):
        validated = self.taxrate + value
        self.taxrate = self.validate_parameter(validated)

        # 商人満足度、経済力
        self.mct_sat, self.eco_pwr, _ = self.effect_other(EFFECT_BASE, [self.mct_sat, self.eco_pwr])
        # 農民満足度（マイナス）
        self.fmr_sat, _, _ = self.effect_other(-EFFECT_BASE, [self.fmr_sat])

    def update_cul_lev(self, value):
        validated = self.cul_lev + value
        self.cul_lev = self.validate_parameter(validated)

        # 政治成熟度
        self.pli_mat, _, _ = self.effect_other(EFFECT_BASE, [self.pli_mat])

    def update_fmr_sat(self, value):
        validated = self.fmr_sat + value
        self.fmr_sat = self.validate_parameter(validated)

        # 農林水産業、自然
        self.agriculture, self.nature, _ = self.effect_other(EFFECT_BASE, [self.agriculture, self.nature])

    def update_mct_sat(self, value):
        validated = self.mct_sat + value
        self.mct_sat = self.validate_parameter(validated)

        # 経済力
        self.eco_pwr, _, _ = self.effect_other(EFFECT_BASE, [self.eco_pwr])

    def update_cbt_sat(self, value):
        validated = self.cbt_sat + value
        self.cbt_sat = self.validate_parameter(validated)

        # 軍事力
        self.mil_pwr, _, _ = self.effect_other(EFFECT_BASE, [self.mil_pwr])

    def update_scl_sat(self, value):
        validated = self.scl_sat + value
        self.scl_sat = self.validate_parameter(validated)

        # 化学、数学、電磁気学
        self.chemistry, self.math, self.elc_mag\
            = self.effect_other(EFFECT_BASE, [self.chemistry, self.math, self.elc_mag])

    def update_crf_sat(self, value):
        validated = self.crf_sat + value
        self.crf_sat = self.validate_parameter(validated)

        # 工芸
        self.tec_art, _, _ = self.effect_other(EFFECT_BASE, [self.tec_art])

    def update_dct_sat(self, value):
        validated = self.dct_sat + value
        self.dct_sat = self.validate_parameter(validated)

        # 医学
        self.med_sci, _, _ = self.effect_other(EFFECT_BASE, [self.med_sci])

    def update_nature(self, value):
        validated = self.nature + value
        self.nature = self.validate_parameter(validated)

        # なし
        _, _, _ = self.effect_other(EFFECT_BASE, [])

    def update_pub_hls(self, value):
        validated = self.pub_hls + value
        self.pub_hls = self.validate_parameter(validated)

        # 戦闘員満足度、農民満足度、医者満足度
        self.cbt_sat, self.fmr_sat, self.dct_sat\
            = self.effect_other(EFFECT_BASE, [self.cbt_sat, self.fmr_sat, self.dct_sat])



class HumanParameter(ParameterBase):
    """人（プレーヤー含む）パラメータクラス"""

    def __init__(self):
        self.life = MAX_PARAMETER
        self.energy = MAX_PARAMETER
        self.hunger = MAX_PARAMETER
        self.thirst = MAX_PARAMETER
        self.body_temperture = NORMAL_BODY_TEMPERTURE
        self.mental_power = MAX_PARAMETER
        self.patriotism = 0
        self.craft_skill = randint(1, MAX_INIT_PARAMETER)
        self.merchant_skill = randint(1, MAX_INIT_PARAMETER)
        self.combat_skill = randint(1, MAX_INIT_PARAMETER)
        self.farming_skill = randint(1, MAX_INIT_PARAMETER)
        self.intelligence = randint(1, MAX_INIT_PARAMETER)

    def update_life(self, value):
        validated = self.life + value
        self.life = self.validate_parameter(validated)

    def update_energy(self, value):
        validated = self.energy + value
        self.energy = self.validate_parameter(validated)

    def update_hunger(self, value):
        validated = self.hunger + value
        self.hunger = self.validate_parameter(validated)

    def update_thirst(self, value):
        validated = self.thirst + value
        self.thirst = self.validate_parameter(validated)

    def update_body_temperture(self, value):
        validated = self.body_temperture + value
        self.body_temperture = self.validate_parameter(validated)

    def update_mental_power(self, value):
        validated = self.mental_power + value
        self.mental_power = self.validate_parameter(validated)

    def update_patriotism(self, value):
        validated = self.patriotism + value
        self.patriotism = self.validate_parameter(validated)

    def update_craft_skill(self, value):
        validated = self.craft_skill + value
        self.craft_skill = self.validate_parameter(validated)

    def update_merchant_skill(self, value):
        validated = self.merchant_skill + value
        self.merchant_skill = self.validate_parameter(validated)

    def update_combat_skill(self, value):
        validated = self.combat_skill + value
        self.combat_skill = self.validate_parameter(validated)

    def update_farming_skill(self, value):
        validated = self.farming_skill + value
        self.farming_skill = self.validate_parameter(validated)

    def update_intelligence(self, value):
        validated = self.intelligence + value
        self.intelligence = self.validate_parameter(validated)

        # 冶金技術、商技術、戦闘技術、農業技術（等しく増加）
        self.craft_skill, _, _ = self.effect_other(EFFECT_BASE, [self.craft_skill])
        self.merchant_skill, _, _ = self.effect_other(EFFECT_BASE, [self.merchant_skill])
        self.combat_skill, _, _ = self.effect_other(EFFECT_BASE, [self.combat_skill])
        self.farming_skill, _, _ = self.effect_other(EFFECT_BASE, [self.farming_skill])
