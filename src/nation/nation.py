

class Nation:
    """国家クラス"""

    def __init__(self, name, coordinates=None, population=0, parameter=None):
        self.name = name
        self.coordinates = coordinates
        self.population = population
        if parameter == None:
            self.parameter = {
            'chemistry': 0,
            'materials_engineering': 0,
            'physics': 0,
            'dynamics': 0,
            'electromagnetism': 0,
            'military_science': 0,
            'politics': 0,
            'life_sciences': 0,
            'agriculture': 0,
            'technical_art': 0,
            'medical_science': 0,
            'mathematics': 0,
            'economic_power': 0,
            'military_power': 0,
            'educational_standard': 0,
            'political_maturation': 0,
            'tax_rate': 0,
            'cultural_level': 0,
            'farmer_satisfaction': 0,
            'merchant_satisfaction': 0,
            'combatant_satisfaction': 0,
            'scholar_satisfaction': 0,
            'craftsman_satisfaction': 0,
            'doctor_satisfaction': 0,
            'nature': 0,
            'public_health': 0
        }
        else:
            self.parameter = parameter
