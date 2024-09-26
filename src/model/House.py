from Buildings import Buildings

class House(Buildings):

    def __init__(self):
        super().__init__(25, 25, 200, 2)
        self.population = 5

    def __repr__(self):
        return "House(%r, %r, %r, %r, %r)" % (self.costW, self.bTime, self.hp, self.sizeMap, self.population)
    
    def print_House(self):
        print("House")
        print("Cost Wood: ", self.costW)
        print("Build Time: ", self.bTime)
        print("Health: ", self.hp)
        print("Size: ", self.sizeMap)
        print("Population: ", self.population)