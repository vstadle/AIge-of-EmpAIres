from Map import Map
from Buildings import Buildings
from TownCenter import TownCenter
from Farm import Farm
from Keep import Keep
from Player import Player
from Gold import Gold
from Wood import Wood

def main():
    map = Map()
    tc = TownCenter()
    f = Farm()
    k = Keep()
    print(tc)
    map.addBuilding(tc, 60, 60)
    map.generateSizeRessources(Gold(), 48, 48)
    map.generateSizeRessources(Wood(), 40, 40)
    map.printMap()

if __name__ == "__main__":
    main()