import pygame
import sys
from .playfield import Playfield
from .entities import Entity
from .config import *
from .config_loader import load_world_config  # Add this import
from .combat import RoundSystem
from .Interface import (
    draw_round_and_turn, draw_move_route, draw_route_info, draw_player_stats
)
from .config_loader import load_actor_config, save_actor_config, update_character_data

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

        self.config_path = "c:/CodingProjects/Games/RPGEngine/characters_config.json"
        actor_cfg = load_actor_config(self.config_path)
        self.round_system = RoundSystem()
        # Initialize player stats
        self.player.speed = actor_cfg["player"]["speed"]
        self.player.max_ap = actor_cfg["player"]["max_ap"]
        self.player.ap = actor_cfg["player"]["current_ap"]

        self.planned_route = []

        self.is_planning_move = False
        self.planned_x = None
        self.planned_y = None
        self.move_cost = 0

        self.offset_x = 0  # Add these for tracking playfield center
        self.offset_y = 0

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0  # seconds passed
            running = self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()

    def get_tile_position(self, screen_x, screen_y):
        """Convert screen coordinates to tile coordinates"""
        # Calculate center offset like playfield does
        self.offset_x = (SCREEN_WIDTH - self.playfield.width * TILE_WIDTH) // 2
        self.offset_y = (SCREEN_HEIGHT - self.playfield.height * TILE_HEIGHT) // 2
        
        # Adjust for offset when converting screen to tile coordinates
        tile_x = (screen_x - self.offset_x) // TILE_WIDTH
        tile_y = (screen_y - self.offset_y) // TILE_HEIGHT
        return tile_x, tile_y

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Right click cancels planned movement
                if event.button == 3:  # Right mouse button
                    self.planned_route.clear()
                    return True
                
                # Left click (existing movement code)
                if event.button == 1:
                    # Convert mouse click to tile coords
                    mx, my = pygame.mouse.get_pos()
                    tile_x, tile_y = self.get_tile_position(mx, my)
                    
                    # Validate clicked position is within playfield bounds
                    if (0 <= tile_x < self.playfield.width and 
                        0 <= tile_y < self.playfield.height):
                        if self.planned_route:
                            # Confirm movement if route cost is within AP
                            route_cost = self.round_system.calculate_move_cost(len(self.planned_route))
                            if route_cost <= self.player.ap:
                                self.player.ap -= route_cost
                                # Move the player to final tile of route
                                final_x, final_y = self.planned_route[-1]
                                self.player.move_to(final_x, final_y, self.playfield)
                                
                                # Prepare state data before ending round
                                world_state = {
                                    "width": self.playfield.width,
                                    "height": self.playfield.height,
                                    "player_pos": {"x": self.player.x, "y": self.player.y, "z": self.player.z}
                                }
                                character_state = {
                                    "player": {
                                        "current_ap": self.player.ap,
                                        "max_ap": self.player.max_ap,
                                        "speed": self.player.speed,
                                        "pos": {"x": self.player.x, "y": self.player.y, "z": self.player.z}
                                    }
                                }
                                self.round_system.end_round(world_state, character_state)
                            self.planned_route.clear()
                        else:
                            # Compute a simple path (straight line for demonstration)
                            self.planned_route = self._compute_route_simple(
                                (self.player.x, self.player.y),
                                (tile_x, tile_y)
                            )
            elif event.type == pygame.KEYDOWN:
                self.pressed_keys.add(event.key)
                if event.key == pygame.K_RETURN and self.is_planning_move:
                    if self.move_cost <= self.player.ap:
                        self.player.ap -= self.move_cost
                        self.player.move_to(self.planned_x, self.planned_y, self.playfield)
                        
                        # Prepare state data before ending round
                        world_state = {
                            "width": self.playfield.width,
                            "height": self.playfield.height,
                            "player_pos": {"x": self.player.x, "y": self.player.y, "z": self.player.z}
                        }
                        character_state = {
                            "player": {
                                "current_ap": self.player.ap,
                                "max_ap": self.player.max_ap,
                                "speed": self.player.speed,
                                "pos": {"x": self.player.x, "y": self.player.y, "z": self.player.z}
                            }
                        }
                        self.round_system.end_round(world_state, character_state)
                    self.is_planning_move = False
                    # Save updated character data
                    self.actor_cfg = update_character_data(self.actor_cfg, self.player)
                    save_actor_config(self.config_path, self.actor_cfg)
            elif event.type == pygame.KEYUP:
                self.pressed_keys.discard(event.key)

        return True

    def _compute_route_simple(self, start, end):
        """
        A simplistic path: walk horizontally, then vertically.
        """
        path = []
        x1, y1 = start
        x2, y2 = end
        # Horizontal steps
        step = 1 if x2 >= x1 else -1
        for x in range(x1, x2, step):
            path.append((x, y1))
        # Vertical steps
        step = 1 if y2 >= y1 else -1
        for y in range(y1, y2, step):
            path.append((x2, y))
        path.append((x2, y2))
        return path

    def update(self, dt):
        self.playfield.update()
        # Remove camera updates since playfield auto-centers

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        # Calculate offsets before drawing anything
        self.offset_x = (SCREEN_WIDTH - self.playfield.width * TILE_WIDTH) // 2
        self.offset_y = (SCREEN_HEIGHT - self.playfield.height * TILE_HEIGHT) // 2
        
        self.playfield.draw(self.screen, self.font)
        draw_round_and_turn(self.screen, self.font, self.round_system)
        if self.planned_route:
            draw_move_route(self.screen, self.font, self.planned_route, 
                          self.offset_x, self.offset_y)
            draw_route_info(self.screen, self.font, len(self.planned_route))
        draw_player_stats(self.screen, self.font, self.player)
        pygame.display.flip()
