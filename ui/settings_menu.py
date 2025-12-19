import pygame


class SettingsMenu:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.visible = False

        # =========================
        # TWEAKS
        # =========================
        self.font_size = 35
        self.padding_x = 60
        self.padding_y = 28
        self.gap = 26
        self.menu_offset = (0, 0)

        # highlight groter dan button
        self.hl_pad_x = 20
        self.hl_pad_y = 12

        # =========================
        # SFX
        # =========================
        self.hover_sfx = pygame.mixer.Sound("assets/Sounds/hover.wav")
        self.hover_sfx.set_volume(0.5)
        self._last_hover = None  # <--- belangrijk

        # =========================
        # LOAD RAW ASSETS
        # =========================
        self.btn_raw = pygame.image.load("assets/Buttons/Button.png").convert_alpha()
        self.hl_raw = pygame.image.load("assets/Buttons/Highlight.png").convert_alpha()

        self.font = pygame.font.SysFont(None, self.font_size)

        # =========================
        # MENU ITEMS
        # =========================
        labels = [
            ("START MENU", "menu"),
            ("RESTART", "restart"),
            ("RESUME", "resume"),
        ]

        # 1) grootste tekst meten
        max_text_w = 0
        max_text_h = 0
        for label, _ in labels:
            surf = self.font.render(label, True, (0, 0, 0))
            max_text_w = max(max_text_w, surf.get_width())
            max_text_h = max(max_text_h, surf.get_height())

        # 2) button size = tekst + padding
        self.btn_w = max_text_w + self.padding_x * 2
        self.btn_h = max_text_h + self.padding_y * 2

        # 3) schaal button en highlight (highlight = groter)
        self.btn = pygame.transform.scale(self.btn_raw, (self.btn_w, self.btn_h))
        self.hl = pygame.transform.scale(
            self.hl_raw,
            (self.btn_w + self.hl_pad_x * 2, self.btn_h + self.hl_pad_y * 2)
        )

        # =========================
        # POSITIONERING
        # =========================
        sw, sh = self.screen.get_size()
        total_h = len(labels) * self.btn_h + (len(labels) - 1) * self.gap

        start_x = sw // 2 - self.btn_w // 2 + self.menu_offset[0]
        start_y = sh // 2 - total_h // 2 + self.menu_offset[1]

        self.items = []
        for i, (label, action) in enumerate(labels):
            rect = pygame.Rect(
                start_x,
                start_y + i * (self.btn_h + self.gap),
                self.btn_w,
                self.btn_h
            )
            self.items.append({"label": label, "action": action, "rect": rect})

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
            return "resume"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for it in self.items:
                if it["rect"].collidepoint((mx, my)):
                    return it["action"]

        return None

    def draw(self):
        if not self.visible:
            return

        # dark overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        mx, my = pygame.mouse.get_pos()

        # -------- hover detect + sound (hover-enter) --------
        hovered = None
        for idx, it in enumerate(self.items):
            if it["rect"].collidepoint((mx, my)):
                hovered = idx
                break

        if hovered is not None and hovered != self._last_hover:
            self.hover_sfx.play()

        self._last_hover = hovered
        # ----------------------------------------------------

        for idx, it in enumerate(self.items):
            r = it["rect"]

            # highlight onder button (groter + offset)
            if idx == hovered:
                self.screen.blit(self.hl, (r.x - self.hl_pad_x, r.y - self.hl_pad_y))

            # button bovenop
            self.screen.blit(self.btn, r.topleft)

            # tekst
            txt = self.font.render(it["label"], True, (25, 25, 25))
            tr = txt.get_rect(center=r.center)
            self.screen.blit(txt, tr)