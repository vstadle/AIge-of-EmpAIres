from model.Buildings import Buildings

class ArcheryRange(Buildings):

    def __init__(self):
        super().__init__(175, 50, 500, 3)
        self.competence1 = "Spawns Archers"

    def __repr__(self):
        return "ArcheryRange(%r, %r, %r, %r, %r)" % (self.costW, self.bTime, self.hp, self.sizeMap, self.competence1)
    
    def print_ArcheryRange(self):
        print("ArcheryRange")
        print("Cost Wood: ", self.costW)
        print("Build Time: ", self.bTime)
        print("Health: ", self.hp)
        print("Size: ", self.sizeMap)
        print("Competence 1: ", self.competence1)
    
