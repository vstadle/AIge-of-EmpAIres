from model.Buildings import Buildings

class Keep(Buildings):

    def __init__(self):
        super().__init__(35, 80, 80, 1, 'K')
        self.costG = 125
        self.attack = 5
        self.range = 8

    def __repr__(self):
        return "Keep(HP: %r, Damage : %r, Range: %r, x: %r, y: %r)" % (self.hp, self.attack, self.range, self.x, self.y)
    
    def print_Keep(self):
        print("Keep")
        print("Cost Wood: ", self.costW)
        print("Build Time: ", self.bTime)
        print("Health: ", self.hp)
        print("Size: ", self.sizeMap)
        print("Cost Gold: ", self.costG)
        print("Attack: ", self.attack)
        print("Range: ", self.range)

        
    