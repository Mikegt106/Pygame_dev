# entities/enemies/zombie.py
from entities.enemies.enemy_base import EnemyBase


class Zombie(EnemyBase):
    def __init__(self, x: int, y: int, config: dict):
        super().__init__(x, y, config)

        self.attack_damage = int(config.get("attack_damage", 1))
        self.attack_range = float(config.get("attack_range", 90))
        self.attack_cooldown = float(config.get("attack_cooldown", 1.0))
        self.attack_hit_time = float(config.get("attack_hit_time", 0.25))
        self.parry_stun = float(config.get("parry_stun", 0.7))

        self.cooldown_timer = 0.0
        self.attack_timer = 0.0
        self.attack_hit_done = False

    def start_attack(self):
        self.anim.play("attack", reset_if_same=True)
        self.attack_timer = 0.0
        self.attack_hit_done = False
        self.cooldown_timer = self.attack_cooldown

    def update_alive(self, dt: float, player):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt

        # ATTACK anim bezig?
        if self.anim.state == "attack":
            self.anim.update(dt)
            self.attack_timer += dt

            if (not self.attack_hit_done) and self.attack_timer >= self.attack_hit_time:
                if abs(player.rect.centerx - self.rect.centerx) <= self.attack_range:
                    blocked = player.take_damage(self.attack_damage)
                    if blocked:
                        self.stun(self.parry_stun)
                self.attack_hit_done = True

            if self.anim.finished:
                self.anim.play("idle")
            return

        # AI
        dx = player.rect.centerx - self.rect.centerx
        dist = abs(dx)

        # in range -> start attack
        if dist <= self.attack_range and self.cooldown_timer <= 0:
            self.facing_right = dx > 0
            self.start_attack()
            return

        # chase
        if dist > 5:
            direction = 1 if dx > 0 else -1
            self.facing_right = direction == 1
            self.pos.x += self.speed * direction * dt
            self.anim.play("walk")
            self.anim.update(dt)
        else:
            self.anim.play("idle")
            self.anim.update(dt)