from model.Map import Map
from model.Map import MapType


class Game():
    def __init__(self):
        self.map = None
        self.lstPlayer = []
    
    
    
    def setGame(self,game):
        self.game = game

    def setLstPlayer(self,lstPlayer):
        self.lstPlayer = lstPlayer

    def setMap(self,map):
        self.map = map
    
    def addPlayer(self,player):
        self.lstPlayer.append(player)