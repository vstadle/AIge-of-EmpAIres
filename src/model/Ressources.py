
class Ressources():

    def __init__(self, capacity, maxCapacity, letter):
        self.capacity = capacity
        self.maxCapacity = maxCapacity
        self.letter = letter
        self.x = None
        self.y = None

    def setX(self, X):
        self.x = X

    def setY(self, Y):
        self.y = Y

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getCapacity(self):
        return self.capacity

    def setCapacity(self, capacity):
        self.capacity = capacity

    def removeCapacity(self):    
        self.capacity -= 1