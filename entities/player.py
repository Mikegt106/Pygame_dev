# entities/player.py
import pygame
from animation import SpriteSheet, Animator
from movement import Movement
from projectiles import BookProjectile

from entities.player_block import BlockSystem, BlockResult
from entities.player_mana import ManaSystem


class Player:
    def __init__(self, x: int, y: int, config: dict):
        self.facing_right = True
        self.coins = 0
        self.inventory = {} 

        # input
        self.attack_key_prev = False
        self.jump_key_prev = False

        # attack timing
        self.attack_timer = 0.0
        self.attack_delay = 0.45
        self.attack_spawned = False

        # stats
        self.max_hp = config.get("hp", 10)
        self.hp = self.max_hp

        # systems
        self.block = BlockSystem(
            block_chance=0.80,
            fail_stun=0.40,
            cooldown=1.0,
            shield_scale=0.1,
            pushback_force=300.0,
        )
        self.mana_sys = ManaSystem(
            max_mana=config.get("mana", 50),
            drain_run=6.0,
            regen=2.0,
        )

        # feedback timers
        self.damage_timer = 0.0
        self.damage_flash_duration = 0.2

        self.slow_timer = 0.0
        self.slow_duration = 0.35
        self.slow_multiplier = 0.4

        self.hurt_timer = 0.0
        self.hurt_duration = 0.25

        # pushback physics
        self.block_push_vel = 0.0
        self.block_push_damping = 1200.0

        # animations
        scale = config.get("scale", 2)
        fps = config.get("fps", 12)

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

        # ✅ jump anim lock (speel jump volledig uit)
        self.jump_anim_lock = False

        # position
        self.image = self.anim.get_image(self.facing_right)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.pos = pygame.Vector2(self.rect.midbottom)

        # movement
        self.movement = Movement(
            speed=config.get("speed", 250),
            sprint_speed=config.get("sprint_speed", 420),
        )

        # physics
        self.vel_y = 0.0
        self.gravity = 2600.0
        self.jump_strength = 950.0

        self.on_ground = True
        self.ground_y = y

        self.dead = False
        self.dead_vel_x = 0.0

    # mana passthroughs
    @property
    def mana(self):
        return self.mana_sys.mana

    @property
    def max_mana(self):
        return self.mana_sys.max_mana

    @property
    def mana_exhausted(self):
        return self.mana_sys.exhausted

    @property
    def mana_draining(self):
        return self.mana_sys.draining

    @property
    def mana_regening(self):
        return self.mana_sys.regening

    def update(self, keys, dt, projectiles, PROJECTILES, ui_block_input=False):
        # ----------------------
        # TIMERS
        # ----------------------
        speed_mult = 1.0
        if self.slow_timer > 0:
            self.slow_timer = max(0.0, self.slow_timer - dt)
            speed_mult = self.slow_multiplier

        if self.damage_timer > 0:
            self.damage_timer = max(0.0, self.damage_timer - dt)

        if self.hurt_timer > 0:
            self.hurt_timer = max(0.0, self.hurt_timer - dt)

        # ----------------------
        # READ INPUTS ONCE
        # ----------------------
        mouse_buttons = pygame.mouse.get_pressed()

        # ---- BLOCK INPUT ----
        block_now = (mouse_buttons[2] or keys[pygame.K_e]) and (not ui_block_input)
        
        if hasattr(self.block, "set_blocking"):
            self.block.set_blocking(block_now)
        else:
            self.block.blocking = block_now
            
        # BlockSystem per frame updaten 
        if hasattr(self.block, "update"):
            self.block.update(dt, block_now)

        # ---- ATTACK INPUT ----
        attack_now = (keys[pygame.K_RETURN] or (mouse_buttons[0] and not ui_block_input))
        attack_pressed = attack_now and not self.attack_key_prev
        self.attack_key_prev = attack_now

        # ----------------------
        # JUMP INPUT
        # ----------------------
        jump_now = keys[pygame.K_SPACE]
        jump_pressed = jump_now and not self.jump_key_prev
        self.jump_key_prev = jump_now

        can_start_jump = (
            jump_pressed
            and self.on_ground
            and (self.anim.state != "attack")
            and (not self.block.blocking)
            and (self.hurt_timer <= 0)
            and (not self.dead)
        )

        if can_start_jump:
            self.vel_y = -self.jump_strength
            self.on_ground = False
            if "jump" in self.anim.animations:
                self.jump_anim_lock = True
                self.anim.play("jump", reset_if_same=True)

        # ======================
        # PHYSICS ALWAYS
        # ======================
        self.vel_y += self.gravity * dt
        self.pos.y += self.vel_y * dt

        if self.pos.y >= self.ground_y:
            self.pos.y = self.ground_y
            self.vel_y = 0.0
            self.on_ground = True
        else:
            self.on_ground = False

        # pushback
        if self.block_push_vel != 0.0:
            self.pos.x += self.block_push_vel * dt
            if self.block_push_vel > 0:
                self.block_push_vel = max(0.0, self.block_push_vel - self.block_push_damping * dt)
            else:
                self.block_push_vel = min(0.0, self.block_push_vel + self.block_push_damping * dt)

        # ----------------------
        # PRIORITY STATES
        # ----------------------
        if self.dead:
            # force release block zodat shield niet kan blijven hangen
            if hasattr(self.block, "set_blocking"):
                self.block.set_blocking(False)
            else:
                self.block.blocking = False
            if hasattr(self.block, "update"):
                self.block.update(dt, block_now)

            self.jump_anim_lock = False
            self.anim.play("dead")
            self.anim.update(dt)
            self.rect.midbottom = self.pos
            return

        if self.hurt_timer > 0:
            # force release block zodat shield niet kan blijven hangen
            if hasattr(self.block, "set_blocking"):
                self.block.set_blocking(False)
            else:
                self.block.blocking = False
            if hasattr(self.block, "update"):
                self.block.update(dt, block_now)

            self.jump_anim_lock = False
            self.anim.play("hurt")
            self.anim.update(dt)
            self.rect.midbottom = self.pos
            return

        # ----------------------
        # MOVEMENT
        # ----------------------
        protecting = self.block.blocking
        can_move = (self.anim.state != "attack") and (not protecting)

        moving = False
        sprinting = False

        if can_move:
            air_mult = 1.6 if not self.on_ground else 1.0
            want_sprint = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
            sprinting = want_sprint and (not self.mana_sys.exhausted) and (self.mana_sys.mana > 0)

            moving, facing_right, sprinting = self.movement.update_horizontal(
                keys, self.pos, dt, speed_mult * air_mult, sprinting=sprinting
            )
            if moving:
                self.facing_right = facing_right

            self.mana_sys.update(dt, sprinting=sprinting, moving=moving)
        else:
            self.mana_sys.update(dt, sprinting=False, moving=False)

        # ======================
        # ANIMATION STATE MACHINE
        # ======================
        if self.anim.state == "attack":
            self.anim.update(dt)
            self.attack_timer += dt

            if (self.attack_timer >= self.attack_delay) and (not self.attack_spawned):
                direction = 1 if self.facing_right else -1
                spawn_x = self.rect.centerx + (30 * direction)
                spawn_y = self.rect.centery + 50
                projectiles.append(BookProjectile(spawn_x, spawn_y, direction, PROJECTILES["book"]))
                self.attack_spawned = True

            if self.anim.finished:
                self.anim.play("idle")

        else:
            if attack_pressed and (not protecting):
                self.anim.play("attack", reset_if_same=True)
                self.attack_timer = 0.0
                self.attack_spawned = False

            elif protecting:
                self.anim.play("protect")
                self.anim.update(dt)

            elif self.jump_anim_lock and ("jump" in self.anim.animations):
                self.anim.play("jump")  # niet resetten
                self.anim.update(dt)

                if self.anim.finished and self.on_ground:
                    self.jump_anim_lock = False

            elif not self.on_ground:
                if "jump" in self.anim.animations:
                    self.anim.play("jump")
                else:
                    self.anim.play("idle")
                self.anim.update(dt)

            elif moving:
                if sprinting and ("run" in self.anim.animations):
                    self.anim.play("run")
                else:
                    self.anim.play("walk")
                self.anim.update(dt)

            else:
                self.anim.play("idle")
                self.anim.update(dt)

        self.rect.midbottom = self.pos

    def take_damage(self, amount: int) -> bool:
        """Return True als hit succesvol geblokt werd."""
        if self.dead:
            return False

        result = self.block.try_block()

        if result == BlockResult.SUCCESS:
            direction = 1 if self.facing_right else -1
            self.block_push_vel = -direction * self.block.pushback_force
            return True

        if result == BlockResult.FAIL:
            self.hurt_timer = max(self.hurt_timer, self.block.fail_stun)

        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

        self.damage_timer = self.damage_flash_duration
        self.slow_timer = self.slow_duration
        self.hurt_timer = max(self.hurt_timer, self.hurt_duration)

        if self.hp == 0:
            self.dead = True
            self.anim.play("dead", reset_if_same=True)

        return False
    
    def add_item(self, item_id: str, amount: int = 1) -> bool:
        if not hasattr(self, "inventory") or self.inventory is None:
            self.inventory = {}

        self.inventory[item_id] = self.inventory.get(item_id, 0) + int(amount)
        return True

    def use_item(self, item_id: str, config):
        if not hasattr(self, "inventory"):
            return False
        if self.inventory.get(item_id, 0) <= 0:
            return False

        item = config.ITEMS.get(item_id)
        if not item:
            return False

        # apply effect
        heal = int(item.get("heal", 0))
        if heal > 0:
            self.hp = min(self.max_hp, self.hp + heal)

        # consume
        self.inventory[item_id] -= 1
        if self.inventory[item_id] <= 0:
            del self.inventory[item_id]

        return True

    def draw(self, screen: pygame.Surface):
        img = self.anim.get_image(self.facing_right)

        if self.damage_timer > 0:
            flash = img.copy()
            flash.fill((255, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(flash, self.rect)
        else:
            screen.blit(img, self.rect)

        self.block.draw_shield(screen, self.rect, self.facing_right)