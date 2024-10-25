from model.Units import Units
from model.Villager import Villager
from model.Horseman import Horseman
from model.Swordsman import Swordsman
from view.ViewUnits import ViewUnits


class ControllerUnits():
    def __init__(self, units):
        if(units == "Villager"):
            self.unit = Villager()
        elif (units == "Archer"):
            self.unit = Units()
        elif (units == "Horseman"):
            self.unit = Horseman()
        elif (units == "Swordman"):
            self.unit = Swordsman()

    def attack(self, ennemy):
        ennemy.setHealth(ennemy.getHealth - self.unit.getAttack())