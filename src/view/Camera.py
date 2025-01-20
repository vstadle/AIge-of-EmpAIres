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
        
        # Pre-calculate max scroll boundaries
        self.max_scroll_x = grid_length_x * self.TILE_SIZE * 2 - width +100000
        self.max_scroll_y = grid_length_y * self.TILE_SIZE + self.TILE_SIZE + 15 - height +100000

    def handle_input(self):
        keys = pygame.key.get_pressed()
        speed = self.speed_max if pygame.key.get_mods() & pygame.KMOD_SHIFT else self.speed
        
        # Vectorized movement calculation
        movement = pygame.Vector2(0, 0)
        if keys[pygame.K_z]: movement.y += speed
        if keys[pygame.K_s]: movement.y -= speed
        if keys[pygame.K_q]: movement.x += speed
        if keys[pygame.K_d]: movement.x -= speed
        
        self.scroll += movement
        self.clamp_scroll()

    def clamp_scroll(self):
        # Using pre-calculated boundaries
        self.scroll.x = max(-self.max_scroll_x, min(self.scroll.x, 100000))
        self.scroll.y = max(-self.max_scroll_y, min(self.scroll.y, 100000))

    def handle_minimap_navigation(self, mouse_pos, minimap_rect, grass_tiles_size):
        """
        Gère la navigation par clic sur la minimap avec correction du décalage horizontal
        """
        if not (pygame.mouse.get_pressed()[0] and minimap_rect.collidepoint(mouse_pos)):
            return
        
        # Position relative du clic sur la minimap (0 à 1)
        rel_x = (mouse_pos[0] - minimap_rect.x) / minimap_rect.width
        rel_y = (mouse_pos[1] - minimap_rect.y) / minimap_rect.height
        
        # Calculer les dimensions maximales de scroll
        scroll_width = grass_tiles_size[0] - self.width
        scroll_height = grass_tiles_size[1] - self.height
        
        # Ajuster le calcul de la position horizontale pour la vue isométrique
        # Le facteur 0.5 ajuste le décalage pour la projection isométrique
        adjusted_rel_x = (rel_x - 0.5) * 2
        self.scroll.x = -((adjusted_rel_x * scroll_width * 0.5) + scroll_width * 0.5)
        
        # Calcul vertical reste inchangé car il est déjà correct
        self.scroll.y = -(rel_y * scroll_height)
        
        self.clamp_scroll()