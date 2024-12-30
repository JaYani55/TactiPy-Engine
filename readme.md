!!RPG Tactical combat engine!!
The goal is to create an engine for tactical fights. Map data (xyz coords), player pos, enemy pos, inventory state management etc. are all handled via JSON configs. Data can be imported via Database for fight calculation to be handled in a different engine by importing via a configured Database OR it could be imported via HTTP request OR the fights could be generated via LLM that has the Schema. 
The goal is to create a component for a modular python-based microservice like engine that can be adapted to any type of game. 
It is a server-side engine which means it is also open for multiplayer games that render in the player's client.

## Items/Inventory/State Management



TODO
• Add Hooks configs to import data and execute data via DB or HTTP
- Inventory system schema
- Character Stats Schema
- Turn based Combat (tactical movement, inventory, abilities)
- UI (Click on entities for information and actions)
- Enemies Schema 
- Enemy AI
• Add Scaffolding for state management and inventory management
• Implement dedicated renderer module to extend ASCII Graphics with imported Tilesets.

## Scene Generation with JSON Config

Below are steps to create and load a scene from JSON:

1. Create a JSON file (e.g., world_config.json) defining:
   • World dimensions (width, height).  
   • Each layer and its fill tile.  
   • Any special tiles (walls, floors, decorations).  

   Example (world_config.json):
   {
     "width": 20,
     "height": 15,
     "layers": [
       { "fill_tile": 2, "walls": true },
       { "fill_tile": 0, "decorations": [{ "x": 10, "y": 7, "tile_id": 4 }] }
     ]
   }

2. Call init_from_config in your code:
   world = World(20, 15)
   world.init_from_config("path/to/world_config.json")

3. Add and update entities:
   from engine.entities import Entity
   player = Entity(5, 5)
   world.add_entity(player)

4. Run the main.py to see your JSON-driven world.

## World Configuration Schema

```json
{
  "width": number,       // Width of the playfield
  "height": number,      // Height of the playfield
  "player_start": {     // Starting position for the player
    "x": number,        // X coordinate
    "y": number,        // Y coordinate
    "z": number         // Z coordinate (for future 3D support)
  },
  "layers": [           // Array of layer configurations
    {
      "fill_tile": number,    // Default tile ID to fill the layer (0-4)
      "random_walls": {       // Optional: Add random walls
        "count": number,      // Base number of walls to place
        "variance": number    // Random +/- variation in wall count
      },
      "random_mountains": number,  // Optional: Simple count of mountains to place
      "layout": [            // Optional: Explicit tile placements
        {
          "x": number,       // X coordinate
          "y": number,       // Y coordinate
          "tile_id": number  // Tile ID to place (0-4)
        }
      ]
    }
  ]
}
```

### Tile IDs
- 0: Empty space (" ")
- 1: Wall ("#")
- 2: Floor (".")
- 3: Water ("~")
- 4: Mountain ("^")

### Example Usage
```json
{
  "width": 30,
  "height": 20,
  "player_start": {
    "x": 5,
    "y": 5,
    "z": 0
  },
  "layers": [
    {
      "fill_tile": 2,
      "random_walls": { "count": 10, "variance": 5 },
      "layout": [
        {"x": 5, "y": 5, "tile_id": 4},
        {"x": 6, "y": 5, "tile_id": 4}
      ]
    }
  ]
}
```

## Controls
• Arrow keys or Numpad 8,4,2,6: Cardinal movement (up, left, down, right)
• Numpad 7,9,1,3: Diagonal movement
  - 7: Up-Left
  - 9: Up-Right
  - 1: Down-Left
  - 3: Down-Right

Note: Diagonal movement has a 1.4x modifier for falling damage calculations.

## Additional Requirements and Context

• Manage your fight calculations via JSON or by hooking to a DB/HTTP/LLM.  
• Use Axis position logic (x, y, z) for advanced movement and layering.  
• Provide scaffolding for inventory or state management as needed.  
• Extend or replace ASCII_RENDER with any advanced Renderer (see renderer.py).  
• Test everything with JSON-based data to verify various scene layouts.