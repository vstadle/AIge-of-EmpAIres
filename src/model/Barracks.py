from model.Buildings import Buildings
from model.Swordsman import Swordsman

class Barracks(Buildings):

    def __init__(self):
        super().__init__(175, 50, 500, 3, 'B')
        self.competence1 = "Spawns Swordsmen"

    def __repr__(self):
        return "Barracks(%r, %r, %r, %r, %r)" % (self.costW, self.bTime, self.hp, self.sizeMap, self.competence1)
    
    def print_Barracks(self):
        print("Barracks")
        print("Cost Wood: ", self.costW)
        print("Build Time: ", self.bTime)
        print("Health: ", self.hp)
        print("Size: ", self.sizeMap)
        print("Competence 1: ", self.competence1)

    def spawnSwordsman(self):
        return Swordsman()