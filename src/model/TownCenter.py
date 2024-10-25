from model.Buildings import Buildings

class TownCenter(Buildings):

    def __init__(self):
        super().__init__(350, 150, 1000, 4, 'T')
        self.competence1 = "Spawns Villagers"
        self.competence2 = "Drop points of resources"
        self.population = 5

    def __repr__(self):
        return "TownCenter(%r, %r, %r, %r, %r, %r)" % (self.costW, self.bTime, self.hp, self.sizeMap, self.competence1, self.competence2)
    
    def print_TownCenter(self):
        print("TownCenter")
        print("Cost Wood: ", self.costW)
        print("Build Time: ", self.bTime)
        print("Health: ", self.hp)
        print("Size: ", self.sizeMap)
        print("Competence 1: ", self.competence1)
        print("Competence 2: ", self.competence2)
        print("Population: ", self.population)