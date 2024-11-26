from model.Units import Units

class Horseman(Units):

    def __init__(self):
        super().__init__(80, 20, 0, 40, 20, 4, 1, 1.2, 1, 'h')

    def __repr__(self):
        return "Horseman :(HP : %r)" % (self.health)
    
    def print_Horseman(self):
        print("Horseman")
        print("Cost Food: ", self.costF)
        print("Cost Gold: ", self.costG)
        print("Cost Wood: ", self.costW)
        print("Health: ", self.health)
        print("Training Time: ", self.trainingTime)
        print("Attack: ", self.attack)
        print("Speed Atack: ", self.speedAtack)
        print("Speed: ", self.speed)
        print("Range: ", self.range)