import pygame
from animation import SpriteSheet, Animator

class BookProjectile:
    def __init__(self, x: float, y: float, direction: int, config: dict):
        self.direction = direction  # +1 rechts, -1 links
        self.speed = config.get("speed", 650)
        self.lifetime = config.get("lifetime", 1.5)
        self.age = 0.0

        scale = config.get("scale", 2)
        fps = config.get("fps", 16)

        sheet = SpriteSheet(config["sheet"])
        frames = config["frames"]

        sheet_w = sheet.sheet.get_width()
        sheet_h = sheet.sheet.get_height()
        frame_w = sheet_w // frames
        frame_h = sheet_h

        right = sheet.slice_row(row=0, frames=frames, frame_w=frame_w, frame_h=frame_h, scale=scale)
        left  = [pygame.transform.flip(f, True, False) for f in right]

        animations = {"fly": {"right": right, "left": left, "loop": True}}
        self.anim = Animator(animations, default="fly", fps=fps)

        self.image = self.anim.get_image(direction == 1)
        self.rect = self.image.get_rect(center=(x, y))

        self.pos = pygame.Vector2(self.rect.center)
        self.vel = pygame.Vector2(self.speed * direction, 0)

    def update(self, dt: float):
        self.age += dt
        self.pos += self.vel * dt
        self.rect.center = self.pos
        self.anim.update(dt)

    def draw(self, screen: pygame.Surface):
        img = self.anim.get_image(self.direction == 1)
        screen.blit(img, self.rect)

    def is_dead(self) -> bool:
        return self.age >= self.lifetime