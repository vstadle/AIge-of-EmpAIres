from model.Buildings import Buildings
from model.Archer import Archer
from view.HealthBar import HealthBar

class ArcheryRange(Buildings):

    def __init__(self, color=None):
        super().__init__(175, 50, 500, 3, 'A')
        self.health_bar = HealthBar(
            max_health=self.max_health, 
            width=40,  # Adjust based on sprite size
            height=5   # Adjust based on preference
        )

    def __repr__(self):
        return "ArcheryRange(HP: %r, x: %r, y: %r)" % (self.health, self.x, self.y)
    
    def print_ArcheryRange(self):
        print("ArcheryRange")
        print("Cost Wood: ", self.costW)
        print("Build Time: ", self.bTime)
        print("Health: ", self.health)
        print("Size: ", self.sizeMap)
    
    def spawnArcher(self):
        return Archer()
    
    