from model.Buildings import Buildings

class Farm(Buildings):

    def __init__(self):
        super().__init__(60, 10, 100, 2, 'F')
        self.food = 300

    def __repr__(self):
        return "Farm(HP: %r, x:%r, y: %r)" % (self.hp, self.x, self.y)
    
    def print_Farm(self):
        print("Farm")
        print("Cost Wood: ", self.costW)
        print("Build Time: ", self.bTime)
        print("Health: ", self.hp)
        print("Size: ", self.sizeMap)
        print("Food: ", self.food)