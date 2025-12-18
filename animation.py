import pygame
from assets import load_image

class SpriteSheet:
    def __init__(self, path: str):
        self.sheet = load_image(path, alpha=True)

    def slice_row(self, row: int, frames: int, frame_w: int, frame_h: int, scale: int = 1):
        out = []
        y = row * frame_h
        for i in range(frames):
            rect = pygame.Rect(i * frame_w, y, frame_w, frame_h)
            frame = self.sheet.subsurface(rect)
            if scale != 1:
                frame = pygame.transform.scale(frame, (frame_w * scale, frame_h * scale))
            out.append(frame)
        return out

class Animator:
    def __init__(self, animations: dict, default: str, fps: int):
        self.animations = animations
        self.state = default
        self.fps = fps
        self.current_frame = 0
        self.timer = 0.0
        self.finished = False

    def play(self, name: str, reset_if_same: bool = False):
        if name != self.state or reset_if_same:
            self.state = name
            self.current_frame = 0
            self.timer = 0.0
            self.finished = False

    def update(self, dt: float):
        if self.finished:
            return

        anim = self.animations[self.state]
        frames = anim["right"]
        loop = anim.get("loop", True)

        self.timer += dt
        step = 1.0 / self.fps

        while self.timer >= step:
            self.timer -= step
            self.current_frame += 1

            if self.current_frame >= len(frames):
                if loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(frames) - 1
                    self.finished = True

    def get_image(self, facing_right: bool) -> pygame.Surface:
        anim = self.animations[self.state]
        frames = anim["right"] if facing_right else anim["left"]
        return frames[self.current_frame]