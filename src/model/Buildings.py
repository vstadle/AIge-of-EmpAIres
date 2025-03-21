from view.HealthBar import HealthBar

class Buildings:
    def __init__(self, costW, bTime, hp, sizeMap, letter,color= None):
        self.costW = costW
        self.bTime = bTime
        self.max_health = hp
        self.health = hp
        self.sizeMap = sizeMap
        self.letter = letter
        self.x = 0
        self.y = 0
        self.color = color
        self.is_constructing = False
        self.player = None
        
        # Create health bar
        self.health_bar = HealthBar(
            max_health=self.max_health, 
            width=50,  # Adjust width as needed
            height=5,   # Adjust height as needed
            player_color=color
        )

    def __repr__(self):
        return f"Buildings(HP: {self.health}, x: {self.x}, y: {self.y})"
   
    def print_Buildings(self):
        print("Buildings")
        print("Cost Wood: ", self.costW)
        print("Build Time: ", self.bTime)
        print("Health: ", self.health)
        print("Size: ", self.sizeMap)

    def getHp(self):
        return self.health

    def setHp(self, hp):
        self.health = max(0, min(hp, self.max_health))
        self.health_bar.update(self.health)

    def setX(self, x):
        self.x = x
   
    def setY(self, y):
        self.y = y

    def getX(self):
        return self.x
   
    def getY(self):
        return self.y
   
    def getSizeMap(self):
        return self.sizeMap
   
    def getBuildingTime(self):
        return self.bTime
    
    def setPlayer(self, player):
        self.player = player