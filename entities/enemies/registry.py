# entities/enemies/registry.py
from __future__ import annotations
from typing import Dict, Type

ENEMY_REGISTRY: Dict[str, Type] = {}

def register_enemy(name: str, cls: Type):
    ENEMY_REGISTRY[name] = cls

def get_enemy_class(name: str):
    if name not in ENEMY_REGISTRY:
        raise KeyError(f"Enemy type '{name}' not registered. Registered: {list(ENEMY_REGISTRY.keys())}")
    return ENEMY_REGISTRY[name]