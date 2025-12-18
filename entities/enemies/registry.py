ENEMY_REGISTRY = {}

def register_enemy(name: str, cls):
    ENEMY_REGISTRY[name] = cls