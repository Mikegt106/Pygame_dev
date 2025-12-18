# movement.py
import pygame

class Movement:
    def __init__(self, speed=250, sprint_speed=420):
        self.speed = speed
        self.sprint_speed = sprint_speed

    def update_horizontal(self, keys, pos, dt, speed_mult=1.0, sprinting=False):
        left  = keys[pygame.K_q]
        right = keys[pygame.K_d]

        direction = 0
        if left and not right:
            direction = -1
        elif right and not left:
            direction = 1

        moving = direction != 0
        facing_right = True if direction >= 0 else False

        speed = (self.sprint_speed if sprinting else self.speed) * speed_mult

        if moving:
            pos.x += direction * speed * dt

        return moving, facing_right, sprinting