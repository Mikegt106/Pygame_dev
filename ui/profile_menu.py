import pygame


class ProfileMenu:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.visible = False

        # SFX
        self.hover_sfx = pygame.mixer.Sound("assets/Sounds/hover.wav")
        self.hover_sfx.set_volume(0.5)
        self._last_hover = None

        # fonts
        self.title_font = pygame.font.SysFont(None, 72)
        self.text_font = pygame.font.SysFont(None, 36)

        # panel
        sw, sh = self.screen.get_size()
        self.panel_w = int(sw * 0.55)
        self.panel_h = int(sh * 0.55)
        self.panel = pygame.Surface((self.panel_w, self.panel_h), pygame.SRCALPHA)
        self.panel_rect = self.panel.get_rect(center=(sw // 2, sh // 2))

        # button (re-use je button assets)
        self.btn_raw = pygame.image.load("assets/Buttons/Button.png").convert_alpha()
        self.hl_raw = pygame.image.load("assets/Buttons/Highlight.png").convert_alpha()

        self.btn_w = 340
        self.btn_h = 110
        self.hl_pad_x = 18
        self.hl_pad_y = 10

        self.btn = pygame.transform.scale(self.btn_raw, (self.btn_w, self.btn_h))
        self.hl = pygame.transform.scale(
            self.hl_raw,
            (self.btn_w + self.hl_pad_x * 2, self.btn_h + self.hl_pad_y * 2),
        )

        # close button rect (onderaan in panel)
        bx = self.panel_rect.centerx - self.btn_w // 2
        by = self.panel_rect.bottom - self.btn_h - 36
        self.close_rect = pygame.Rect(bx, by, self.btn_w, self.btn_h)

    def toggle(self):
        self.visible = not self.visible
        if not self.visible:
            self._last_hover = None

    def handle_event(self, event):
        if not self.visible:
            return None

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.visible = False
            self._last_hover = None
            return "close"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.close_rect.collidepoint(event.pos):
                self.visible = False
                self._last_hover = None
                return "close"

        return None

    def draw(self, player):
        if not self.visible:
            return

        # overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        # panel bg
        self.panel.fill((0, 0, 0, 0))
        pygame.draw.rect(self.panel, (30, 30, 30, 235), self.panel.get_rect(), border_radius=18)
        pygame.draw.rect(self.panel, (255, 255, 255, 70), self.panel.get_rect(), width=2, border_radius=18)
        self.screen.blit(self.panel, self.panel_rect.topleft)

        # content
        title = self.title_font.render("PROFILE", True, (255, 255, 255))
        self.screen.blit(title, (self.panel_rect.x + 40, self.panel_rect.y + 30))

        # stats
        hp = getattr(player, "hp", 0)
        max_hp = getattr(player, "max_hp", hp)
        coins = getattr(player, "coins", 0)

        lines = [
            f"HP: {hp} / {max_hp}",
            f"COINS: {coins}",
        ]

        # (optioneel) kills als je die ooit toevoegt
        if hasattr(player, "kills"):
            lines.append(f"KILLS: {getattr(player, 'kills', 0)}")

        y = self.panel_rect.y + 140
        for ln in lines:
            t = self.text_font.render(ln, True, (230, 230, 230))
            self.screen.blit(t, (self.panel_rect.x + 50, y))
            y += 48

        # hover detect + sound
        mx, my = pygame.mouse.get_pos()
        hovered = 0 if self.close_rect.collidepoint((mx, my)) else None

        if hovered is not None and hovered != self._last_hover:
            self.hover_sfx.play()
        self._last_hover = hovered

        # button
        if hovered == 0:
            self.screen.blit(self.hl, (self.close_rect.x - self.hl_pad_x, self.close_rect.y - self.hl_pad_y))
        self.screen.blit(self.btn, self.close_rect.topleft)

        txt = self.text_font.render("CLOSE", True, (25, 25, 25))
        tr = txt.get_rect(center=self.close_rect.center)
        self.screen.blit(txt, tr)