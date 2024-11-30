import curses
import pygame
import sys

from model.Game import Game
from view.ViewTerminal import ViewTerminal
from view.ViewPygame import ViewPygame

class ControllerGame():

    def __init__(self, game, uiHanlder):
        self.game = game
        self.mode = True
        self.viewTerminal = ViewTerminal(self.game.map)
        self.viewPygame = ViewPygame(self.game.map)
        self.uiHandler = uiHanlder
        self.paused = False
        self.tab_pressed = False

    @classmethod
    def start_game(cls, uiHandler):
        return cls(Game(), uiHandler)
    
    @classmethod
    def load_game(cls, game, uiHandler):
        return cls(game, uiHandler)
    
    def run_init(self):
        self.viewTerminal = ViewTerminal(self.game.map)
        self.viewPygame = ViewPygame(self.game.map)
        curses.wrapper(self.run_terminal)

    def run_terminal(self, stdscr):
        self.viewTerminal.initialiser(stdscr)

        while self.mode:
            self.viewTerminal.draw_map()
            stdscr.refresh()

            key = stdscr.getch()
            
            if key == 9:
                print("Press tab")

            if not self.paused:
                
                if key == ord('z'):
                    self.viewTerminal.deplacer_camera(0,-1)
                elif key == ord('s'):
                    self.viewTerminal.deplacer_camera(0,1)
                elif key == ord('q'):
                    self.viewTerminal.deplacer_camera(-1,0)
                elif key == ord('d'):
                    self.viewTerminal.deplacer_camera(1,0)
                elif key == ord('p'):
                    self.uiHandler.saveGame()
                    sys.exit()
                    break
                elif key == ord('v'):
                    self.changer_mode()
                    break
                '''
                for player in self.game.lstPlayer:
                    player.update_trainings()
                    player.update_buildings()'''
    
    def changer_mode(self):
        if self.mode:
            self.mode = False
            pygame.init()
            self.run_pygame()
        elif not self.mode:
            pygame.quit()
            self.mode = True
            self.run_init()

    def run_pygame(self):
        running_pygame = True
        pos_x, pos_y = 0, 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_pygame = False
                    self.changer_mode()
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        self.tab_pressed = True
                        self.toggle_pause()
                    elif event.key == pygame.K_v:
                        running = False
                        self.changer_mode()
                    elif event.key == pygame.K_p:
                        self.uiHandler.saveGame()
                        pygame.quit()
                        sys.exit()
            
            if not running_pygame:
                break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_z]:
                pos_y -= 1
            if keys[pygame.K_s]:
                pos_y += 1
            if keys[pygame.K_q]:
                pos_x -= 1
            if keys[pygame.K_d]:
                pos_x += 1
            
            self.viewPygame.draw_map_2_5D(pos_x, pos_y)

            '''
            for player in self.game.lstPlayer:
                player.update_trainings()
                player.update_buildings()  '''          
                    
    def run(self):
        if self.mode:
            self.run_init()
        else:
            self.run_pygame()

    