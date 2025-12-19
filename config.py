PLAYER = {
    "scale": 3,
    "fps": 12,
    "hp": 10,
    "mana": 10,

    "speed": 250,
    "sprint_speed": 420,

    "anims": {
        "idle":    {"sheet": "assets/Schoolgirl/Idle.png",       "frames": 9,  "loop": True},
        "walk":    {"sheet": "assets/Schoolgirl/Walk.png",       "frames": 12, "loop": True},
        "run":      {"sheet": "assets/Schoolgirl/Run.png",       "frames": 12, "loop": True},
        "attack":  {"sheet": "assets/Schoolgirl/Attack.png",     "frames": 8,  "loop": False},
        "protect": {"sheet": "assets/Schoolgirl/Protection.png", "frames": 4,  "loop": False},
        "dead":    {"sheet": "assets/Schoolgirl/Death.png",      "frames": 5,  "loop": False},
        "hurt":    {"sheet": "assets/Schoolgirl/Hurt.png",       "frames": 3, "loop": True},
        "jump":    {"sheet": "assets/Schoolgirl/Jump.png",       "frames": 15, "loop": False},
    }
}

ENEMY_POOL = [
    {"type": "zombie",      "cfg_key": "ZOMBIE",        "weight": 10},
    {"type": "zombie2",     "cfg_key": "ZOMBIE2",       "weight": 10},
    
    {"type": "skeleton",    "cfg_key": "SKELETON",      "weight": 10},
    {"type": "skeleton2",   "cfg_key": "SKELETON2",     "weight": 10},
    
    {"type": "hellhound",   "cfg_key": "HELLHOUND",     "weight": 10},
    {"type": "hellhound2",   "cfg_key": "HELLHOUND2",     "weight": 10},

    {"type": "demon",       "cfg_key": "DEMON",         "weight": 20},

    {"type": "dragon",      "cfg_key": "DRAGON",        "weight": 10},
    {"type": "dragon2",     "cfg_key": "DRAGON2",       "weight": 10},

]

WAVES = {
# zombie lvls
    1: {"pool": [{"type":"zombie","cfg_key":"ZOMBIE","weight":100}],
        "max_enemies": 1,
        "interval": (1.6, 2.4),
        "total_spawns": 2,
        "scene": "assets/Scenes/schoolyard.png",
    },
    
    2: {"pool": [{"type":"zombie","cfg_key":"ZOMBIE","weight":50},
                 {"type":"zombie2","cfg_key":"ZOMBIE2","weight":50}],
        "max_enemies": 2,
        "interval": (1.3, 2.0),
        "total_spawns": 2,
        "scene": "assets/Scenes/schoolyard.png", 
    },
    
# skeleton lvls
    3: {"pool": [{"type":"skeleton2","cfg_key":"SKELETON2","weight":100}],
        "max_enemies": 2,
        "interval": (1.1, 1.7),
        "total_spawns": 3,
        "scene": "assets/Scenes/schoolyard.png",
    },
    
    4: {"pool": [{"type":"skeleton2","cfg_key":"SKELETON2","weight":70},
                 {"type":"skeleton","cfg_key":"SKELETON","weight":30}],
        "max_enemies": 3,
        "interval": (1.1, 1.7),
        "total_spawns": 5,
        "scene": "assets/Scenes/schoolyard.png",
    },

# hellhound lvls    
    5: {"pool": [{"type":"hellhound","cfg_key":"HELLHOUND","weight":100}],
        "max_enemies": 1,
        "interval": (1.1, 1.7),
        "total_spawns": 2,
        "scene": "assets/Scenes/schoolyard.png",
    },
    
    6: {"pool": [{"type":"hellhound2","cfg_key":"HELLHOUND2","weight":100}],
        "max_enemies": 2,
        "interval": (1.1, 1.7),
        "total_spawns": 4,
        "scene": "assets/Scenes/schoolyard.png",
    },

# demon lvls
    7: {"pool": [{"type":"demon","cfg_key":"DEMON","weight":100}],
        
        "max_enemies": 2,
        "interval": (1.3, 2.0),
        "total_spawns": 2,
        "scene": "assets/Scenes/schoolyard.png",
    },

    8: {"pool": [{"type":"demon","cfg_key":"DEMON","weight":100}],
        
        "max_enemies": 2,
        "interval": (1.3, 2.0),
        "total_spawns": 4,
        "scene": "assets/Scenes/schoolyard.png",
    },

# dragon lvl
    9: {"pool": [{"type":"dragon","cfg_key":"DRAGON","weight":30},
                 {"type":"dragon2","cfg_key":"DRAGON2","weight":70}],
        "max_enemies": 2,
        "interval": (1.1, 1.7),
        "total_spawns": 4,
        "scene": "assets/Scenes/schoolyard.png",
    },


}

ZOMBIE = {
    "scale": 3,
    "fps": 10,
    "speed": 120,
    "hp": 5,

    "attack_damage": 2,
    "attack_range": 90,
    "attack_cooldown": 1.0,
    "attack_hit_time": 0.25,
    "stun_duration": 0.35,

    "loot": {
        "coins_min": 4,
        "coins_max": 6,

        "item_chance": 0.25,  # 25% kans op een HP-item
        "item_weights": {     # als item dropt: meestal apple
            "apple": 80,
            "hp_potion": 20,
        },
    },

    "anims": {
        "idle":   {"sheet": "assets/Zombie/Idle.png",   "frames": 6,  "loop": True},
        "walk":   {"sheet": "assets/Zombie/Walk.png",   "frames": 10, "loop": True},
        "attack": {"sheet": "assets/Zombie/Attack.png", "frames": 4,  "loop": False},
        "hurt":   {"sheet": "assets/Zombie/Hurt.png",   "frames": 4,  "loop": False},
        "dead":   {"sheet": "assets/Zombie/Dead.png",   "frames": 5,  "loop": False},
    }
}

ZOMBIE2 = {
    "scale": 3,
    "fps": 10,
    "speed": 120,
    "hp": 5,

    "attack_damage": 2,
    "attack_range": 90,
    "attack_cooldown": 1.0,
    "attack_hit_time": 0.25,
    "stun_duration": 0.35,

    "loot": {
        "coins_min": 9,
        "coins_max": 11,

        "item_chance": 0.55,  # 55% kans op item (sterker enemy)
        "item_weights": {     # potion vaker dan apple
            "apple": 30,
            "hp_potion": 70,
        },
    },

    "anims": {
        "idle":   {"sheet": "assets/Zombie2/Idle.png",   "frames": 7,  "loop": True},
        "walk":   {"sheet": "assets/Zombie2/Walk.png",   "frames": 12, "loop": True},
        "attack": {"sheet": "assets/Zombie2/Attack.png", "frames": 10, "loop": False},
        "hurt":   {"sheet": "assets/Zombie2/Hurt.png",   "frames": 4,  "loop": False},
        "dead":   {"sheet": "assets/Zombie2/Dead.png",   "frames": 5,  "loop": False},
    }
}

SKELETON = {
    "scale": 3,
    "fps": 10,
    "speed": 120,
    "hp": 6,

    "attack_damage": 3,
    "attack_range": 90,
    "attack_cooldown": 1.0,
    "attack_hit_time": 0.25,
    "stun_duration": 0.35,

    "loot": {
        "coins_min": 9,
        "coins_max": 11,

        "item_chance": 0.55,  # 55% kans op item (sterker enemy)
        "item_weights": {     # potion vaker dan apple
            "apple": 30,
            "hp_potion": 70,
        },
    },

    "anims": {
        "idle":   {"sheet": "assets/Skeleton/Idle.png",   "frames": 7,  "loop": True},
        "walk":   {"sheet": "assets/Skeleton/Walk.png",   "frames": 8, "loop": True},
        "attack": {"sheet": "assets/Skeleton/Attack.png", "frames": 15, "loop": False},
        "hurt":   {"sheet": "assets/Skeleton/Hurt.png",   "frames": 2,  "loop": False},
        "dead":   {"sheet": "assets/Skeleton/Dead.png",   "frames": 5,  "loop": False},
    }
}

SKELETON2 = {
    "scale": 3,
    "fps": 10,
    "speed": 120,
    "hp": 6,

    "attack_damage": 3,
    "attack_range": 90,
    "attack_cooldown": 1.0,
    "attack_hit_time": 0.25,
    "stun_duration": 0.35,

    "loot": {
        "coins_min": 9,
        "coins_max": 11,

        "item_chance": 0.55,  # 55% kans op item (sterker enemy)
        "item_weights": {     # potion vaker dan apple
            "apple": 30,
            "hp_potion": 70,
        },
    },

    "anims": {
        "idle":   {"sheet": "assets/Skeleton2/Idle.png",   "frames": 7,  "loop": True},
        "walk":   {"sheet": "assets/Skeleton2/Walk.png",   "frames": 7, "loop": True},
        "attack": {"sheet": "assets/Skeleton2/Attack.png", "frames": 4, "loop": False},
        "hurt":   {"sheet": "assets/Skeleton2/Hurt.png",   "frames": 3,  "loop": False},
        "dead":   {"sheet": "assets/Skeleton2/Dead.png",   "frames": 5,  "loop": False},
    }
}

HELLHOUND = {
    "scale": 3,
    "fps": 10,
    "speed": 120,
    "hp": 6,

    "attack_damage": 3,
    "attack_range": 90,
    "attack_cooldown": 1.0,
    "attack_hit_time": 0.25,
    "stun_duration": 0.35,

    "loot": {
        "coins_min": 13,
        "coins_max": 16,

        "item_chance": 0.65,  # 55% kans op item (sterker enemy)
        "item_weights": {     # potion vaker dan apple
            "apple": 25,
            "hp_potion": 75,
        },
    },

    "anims": {
        "idle":   {"sheet": "assets/Hellhound/Idle.png",   "frames": 6,  "loop": True},
        "walk":   {"sheet": "assets/Hellhound/Walk.png",   "frames": 9, "loop": True},
        "attack": {"sheet": "assets/Hellhound/Attack.png", "frames": 3, "loop": False},
        "hurt":   {"sheet": "assets/Hellhound/Hurt.png",   "frames": 3,  "loop": False},
        "dead":   {"sheet": "assets/Hellhound/Dead.png",   "frames": 6,  "loop": False},
    }
}

HELLHOUND2 = {
    "scale": 3,
    "fps": 10,
    "speed": 120,
    "hp": 6,

    "attack_damage": 3,
    "attack_range": 90,
    "attack_cooldown": 1.0,
    "attack_hit_time": 0.25,
    "stun_duration": 0.35,

    "loot": {
        "coins_min": 13,
        "coins_max": 16,

        "item_chance": 0.65,  # 55% kans op item (sterker enemy)
        "item_weights": {     # potion vaker dan apple
            "apple": 25,
            "hp_potion": 75,
        },
    },

    "anims": {
        "idle":   {"sheet": "assets/Hellhound2/Idle.png",   "frames": 7,  "loop": True},
        "walk":   {"sheet": "assets/Hellhound2/Walk.png",   "frames": 9, "loop": True},
        "attack": {"sheet": "assets/Hellhound2/Attack.png", "frames": 6, "loop": False},
        "hurt":   {"sheet": "assets/Hellhound2/Hurt.png",   "frames": 3,  "loop": False},
        "dead":   {"sheet": "assets/Hellhound2/Dead.png",   "frames": 5,  "loop": False},
    }
}

DEMON = {
    "scale": 3,
    "fps": 10,
    "speed": 120,
    "hp": 10,

    "attack_damage": 5,
    "attack_range": 90,
    "attack_cooldown": 1.0,
    "attack_hit_time": 0.25,
    "stun_duration": 0.35,

    "loot": {
        "coins_min": 15,
        "coins_max": 18,

        "item_chance": 0.75,  # 75% kans op item (sterker enemy)
        "item_weights": {     # potion vaker dan apple
            "apple": 25,
            "hp_potion": 75,
        },
    },

    "anims": {
        "idle":   {"sheet": "assets/Demon/Idle.png",   "frames": 6,  "loop": True},
        "walk":   {"sheet": "assets/Demon/Walk.png",   "frames": 12, "loop": True},
        "attack": {"sheet": "assets/Demon/Attack.png", "frames": 5, "loop": False},
        "hurt":   {"sheet": "assets/Demon/Hurt.png",   "frames": 3,  "loop": False},
        "dead":   {"sheet": "assets/Demon/Dead.png",   "frames": 3,  "loop": False},
    }
}

DRAGON = {
    "scale": 3,
    "fps": 10,
    "speed": 120,
    "hp": 10,

    "attack_damage": 5,
    "attack_range": 90,
    "attack_cooldown": 1.0,
    "attack_hit_time": 0.25,
    "stun_duration": 0.35,

    "loot": {
        "coins_min": 13,
        "coins_max": 17,

        "item_chance": 0.90,  # 75% kans op item (sterker enemy)
        "item_weights": {     # potion vaker dan apple
            "apple": 30,
            "hp_potion": 70,
        },
    },

    "anims": {
        "idle":   {"sheet": "assets/Dragon/Idle.png",   "frames": 7,  "loop": True},
        "walk":   {"sheet": "assets/Dragon/Walk.png",   "frames": 12, "loop": True},
        "attack": {"sheet": "assets/Dragon/Attack.png", "frames": 10, "loop": False},
        "hurt":   {"sheet": "assets/Dragon/Hurt.png",   "frames": 4,  "loop": False},
        "dead":   {"sheet": "assets/Dragon/Dead.png",   "frames": 3,  "loop": False},
    }
}

DRAGON2 = {
    "scale": 3,
    "fps": 10,
    "speed": 120,
    "hp": 10,

    "attack_damage": 5,
    "attack_range": 90,
    "attack_cooldown": 1.0,
    "attack_hit_time": 0.25,
    "stun_duration": 0.35,

    "loot": {
        "coins_min": 13,
        "coins_max": 17,

        "item_chance": 0.75,  # 75% kans op item (sterker enemy)
        "item_weights": {     # potion vaker dan apple
            "apple": 30,
            "hp_potion": 70,
        },
    },

    "anims": {
        "idle":   {"sheet": "assets/Dragon2/Idle.png",   "frames": 7,  "loop": True},
        "walk":   {"sheet": "assets/Dragon2/Walk.png",   "frames": 12, "loop": True},
        "attack": {"sheet": "assets/Dragon2/Attack.png", "frames": 10, "loop": False},
        "hurt":   {"sheet": "assets/Dragon2/Hurt.png",   "frames": 4,  "loop": False},
        "dead":   {"sheet": "assets/Dragon2/Dead.png",   "frames": 3,  "loop": False},
    }
}


PROJECTILES = {
    "book": {
        "sheet": "assets/Schoolgirl/Book.png",
        "frames": 10,     
        "fps": 16,
        "scale": 2,
        "speed": 650,
        "lifetime": 1.5,
    }
}

DAMAGE = {
    "book": 1
}

ITEMS = {
    "apple": {
        "id": "apple",
        "name": "Apple",
        "image": "assets/Items/Apple.png",
        "heal": 10,
        "stack_limit": 99,
    },
    "hp_potion": {
        "id": "hp_potion",
        "name": "HP Potion",
        "image": "assets/Items/HP_potion.png",
        "heal": 35,
        "stack_limit": 99,
    },
}