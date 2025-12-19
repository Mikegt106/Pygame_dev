from entities.enemies.hellhound import Hellhound
from entities.enemies.registry import register_enemy

class Hellhound2(Hellhound):
    pass

register_enemy("hellhound2", Hellhound2)