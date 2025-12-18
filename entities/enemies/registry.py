# entities/enemies/registry.py
from entities.enemies.zombie import Zombie
from entities.enemies.zombie2 import Zombie2

ENEMY_REGISTRY = {
    "zombie": Zombie,
    "zombie2": Zombie2,
}

def get_enemy_class(enemy_type: str):
    if enemy_type not in ENEMY_REGISTRY:
        raise KeyError(f"Unknown enemy type: {enemy_type}")
    return ENEMY_REGISTRY[enemy_type]