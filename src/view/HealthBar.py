import pygame

class HealthBar:
    def __init__(self, max_health, width=50, height=5, border_color=(0,0,0), health_color=(0,255,0), background_color=(255,0,0)):
        self.max_health = max_health
        self.current_health = max_health
        self.width = width
        self.height = height
        self.border_color = border_color
        self.health_color = health_color
        self.background_color = background_color

    def update(self, current_health):
        self.current_health = max(0, min(current_health, self.max_health))

    def draw(self, screen, x, y):
        # On affiche uniquement si des dégâts ont été subis
        if self.current_health < self.max_health:
            # Calculate health percentage
            ratio = self.current_health / self.max_health
            
            # Draw border
            pygame.draw.rect(screen, self.border_color, (x-1, y-1, self.width+2, self.height+2))
            
            # Draw background (depleted health)
            pygame.draw.rect(screen, self.background_color, (x, y, self.width, self.height))
            
            # Draw current health
            health_width = int(self.width * ratio)
            if health_width > 0:  # S'assurer qu'il y a encore de la vie à afficher
                pygame.draw.rect(screen, self.health_color, (x, y, health_width, self.height))