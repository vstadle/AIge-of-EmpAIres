from Buildings import Buildings

class Keep(Buildings):

    def __init__(self):
        super().__init__(35, 80, 80, 1)
        self.costG = 125
        self.attack = 5
        self.range = 8
        
    