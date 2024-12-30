from .config import (
    TILE_WIDTH, 
    TILE_HEIGHT, 
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)

def draw_round_and_turn(surface, font, round_system):
    text = f"Round: {round_system.round_number} - Player Turn"
    text_surface = font.render(text, True, (255, 255, 255))
    surface.blit(text_surface, (10, 40))  # Position below movement info

def draw_move_route(surface, font, route, offset_x, offset_y):
    """Draw movement path with proper screen position calculation"""
    import pygame
    for (rx, ry) in route:
        rect = pygame.Rect(
            offset_x + rx * TILE_WIDTH,  # Use TILE_WIDTH/HEIGHT constants
            offset_y + ry * TILE_HEIGHT,
            TILE_WIDTH,
            TILE_HEIGHT
        )
        # Draw slightly transparent red rectangle
        s = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
        s.set_alpha(128)
        s.fill((255, 0, 0))
        surface.blit(s, rect)
        # Draw border
        pygame.draw.rect(surface, (255, 0, 0), rect, 1)

def draw_route_info(surface, font, cost):
    info_text = f"Movement Cost: {cost} AP (Click again to move)"
    text_surface = font.render(info_text, True, (255, 255, 255))
    # Draw with black outline for better visibility
    outline = font.render(info_text, True, (0, 0, 0))
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        surface.blit(outline, (11+dx, 11+dy))
    surface.blit(text_surface, (11, 11))

def draw_player_stats(surface, font, player):
    """Draw current/max AP in the top-right corner"""
    ap_text = f"AP: {player.ap}/{player.max_ap}"
    text_surface = font.render(ap_text, True, (255, 255, 255))
    # Position in top-right with padding
    x = SCREEN_WIDTH - text_surface.get_width() - 10
    surface.blit(text_surface, (x, 10))
