from model.Buildings import Buildings

class House(Buildings):

    def __init__(self):
        super().__init__(25, 25, 200, 2, 'H')
        self.population = 5

    def __repr__(self):
        return "House(HP: %r, x: %r, y: %r, Population : %r)" % (self.hp, self.x, self.y, self.population)
    
    def print_House(self):
        print("House")
        print("Cost Wood: ", self.costW)
        print("Build Time: ", self.bTime)
        print("Health: ", self.hp)
        print("Size: ", self.sizeMap)
        print("Population: ", self.population)