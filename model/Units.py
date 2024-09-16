from abc import ABC

class Units(ABC):

    def __init__(self, cost, health, trainingTime, attack, speedAtack, speed, range):
        self.cost = cost
        self.health = health
        self.trainingTime = trainingTime
        self.attack = attack
        self.speedAtack = speedAtack
        self.speed = speed
        self.range = range
