import pygame

_image_cache: dict[tuple[str, bool], pygame.Surface] = {}

def load_image(path: str, alpha: bool = True) -> pygame.Surface:
    key = (path, alpha)
    if key in _image_cache:
        return _image_cache[key]

    img = pygame.image.load(path)
    img = img.convert_alpha() if alpha else img.convert()
    _image_cache[key] = img
    return img