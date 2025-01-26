from view.HealthBar import HealthBar  # Assurez-vous que le chemin est correct

class Units():
    #Parameters costF: int, costG: int, costW: int, health: int, trainingTime: int, attack: int, speedAtack: int, speed: int, range: int
    def __init__(self, costF, costG, costW, health, trainingTime, attack, speedAtack, speed, range, letter, color = None):
        self.costF = costF
        self.costG = costG
        self.costW = costW
        self.max_health = health  # Define max_health first
        self.health = health      # Current health starts at max
        self.trainingTime = trainingTime
        self.attack = attack
        self.speedAtack = speedAtack
        self.speed = speed
        self.range = range
        self.letter = letter
        self.action = None
        self.x = None
        self.y = None
        self.health_bar = HealthBar(
            max_health=self.max_health, 
            width=40,  # Adjust width as needed
            height=4   # Adjust height as needed
        )
        self.color = color

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
    def attack(self, target):
        target.health -= self.attack

    #Parameters target: Building
    def attackBuildings(self, target):
        target.health -= self.attack
    
    def getLetter(self):
        return self.letter
    
    def getCostF(self):
        return self.costF
    
    def getCostG(self):
        return self.costG
    
    def getCostW(self):
        return self.costW
    
    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def getPosition(self):
        if self.x == None or self.y == None:
            return None
        return self.x, self.y