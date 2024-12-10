import asyncio

from model.Units import Units
from model.Ressources import Ressources

class Villager(Units):

    def __init__(self):
        super().__init__(50, 0, 0, 25, 25, 2, 1, 0.8, 1,"v")
        self.collectPerMin = 25 #par min
        self.carryingCapacity = 20 
        self.carrying = 0
        self.carryingType = None
    
    def __repr__(self):
        return "Villager :(HP : %r)" % (self.health)
    
    def print_Villager(self):
        print("Collect Ressources per min: ", self.collectPerMin)
        print("Carrying Capacity: ", self.carryingCapacity)

    def canCollectRessources(self):
        return self.carrying < self.carryingCapacity
        
    def addRessource(self):
        self.carrying += 1

    def depot(self):
        self.carrying = 0
        self.carryingType = None

    async def collect(self, Ressource):
        while(self.canCollectRessources() and Ressource.getCapacity() > 0):
            self.addRessource()
            Ressource.removeCapacity()
            await asyncio.sleep(60/self.collectPerMin)
