from model.Units import Units

class Swordsman(Units):

      def __init__(self):
        super().__init__(50, 20, 0,40, 20, 4, 1, 0.9, 1,'s')
      
      def __repr__(self):
        return "Swordsman(%r, %r, %r, %r, %r, %r, %r, %r, %r)" % (self.costF, self.costG, self.costW, self.health, self.trainingTime, self.attack, self.speedAtack, self.speed, self.range)
      
      def print_Swordsman(self):
         print("Swordsman")
         print("Cost Food: ", self.costF)
         print("Cost Gold: ", self.costG)
         print("Cost Wood: ", self.costW)
         print("Health: ", self.health)
         print("Training Time: ", self.trainingTime)
         print("Attack: ", self.attack)
         print("Speed Atack: ", self.speedAtack)
         print("Speed: ", self.speed)
         print("Range: ", self.range)
           