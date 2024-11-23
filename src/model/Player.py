
from model.TownCenter import TownCenter

class Color():
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    PURPLE = (255, 0, 255)
    ORANGE = (255, 165, 0)
    CYAN = (0, 255, 255)
    PINK = (255, 192, 203)
    BROWN = (165, 42, 42)
    GREY = (128, 128, 128)

class Player():

    cptPlayer = 0

    lstColor = [Color.GREEN, Color.BLUE, Color.RED, Color.YELLOW, Color.PURPLE, Color.ORANGE, Color.CYAN, Color.PINK, Color.BROWN, Color.GREY]

    def __init__(self, name, f, w, g):
        self.name = name
        self.units = []
        self.buildings = []
        self.food = f
        self.wood = w
        self.gold = g
        self.training_queue = []
        self.buildings_queue = []
        self.id = Player.cptPlayer
        Player.cptPlayer += 1
        self.color = Player.lstColor[self.id]

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

    def getColor(self):
        return self.color