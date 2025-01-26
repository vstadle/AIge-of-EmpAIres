import pygame

class HealthBar:
    def __init__(self, max_health, width=50, height=5, border_color=(0,0,0), health_color=(0,255,0), background_color=(255,0,0)):
        """
        Initialize a health bar
        
        :param max_health: Maximum health of the entity
        :param width: Width of the health bar
        :param height: Height of the health bar
        :param border_color: Color of the health bar border
        :param health_color: Color of the remaining health
        :param background_color: Color of the depleted health
        """
        self.max_health = max_health
        self.current_health = max_health
        self.width = width
        self.height = height
        self.border_color = border_color
        self.health_color = health_color
        self.background_color = background_color

    def update(self, current_health):
        """
        Update the current health of the entity
        
        :param current_health: Current health of the entity
        """
        self.current_health = max(0, min(current_health, self.max_health))

    def draw(self, screen, x, y):
        """
        Draw the health bar on the screen
        
        :param screen: Pygame screen surface
        :param x: X coordinate to draw the health bar
        :param y: Y coordinate to draw the health bar
        """
        # Calculate health percentage
        ratio = self.current_health / self.max_health
        
        # Draw border
        pygame.draw.rect(screen, self.border_color, (x-1, y-1, self.width+2, self.height+2))
        
        # Draw background (depleted health)
        pygame.draw.rect(screen, self.background_color, (x, y, self.width, self.height))
        
        # Draw current health
        health_width = int(self.width * ratio)
        pygame.draw.rect(screen, self.health_color, (x, y, health_width, self.height))