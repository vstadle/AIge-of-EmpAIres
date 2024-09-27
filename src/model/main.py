from Map import Map
from Buildings import Buildings
from TownCenter import TownCenter
from Farm import Farm
from Keep import Keep
from Player import Player

def main():
    map = Map()
    tc = TownCenter()
    f = Farm()
    k = Keep()
    print(tc)
    map.addBuilding(k, 35, 35)
    map.printMap()

if __name__ == "__main__":
    main()