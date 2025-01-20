
class Units():


    #Parameters costF: int, costG: int, costW: int, health: int, trainingTime: int, attack: int, speedAtack: int, speed: int, range: int
    def __init__(self, costF, costG, costW, health, trainingTime, attack, speedAtack, speed, range, letter):
        self.costF = costF
        self.costG = costG
        self.costW = costW
        self.health = health
        self.trainingTime = trainingTime
        self.attack = attack
        self.speedAtack = speedAtack
        self.speed = speed
        self.range = range
        self.letter = letter
        self.action = None
        self.x = None
        self.y = None
        self.player = None

    def __repr__(self):
        return "Units(%r, %r, %r, %r, %r)" % (self.health, self.attack, self.speedAtack, self.speed, self.range)

    def print_Units(self):
        print("Cost Food: ", self.costF)
        print("Cost Gold: ", self.costG)
        print("Cost Wood: ", self.costW)
        print("Health: ", self.health)
        print("Training Time: ", self.trainingTime)
        print("Attack: ", self.attack)
        print("Speed Atack: ", self.speedAtack)
        print("Speed: ", self.speed)


    #Parameters target: Units
    def Attack(self, target):
        target.health -= self.attack

    #Parameters target: Building
    def attackBuildings(self, target):
        target.hp -= self.attack

    def getHp(self):
        return self.health
    
    def getLetter(self):
        return self.letter
    
    def getCostF(self):
        return self.costF
    
    def getCostG(self):
        return self.costG
    
    def getCostW(self):
        return self.costW
    
    def getRange(self):
        return self.range
    
    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def getPosition(self):
        if self.x == None or self.y == None:
            return None
        return self.x, self.y
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y