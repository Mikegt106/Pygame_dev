# entities/enemies/__init__.py
from .registry import get_enemy_class, ENEMY_REGISTRY, register_enemy

# Import enemy modules so they register themselves
from . import zombie
from . import zombie2