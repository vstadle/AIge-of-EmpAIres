import pygame
import sys

from controller import ControllerMap

class UIHandler():
    def __init__(self):
        None
    def start():
        ControllerMap()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Quitter en appuyant sur 'q'
                        pygame.quit()
                        sys.exit()
