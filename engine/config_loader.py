
import json

def load_world_config(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data

def load_actor_config(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data

def load_data_from_db_or_http_or_llm(source):
    # Stub for DB, HTTP, or LLM-based data import
    return {}