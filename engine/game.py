import pygame
import sys
from .playfield import Playfield
from .entities import Entity
from .config import *
from .config_loader import load_world_config  # Add this import

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("RPG Engine Prototype (ASCII)")

        # Simple font for ASCII
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

        self.clock = pygame.time.Clock()

        # Load config and initialize playfield - Fix the order and usage
        self.playfield = Playfield(1, 1)
        self.playfield.init_from_config("c:/CodingProjects/Games/RPGEngine/world_config.json")
        
        # Now get the config after it's been loaded
        self.config = load_world_config("c:/CodingProjects/Games/RPGEngine/world_config.json")

        # Get player position from config
        player_start = self.config.get("player_start", {"x": 15, "y": 10, "z": 0})
        self.player = Entity(
            player_start.get("x", 15),
            player_start.get("y", 10),
            player_start.get("z", 0)
        )
        self.playfield.add_entity(self.player)
        self.pressed_keys = set()  # Track currently pressed keys

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

            # Track key states
            if event.type == pygame.KEYDOWN:
                self.pressed_keys.add(event.key)
            elif event.type == pygame.KEYUP:
                self.pressed_keys.discard(event.key)

            # Process movement based on current key combination
            new_x, new_y = self.player.x, self.player.y
            
            # Check combinations of pressed keys for diagonal movement
            up = pygame.K_UP in self.pressed_keys
            down = pygame.K_DOWN in self.pressed_keys
            left = pygame.K_LEFT in self.pressed_keys
            right = pygame.K_RIGHT in self.pressed_keys

            if up and left:
                new_x -= 1
                new_y -= 1
            elif up and right:
                new_x += 1
                new_y -= 1
            elif down and left:
                new_x -= 1
                new_y += 1
            elif down and right:
                new_x += 1
                new_y += 1
            elif up:
                new_y -= 1
            elif down:
                new_y += 1
            elif left:
                new_x -= 1
            elif right:
                new_x += 1

            if (new_x, new_y) != (self.player.x, self.player.y):
                self.player.move_to(new_x, new_y, self.playfield)

        return True

    def update(self, dt):
        self.playfield.update()
        # Remove camera updates since playfield auto-centers

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.playfield.draw(self.screen, self.font)
        pygame.display.flip()
