import curses
import pygame
import sys
from controller.ControllerMap import ControllerMap 
from view.ViewMap import ViewMap
from view.ViewTerminal import ViewTerminal


class ControllerGame():

    cpt = 0

    def __init__(self, ControllerMap):
        self.ControllerMap = ControllerMap
        self.mode = "terminal"
        self.viewTerminal = ViewTerminal(ControllerMap.getMap())
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
                self.changer_mode()
                break
            elif touche == ord('p'):
                break

    def changer_mode(self):
        if self.mode == "terminal":
            pygame.init()
            self.mode = "pygame"
            self.viewTerminal = None
            self.viewPygame = ViewMap(self.ControllerMap.getMap(), self.ControllerMap)
            self.run_pyGame()
        elif self.mode == "pygame":
            pygame.quit()
            self.mode = "terminal"
            self.viewTerminal = ViewTerminal(self.ControllerMap.getMap())
            self.viewPygame = None
            self.lancer_mode_terminal()


    def run(self):
        if self.mode == "terminal":
            self.lancer_mode_terminal()
        else:
            self.run_pyGame()

    def run_pyGame(self):
        running = True
        pos_x, pos_y = 0, 0

        ControllerGame.cpt += 1
        print(ControllerGame.cpt)

        while running and self.mode == "pygame":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.mode = "terminal"  # Revenir au mode terminal si la fenêtre Pygame est fermée
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_v:
                        running = False
                        self.changer_mode()
                        print("mode terminal")
                        print("Running : ", running)
                        print("Mode : ", self.mode)
                        break
                    elif event.key == pygame.K_p:
                        pygame.quit()
                        sys.exit()
            if not running:
                break
            keys = pygame.key.get_pressed()
            if keys[pygame.K_z]:  # Avancer
                pos_y -= 1
            if keys[pygame.K_s]:  # Reculer
                pos_y += 1
            if keys[pygame.K_q]:  # Gauche
                pos_x -= 1
            if keys[pygame.K_d]:  # Droite
                pos_x += 1

            if self.viewPygame:
                self.viewPygame.draw_map_2_5D(self.viewPygame.screen, pos_x, pos_y)

        pygame.quit()
