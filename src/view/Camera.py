import pygame

class Camera:
    def __init__(self, width, height, grid_length_x, grid_length_y):
        self.width = width
        self.height = height
        self.scroll = pygame.Vector2(0, 0)
        self.speed = 10
        self.speed_max = 20
        self.TILE_SIZE = 64
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        
        # Pré-calcul des limites isométriques
        self.max_scroll_x = (grid_length_x * self.TILE_SIZE) - (width/2) + 1000
        self.max_scroll_y = (grid_length_y * self.TILE_SIZE) - (height/2) + 1000
        self.iso_offset_x = (abs(grid_length_x - grid_length_y) * self.TILE_SIZE) / 2
        self.iso_offset_y = (grid_length_y - 0.5 * grid_length_x) * self.TILE_SIZE
        
    def handle_input(self):
        keys = pygame.key.get_pressed()
        speed = self.speed_max if pygame.key.get_mods() & pygame.KMOD_SHIFT else self.speed
        
        # Vectorized movement calculation
        movement = pygame.Vector2(0, 0)
        if keys[pygame.K_z] or keys[pygame.K_UP]: movement.y += speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: movement.y -= speed
        if keys[pygame.K_q] or keys[pygame.K_LEFT]: movement.x += speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: movement.x -= speed
        
        self.scroll += movement
        self.clamp_scroll()

    def clamp_scroll(self):
        # Utilisation des limites de la carte
        self.scroll.x = max(-self.max_scroll_x - self.iso_offset_x, min(self.scroll.x, self.max_scroll_x + self.iso_offset_x))
        self.scroll.y = max(-self.max_scroll_y - self.iso_offset_y, min(self.scroll.y, self.max_scroll_y + self.iso_offset_y))

    def handle_minimap_navigation(self, mouse_pos, minimap_rect, grass_tiles_size):
        if not (pygame.mouse.get_pressed()[0] and minimap_rect.collidepoint(mouse_pos)):
            return
    
        # Calculer la position relative du clic sur la minimap
        rel_x = (mouse_pos[0] - minimap_rect.x) / minimap_rect.width
        rel_y = (mouse_pos[1] - minimap_rect.y) / minimap_rect.height

        # Calculer l'offset nécessaire
        viewport_width = self.width
        viewport_height = self.height
    
        # Ajuster le calcul en x pour centrer correctement le viewport
        # On ajoute un demi-décalage pour centrer la vue
        target_scroll_x = (rel_x * (grass_tiles_size[0] - viewport_width)) - (grass_tiles_size[0] / 2)
        target_scroll_y = (rel_y * (grass_tiles_size[1] - viewport_height))
    
        # Ajustement pour centrer la caméra par rapport au clic
        self.scroll.x = -target_scroll_x + viewport_width / 2 - self.iso_offset_x
        self.scroll.y = -target_scroll_y + viewport_height / 2
        self.clamp_scroll()