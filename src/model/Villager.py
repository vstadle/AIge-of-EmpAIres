from model.Units import Units
from view.HealthBar import HealthBar

class Villager(Units):

    def __init__(self):
        super().__init__(50, 0, 0, 25, 25, 1, 1, 0.8, 1,"v")
        self.collectPerSecond = 2.4 #sec
        self.carryingCapacity = 20 #min
        self.carrying = 0
        self.carryingType = None
        self.attackNotUnit = 2
        self.health_bar = HealthBar(
            max_health=self.max_health, 
            width=40,  # Adjust based on sprite size
            height=5   # Adjust based on preference
        )
    
    def __repr__(self):
        return "Villager :(HP : %r)" % (self.health)
    
    def print_Villager(self):
        print("Collect Ressources: ", self.collectPerSecond)
        print("Carrying Capacity: ", self.carryingCapacity)

    def collect(self, ressource):
        self.carrying += 1
        ressource.capacity -= 1

    def canCollectRessources(self):
        return self.carrying < self.carryingCapacity
    