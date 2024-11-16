
class Ressources():

    def __init__(self, capacity, maxCapacity, letter):
        self.capacity = capacity
        self.maxCapacity = maxCapacity
        self.letter = letter

    def getCapacity(self):
        return self.capacity

    def setCapacity(self, capacity):
        self.capacity = capacity