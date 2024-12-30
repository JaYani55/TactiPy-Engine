from .config_loader import save_world_state, save_character_state

class RoundSystem:
    def __init__(self):
        self.round_number = 1

    def start_round(self, player):
        player.ap = player.max_ap
        # ...existing code...

    def calculate_move_cost(self, distance):
        """
        1 AP per tile traveled.
        """
        return distance  # e.g., diagonal also 1 if you prefer

    def end_round(self, world_state, character_state):
        """End round and save all state changes"""
        self.round_number += 1
        
        # Save both world and character state at end of round
        save_world_state(world_state)
        save_character_state(character_state)
        # ...existing code...
