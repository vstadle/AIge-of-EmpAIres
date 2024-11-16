from model.Buildings import Buildings

class Farm(Buildings):

    def __init__(self):
        super().__init__(60, 10, 100, 2, 'F')
        self.food = 300

    def __repr__(self):
        return "Farm(%r, %r, %r, %r, %r)" % (self.costW, self.bTime, self.hp, self.sizeMap, self.food)
    
    def print_Farm(self):
        print("Farm")
        print("Cost Wood: ", self.costW)
        print("Build Time: ", self.bTime)
        print("Health: ", self.hp)
        print("Size: ", self.sizeMap)
        print("Food: ", self.food)