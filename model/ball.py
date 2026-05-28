class Ball:
    """Модель мяча."""

    def __init__(self, x, y, radius, vx, vy):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = vx
        self.vy = vy

    def move(self, dt):
        """Обновление позиции на dt секунд."""
        self.x += self.vx * dt
        self.y += self.vy * dt

    def bounce_x(self):
        """Отскок по горизонтали."""
        self.vx = -self.vx

    def bounce_y(self):
        """Отскок по вертикали."""
        self.vy = -self.vy

    def get_rect(self):
        """Возвращает ограничивающий прямоугольник."""
        return (self.x - self.radius, self.y - self.radius,
                2 * self.radius, 2 * self.radius)