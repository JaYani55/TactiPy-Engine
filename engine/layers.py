class Layer:
    """
    Represents a single layer of the map.
    Each cell in this layer has an integer tile ID referencing ASCII_TILESET.
    """
    def __init__(self, width, height, fill_tile=0):
        self.width = width
        self.height = height
        self.tiles = [
            [{"id": fill_tile, "z": 0} for _ in range(width)]
            for _ in range(height)
        ]

    def get_tile(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return {"id": 0, "z": 0}

    def set_tile(self, x, y, tile_id, z=0):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.tiles[y][x] = {"id": tile_id, "z": z}

    def get_z(self, x, y):
        return self.get_tile(x, y)["z"]
