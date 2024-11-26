from model.Buildings import Buildings
from model.Horseman import Horseman

class Stable(Buildings):
    
    def __init__(self):
        super().__init__(175, 50, 500, 3, 'S')

    def __repr__(self):
        return "Stable(HP: %r, x: %r, y: %r)" % (self.hp, self.x, self.y)
    
    def print_Stable(self):
        print("Stable")
        print("Cost Wood: ", self.costW)
        print("Build Time: ", self.bTime)
        print("Health: ", self.hp)
        print("Size: ", self.sizeMap)

    def spawnHorseman(self):
        return Horseman()