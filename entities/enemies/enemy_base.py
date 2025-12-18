# entities/enemies/enemy_base.py
import pygame
from animation import SpriteSheet, Animator


class EnemyBase:
    """
    Basisklasse voor alle enemies.
    Subclasses implementeren alleen: update_alive(dt, player)
    """

    def __init__(self, x: int, y: int, config: dict):
        self.cfg = config

        self.facing_right = False
        self.speed = float(config.get("speed", 120))
        self.hp = int(config.get("hp", 5))
        self.alpha = 255

        # life state
        self.dead = False
        self.remove = False

        # death timing
        self.death_linger = float(config.get("death_linger", 1.2))
        self.death_timer = 0.0

        # optional stun (parry etc)
        self.stun_timer = 0.0

        # animations
        scale = int(config.get("scale", 2))
        fps = int(config.get("fps", 10))

        animations = {}
        for name, a in config["anims"].items():
            sheet = SpriteSheet(a["sheet"])
            frames = a["frames"]
            fw = sheet.sheet.get_width() // frames
            fh = sheet.sheet.get_height()

            right = sheet.slice_row(0, frames, fw, fh, scale)
            left = [pygame.transform.flip(f, True, False) for f in right]
            animations[name] = {
                "right": right,
                "left": left,
                "loop": a.get("loop", True),
            }

        self.anim = Animator(animations, default="idle", fps=fps)

        # position
        self.image = self.anim.get_image(self.facing_right)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.pos = pygame.Vector2(self.rect.midbottom)

    # -------------------------
    # COMMON HELPERS
    # -------------------------
    def stun(self, duration: float = 0.6):
        """Stop beweging/attack tijdelijk."""
        self.stun_timer = max(self.stun_timer, float(duration))
        if "stun" in self.anim.animations:
            self.anim.play("stun", reset_if_same=True)
        elif "hurt" in self.anim.animations:
            self.anim.play("hurt", reset_if_same=True)

    def take_damage(self, amount: int):
        if self.dead:
            return

        self.hp -= int(amount)
        if self.hp <= 0:
            self.hp = 0
            self.dead = True
            self.death_timer = self.death_linger
            if "dead" in self.anim.animations:
                self.anim.play("dead", reset_if_same=True)
            return

        if "hurt" in self.anim.animations:
            self.anim.play("hurt", reset_if_same=True)

    # -------------------------
    # UPDATE
    # -------------------------
    def update(self, dt: float, player):
        # death
        if self.dead:
            self.anim.update(dt)

            self.death_timer = max(0.0, self.death_timer - dt)

            # ✅ fade alpha van 255 -> 0 over death_linger
            if self.death_linger > 0:
                self.alpha = int(255 * (self.death_timer / self.death_linger))
            else:
                self.alpha = 0

            if self.death_timer <= 0.0:
                self.remove = True

            self.rect.midbottom = self.pos
            return

        # stun
        if self.stun_timer > 0:
            self.stun_timer = max(0.0, self.stun_timer - dt)
            self.anim.update(dt)
            self.rect.midbottom = self.pos
            return

        # alive behaviour
        self.update_alive(dt, player)
        self.rect.midbottom = self.pos

    def update_alive(self, dt: float, player):
        """Subclasses override."""
        self.anim.play("idle")
        self.anim.update(dt)

    # -------------------------
    # DRAW
    # -------------------------
    def draw(self, screen: pygame.Surface):
        img = self.anim.get_image(self.facing_right)

        # ✅ apply fade when dead
        if self.dead and self.alpha < 255:
            img = img.copy()
            img.set_alpha(self.alpha)

        screen.blit(img, self.rect)