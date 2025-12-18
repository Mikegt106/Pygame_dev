import pygame
from animation import SpriteSheet, Animator
from movement import Movement
from projectiles import BookProjectile

class Player:
    def __init__(self, x: int, y: int, config: dict):
        self.facing_right = True
        self.attack_key_prev = False
        self.attack_timer = 0.0
        self.attack_delay = 0.45
        self.attack_spawned = False
        self.hp = config.get("hp", 10)
        
        # damage feedback
        self.damage_timer = 0.0
        self.damage_flash_duration = 0.2  # seconden
        
        # damage slow
        self.slow_timer = 0.0
        self.slow_duration = 0.35   # seconden
        self.slow_multiplier = 0.4  # 40% speed

        scale = config.get("scale", 2)
        fps = config.get("fps", 12)

        animations = {}
        for name, a in config["anims"].items():
            sheet = SpriteSheet(a["sheet"])
            frames = a["frames"]

            sheet_w = sheet.sheet.get_width()
            sheet_h = sheet.sheet.get_height()
            frame_w = sheet_w // frames
            frame_h = sheet_h

            right = sheet.slice_row(row=0, frames=frames, frame_w=frame_w, frame_h=frame_h, scale=scale)
            left  = [pygame.transform.flip(f, True, False) for f in right]

            animations[name] = {"right": right, "left": left, "loop": a.get("loop", True)}

        self.anim = Animator(animations, default="idle", fps=fps)

        self.image = self.anim.get_image(self.facing_right)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.pos = pygame.Vector2(self.rect.midbottom)
        
        # death VFX
        self.dead = False
        self.death_image = None          # frozen frame
        self.death_pos = pygame.Vector2(self.rect.center)
        self.death_vel = pygame.Vector2(0, 0)
        self.death_alpha = 255
        self.death_gravity = 1400        # tweak
        self.death_fade_speed = 220      # alpha per sec
        self.death_landed = False
        self.death_ground_y = self.rect.midbottom[1]   # grondlijn (jouw y=680)
        self.death_rot_dir = 1
        self.death_rotation = 0.0

        self.movement = Movement(
            speed=config.get("speed", 250),
            sprint_speed=config.get("sprint_speed", 420),
        )

    def update(self, keys, dt: float, projectiles: list, projectile_cfg: dict):
        mouse_buttons = pygame.mouse.get_pressed()
        attack_now = keys[pygame.K_RETURN] or mouse_buttons[0] 
        attack_pressed = attack_now and not self.attack_key_prev
        self.attack_key_prev = attack_now

        protecting = keys[pygame.K_e]

        # death: knockback → land → fade
        if self.dead:
            if not self.death_landed:
                self.death_vel.y += self.death_gravity * dt
                self.death_pos += self.death_vel * dt

                # rotate tijdens val naar 90°
                self.death_rotation += self.death_rot_dir * 420 * dt
                if self.death_rot_dir == 1:
                    if self.death_rotation > 90:
                        self.death_rotation = 90
                else:
                    if self.death_rotation < -90:
                        self.death_rotation = -90

                # landing op grond
                if self.death_pos.y >= self.death_ground_y:
                    self.death_pos.y = self.death_ground_y
                    self.death_landed = True
                    self.death_vel = pygame.Vector2(0, 0)

            else:
                self.death_alpha -= self.death_fade_speed * dt
                if self.death_alpha < 0:
                    self.death_alpha = 0

            return
        
        # update slow timer
        if self.slow_timer > 0:
            self.slow_timer = max(0, self.slow_timer - dt)
            speed_mult = self.slow_multiplier
        else:
            speed_mult = 1.0
            
        # movement blokken tijdens protect/attack
        can_move = (self.anim.state != "attack") and (not protecting)

        moving = False
        if can_move:
            moving, facing_right, sprinting = self.movement.update_horizontal(
                keys, self.pos, dt, speed_mult
            )
            if moving:
                self.facing_right = facing_right

        if self.anim.state == "attack":
            # attack anim loopt altijd door
            self.anim.update(dt)

            # timer telt op
            self.attack_timer += dt

            # spawn pas na delay (1x)
            if (self.attack_timer >= self.attack_delay) and (not self.attack_spawned):
                direction = 1 if self.facing_right else -1
                spawn_x = self.rect.centerx + (30 * direction)
                spawn_y = self.rect.centery + 50  # pas dit aan naar je handhoogte

                projectiles.append(
                    BookProjectile(spawn_x, spawn_y, direction, projectile_cfg["book"])
                )

                self.attack_spawned = True

            # als attack klaar is
            if self.anim.finished:
                self.anim.play("idle")

        else:
            if attack_pressed:
                self.anim.play("attack", reset_if_same=True)

                # reset delay-state
                self.attack_timer = 0.0
                self.attack_spawned = False

            elif protecting:
                self.anim.play("protect")

            elif moving:
                self.anim.play("walk")
                self.anim.update(dt)

            else:
                self.anim.play("idle")
                self.anim.update(dt)

        self.rect.midbottom = self.pos
        
        # Damage flikkering
        if self.damage_timer > 0:
            self.damage_timer -= dt
            
    def take_damage(self, amount: int):
        if self.dead:
            return

        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

        # hit flash
        self.damage_timer = self.damage_flash_duration
        # start movement slow
        self.slow_timer = self.slow_duration

        if self.hp == 0:
            self.dead = True

            # freeze current frame + make grayscale
            frame = self.anim.get_image(self.facing_right)
            self.death_image = self._to_grayscale(frame)

            # start physics from current center
            self.death_pos = pygame.Vector2(self.rect.center)

            # knockback backwards
            direction = 1 if self.facing_right else -1
            self.death_vel = pygame.Vector2(-direction * 520, -220)
            
            # rotate opposite of movement direction (backwards)
            # als je naar links vliegt (death_vel.x < 0) -> rotate +90
            # als je naar rechts vliegt (death_vel.x > 0) -> rotate -90
            self.death_rot_dir = -1 if self.death_vel.x > 0 else 1

            self.death_alpha = 255
            self.death_landed = False
            self.death_rotation = 0.0
            self.death_ground_y = self.rect.midbottom[1]
        
    def _to_grayscale(self, surf: pygame.Surface) -> pygame.Surface:
        gray = surf.copy()
        arr = pygame.surfarray.pixels3d(gray)
        r = arr[:, :, 0].astype("float32")
        g = arr[:, :, 1].astype("float32")
        b = arr[:, :, 2].astype("float32")
        lum = (0.299 * r + 0.587 * g + 0.114 * b).astype(arr.dtype)
        arr[:, :, 0] = lum
        arr[:, :, 1] = lum
        arr[:, :, 2] = lum
        del arr
        return gray

    def draw(self, screen: pygame.Surface):
        # death draw
        if self.dead and self.death_image is not None:
            img = self.death_image.copy()
            img.set_alpha(int(self.death_alpha))

            # kleine rotatie ziet er “knockback” uit (optioneel)
            img = pygame.transform.rotate(img, self.death_rotation)

            r = img.get_rect(center=(int(self.death_pos.x), int(self.death_pos.y)))
            screen.blit(img, r)
            return

        # normal draw
        img = self.anim.get_image(self.facing_right)

        # damage flash (als je dat al hebt)
        if getattr(self, "damage_timer", 0) > 0:
            flash = img.copy()
            flash.fill((255, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(flash, self.rect)
        else:
            screen.blit(img, self.rect)