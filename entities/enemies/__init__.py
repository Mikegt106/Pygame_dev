# entities/enemies/__init__.py
from .registry import get_enemy_class, ENEMY_REGISTRY, register_enemy

# Import enemy modules so they register themselves
from . import zombie
from . import zombie2
from . import skeleton
from . import skeleton2
from . import hellhound
from . import hellhound2
from . import demon
from . import dragon
from . import dragon2