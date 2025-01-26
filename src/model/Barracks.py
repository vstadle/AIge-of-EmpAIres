from model.Buildings import Buildings
from model.Swordsman import Swordsman
from view.HealthBar import HealthBar

class Barracks(Buildings):

    def __init__(self, color=None):
        super().__init__(175, 50, 500, 3, 'B')
        self.health_bar = HealthBar(
            max_health=self.max_health, 
            width=40,  # Adjust based on sprite size
            height=5   # Adjust based on preference
        )

    def __repr__(self):
        return "Barracks(HP: %r, x: %r, y: %r)" % (self.health, self.x, self.y)
    
    def print_Barracks(self):
        print("Barracks")
        print("Cost Wood: ", self.costW)
        print("Build Time: ", self.bTime)
        print("Health: ", self.health)
        print("Size: ", self.sizeMap)
        print("Competence 1: ", self.competence1)

    def spawnSwordsman(self):
        return Swordsman()

    