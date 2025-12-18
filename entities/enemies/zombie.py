# entities/enemies/zombie.py
import pygame
from entities.enemies.enemy_base import EnemyBase
from entities.enemies.registry import register_enemy


class Zombie(EnemyBase):
    def __init__(self, x: int, y: int, config: dict):
        super().__init__(x, y, config)

        # --- ATTACK ---
        self.attack_damage = int(config.get("attack_damage", 1))
        self.attack_range = float(config.get("attack_range", 90))
        self.attack_cooldown = float(config.get("attack_cooldown", 1.0))
        self.attack_hit_time = float(config.get("attack_hit_time", 0.25))

        self.cooldown_timer = 0.0
        self.attack_timer = 0.0
        self.attack_hit_done = False

        # --- STUN (parry) ---
        # ❗ NIET: self.stun_timer = 0.0 (zit al in EnemyBase)
        self.stun_duration = float(config.get("stun_duration", 0.70))
        self.stun_anim_speed = float(config.get("stun_anim_speed", 0.20))

        # --- grayscale cache (per surface id) ---
        self._gray_cache: dict[int, pygame.Surface] = {}

    # -------------------------
    # STUN
    # -------------------------
    def stun(self, duration: float | None = None):
        dur = self.stun_duration if duration is None else float(duration)

        # ✅ gebruik de base stun_timer + (optioneel) base anim
        super().stun(dur)

        # cancel attack instantly
        self.attack_timer = 0.0
        self.attack_hit_done = True
        self.cooldown_timer = max(self.cooldown_timer, 0.25)

        # optional: show hurt if exists (one-shot)
        if "hurt" in self.anim.animations:
            self.anim.play("hurt", reset_if_same=True)

    # -------------------------
    # ATTACK
    # -------------------------
    def start_attack(self):
        self.anim.play("attack", reset_if_same=True)
        self.attack_timer = 0.0
        self.attack_hit_done = False
        self.cooldown_timer = self.attack_cooldown

    # -------------------------
    # UPDATE (override enkel om stun anim trager te maken)
    # -------------------------
    def update(self, dt: float, player):
        # death fade + remove => EnemyBase regelt dit
        if self.dead:
            super().update(dt, player)
            return

        # stun: zelf afhandelen zodat anim trager loopt + grey effect zichtbaar blijft
        if self.stun_timer > 0:
            self.stun_timer = max(0.0, self.stun_timer - dt)
            self.anim.update(dt * self.stun_anim_speed)
            self.rect.midbottom = self.pos
            return

        # anders normale flow (roept update_alive)
        super().update(dt, player)

    # -------------------------
    # UPDATE ALIVE
    # -------------------------
    def update_alive(self, dt: float, player):
        # cooldown
        if self.cooldown_timer > 0:
            self.cooldown_timer = max(0.0, self.cooldown_timer - dt)

        # hurt one-shot
        if self.anim.state == "hurt":
            self.anim.update(dt)
            if self.anim.finished:
                self.anim.play("idle")
            return

        # attack state
        if self.anim.state == "attack":
            self.anim.update(dt)
            self.attack_timer += dt

            if (not self.attack_hit_done) and (self.attack_timer >= self.attack_hit_time):
                if abs(player.rect.centerx - self.rect.centerx) <= self.attack_range:
                    blocked = player.take_damage(self.attack_damage)
                    if blocked:
                        self.stun()
                self.attack_hit_done = True

            if self.anim.finished:
                self.anim.play("idle")
            return

        # AI: decide move/attack
        dx = player.rect.centerx - self.rect.centerx
        dist = abs(dx)

        # in range -> start attack
        if dist <= self.attack_range and self.cooldown_timer <= 0:
            self.facing_right = (dx > 0)
            self.start_attack()
            return

        # walk towards player
        if dist < 5:
            self.anim.play("idle")
            self.anim.update(dt)
        else:
            direction = 1 if dx > 0 else -1
            self.facing_right = (direction == 1)
            self.pos.x += self.speed * direction * dt
            self.anim.play("walk")
            self.anim.update(dt)

    # -------------------------
    # GRAYSCALE HELP
    # -------------------------
    def _get_grayscale(self, surf: pygame.Surface) -> pygame.Surface:
        key = id(surf)
        cached = self._gray_cache.get(key)
        if cached is not None:
            return cached

        s = surf.convert_alpha()
        arr = pygame.surfarray.array3d(s)

        gray = (arr[:, :, 0] * 0.299 + arr[:, :, 1] * 0.587 + arr[:, :, 2] * 0.114).astype(arr.dtype)
        arr[:, :, 0] = gray
        arr[:, :, 1] = gray
        arr[:, :, 2] = gray

        gray_surf = pygame.surfarray.make_surface(arr).convert_alpha()
        alpha = pygame.surfarray.array_alpha(s)
        pygame.surfarray.pixels_alpha(gray_surf)[:, :] = alpha

        self._gray_cache[key] = gray_surf
        return gray_surf

    # -------------------------
    # DRAW
    # -------------------------
    def draw(self, screen: pygame.Surface):
        img = self.anim.get_image(self.facing_right)

        # stun tint (grey + slight blue add) — ook tijdens stun zichtbaar
        if self.stun_timer > 0 and (not self.dead):
            gray = self._get_grayscale(img)
            fx = gray.copy()
            fx.fill((15, 25, 45), special_flags=pygame.BLEND_RGB_ADD)
            img = fx

        # ✅ death fade komt uit EnemyBase (self.alpha), dus respecteer dat
        if self.dead and getattr(self, "alpha", 255) < 255:
            img = img.copy()
            img.set_alpha(self.alpha)

        screen.blit(img, self.rect)


register_enemy("zombie", Zombie)