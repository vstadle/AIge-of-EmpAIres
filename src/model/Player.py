import curses



class Player():

    cptPlayer = 0
    lstColor = [curses.COLOR_RED, curses.COLOR_GREEN, curses.COLOR_BLUE, curses.COLOR_YELLOW, curses.COLOR_MAGENTA, curses.COLOR_CYAN]

    def __init__(self, name, f, w, g):
        self.name = name
        self.mode_ia = None
        self.units = []
        self.buildings = []
        self.food = f
        self.wood = w
        self.gold = g
        self.population = 0
        self.training_queue = []
        self.buildings_queue = []
        self.id = Player.cptPlayer
        Player.cptPlayer += 1
        self.color = None
        try:
            self.color = Player.lstColor[self.id]
        except IndexError:
            self.color = Player.lstColor[0]

    def setModeIA(self, mode_ia):
        self.mode_ia = mode_ia
    def __repr__(self):
        return "Player: %r, Gold: %r, Wood: %r, Food: %r Population: %r" % (self.name, self.gold, self.wood, self.food, self.population)

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

    def canAffordBuilding(self, building):
        return (self.wood >= building.costW)

    def canAffordUnit(self, unit):
        temp = len(self.units) + len(self.training_queue)
        return (self.food >= unit.costF and self.wood >= unit.costW and self.gold >= unit.costG and temp <= self.population)

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
    
    def removeUnit(self, unit):
        if unit.health <= 0:
            self.units.remove(unit)
        
    