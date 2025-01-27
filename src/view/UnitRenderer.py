import pygame

class UnitRenderer:
    def __init__(self, unit, sprites_walk_down):
        self.unit = unit  # Instance de la classe Unit
        self.sprites_walk_down = sprites_walk_down
        self.current_sprites = None
        self.current_frame = 0
        self.flip_sprite = False
        self.animation_speed = 1
        self.animation_counter = 0
        self.initialized = False
    def set_animation_direction(self):
        """Choisit la bonne animation en fonction de la direction du déplacement."""
        
        if self.unit.target_x == self.unit.x:
            if self.unit.target_y > self.unit.y:
                self.current_sprites = self.sprites_walk_down # Marcher vers le bas

    def update(self):
        """Update the animation frame of the unit"""
        if self.unit.action == "move" :
            if not self.initialized:
               self.set_animation_direction()
               self.initialized = True
            if self.current_sprites is not None:
             self.animation_counter += 1
             if self.animation_counter >= self.animation_speed:
                self.current_frame = (self.current_frame + 1) % len(self.current_sprites)
                self.animation_counter = 0


    def get_current_sprite(self):
        """Return the current sprite to display"""
        if self.current_sprites:
           return self.current_sprites[self.current_frame]
        return None