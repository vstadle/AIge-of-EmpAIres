
class Ressources():

    def __init__(self, capacity, maxCapacity, letter):
        self.capacity = capacity
        self.maxCapacity = maxCapacity
        self.letter = letter
        self.x = 0
        self.y = 0

    def getCapacity(self):
        return self.capacity

    def setCapacity(self, capacity):
        self.capacity = capacity

    def setXY(self, x, y):
        self.x = x
        self.y = y
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y