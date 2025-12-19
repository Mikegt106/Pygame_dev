# ui/dialogue_ui.py
import pygame


class DialogueUI:
    def __init__(
        self,
        screen: pygame.Surface,
        box_h: int = 170,
        margin: int = 24,
        padding: int = 16,
        face_size: int = 110,
        cps: float = 55.0,  # characters per second (typewriter speed)
    ):
        self.screen = screen
        self.box_h = box_h
        self.margin = margin
        self.padding = padding
        self.face_size = face_size

        self.font = pygame.font.SysFont(None, 34)
        self.font_small = pygame.font.SysFont(None, 24)

        self.active = False
        self.index = 0
        self.lines = []  # list[dict]

        # caches
        self.faces_cache = {}
        self.scene_cache = {}

        # ✅ scene persistence
        self.current_scene_path = None

        # --- typewriter state ---
        self.cps = float(cps)
        self._char_pos = 0.0
        self._shown_chars = 0
        self._line_done = False

    def start(self, lines: list[dict]):
        self.lines = lines
        self.index = 0
        self.active = True

        # ✅ reset scene for a new dialogue sequence
        self.current_scene_path = None

        self._reset_typewriter_for_current_line()

    def is_done(self) -> bool:
        return (not self.active) or self.index >= len(self.lines)

    def _current(self) -> dict:
        if not self.active or self.index >= len(self.lines):
            return {}
        return self.lines[self.index]

    def _current_text(self) -> str:
        return self._current().get("text", "")

    def _reset_typewriter_for_current_line(self):
        self._char_pos = 0.0
        self._shown_chars = 0
        self._line_done = False

        text = self._current_text()
        if len(text) == 0:
            self._line_done = True

    # -------------------------
    # ASSET LOADERS (cached)
    # -------------------------
    def _load_face(self, path: str) -> pygame.Surface:
        if path not in self.faces_cache:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (self.face_size, self.face_size))
            self.faces_cache[path] = img
        return self.faces_cache[path]

    def _load_scene(self, path: str) -> pygame.Surface:
        """Load + scale background to screen size, cached per path."""
        if path not in self.scene_cache:
            sw, sh = self.screen.get_size()
            img = pygame.image.load(path).convert()  # background: no alpha needed
            img = pygame.transform.scale(img, (sw, sh))
            self.scene_cache[path] = img
        return self.scene_cache[path]

    # -------------------------
    # UPDATE / INPUT
    # -------------------------
    def update(self, dt: float):
        """Typewriter progression."""
        if not self.active:
            return
        if self.index >= len(self.lines):
            self.active = False
            return
        if self._line_done:
            return

        text = self._current_text()
        self._char_pos += self.cps * dt
        self._shown_chars = min(len(text), int(self._char_pos))

        if self._shown_chars >= len(text):
            self._shown_chars = len(text)
            self._line_done = True

    def _advance(self):
        self.index += 1
        if self.index >= len(self.lines):
            self.active = False
            return
        self._reset_typewriter_for_current_line()

    def handle_event(self, event) -> bool:
        """Return True if UI used the input (so player shouldn't attack)."""
        if not self.active:
            return False

        proceed = False
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):
            proceed = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            proceed = True

        if not proceed:
            return False

        # 1) if text still typing => reveal instantly
        if not self._line_done:
            text = self._current_text()
            self._shown_chars = len(text)
            self._char_pos = float(len(text))
            self._line_done = True
            return True

        # 2) else go next line
        self._advance()
        return True

    # -------------------------
    # TEXT WRAP
    # -------------------------
    def _wrap(self, text: str, max_w: int):
        words = text.split(" ")
        lines = []
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            if self.font.size(test)[0] <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    # -------------------------
    # DRAW
    # -------------------------
    def draw(self):
        if not self.active or self.index >= len(self.lines):
            return

        cur = self._current()
        scene_path = cur.get("scene", None)

        # ✅ update scene ONLY if this line provides one
        if scene_path:
            self.current_scene_path = scene_path

        # ✅ draw current scene if it exists (persist across lines)
        if self.current_scene_path:
            try:
                bg = self._load_scene(self.current_scene_path)
                self.screen.blit(bg, (0, 0))
            except Exception:
                self.screen.fill((10, 10, 10))
        else:
            self.screen.fill((10, 10, 10))

        # 2) dialogue box
        sw, sh = self.screen.get_size()
        box_rect = pygame.Rect(
            self.margin,
            sh - self.margin - self.box_h,
            sw - 2 * self.margin,
            self.box_h,
        )

        overlay = pygame.Surface((box_rect.w, box_rect.h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, box_rect.topleft)

        name = cur.get("name", "")
        face_path = cur.get("face", "")
        full_text = cur.get("text", "")

        shown_text = full_text[: self._shown_chars]

        # face
        tint = cur.get("tint", None)
        
        face_x = box_rect.x + self.padding
        face_y = box_rect.y + self.padding
        if face_path:
            face = self._load_face(face_path)

            if tint is not None:
                # tint = (0,0,0) => volledig zwart silhouette
                tinted = face.copy()
                tinted.fill(tint, special_flags=pygame.BLEND_RGBA_MULT)
                face = tinted

            self.screen.blit(face, (face_x, face_y))

        # name + text
        text_x = face_x + self.face_size + self.padding
        text_y = box_rect.y + self.padding

        name_surf = self.font.render(name, True, (255, 255, 255))
        self.screen.blit(name_surf, (text_x, text_y))
        text_y += name_surf.get_height() + 8

        max_w = box_rect.right - self.padding - text_x
        wrapped = self._wrap(shown_text, max_w)

        for line in wrapped[:4]:
            t = self.font.render(line, True, (235, 235, 235))
            self.screen.blit(t, (text_x, text_y))
            text_y += t.get_height() + 4

        hint_text = "Click / SPACE / ENTER"
        if not self._line_done:
            hint_text = "Click / SPACE / ENTER (skip typing)"

        hint = self.font_small.render(hint_text, True, (220, 220, 220))
        self.screen.blit(
            hint,
            (box_rect.right - hint.get_width() - self.padding, box_rect.bottom - hint.get_height() - self.padding),
        )