"""Модель кирпича с прочностью и возможностью неразрушимости."""

class Brick:
    """Кирпич: обычный, прочный или неразрушаемый."""

    def __init__(self, x, y, width, height, strength, indestructible=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.strength = strength
        self.indestructible = indestructible
        self.alive = True

    def hit(self):
        """Уменьшает прочность на 1. Возвращает True, если кирпич разрушен.

        Неразрушаемые кирпичи никогда не ломаются и возвращают False.
        """
        if not self.alive or self.indestructible:
            return False
        self.strength -= 1
        if self.strength <= 0:
            self.alive = False
            return True
        return False

    def get_rect(self):
        """Возвращает (x, y, w, h) bounding box кирпича."""
        return (self.x, self.y, self.width, self.height)
