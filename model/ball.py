from collections import deque
from utils.constants import BALL_TRAIL_LEN


class Ball:
    """Модель мяча."""

    def __init__(self, x, y, radius, vx, vy):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = vx
        self.vy = vy
        self.base_vx = vx
        self.base_vy = vy
        self.trail = deque(maxlen=BALL_TRAIL_LEN)

    def move(self, dt, speed_mul=1.0):
        """Обновление позиции на dt секунд."""
        self.trail.append((self.x, self.y))
        self.x += self.vx * speed_mul * dt
        self.y += self.vy * speed_mul * dt

    def set_speed(self, vx, vy):
        """Задаёт скорость и базовые значения."""
        self.vx = vx
        self.vy = vy
        self.base_vx = vx
        self.base_vy = vy

    def apply_slow(self, factor=0.72):
        """Замедляет мяч."""
        self.vx = self.base_vx * factor
        self.vy = self.base_vy * factor

    def restore_speed(self):
        """Восстанавливает базовую скорость."""
        self.vx = self.base_vx
        self.vy = self.base_vy

    def bounce_x(self):
        """Отскок по горизонтали."""
        self.vx = -self.vx
        self.base_vx = -self.base_vx

    def bounce_y(self):
        """Отскок по вертикали."""
        self.vy = -self.vy
        self.base_vy = -self.base_vy

    def get_rect(self):
        """Возвращает ограничивающий прямоугольник."""
        return (self.x - self.radius, self.y - self.radius,
                2 * self.radius, 2 * self.radius)
