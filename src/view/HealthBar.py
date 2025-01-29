import pygame
import curses

class HealthBar:
    def __init__(self, max_health, width=50, height=5, player_color=None):
        print(f"HealthBar.__init__ - player_color reçu: {player_color}, Type: {type(player_color)}")
        self.max_health = max_health
        self.current_health = max_health
        self.width = width
        self.height = height
        
        # Définir les couleurs de base
        self.border_color = (0, 0, 0)
        self.background_color = (127, 0, 0)  # Fond rouge pour la partie "vide"
        
        # Mapper les couleurs curses aux couleurs RGB pour la partie "pleine"
        if player_color is not None:
            if player_color == curses.COLOR_RED:
                self.health_color = (255, 0, 0)
            elif player_color == curses.COLOR_GREEN:
                self.health_color = (0, 255, 0)
            elif player_color == curses.COLOR_BLUE:
                self.health_color = (0, 0, 255)
            elif player_color == curses.COLOR_YELLOW:
                self.health_color = (255, 255, 0)
            elif player_color == curses.COLOR_MAGENTA:
                self.health_color = (255, 0, 255)
            elif player_color == curses.COLOR_CYAN:
                self.health_color = (0, 255, 255)
            else:
                self.health_color = (255, 255, 255) 
        else:
            self.health_color = (0, 0, 0) 

    def update(self, current_health):
        self.current_health = max(0, min(current_health, self.max_health))

    def draw(self, screen, x, y):
        print(f"HealthBar.draw() appelée - self.health_color: {self.health_color}, x: {x}, y: {y}") # Gardez ce print

        print(f"  Couleurs RGB: border={self.border_color}, background={self.background_color}, health={self.health_color}") # AJOUTEZ CETTE LIGNE

        if self.current_health < self.max_health:
            ratio = self.current_health / self.max_health

            # Draw border (NOIR)
            pygame.draw.rect(screen, self.border_color, (x-1, y-1, self.width+2, self.height+2))

            # Draw background (ROUGE)
            pygame.draw.rect(screen, self.background_color, (x, y, self.width, self.height))

            # Draw current health with player color (COULEUR DU JOUEUR ou BLANC par défaut)
            health_width = int(self.width * ratio)
            if health_width > 0:
                pygame.draw.rect(screen, self.health_color, (x, y, health_width, self.height))