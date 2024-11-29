import pygame
from controller.UIHandler import *

def main():
    pygame.init()
    uihandler = UIHandler()
    uihandler.start()

if __name__ == "__main__":
    main()