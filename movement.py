import pygame

class Movement:
    def __init__(self, speed: float = 250, sprint_speed: float = 420):
        self.speed = speed
        self.sprint_speed = sprint_speed

    def update_horizontal(self, keys, pos, dt, speed_mult=1.0):
        moving = False
        facing_right = True

        sprinting = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        base_speed = self.sprint_speed if sprinting else self.speed
        current_speed = base_speed * speed_mult

        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            pos.x -= current_speed * dt
            moving = True
            facing_right = False

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            pos.x += current_speed * dt
            moving = True
            facing_right = True

        return moving, facing_right, sprinting