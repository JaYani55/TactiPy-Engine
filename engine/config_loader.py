import json
import os
import time
from pathlib import Path
import tempfile
import shutil
from threading import Lock

class ConfigManager:
    """Manages atomic writes and reads to config files"""
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.last_write = {}
        self.dirty = set()
        self.cached_data = {}

    def _atomic_write(self, filepath, data):
        """Write data atomically to prevent corruption"""
        temp = tempfile.NamedTemporaryFile(delete=False)
        try:
            with open(temp.name, 'w') as f:
                json.dump(data, f, indent=2)
            shutil.move(temp.name, filepath)
        except Exception as e:
            os.unlink(temp.name)
            raise e

    def save_config(self, config_type, data, force=False):
        """
        Save config data with timestamp checking
        """
        with self._lock:
            filepath = self._get_config_path(config_type)
            current_time = time.time()
            
            # Only write if data is marked dirty or forced
            if config_type in self.dirty or force:
                try:
                    self._atomic_write(filepath, data)
                    self.last_write[config_type] = current_time
                    self.cached_data[config_type] = data
                    self.dirty.discard(config_type)
                except Exception as e:
                    print(f"Error saving {config_type} config: {e}")

    def load_config(self, config_type):
        """
        Load config data with caching
        """
        with self._lock:
            filepath = self._get_config_path(config_type)
            if not os.path.exists(filepath):
                return self._get_default_config(config_type)

            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                self.cached_data[config_type] = data
                return data
            except Exception as e:
                print(f"Error loading {config_type} config: {e}")
                return self._get_default_config(config_type)

    def mark_dirty(self, config_type):
        """Mark a config as needing to be saved"""
        with self._lock:
            self.dirty.add(config_type)

    def _get_config_path(self, config_type):
        """Get the appropriate config file path"""
        base_path = Path("c:/CodingProjects/Games/RPGEngine")
        return str(base_path / f"{config_type}_config.json")

    def _get_default_config(self, config_type):
        """Return default config structure"""
        defaults = {
            "world": {"width": 40, "height": 25},
            "characters": {"player": {"max_ap": 100, "current_ap": 100}}
        }
        return defaults.get(config_type, {})

# Global config manager instance
config_manager = ConfigManager()

def save_world_state(world_data):
    """Save world state at end of round"""
    config_manager.mark_dirty('world')
    config_manager.save_config('world', world_data)

def save_character_state(character_data):
    """Save character state at end of round"""
    config_manager.mark_dirty('characters')
    config_manager.save_config('characters', character_data)

def load_world_config(json_path):
    return config_manager.load_config('world')

def load_actor_config(json_path):
    return config_manager.load_config('characters')

def save_actor_config(json_path, data):
    """Save updated character data back to config file"""
    config_manager.save_config('characters', data, force=True)

def update_character_data(actor_cfg, player):
    """Update config with current character stats"""
    actor_cfg["player"].update({
        "current_ap": player.ap,
        "max_ap": player.max_ap,
        "speed": player.speed,
        "last_update": time.time()
    })
    save_character_state(actor_cfg)
    return actor_cfg

def load_data_from_db_or_http_or_llm(source):
    # Stub for DB, HTTP, or LLM-based data import
    return {}