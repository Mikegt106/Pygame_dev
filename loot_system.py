# loot_system.py
import random
from pickups import CoinPickup


class LootSystem:
    def __init__(self, coins_min: int = 0, coins_max: int = 4):
        # dit betekent nu: VALUE range per kill (niet aantal coins)
        self.coins_min = int(coins_min)
        self.coins_max = int(coins_max)

    def on_enemy_death(self, enemy, pickups: list):
        """
        Call dit EXACT 1x wanneer een enemy net dood gaat.
        Spawnt 0-4 VALUE coins als 1 pickup (of override via enemy.cfg["loot"]).
        """
        # anti-double-drop guard
        if getattr(enemy, "_loot_dropped", False):
            return
        enemy._loot_dropped = True

        # per-enemy override via config (optioneel)
        loot_cfg = getattr(enemy, "cfg", {}).get("loot", {})
        vmin = int(loot_cfg.get("coins_min", self.coins_min))
        vmax = int(loot_cfg.get("coins_max", self.coins_max))
        if vmax < vmin:
            vmax = vmin

        value = random.randint(vmin, vmax)
        if value <= 0:
            return

        # spawn 1 coin pickup met value
        x = enemy.rect.centerx
        y = enemy.rect.centery
        pickups.append(CoinPickup(x, y, value=value))