from model.Units import Units
from view.HealthBar import HealthBar

class Horseman(Units):

    def __init__(self, color=None):
        super().__init__(80, 20, 0, 40, 20, 4, 1, 1.2, 1, 'h')
        self.health_bar = HealthBar(
            max_health=self.max_health, 
            width=40,  # Adjust based on sprite size
            height=5 ,  # Adjust based on preference
            player_color=color
        )
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
    