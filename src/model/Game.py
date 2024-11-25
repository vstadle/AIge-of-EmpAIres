from model.Map import Map
from model.Map import MapType


class Game():
    def __init__(self):
        self.map = Map(MapType.GENEROUS_RESOURCES)
        self.lstPlayer = []
    
    
    
    def set_game(self,game):
        self = game

    