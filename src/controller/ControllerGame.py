import curses
import pygame
import sys
from view.ViewMap import ViewMap
from view.ViewTerminal import ViewTerminal


class ControllerGame():
    def __init__(self, controllerMap):
        self.controllerMap = controllerMap
        self.mode = "terminal"
        self.viewTerminal = ViewTerminal(controllerMap.getMap())
        self.viewPygame = None

    def lancer_mode_terminal(self):
        curses.wrapper(self.boucle_terminal)

    def boucle_terminal(self, stdscr):
        self.viewTerminal.initialiser(stdscr)

        while self.mode == "terminal":
            self.viewTerminal.draw_map()
            stdscr.refresh()

            touche = stdscr.getch()
            if touche == ord('z'):
                self.viewTerminal.deplacer_camera(0, -1)
            elif touche == ord('s'):
                self.viewTerminal.deplacer_camera(0, 1)
            elif touche == ord('q'):
                self.viewTerminal.deplacer_camera(-1, 0)
            elif touche == ord('d'):
                self.viewTerminal.deplacer_camera(1, 0)
            elif touche == ord('v'):
                self.changer_mode_pygame()
                break
            elif touche == ord('p'):
                break

    def changer_mode_pygame(self):
        if self.mode == "terminal":
            pygame.init()
            self.mode = "pygame"
            self.viewPygame = ViewMap(self.controllerMap.getMap(), self.controllerMap)
        elif self.mode == "pygame":
            pygame.quit()
            self.mode = "terminal"
            self.viewTerminal = ViewTerminal(controllerMap.getMap())


    def run(self):
        if self.mode == "terminal":
            self.lancer_mode_terminal()
        else:
            self.run_pyGame()

    def run_pyGame(self):
        running = True
        pos_x, pos_y = 0, 0

        while running and self.mode == "pygame":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.mode = "terminal"  # Revenir au mode terminal si la fenêtre Pygame est fermée
                    break

                # Gestion des touches
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        pos_y = max(0, pos_y - 1)
                    elif event.key == pygame.K_DOWN:
                        pos_y = min(self.controllerMap.map.map_height - 1, pos_y + 1)
                    elif event.key == pygame.K_LEFT:
                        pos_x = max(0, pos_x - 1)
                    elif event.key == pygame.K_RIGHT:
                        pos_x = min(self.controllerMap.map.map_width - 1, pos_x + 1)
                    elif event.key == pygame.K_v:
                        running = False
                        changer_mode_pygame()

            # Dessiner la carte avec Pygame
            if self.viewPygame:
                self.viewPygame.draw_map_2_5D(self.viewPygame.screen, pos_x, pos_y)

        pygame.quit()
