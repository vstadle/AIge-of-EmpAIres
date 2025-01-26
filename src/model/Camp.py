from model.Buildings import Buildings
from view.HealthBar import HealthBar

class Camp(Buildings):

    def __init__(self):
        super().__init__(100, 25, 200, 2, 'C')
        self.competence1 = "Drop points of resources"
        self.health_bar = HealthBar(
            max_health=self.max_health, 
            width=40,  # Adjust based on sprite size
            height=5   # Adjust based on preference
        )
    def __repr__(self):
        return "Camp(HP: %r, x: %r, y: %r)" % (self.health, self.x, self.y)
    
    def print_Camp(self):
        print("Camp")
        print("Cost Wood: ", self.costW)
        print("Build Time: ", self.bTime)
        print("Health: ", self.health)
        print("Size: ", self.sizeMap)
        print("Competence 1: ", self.competence1)
    