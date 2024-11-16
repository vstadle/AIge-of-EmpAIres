
from model.TownCenter import TownCenter

class Player():

    def __init__(self, name, f, w, g):
        self.name = name
        self.units = []
        self.buildings = []
        self.food = f
        self.wood = w
        self.gold = g
        self.training_queue = []
        self.buildings_queue = []

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
        return (self.wood >= building.costW)

    def canAffordUnit(self, unit):
        return (self.food >= unit.costF and self.wood >= unit.costW and self.gold >= unit.costG)

    def removeResourcesForBuilding(self, building):
        self.wood -= building.costW

    def removeResourcesForUnit(self, unit_type):
        self.food -= unit_type.costF
        self.wood -= unit_type.costW
        self.gold -= unit_type.costG

    def getTrainingQueue(self):
        return self.training_queue
    
    def getBuildingQueue(self):
        return self.buildings_queue