# ui/inventory_ui.py
import pygame

# ---------- HOVER SOUND ----------
HOVER_SOUND = pygame.mixer.Sound("assets/Sounds/hover.wav")
HOVER_SOUND.set_volume(0.5)

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
        self.slots = int(slots)
        self.scale = float(scale)
        self.bottom_margin = int(bottom_margin)
        self.spacing = int(spacing * scale)
        self.slide_speed = float(slide_speed)

        self.visible = False
        self._last_hover_index = None

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

        # fonts
        self.font_small = pygame.font.SysFont(None, int(22 * scale))
        self.font_count = pygame.font.SysFont(None, int(24 * scale))

        # item image cache: item_id -> Surface
        self._item_img_cache = {}

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
    def is_hovered(self) -> bool:
        if not self.visible:
            return False
        mx, my = pygame.mouse.get_pos()
        return any(r.collidepoint((mx, my)) for r in self.rects)

    # -------------------------
    def handle_event(self, event):
        if not self.visible:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, r in enumerate(self.rects):
                if r.collidepoint(event.pos):
                    return i
        return None

    # -------------------------
    def update(self, dt: float):
        if not self.visible:
            self._last_hover_index = None
            return

        mx, my = pygame.mouse.get_pos()
        current_hover = None

        for i, r in enumerate(self.rects):
            hovering = r.collidepoint((mx, my))
            target = 0.0 if hovering else float(self.hidden_offset)

            self.label_offset[i] += (target - self.label_offset[i]) * min(
                1.0, self.slide_speed * dt
            )

            if hovering:
                current_hover = i

        # 🔊 HOVER SOUND (alleen bij nieuw slot)
        if current_hover is not None and current_hover != self._last_hover_index:
            HOVER_SOUND.play()

        self._last_hover_index = current_hover

    # -------------------------
    def _get_hotbar_items(self, player, config):
        inv = getattr(player, "inventory", {}) or {}
        items = []
        for item_id, count in inv.items():
            if count <= 0:
                continue
            if item_id not in getattr(config, "ITEMS", {}):
                continue
            items.append((item_id, int(count)))
            if len(items) >= self.slots:
                break
        return items

    def _get_item_image(self, item_id: str, config):
        if item_id in self._item_img_cache:
            return self._item_img_cache[item_id]

        item = config.ITEMS.get(item_id, {})
        path = item.get("image")
        if not path:
            return None

        img = pygame.image.load(path).convert_alpha()

        # schaal naar box (subtiel kleiner)
        max_w = int(self.box_w * 0.65)
        max_h = int(self.box_h * 0.65)
        iw, ih = img.get_size()
        scale = min(max_w / iw, max_h / ih)
        new_size = (max(1, int(iw * scale)), max(1, int(ih * scale)))
        img = pygame.transform.scale(img, new_size)

        self._item_img_cache[item_id] = img
        return img

    # -------------------------
    def draw(self, player, config):
        if not self.visible:
            return

        hotbar = self._get_hotbar_items(player, config)  # list[(id,count)]
        slot_items = [None] * self.slots
        for i, tup in enumerate(hotbar):
            slot_items[i] = tup

        mx, my = pygame.mouse.get_pos()

        for i, r in enumerate(self.rects):
            # -------------------------
            # ✅ HOVER LABEL terug (zonder tekst)
            # -------------------------
            label_x = r.centerx - self.label_w // 2
            label_y = r.y - self.label_h + int(self.label_offset[i])
            self.screen.blit(self.label, (label_x, label_y))

            # box
            self.screen.blit(self.box, r.topleft)

            # item icon + count
            if slot_items[i] is not None:
                item_id, count = slot_items[i]

                icon = self._get_item_image(item_id, config)
                if icon:
                    ix = r.centerx - icon.get_width() // 2
                    iy = r.centery - icon.get_height() // 2
                    self.screen.blit(icon, (ix, iy))

                # stack count rechtsonder (alleen tonen als > 1)
                if count > 1:
                    text = str(count)
                    cnt = self.font_count.render(text, True, (255, 255, 255))
                    shadow = self.font_count.render(text, True, (0, 0, 0))

                    pad_x = int(4 * self.scale)   
                    pad_y = int(3.2 * self.scale)  
                    cx = r.right - cnt.get_width() - pad_x
                    cy = r.bottom - cnt.get_height() - pad_y

                    self.screen.blit(shadow, (cx + 1, cy + 1))
                    self.screen.blit(cnt, (cx, cy))

            # hover border (optioneel)
            if r.collidepoint((mx, my)):
                pygame.draw.rect(self.screen, (255, 255, 255), r, 2, border_radius=8)

    # -------------------------
    def get_item_in_slot(self, slot_index: int, player, config):
        hotbar = self._get_hotbar_items(player, config)
        if 0 <= slot_index < len(hotbar):
            return hotbar[slot_index][0]  # item_id
        return None