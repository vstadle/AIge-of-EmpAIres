
class Units():

    def __init__(self, costF, costG, costW, health, trainingTime, attack, speedAtack, speed, range):
        self.costF = costF
        self.costG = costG
        self.costW = costW
        self.health = health
        self.trainingTime = trainingTime
        self.attack = attack
        self.speedAtack = speedAtack
        self.speed = speed
        self.range = range

    def __repr__(self):
        return "Units(%r, %r, %r, %r, %r, %r, %r, %r, %r)" % (self.costF, self.costG, self.costW, self.health, self.trainingTime, self.attack, self.speedAtack, self.speed, self.range)

    def print_Units(self):
        print("Cost Food: ", self.costF)
        print("Cost Gold: ", self.costG)
        print("Cost Wood: ", self.costW)
        print("Health: ", self.health)
        print("Training Time: ", self.trainingTime)
        print("Attack: ", self.attack)
        print("Speed Atack: ", self.speedAtack)
        print("Speed: ", self.speed)


def test_Units():
    uTest = Units(100, 100, 100, 100, 100, 100, 100, 100, 100)
    print(uTest)
    uTest.print_Units()

test_Units()