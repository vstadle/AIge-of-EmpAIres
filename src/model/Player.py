
class Player():

    def __init__(self, name):
        self.name = name
        self.units = []
        self.buildings = []

    def addUnit(self, unit):
        self.units.append(unit)

    def addBuilding(self, building):
        self.buildings.append(building)