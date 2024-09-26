from Units import Units

class Villager(Units):

    def __init__(self):
        super().__init__(50, 0, 0, 25, 25, 2, 1, 0.8, 1)
        self.collectRessources = 25 #min
        self.carryingCapacity = 20 #min
    
    def __repr__(self):
        return "Villager(%r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r)" % (self.costF, self.costG, self.costW, self.health, self.trainingTime, self.attack, self.speedAtack, self.speed, self.range, self.collectRessources, self.carryingCapacity)
    
    def print_Villager(self):
        print("Collect Ressources: ", self.collectRessources)
        print("Carrying Capacity: ", self.carryingCapacity)