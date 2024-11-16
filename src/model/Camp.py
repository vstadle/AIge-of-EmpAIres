from model.Buildings import Buildings

class Camp(Buildings):

    def __init__(self):
        super().__init__(100, 25, 200, 2, 'C')
        self.competence1 = "Drop points of resources"

    def __repr__(self):
        return "Camp(%r, %r, %r, %r, %r)" % (self.costW, self.bTime, self.hp, self.sizeMap, self.competence1)
    
    def print_Camp(self):
        print("Camp")
        print("Cost Wood: ", self.costW)
        print("Build Time: ", self.bTime)
        print("Health: ", self.hp)
        print("Size: ", self.sizeMap)
        print("Competence 1: ", self.competence1)