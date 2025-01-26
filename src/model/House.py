from model.Buildings import Buildings
from view.HealthBar import HealthBar

class House(Buildings):

    def __init__(self):
        super().__init__(25, 25, 200, 2, 'H')
        self.population = 5
        self.health_bar = HealthBar(
            max_health=self.max_health, 
            width=40,  # Adjust based on sprite size
            height=5   # Adjust based on preference
        )

    def __repr__(self):
        return "House(HP: %r, x: %r, y: %r, Population : %r)" % (self.health, self.x, self.y, self.population)
    
    def print_House(self):
        print("House")
        print("Cost Wood: ", self.costW)
        print("Build Time: ", self.bTime)
        print("Health: ", self.health)
        print("Size: ", self.sizeMap)
        print("Population: ", self.population)
    