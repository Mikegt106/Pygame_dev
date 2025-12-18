import pygame
from animation import SpriteSheet, Animator
from movement import Movement
from projectiles import BookProjectile


class Player:
    def __init__(self, x: int, y: int, config: dict):
        self.facing_right = True

        # input
        self.attack_key_prev = False
        self.jump_key_prev = False

        # attack (projectile timing)
        self.attack_timer = 0.0
        self.attack_delay = 0.45
        self.attack_spawned = False

        # stats
        self.hp = config.get("hp", 10)

        # damage feedback
        self.damage_timer = 0.0
        self.damage_flash_duration = 0.2

        # damage slow
        self.slow_timer = 0.0
        self.slow_duration = 0.35
        self.slow_multiplier = 0.4

        # hurt state
        self.hurt_timer = 0.0
        self.hurt_duration = 0.25

        # config
        scale = config.get("scale", 2)
        fps = config.get("fps", 12)

        # animations
        animations = {}
        for name, a in config["anims"].items():
            sheet = SpriteSheet(a["sheet"])
            frames = a["frames"]

            sheet_w = sheet.sheet.get_width()
            sheet_h = sheet.sheet.get_height()
            frame_w = sheet_w // frames
            frame_h = sheet_h

            right = sheet.slice_row(
                row=0,
                frames=frames,
                frame_w=frame_w,
                frame_h=frame_h,
                scale=scale
            )
            left = [pygame.transform.flip(f, True, False) for f in right]

            animations[name] = {
                "right": right,
                "left": left,
                "loop": a.get("loop", True)
            }

        self.anim = Animator(animations, default="idle", fps=fps)

        # position (feet-based)
        self.image = self.anim.get_image(self.facing_right)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.pos = pygame.Vector2(self.rect.midbottom)

        # movement
        self.movement = Movement(
            speed=config.get("speed", 250),
            sprint_speed=config.get("sprint_speed", 420),
        )

        # ---- JUMP / PHYSICS ----
        self.vel_y = 0.0
        self.gravity = 2600.0
        self.jump_strength = 950.0
        self.on_ground = True

        # jump anim sync (progress-based)
        self.jump_t = 0.0
        self.jump_total = (2 * self.jump_strength) / self.gravity

        # fixed ground (for now)
        self.ground_y = y

        # state
        self.dead = False
        self.dead_vel_x = 0.0  # forward drift after death

    def update(self, keys, dt: float, projectiles: list, projectile_cfg: dict):
        # ----- inputs -----
        mouse_buttons = pygame.mouse.get_pressed()
        attack_now = keys[pygame.K_RETURN] or mouse_buttons[0]
        attack_pressed = attack_now and not self.attack_key_prev
        self.attack_key_prev = attack_now

        protecting = keys[pygame.K_e]

        # --- Jump input (just pressed) ---
        jump_now = keys[pygame.K_SPACE]
        jump_pressed = jump_now and not self.jump_key_prev
        self.jump_key_prev = jump_now

        # ----- timers -----
        if self.slow_timer > 0:
            self.slow_timer = max(0.0, self.slow_timer - dt)
            speed_mult = self.slow_multiplier
        else:
            speed_mult = 1.0

        if self.damage_timer > 0:
            self.damage_timer = max(0.0, self.damage_timer - dt)

        # ---- START JUMP (only if grounded and allowed) ----
        # (Do this BEFORE physics update so jump starts instantly)
        if jump_pressed and self.on_ground and (self.anim.state != "attack") and (not protecting) and (not self.dead):
            self.vel_y = -self.jump_strength
            self.on_ground = False
            self.jump_t = 0.0
            self.jump_total = (2 * self.jump_strength) / self.gravity

        # =========================================================
        # ✅ PHYSICS ALWAYS (so hurt/dead never "hang" mid-air)
        # =========================================================
        self.vel_y += self.gravity * dt
        self.pos.y += self.vel_y * dt

        # ground collision
        if self.pos.y >= self.ground_y:
            self.pos.y = self.ground_y
            self.vel_y = 0.0
            self.on_ground = True
        else:
            self.on_ground = False

        # horizontal drift while dead
        if self.dead:
            self.pos.x += self.dead_vel_x * dt
            if self.on_ground:
                self.dead_vel_x *= 0.85  # friction on ground

        # ----- PRIORITY STATES -----

        # DEAD: play death sheet, no input/movement
        if self.dead:
            self.anim.play("dead")
            self.anim.update(dt)
            self.rect.midbottom = self.pos
            return

        # HURT: short stun, blocks input/movement BUT still falls due to physics above
        if self.hurt_timer > 0:
            self.hurt_timer = max(0.0, self.hurt_timer - dt)
            self.anim.play("hurt")
            self.anim.update(dt)
            self.rect.midbottom = self.pos
            return

        # movement is blocked during protect/attack
        can_move = (self.anim.state != "attack") and (not protecting)

        moving = False
        sprinting = False
        if can_move:
            air_mult = 1.6 if not self.on_ground else 1.0  # forward momentum in air
            moving, facing_right, sprinting = self.movement.update_horizontal(
                keys, self.pos, dt, speed_mult * air_mult
            )
            if moving:
                self.facing_right = facing_right

        # ---- JUMP ANIM SYNC (NO MID-AIR END) ----
        if (not self.on_ground) and ("jump" in self.anim.animations) and (self.anim.state != "attack") and (not protecting):
            self.jump_t += dt
            progress = 0.0 if self.jump_total <= 0 else (self.jump_t / self.jump_total)
            progress = max(0.0, min(1.0, progress))

            self.anim.play("jump")

            frames = self.anim.animations["jump"]["right"]
            n = len(frames)

            idx = int(progress * (n - 1))
            idx = max(0, min(n - 1, idx))

            self.anim.current_frame = idx
            self.anim.timer = 0.0

            self.rect.midbottom = self.pos
            return

        # ATTACK state
        if self.anim.state == "attack":
            self.anim.update(dt)
            self.attack_timer += dt

            # spawn projectile once, after delay
            if (self.attack_timer >= self.attack_delay) and (not self.attack_spawned):
                direction = 1 if self.facing_right else -1
                spawn_x = self.rect.centerx + (30 * direction)
                spawn_y = self.rect.centery + 50

                projectiles.append(
                    BookProjectile(spawn_x, spawn_y, direction, projectile_cfg["book"])
                )
                self.attack_spawned = True

            if self.anim.finished:
                self.anim.play("idle")

        else:
            if attack_pressed:
                self.anim.play("attack", reset_if_same=True)
                self.attack_timer = 0.0
                self.attack_spawned = False

            elif protecting:
                self.anim.play("protect")

            elif moving:
                if sprinting and ("run" in self.anim.animations):
                    self.anim.play("run")
                else:
                    self.anim.play("walk")
                self.anim.update(dt)

            else:
                self.anim.play("idle")
                self.anim.update(dt)

        # sync rect
        self.rect.midbottom = self.pos

    def take_damage(self, amount: int):
        if self.dead:
            return

        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

        # flash + slow + hurt stun
        self.damage_timer = self.damage_flash_duration
        self.slow_timer = self.slow_duration
        self.hurt_timer = self.hurt_duration

        if self.hp == 0:
            self.dead = True
            self.anim.play("dead", reset_if_same=True)

            # keep momentum: drift in facing direction (gravity continues in update)
            direction = 1 if self.facing_right else -1
            self.dead_vel_x = direction * 260.0  # tweak (200-450)

    def draw(self, screen: pygame.Surface):
        img = self.anim.get_image(self.facing_right)

        # damage flash
        if self.damage_timer > 0:
            flash = img.copy()
            flash.fill((255, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(flash, self.rect)
        else:
            screen.blit(img, self.rect)