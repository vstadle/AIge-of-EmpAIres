from units import Units

class Villager(Units):

    def __init__(self):
        super().__init__(50, 25, 25, 2, 1, 0.8, 1)
        self.collectRessources = 25 #min
        self.carryingCapacity = 20 #min