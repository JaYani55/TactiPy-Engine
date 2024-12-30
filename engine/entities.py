import pygame
from .config import TILE_WIDTH, TILE_HEIGHT

class Entity:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z  # For future usage (e.g., flying, jumping, layering)
        self.char = "@"  # ASCII symbol for demonstration
        self.color = (255, 255, 0)  # Bright yellow for better visibility
        self.axis = (x, y, z)  # storing axes in a tuple
        self.inventory = []    # placeholder for inventory
        self.max_health = 100
        self.current_health = self.max_health
        self.falling_multiplier = 10  # damage per z-level beyond safe distance

    def update(self, world):
        """
        Logic for what this entity should do each frame.
        E.g., handle movement, collision, etc.
        """
        pass

    def move_to(self, new_x, new_y, playfield):
        """Check if movement is possible based on Z-axis differences"""
        current_z = self.z
        # Get highest z-value from all layers at target position
        target_z = max(layer.get_z(new_x, new_y) for layer in playfield.layers)
        
        z_diff = target_z - current_z

        # Moving up
        if z_diff > 1:
            return False  # Can't climb more than 1 unit up
        
        if z_diff < -1:
            fall_damage = abs(z_diff - 1) * self.falling_multiplier
            self.take_damage(fall_damage)
        
        # Update position
        self.x = new_x
        self.y = new_y
        self.z = target_z
        return True

    def take_damage(self, amount):
        self.current_health = max(0, self.current_health - amount)

    def draw(self, surface, font, offset_x, offset_y):
        """
        Draws the entity onto the surface using ASCII for now.
        offset_x, offset_y are the playfield's calculated center offsets
        """
        text_surface = font.render(self.char, True, self.color)
        screen_x = offset_x + (self.x * TILE_WIDTH)
        screen_y = offset_y + (self.y * TILE_HEIGHT)
        # Draw a black background for better visibility
        pygame.draw.rect(surface, (0, 0, 0), 
                        (screen_x, screen_y, TILE_WIDTH, TILE_HEIGHT))
        # Center the character in its tile
        surface.blit(text_surface, (screen_x, screen_y))
        
        # Draw health bar
        health_text = f"{self.current_health}/{self.max_health}"
        health_surface = font.render(health_text, True, (255, 0, 0) if self.current_health < 50 else (0, 255, 0))
        health_x = offset_x + (self.x * TILE_WIDTH)
        health_y = offset_y + (self.y * TILE_HEIGHT) - TILE_HEIGHT
        surface.blit(health_surface, (health_x, health_y))
