# loot_system.py
import random
from pickups import CoinPickup

class LootSystem:
    def __init__(self, coins_min: int = 0, coins_max: int = 4):
        self.coins_min = int(coins_min)
        self.coins_max = int(coins_max)

    def on_enemy_death(self, enemy, pickups: list):
        """
        Call dit EXACT 1x wanneer een enemy net dood gaat.
        Spawnt 0-4 coins (of per-enemy override via enemy.cfg["loot"]).
        """
        # anti-double-drop guard
        if getattr(enemy, "_loot_dropped", False):
            return
        enemy._loot_dropped = True

        # per-enemy override via config (optioneel)
        loot_cfg = getattr(enemy, "cfg", {}).get("loot", {})
        cmin = int(loot_cfg.get("coins_min", self.coins_min))
        cmax = int(loot_cfg.get("coins_max", self.coins_max))
        if cmax < cmin:
            cmax = cmin

        n = random.randint(cmin, cmax)
        if n <= 0:
            return

        # spawn coins rond enemy center
        x = enemy.rect.centerx
        y = enemy.rect.centery
        for _ in range(n):
            pickups.append(CoinPickup(x, y, value=1))