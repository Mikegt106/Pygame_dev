from entities.enemies.dragon import Dragon
from entities.enemies.registry import register_enemy

class Dragon2(Dragon):
    pass

register_enemy("dragon2", Dragon2)