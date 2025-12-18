import pygame
from animation import SpriteSheet, Animator


class EnemyBase:
    """
    Universele basis voor enemies:
    - anim loading uit config["anims"]
    - hp/dead/remove
    - death linger + fade-out
    - rect/pos handling
    """

    def __init__(self, x: int, y: int, config: dict):
        self.cfg = config

        # facing & stats
        self.facing_right = False
        self.speed = config.get("speed", 120)
        self.max_hp = config.get("hp", 5)
        self.hp = self.max_hp

        # life state
        self.dead = False
        self.remove = False

        # death linger + fade
        self.death_linger = float(config.get("death_linger", 1.2))
        self.death_timer = 0.0
        self.fade_time = float(config.get("death_fade_time", 0.6))
        self.alpha = 255

        # animations
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

        # position
        self.image = self.anim.get_image(self.facing_right)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.pos = pygame.Vector2(self.rect.midbottom)

    # -------------------------
    # DAMAGE / DEATH
    # -------------------------
    def take_damage(self, amount: int):
        if self.dead:
            return

        self.hp -= int(amount)
        if self.hp <= 0:
            self.hp = 0
            self.die()
            return

        if "hurt" in self.anim.animations:
            self.anim.play("hurt", reset_if_same=True)

    def die(self):
        if self.dead:
            return
        self.dead = True
        self.death_timer = self.death_linger
        if "dead" in self.anim.animations:
            self.anim.play("dead", reset_if_same=True)

    # -------------------------
    # UPDATE
    # -------------------------
    def update(self, dt: float, player):
        # base death handling
        if self.dead:
            self.anim.update(dt)

            self.death_timer -= dt
            if self.death_timer <= 0:
                # start fade-out
                if self.fade_time <= 0:
                    self.remove = True
                else:
                    self.alpha -= int(255 * (dt / self.fade_time))
                    if self.alpha <= 0:
                        self.alpha = 0
                        self.remove = True

            self.rect.midbottom = self.pos
            return

        # subclass should implement alive behavior
        self.update_alive(dt, player)
        self.rect.midbottom = self.pos

    def update_alive(self, dt: float, player):
        """Override in subclass."""
        self.anim.update(dt)

    # -------------------------
    # DRAW
    # -------------------------
    def draw(self, screen: pygame.Surface):
        img = self.anim.get_image(self.facing_right)

        # fade when dead
        if self.dead and self.alpha < 255:
            img = img.copy()
            img.set_alpha(self.alpha)

        screen.blit(img, self.rect)