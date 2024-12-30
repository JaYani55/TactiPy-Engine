import random
from .config_loader import load_world_config
from .config import ASCII_TILESET, TILE_WIDTH, TILE_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT
from .layers import Layer  # Import Layer from layers.py

class Playfield:
    """
    Manages layers, entities, and random generation. Always centers itself to the screen.
    """
    def __init__(self, width, height):
        # Remove hardcoded layer creation
        self.width = width
        self.height = height
        self.layers = []
        self.entities = []
        self._setup_z_colors()

    def _setup_z_colors(self):
        """Setup color gradients for Z-axis visualization"""
        # Colors for z < 0 (green getting brighter)
        self.below_colors = [
            (0, 25 * (i + 1), 0) for i in range(10)
        ]
        # Colors for z > 0 (red getting brighter)
        self.above_colors = [
            (25 * (i + 1), 0, 0) for i in range(10)
        ]
        # Base color for z = 0
        self.base_color = (200, 200, 200)

    def _get_z_color(self, z):
        """Get color based on Z coordinate"""
        if z == 0:
            return self.base_color
        elif z < 0:
            index = min(abs(z) - 1, 9)  # -1 to -10 maps to 0-9
            return self.below_colors[int(index)]
        else:
            index = min(z - 1, 9)  # 1 to 10 maps to 0-9
            return self.above_colors[int(index)]

    def init_from_config(self, json_config_path):
        """
        Example of initializing the playfield from a JSON config.
        """
        config = load_world_config(json_config_path)
        self.width = config.get("width", self.width)
        self.height = config.get("height", self.height)
        self.layers.clear()

        for layer_data in config.get("layers", []):
            fill_tile = layer_data.get("fill_tile", 0)
            layer = Layer(self.width, self.height, fill_tile=fill_tile)

            # Parse random_walls
            random_walls = layer_data.get("random_walls", 0)
            wall_count, wall_variance = self._parse_count_variance(random_walls)
            self._place_random_tiles(layer, wall_count, wall_variance, 1)

            # Parse random_mountains
            random_mtns = layer_data.get("random_mountains", 0)
            mtn_count, mtn_variance = self._parse_count_variance(random_mtns)
            self._place_random_tiles(layer, mtn_count, mtn_variance, 4)

            # Parse explicit layout with Z values
            for tile_def in layer_data.get("layout", []):
                x = tile_def.get("x", 0)
                y = tile_def.get("y", 0)
                tile_id = tile_def.get("tile_id", 0)
                z = tile_def.get("z", 0)
                layer.set_tile(x, y, tile_id, z)

            self.layers.append(layer)

    def _parse_count_variance(self, val):
        """
        Allows random_x to be either a numeric or object { count: X, variance: Y }
        Returns (count, variance) tuple.
        """
        if isinstance(val, dict):
            return val.get("count", 0), val.get("variance", 0)
        return val, 0

    def _place_random_tiles(self, layer, base_count, variance, tile_id):
        """
        Places tile_id base_count ± some random variation times.
        """
        final_count = base_count + random.randint(-variance, variance) if variance else base_count
        final_count = max(0, final_count)  # clamp to 0
        for _ in range(final_count):
            rx = random.randint(0, self.width - 1)
            ry = random.randint(0, self.height - 1)
            layer.set_tile(rx, ry, tile_id)

    def add_entity(self, entity):
        self.entities.append(entity)

    def update(self):
        for entity in self.entities:
            entity.update(self)

    def draw(self, surface, font):
        """
        Draws the entire playfield centered on the screen.
        """
        # Calculate how to center the entire map
        total_width = self.width * TILE_WIDTH
        total_height = self.height * TILE_HEIGHT
        offset_x = (SCREEN_WIDTH - total_width) // 2
        offset_y = (SCREEN_HEIGHT - total_height) // 2

        # Draw all layers first
        for layer in self.layers:
            for y in range(self.height):
                for x in range(self.width):
                    tile = layer.get_tile(x, y)  # Now returns a dict with 'id' and 'z'
                    char = ASCII_TILESET.get(tile["id"], "?")
                    color = self._get_z_color(tile["z"])
                    text_surface = font.render(char, True, color)
                    surface.blit(
                        text_surface,
                        (
                            offset_x + x * TILE_WIDTH,
                            offset_y + y * TILE_HEIGHT
                        )
                    )
        
        # Draw entities last to ensure they're on top
        for entity in self.entities:
            entity.draw(surface, font, offset_x, offset_y)
