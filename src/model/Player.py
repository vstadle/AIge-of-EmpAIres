
class Player():

    def __init__(self, name, f, w, g):
        self.name = name
        self.units = []
        self.buildings = []
        self.food = f
        self.wood = w
        self.gold = g

    def addUnit(self, unit):
        self.units.append(unit)

    def addBuilding(self, building):
        self.buildings.append(building)
        
    def addFood(self, Food):
        self.food += Food
    
    def addWood(self, Wood):    
        self.wood += Wood
        
    def addGold(self, Gold):
        self.gold += Gold
        
    def removeFood(self, Food):
        self.food -= Food
    
    def removeWood(self, Wood):    
        self.wood -= Wood
        
    def removeGold(self, Gold):
        self.gold -= Gold
    
    def countUnits(self):
        return len(self.units)
