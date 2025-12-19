# loot_system.py
import random
import config
from pickups import CoinPickup, ItemPickup


class LootSystem:
    def __init__(self, coins_min: int = 0, coins_max: int = 4, item_drop_chance=0.4):
        self.coins_min = int(coins_min)
        self.coins_max = int(coins_max)
        self.item_drop_chance = float(item_drop_chance)

    def on_enemy_death(self, enemy, pickups: list):

        # anti-double-drop guard
        if getattr(enemy, "_loot_dropped", False):
            return
        enemy._loot_dropped = True

        # ==========================
        # COINS
        # ==========================
        loot_cfg = getattr(enemy, "cfg", {}).get("loot", {})
        vmin = int(loot_cfg.get("coins_min", self.coins_min))
        vmax = int(loot_cfg.get("coins_max", self.coins_max))
        if vmax < vmin:
            vmax = vmin

        value = random.randint(vmin, vmax)
        if value > 0:
            pickups.append(
                CoinPickup(enemy.rect.centerx, enemy.rect.centery, value=value)
            )

        # ==========================
        # ITEMS (HP regen)
        # ==========================
        item_chance = float(loot_cfg.get("item_chance", self.item_drop_chance))
        if random.random() > item_chance:
            return

        items = config.ITEMS
        if not items:
            return

        # enemy override weights, anders default uit config.ITEMS["..."]["weight"]
        w_override = loot_cfg.get("item_weights", None)

        if isinstance(w_override, dict) and len(w_override) > 0:
            names = [k for k in w_override.keys() if k in items]
            weights = [w_override[k] for k in names]
        else:
            names = list(items.keys())
            weights = [items[k].get("weight", 1) for k in names]

        choice = random.choices(names, weights=weights, k=1)[0]
        cfg = items[choice]

        pickups.append(ItemPickup(enemy.rect.centerx, enemy.rect.centery, cfg))