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

DAMAGE = {
    "book": 1
}