import pygame
import sys

from model.Player import Player

class ControllerPlayer(Player.name, Player.f, Player.w, Player.g):
    
    def __init__(self):
        self.player = Player(Player.name, Player.f, Player.w, Player.g)