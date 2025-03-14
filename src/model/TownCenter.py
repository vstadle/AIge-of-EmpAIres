from model.Buildings import Buildings
from model.Villager import Villager
from view.HealthBar import HealthBar

class TownCenter(Buildings):

    def __init__(self, color=None):
        super().__init__(350, 150, 1000, 4, 'T')
        self.competence2 = "Drop points of resources"
        self.population = 5
        self.health_bar = HealthBar(
            max_health=self.max_health, 
            width=40,  # Adjust based on sprite size
            height=5 ,  # Adjust based on preference
            player_color=color
        )

    def __repr__(self):
        return "TownCenter(HP: %r, x: %r, y: %r)" % (self.health, self.x, self.y)
    
    def print_TownCenter(self):
        print("TownCenter")
        print("Cost Wood: ", self.costW)
        print("Build Time: ", self.bTime)
        print("Health: ", self.hp)
        print("Size: ", self.sizeMap)
        print("Competence 2: ", self.competence2)
        print("Population: ", self.population)

    def spawnVillager(self):
        return Villager()

    