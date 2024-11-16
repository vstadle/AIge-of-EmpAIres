
class Buildings():

    def __init__(self, costW, bTime, hp, sizeMap, letter):
        self.costW = costW
        self.bTime = bTime
        self.hp = hp
        self.sizeMap = sizeMap
        self.letter = letter
        self.x = 0
        self.y = 0

    def __repr__(self):
        return "Buildings(%r, %r, %r, %r, %r, %r)" % (self.costW, self.bTime, self.hp, self.sizeMap, self.x, self.y)
    
    def print_Buildings(self):
        print("Buildings")
        print("Cost Wood: ", self.costW)
        print("Build Time: ", self.bTime)
        print("Health: ", self.hp)
        print("Size: ", self.sizeMap)

    def getHp(self):
        return self.hp

    def setHp(self, hp):
        self.hp = hp

    def setX (self, x):
        self.x = x
    
    def setY (self, y):
        self.y = y

    def getX (self):
        return self.x
    
    def getY (self):
        return self.y
    
    def getSizeMap(self):
        return self.sizeMap
    
    def getBuildingTime(self):
        return self.bTime