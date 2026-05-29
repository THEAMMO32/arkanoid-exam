class Paddle:
    """Модель платформы."""

    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.base_width = width
        self.speed = speed

    def move(self, direction, dt, boundary_left, boundary_right):
        """Перемещает платформу с учётом границ."""
        self.x += direction * self.speed * dt
        if self.x < boundary_left:
            self.x = boundary_left
        if self.x + self.width > boundary_right:
            self.x = boundary_right - self.width

    def set_width(self, width, boundary_right):
        """Меняет ширину, не выходя за экран."""
        self.width = width
        if self.x + self.width > boundary_right:
            self.x = boundary_right - self.width

    def reset_width(self):
        """Возвращает базовую ширину."""
        self.width = self.base_width

    def widen(self, bonus, boundary_right):
        """Расширяет платформу."""
        self.set_width(self.base_width + bonus, boundary_right)

    def get_rect(self):
        return (self.x, self.y, self.width, self.height)
