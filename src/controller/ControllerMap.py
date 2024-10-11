import pygame 
from    view.ViewMap import ViewMap
from src.model.Map import Map

class Controllermap():
    def __init__(self):
        self.map = Map()
        self.vMap = ViewMap(map)
    



