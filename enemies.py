import pygame
from animation import SpriteSheet, Animator


class Zombie:
    def __init__(self, x: int, y: int, config: dict):
        self.facing_right = False
        self.speed = config.get("speed", 120)
        self.hp = config.get("hp", 5)

        # life state
        self.dead = False
        self.remove = False

        # death timing
        self.death_linger = 1.2
        self.death_timer = 0.0

        # attack
        self.attack_damage = config.get("attack_damage", 1)
        self.attack_range = config.get("attack_range", 90)
        self.attack_cooldown = config.get("attack_cooldown", 1.0)
        self.attack_hit_time = config.get("attack_hit_time", 0.25)

        self.cooldown_timer = 0.0
        self.attack_timer = 0.0
        self.attack_hit_done = False

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

        self.image = self.anim.get_image(self.facing_right)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.pos = pygame.Vector2(self.rect.midbottom)

    # -------------------------------------------------

    def take_damage(self, amount: int):
        if self.dead:
            return

        self.hp -= amount
        if self.hp <= 0:
            self.dead = True
            self.death_timer = self.death_linger
            self.anim.play("dead", reset_if_same=True)
            return

        if "hurt" in self.anim.animations:
            self.anim.play("hurt", reset_if_same=True)

    # -------------------------------------------------

    def start_attack(self):
        self.anim.play("attack", reset_if_same=True)
        self.attack_timer = 0.0
        self.attack_hit_done = False
        self.cooldown_timer = self.attack_cooldown

    # -------------------------------------------------

    def update(self, dt: float, player):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt

        # DEAD STATE
        if self.dead:
            self.anim.update(dt)
            self.death_timer -= dt
            if self.death_timer <= 0:
                self.remove = True
            self.rect.midbottom = self.pos
            return

        # ATTACK
        if self.anim.state == "attack":
            self.anim.update(dt)
            self.attack_timer += dt

            if (not self.attack_hit_done) and self.attack_timer >= self.attack_hit_time:
                if abs(player.rect.centerx - self.rect.centerx) <= self.attack_range:
                    player.take_damage(self.attack_damage)
                self.attack_hit_done = True

            if self.anim.finished:
                self.anim.play("idle")

            self.rect.midbottom = self.pos
            return

        # AI
        dx = player.rect.centerx - self.rect.centerx
        dist = abs(dx)

        if dist <= self.attack_range and self.cooldown_timer <= 0:
            self.facing_right = dx > 0
            self.start_attack()
            self.rect.midbottom = self.pos
            return

        if dist > 5:
            direction = 1 if dx > 0 else -1
            self.facing_right = direction == 1
            self.pos.x += self.speed * direction * dt
            self.anim.play("walk")
            self.anim.update(dt)
        else:
            self.anim.play("idle")
            self.anim.update(dt)

        self.rect.midbottom = self.pos

    # -------------------------------------------------

    def draw(self, screen: pygame.Surface):
        img = self.anim.get_image(self.facing_right)
        screen.blit(img, self.rect)