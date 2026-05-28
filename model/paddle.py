class Paddle:
    """Модель платформы."""

    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def move(self, direction, dt, boundary_left, boundary_right):
        """Перемещает платформу с учётом границ."""
        self.x += direction * self.speed * dt
        if self.x < boundary_left:
            self.x = boundary_left
        if self.x + self.width > boundary_right:
            self.x = boundary_right - self.width

    def get_rect(self):
        return (self.x, self.y, self.width, self.height)