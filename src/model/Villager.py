from model.Units import Units

class Villager(Units):

    def __init__(self):
        super().__init__(50, 0, 0, 25, 25, 2, 1, 0.8, 1,"v")
        self.collectRessources = 25 #min
        self.carryingCapacity = 20 #min
    
    def __repr__(self):
        return "Villager :(HP : %r)" % (self.health)
    
    def print_Villager(self):
        print("Collect Ressources: ", self.collectRessources)
        print("Carrying Capacity: ", self.carryingCapacity)