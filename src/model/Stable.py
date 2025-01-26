from model.Buildings import Buildings
from model.Horseman import Horseman
from view.HealthBar import HealthBar

class Stable(Buildings):
    
    def __init__(self):
        super().__init__(175, 50, 500, 3, 'S')
        self.health_bar = HealthBar(
            max_health=self.max_health, 
            width=40,  # Adjust based on sprite size
            height=5   # Adjust based on preference
        )
    def __repr__(self):
        return "Stable(HP: %r, x: %r, y: %r)" % (self.health, self.x, self.y)
    
    def print_Stable(self):
        print("Stable")
        print("Cost Wood: ", self.costW)
        print("Build Time: ", self.bTime)
        print("Health: ", self.health)
        print("Size: ", self.sizeMap)

    def spawnHorseman(self):
        return Horseman()

    