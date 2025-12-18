import pygame

_image_cache: dict[tuple[str, bool, int], pygame.Surface] = {}

def load_image(path: str, alpha: bool = True, scale: int = 1) -> pygame.Surface:
    key = (path, alpha, scale)
    if key in _image_cache:
        return _image_cache[key]

    img = pygame.image.load(path)
    img = img.convert_alpha() if alpha else img.convert()

    if scale != 1:
        w, h = img.get_size()
        img = pygame.transform.scale(img, (w * scale, h * scale))

    _image_cache[key] = img
    return img