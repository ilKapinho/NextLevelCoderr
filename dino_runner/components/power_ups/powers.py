from dino_runner.utils.constants import HAMMER, HAMMER_TYPE, SHIELD, SHIELD_TYPE
from dino_runner.components.power_ups.power_up import PowerUp

class Shield(PowerUp):
    def __init__(self):
        self.image = SHIELD
        self.type = SHIELD_TYPE
        super().__init__(self.image,self.type)

class Hammer(PowerUp):
    def __init__(self):
        self.image = HAMMER
        self.type = HAMMER_TYPE
        super().__init__(self.image,self.type)



