
class Buildings():

    def __init__(self, costW, bTime, hp, sizeMap):
        self.costW = costW
        self.bTime = bTime
        self.hp = hp
        self.sizeMap = sizeMap

    def __repr__(self):
        return "Buildings(%r, %r, %r, %r)" % (self.costW, self.bTime, self.hp, self.sizeMap)
    
    def print_Buildings(self):
        print("Buildings")
        print("Cost Wood: ", self.costW)
        print("Build Time: ", self.bTime)
        print("Health: ", self.hp)
        print("Size: ", self.sizeMap)
