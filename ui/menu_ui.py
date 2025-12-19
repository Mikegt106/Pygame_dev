# ui/menu_ui.py
import pygame

# ---------- HOVER SOUND ----------
HOVER_SOUND = pygame.mixer.Sound("assets/Sounds/hover.wav")
HOVER_SOUND.set_volume(0.5)

class MenuUI:
    def __init__(self, screen: pygame.Surface, scale: float = 1.6, margin: int = 24, spacing: int = 10):
        self.screen = screen
        self.scale = float(scale)
        self.margin = int(margin)
        self.spacing = int(spacing * self.scale)

        # hover state
        self.hover_index = None
        self._last_hover = None

        # -------------------------
        # load + scale assets
        # -------------------------
        box_raw = pygame.image.load("assets/MenuUI/MenuBox.png").convert_alpha()
        icon_paths = [
            "assets/MenuUI/Backpack.png",
            "assets/MenuUI/Profile.png",
            "assets/MenuUI/Settings.png",
        ]

        self.box = pygame.transform.scale(
            box_raw,
            (int(box_raw.get_width() * self.scale), int(box_raw.get_height() * self.scale))
        )

        # hover variant (iets lichter)
        self.box_hover = self.box.copy()
        self.box_hover.fill((35, 35, 35), special_flags=pygame.BLEND_RGB_ADD)

        # icons + (optioneel) hover icons iets groter
        self.icons = []
        self.icons_hover = []

        for p in icon_paths:
            img = pygame.image.load(p).convert_alpha()

            normal = pygame.transform.scale(
                img,
                (int(img.get_width() * self.scale), int(img.get_height() * self.scale))
            )
            self.icons.append(normal)

            # hover icon net iets groter (subtiel)
            hover = pygame.transform.scale(
                img,
                (int(img.get_width() * self.scale * 1.08), int(img.get_height() * self.scale * 1.08))
            )
            self.icons_hover.append(hover)

        self.box_w = self.box.get_width()
        self.box_h = self.box.get_height()

        # -------------------------
        # position: top-right
        # -------------------------
        screen_w = self.screen.get_width()
        total_w = (3 * self.box_w) + (2 * self.spacing)

        self.x = screen_w - total_w - self.margin
        self.y = self.margin

        # clickable rects
        self.rects = []
        for i in range(3):
            bx = self.x + i * (self.box_w + self.spacing)
            by = self.y
            self.rects.append(pygame.Rect(bx, by, self.box_w, self.box_h))

    # -------------------------
    def update(self):
        mx, my = pygame.mouse.get_pos()

        new_hover = None
        for i, r in enumerate(self.rects):
            if r.collidepoint((mx, my)):
                new_hover = i
                break

        # 🔊 play sound only when hover ENTERS a new button
        if new_hover is not None and new_hover != self._last_hover:
            HOVER_SOUND.play()

        self.hover_index = new_hover
        self._last_hover = new_hover

    # -------------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, r in enumerate(self.rects):
                if r.collidepoint(event.pos):
                    return True, i   # UI gebruikte de click
        return False, None

    # -------------------------
    def draw(self):
        for i in range(3):
            r = self.rects[i]

            # box (hover highlight)
            box_img = self.box_hover if self.hover_index == i else self.box
            self.screen.blit(box_img, r.topleft)

            # icon (hover grootte)
            icon = self.icons_hover[i] if self.hover_index == i else self.icons[i]

            ix = r.x + (r.width - icon.get_width()) // 2
            iy = r.y + (r.height - icon.get_height()) // 2
            self.screen.blit(icon, (ix, iy))

            if self.hover_index == i:
                pygame.draw.rect(self.screen, (255, 255, 255), r, 2, border_radius=8)