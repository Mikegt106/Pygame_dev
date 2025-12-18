import pygame
from animation import SpriteSheet, Animator


class Zombie:
    def __init__(self, x: int, y: int, config: dict):
        self.facing_right = False
        self.speed = config.get("speed", 120)
        self.hp = config.get("hp", 5)
        self.dead = False

        # --- ATTACK ---
        self.attack_damage = config.get("attack_damage", 1)
        self.attack_range = config.get("attack_range", 90)
        self.attack_cooldown = config.get("attack_cooldown", 1.0)
        self.attack_hit_time = config.get("attack_hit_time", 0.25)

        self.cooldown_timer = 0.0
        self.attack_timer = 0.0
        self.attack_hit_done = False

        # --- STUN (parry) ---
        self.stun_timer = 0.0
        self.stun_duration = config.get("stun_duration", 0.70)
        self.stun_anim_speed = config.get("stun_anim_speed", 0.20)  # 20% anim speed

        # --- POST-STUN SLOW WALK ---
        self.slow_timer = 0.0
        self.slow_duration = config.get("slow_duration", 0.60)
        self.slow_multiplier = config.get("slow_multiplier", 0.45)

        # --- ANIMATIONS ---
        scale = config.get("scale", 2)
        fps = config.get("fps", 10)

        animations = {}
        for name, a in config["anims"].items():
            sheet = SpriteSheet(a["sheet"])
            frames = a["frames"]

            fw = sheet.sheet.get_width() // frames
            fh = sheet.sheet.get_height()

            right = sheet.slice_row(0, frames, fw, fh, scale)
            left = [pygame.transform.flip(f, True, False) for f in right]
            animations[name] = {"right": right, "left": left, "loop": a.get("loop", True)}

        self.anim = Animator(animations, default="idle", fps=fps)

        self.image = self.anim.get_image(self.facing_right)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.pos = pygame.Vector2(self.rect.midbottom)

        # --- grayscale cache (per frame surface) ---
        self._gray_cache = {}  # key = id(surface) -> gray_surface

    # ------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------
    def _get_grayscale(self, surf: pygame.Surface) -> pygame.Surface:
        """Return cached grayscale version of surf (fast after first time)."""
        key = id(surf)
        cached = self._gray_cache.get(key)
        if cached is not None:
            return cached

        # ensure we have alpha
        s = surf.convert_alpha()
        arr = pygame.surfarray.array3d(s)  # (w,h,3)

        # luminance grayscale
        # gray = 0.299R + 0.587G + 0.114B
        gray = (arr[:, :, 0] * 0.299 + arr[:, :, 1] * 0.587 + arr[:, :, 2] * 0.114).astype(arr.dtype)
        arr[:, :, 0] = gray
        arr[:, :, 1] = gray
        arr[:, :, 2] = gray

        gray_surf = pygame.surfarray.make_surface(arr).convert_alpha()

        # restore alpha from original
        alpha = pygame.surfarray.array_alpha(s)
        pygame.surfarray.pixels_alpha(gray_surf)[:, :] = alpha

        self._gray_cache[key] = gray_surf
        return gray_surf

    # ------------------------------------------------------------
    # DAMAGE / STUN
    # ------------------------------------------------------------
    def take_damage(self, amount: int):
        if self.dead:
            return

        self.hp -= amount
        if self.hp <= 0:
            self.dead = True
            self.anim.play("dead", reset_if_same=True)
            return

        if "hurt" in self.anim.animations:
            self.anim.play("hurt", reset_if_same=True)

    def stun(self, duration: float | None = None):
        """Called when player successfully blocks (parry)."""
        dur = self.stun_duration if duration is None else duration
        self.stun_timer = max(self.stun_timer, dur)

        # cancel attack instantly
        self.attack_timer = 0.0
        self.attack_hit_done = True
        self.cooldown_timer = max(self.cooldown_timer, 0.25)

        # after stun: walk slower for a bit
        self.slow_timer = max(self.slow_timer, self.slow_duration)

        # keep current anim, or optionally show hurt
        if "hurt" in self.anim.animations:
            self.anim.play("hurt", reset_if_same=True)

    # ------------------------------------------------------------
    # ATTACK
    # ------------------------------------------------------------
    def start_attack(self):
        self.anim.play("attack", reset_if_same=True)
        self.attack_timer = 0.0
        self.attack_hit_done = False
        self.cooldown_timer = self.attack_cooldown

    # ------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------
    def update(self, dt: float, player):
        # cooldown
        if self.cooldown_timer > 0:
            self.cooldown_timer = max(0.0, self.cooldown_timer - dt)

        # post-stun slow timer
        if self.slow_timer > 0:
            self.slow_timer = max(0.0, self.slow_timer - dt)

        # death
        if self.dead:
            self.anim.update(dt)
            return

        # --- STUN BLOCKS EVERYTHING ---
        if self.stun_timer > 0:
            self.stun_timer = max(0.0, self.stun_timer - dt)

            # ✅ anim slower during stun
            self.anim.update(dt * self.stun_anim_speed)

            self.rect.midbottom = self.pos
            return

        # hurt one-shot
        if self.anim.state == "hurt":
            self.anim.update(dt)
            if self.anim.finished:
                self.anim.play("idle")
            self.rect.midbottom = self.pos
            return

        # --- ATTACK STATE ---
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

            self.rect.midbottom = self.pos
            return

        # --- AI ---
        dx = player.rect.centerx - self.rect.centerx
        dist = abs(dx)

        if dist <= self.attack_range and self.cooldown_timer <= 0:
            self.facing_right = (dx > 0)
            self.start_attack()
            self.rect.midbottom = self.pos
            return

        # walk towards player
        if dist < 5:
            self.anim.play("idle")
            self.anim.update(dt)
        else:
            direction = 1 if dx > 0 else -1
            self.facing_right = (direction == 1)

            speed_mult = self.slow_multiplier if self.slow_timer > 0 else 1.0
            self.pos.x += self.speed * speed_mult * direction * dt

            self.anim.play("walk")
            self.anim.update(dt)

        self.rect.midbottom = self.pos

    # ------------------------------------------------------------
    # DRAW
    # ------------------------------------------------------------
    def draw(self, screen: pygame.Surface):
        img = self.anim.get_image(self.facing_right)

        if self.stun_timer > 0:
            gray = self._get_grayscale(img)

            # extra “frozen” tint (optioneel, maar zichtbaar)
            fx = gray.copy()
            fx.fill((15, 25, 45), special_flags=pygame.BLEND_RGB_ADD)

            screen.blit(fx, self.rect)
        else:
            screen.blit(img, self.rect)