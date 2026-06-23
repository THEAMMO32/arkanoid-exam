"""Модель неразрушаемой стены-перегородки."""

class Wall:
    """Недвижимая неразрушаемая стенка, от которой отскакивает мяч."""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_rect(self):
        """Возвращает (x, y, w, h) bounding box стенки."""
        return (self.x, self.y, self.width, self.height)
