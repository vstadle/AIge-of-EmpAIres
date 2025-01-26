from model.Units import Units
from view.HealthBar import HealthBar

class Archer(Units):

    def __init__(self):
        super().__init__(0, 45, 25, 30, 35, 4, 1, 1, 4, 'a')
        self.health_bar = HealthBar(
            max_health=self.max_health, 
            width=40,  # Adjust based on sprite size
            height=5   # Adjust based on preference
        )

    def __repr__(self):
        return "Archer :(HP : %r)" % (self.health)
    
    def print_Archer(self):
        print("Archer")
        print("Cost Food: ", self.costF)
        print("Cost Gold: ", self.costG)
        print("Cost Wood: ", self.costW)
        print("Health: ", self.health)
        print("Training Time: ", self.trainingTime)
        print("Attack: ", self.attack)
        print("Speed Atack: ", self.speedAtack)
        print("Speed: ", self.speed)
        print("Range: ", self.range)

    

