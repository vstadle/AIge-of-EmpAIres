
from model.TownCenter import TownCenter

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
    
    def getBuildings(self):
        return self.buildings
    
    def getTownCenter(self):
        for building in self.buildings:
            if isinstance(building, TownCenter):
                return building
        return None    

    def canAffordBuilding(self, building):
        return (self.food >= building.costFood and self.wood >= building.costWood and self.gold >= building.costGold)

    def canAffordUnit(self, unit_type):
        return (self.food >= unit_type.costFood and self.wood >= unit_type.costWood and self.gold >= unit_type.costGold)

    def removeResourcesForBuilding(self, building):
        self.wood -= building.costWood

    def removeResourcesForUnit(self, unit_type):
        self.food -= unit_type.costFood
        self.wood -= unit_type.costWood
        self.gold -= unit_type.costGold
