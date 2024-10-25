import pygame
import sys

from controller.ControllerMap import ControllerMap

class UIHandler():
    def __init__(self):
        self.controller = ControllerMap()
    
    def start(self):
        self.controller.run()