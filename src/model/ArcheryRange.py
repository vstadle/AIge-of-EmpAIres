from model.Buildings import Buildings
from model.Archer import Archer

class ArcheryRange(Buildings):

    def __init__(self):
        super().__init__(175, 50, 500, 3, 'A')

    def __repr__(self):
        return "ArcheryRange(HP: %r, x: %r, y: %r)" % (self.hp, self.x, self.y)
    
    def print_ArcheryRange(self):
        print("ArcheryRange")
        print("Cost Wood: ", self.costW)
        print("Build Time: ", self.bTime)
        print("Health: ", self.hp)
        print("Size: ", self.sizeMap)
    
    def spawnArcher(self):
        return Archer()
    
