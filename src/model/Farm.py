from model.Buildings import Buildings
from view.HealthBar import HealthBar

class Farm(Buildings):

    def __init__(self):
        super().__init__(60, 10, 100, 2, 'F')
        self.food = 300
        self.health_bar = HealthBar(
            max_health=self.max_health, 
            width=40,  # Adjust based on sprite size
            height=5   # Adjust based on preference
        )
    def __repr__(self):
        return "Farm(HP: %r, x:%r, y: %r)" % (self.health, self.x, self.y)
    
    def print_Farm(self):
        print("Farm")
        print("Cost Wood: ", self.costW)
        print("Build Time: ", self.bTime)
        print("Health: ", self.health)
        print("Size: ", self.sizeMap)
        print("Food: ", self.food)
