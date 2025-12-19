# ui/inventory_ui.py
import pygame


class InventoryUI:
    def __init__(
        self,
        screen: pygame.Surface,
        slots: int = 6,
        scale: float = 1.7,        
        bottom_margin: int = 20,
        spacing: int = 6,
        slide_speed: float = 16.0,
    ):
        self.screen = screen
        self.slots = slots
        self.scale = scale
        self.bottom_margin = bottom_margin
        self.spacing = int(spacing * scale)
        self.slide_speed = slide_speed

        self.visible = False

        # ---------- LOAD ASSETS ----------
        self.box = pygame.image.load("assets/Inventory/HotkeyBox.png").convert_alpha()
        self.label = pygame.image.load("assets/Inventory/Hover_label.png").convert_alpha()

        self.box = pygame.transform.scale(
            self.box,
            (int(self.box.get_width() * scale), int(self.box.get_height() * scale)),
        )
        self.label = pygame.transform.scale(
            self.label,
            (int(self.label.get_width() * scale), int(self.label.get_height() * scale)),
        )

        self.box_w, self.box_h = self.box.get_size()
        self.label_w, self.label_h = self.label.get_size()

        self.rects = []
        self._layout()

        # label start volledig VERBORGEN onder box
        self.hidden_offset = self.label_h
        self.label_offset = [float(self.hidden_offset) for _ in range(self.slots)]

    # -------------------------
    def _layout(self):
        sw, sh = self.screen.get_size()

        total_w = self.slots * self.box_w + (self.slots - 1) * self.spacing
        start_x = (sw - total_w) // 2
        y = sh - self.bottom_margin - self.box_h

        self.rects = []
        for i in range(self.slots):
            x = start_x + i * (self.box_w + self.spacing)
            self.rects.append(pygame.Rect(x, y, self.box_w, self.box_h))

    # -------------------------
    def toggle(self):
        self.visible = not self.visible
        if not self.visible:
            for i in range(self.slots):
                self.label_offset[i] = float(self.hidden_offset)

    # -------------------------
    def update(self, dt: float):
        if not self.visible:
            return

        mx, my = pygame.mouse.get_pos()

        for i, r in enumerate(self.rects):
            hovering = r.collidepoint((mx, my))
            target = 0.0 if hovering else float(self.hidden_offset)

            self.label_offset[i] += (target - self.label_offset[i]) * min(1.0, self.slide_speed * dt)

    # -------------------------
    def draw(self):
        if not self.visible:
            return

        for i, r in enumerate(self.rects):
            # 🔑 label zit BOVEN box, en schuift omhoog
            label_x = r.centerx - self.label_w // 2
            label_y = r.y - self.label_h + int(self.label_offset[i])

            self.screen.blit(self.label, (label_x, label_y))
            self.screen.blit(self.box, r.topleft)