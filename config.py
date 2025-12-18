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
    {"type": "zombie",  "cfg_key": "ZOMBIE",  "weight": 70},
    {"type": "zombie2", "cfg_key": "ZOMBIE2", "weight": 30},
]

WAVES = {
    1: {"pool": [{"type":"zombie","cfg_key":"ZOMBIE","weight":100}],
        "max_enemies": 4,      #Totaal enemies tegelijk
        "interval": (1.6, 2.4),
        "total_spawns": 4,     #totaal in deze wave
    },

    2: {"pool": [{"type":"zombie","cfg_key":"ZOMBIE","weight":80},
                 {"type":"zombie2","cfg_key":"ZOMBIE2","weight":20}],
        "max_enemies": 5,
        "interval": (1.3, 2.0),
        "total_spawns": 8,
    },

    3: {"pool": [{"type":"zombie","cfg_key":"ZOMBIE","weight":60},
                 {"type":"zombie2","cfg_key":"ZOMBIE2","weight":40}],
        "max_enemies": 6,
        "interval": (1.1, 1.7),
        "total_spawns": 12,
    },
}

ZOMBIE = {
    "scale": 3,
    "fps": 10,
    "speed": 120,
    "hp": 5,

    "attack_damage": 2,
    "attack_range": 90,        # pixels (tweak)
    "attack_cooldown": 1.0,    # seconden tussen aanvallen
    "attack_hit_time": 0.25,   # wanneer hit gebeurt tijdens attack anim (sec)
    "stun_duration": 0.35,

    "anims": {
        "idle":   {"sheet": "assets/Zombie/Idle.png",   "frames": 6,  "loop": True},
        "walk":   {"sheet": "assets/Zombie/Walk.png",   "frames": 10, "loop": True},
        "attack": {"sheet": "assets/Zombie/Attack.png", "frames": 4,  "loop": False},  # <-- belangrijk
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
    "attack_range": 90,        # pixels (tweak)
    "attack_cooldown": 1.0,    # seconden tussen aanvallen
    "attack_hit_time": 0.25,   # wanneer hit gebeurt tijdens attack anim (sec)
    "stun_duration": 0.35,

    "anims": {
        "idle":   {"sheet": "assets/Zombie2/Idle.png",   "frames": 7,  "loop": True},
        "walk":   {"sheet": "assets/Zombie2/Walk.png",   "frames": 12, "loop": True},
        "attack": {"sheet": "assets/Zombie2/Attack.png", "frames": 10,  "loop": False},  # <-- belangrijk
        "hurt":   {"sheet": "assets/Zombie2/Hurt.png",   "frames": 4,  "loop": False},
        "dead":   {"sheet": "assets/Zombie2/Dead.png",   "frames": 5,  "loop": False},
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

