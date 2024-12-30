import pygame
import sys

# ---------------------------------------------------------------------
# Configuration constants
# ---------------------------------------------------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

# For ASCII “tiles”
FONT_SIZE = 16
FONT_NAME = "Courier New"

# Adjust this if you want bigger or smaller tile spacing
TILE_WIDTH = 16
TILE_HEIGHT = 16

# Example tile codes (each tile type maps to an ASCII char).
# You can extend or replace this later with images.
ASCII_TILESET = {
    0: " ",    # empty space
    1: "#",    # wall
    2: ".",    # floor
    3: "~",    # water
    4: "^",    # mountain
}

# ---------------------------------------------------------------------
# Entity and Layer classes
# ---------------------------------------------------------------------
class Entity:
    """
    Base class for any entity (player, NPC, monster) that lives in the world.
    Has x, y, z for positioning in 3D logic but only x, y matter in top-down.
    """
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z  # For future usage (e.g., flying, jumping, layering)
        self.char = "@"  # ASCII symbol for demonstration

    def update(self, world):
        """
        Logic for what this entity should do each frame.
        E.g., handle movement, collision, etc.
        """
        pass

    def draw(self, surface, font, offset_x, offset_y):
        """
        Draws the entity onto the surface using ASCII for now.
        offset_x, offset_y can help shift where the camera or viewport is.
        """
        text_surface = font.render(self.char, True, (255, 255, 255))
        surface.blit(
            text_surface,
            (
                (self.x - offset_x) * TILE_WIDTH,
                (self.y - offset_y) * TILE_HEIGHT,
            )
        )

class Layer:
    """
    Represents a single layer of the map.
    Each cell in this layer has an integer tile ID referencing ASCII_TILESET.
    """
    def __init__(self, width, height, fill_tile=0):
        self.width = width
        self.height = height
        self.tiles = [
            [fill_tile for _ in range(width)] 
            for _ in range(height)
        ]

    def get_tile(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return 0

    def set_tile(self, x, y, tile_id):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x] = tile_id

# ---------------------------------------------------------------------
# World class
# ---------------------------------------------------------------------
class World:
    """
    Holds all layers and entities. 
    Coordinates are in 2D for top-down, 
    but each entity has a z coordinate for 3D logic if desired.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Example: layers[0] is the base layer, layers[1] could be above the player, etc.
        self.layers = []
        self.entities = []

        # Create some example layers
        base_layer = Layer(width, height, fill_tile=2)  # default floor (.)
        # Add walls around the edges just as an example
        for x in range(width):
            base_layer.set_tile(x, 0, 1)          # top wall
            base_layer.set_tile(x, height - 1, 1) # bottom wall
        for y in range(height):
            base_layer.set_tile(0, y, 1)          # left wall
            base_layer.set_tile(width - 1, y, 1)  # right wall

        # Additional decorative layer
        deco_layer = Layer(width, height, fill_tile=0)
        deco_layer.set_tile(width//2, height//2, 4)  # mountain symbol in the middle

        self.layers.append(base_layer)
        self.layers.append(deco_layer)

    def add_entity(self, entity):
        self.entities.append(entity)

    def update(self):
        for entity in self.entities:
            entity.update(self)

    def draw(self, surface, font, camera_x, camera_y):
        """
        Draw each layer, then each entity.
        camera_x, camera_y define which part of the world is visible 
        (if you implement a scrolling camera).
        """
        # Draw each layer
        for layer in self.layers:
            for y in range(self.height):
                for x in range(self.width):
                    tile_id = layer.get_tile(x, y)
                    char = ASCII_TILESET.get(tile_id, "?")
                    text_surface = font.render(char, True, (200, 200, 200))
                    surface.blit(
                        text_surface,
                        (
                            (x - camera_x) * TILE_WIDTH,
                            (y - camera_y) * TILE_HEIGHT
                        )
                    )
        # Draw entities
        for entity in self.entities:
            entity.draw(surface, font, camera_x, camera_y)

# ---------------------------------------------------------------------
# Game class: main logic
# ---------------------------------------------------------------------
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("RPG Engine Prototype (ASCII)")

        # Simple font for ASCII
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

        self.clock = pygame.time.Clock()

        # Replace the fixed-size world with a config-based init
        self.world = World(width=1, height=1)
        self.world.init_from_config("c:/CodingProjects/Games/RPGEngine/world_config.json")

        # Add a player in the center
        self.player = Entity(25, 15, 0)
        self.world.add_entity(self.player)

        # Simple camera tracking
        self.camera_x = 0
        self.camera_y = 0

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0  # seconds passed
            running = self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Very simple movement for the player using arrow keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.y -= 1
                elif event.key == pygame.K_DOWN:
                    self.player.y += 1
                elif event.key == pygame.K_LEFT:
                    self.player.x -= 1
                elif event.key == pygame.K_RIGHT:
                    self.player.x += 1

        return True

    def update(self, dt):
        # Update game state
        self.world.update()
        # Update camera position to keep the player centered, for example
        self.camera_x = max(0, self.player.x - (SCREEN_WIDTH // TILE_WIDTH) // 2)
        self.camera_y = max(0, self.player.y - (SCREEN_HEIGHT // TILE_HEIGHT) // 2)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.world.draw(self.screen, self.font, self.camera_x, self.camera_y)
        pygame.display.flip()

# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
from engine.game import Game

if __name__ == "__main__":
    game = Game()
    game.run()
