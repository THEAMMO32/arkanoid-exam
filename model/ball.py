"""Модель мяча с траекторией следа."""

from collections import deque
from utils.constants import BALL_TRAIL_LEN


class Ball:
    """Мяч, движущийся по экрану с отскоком и следом."""

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
        """Смещает мяч на один кадр и сохраняет точку в след."""
        self.trail.append((self.x, self.y))
        self.x += self.vx * speed_mul * dt
        self.y += self.vy * speed_mul * dt

    def set_speed(self, vx, vy):
        """Устанавливает текущую и базовую скорость мяча."""
        self.vx = vx
        self.vy = vy
        self.base_vx = vx
        self.base_vy = vy

    def apply_slow(self, factor=0.72):
        """Уменьшает текущую скорость относительно базовой."""
        self.vx = self.base_vx * factor
        self.vy = self.base_vy * factor

    def restore_speed(self):
        """Возвращает скорость к базовым значениям."""
        self.vx = self.base_vx
        self.vy = self.base_vy

    def bounce_x(self):
        """Отражает мяч по горизонтали."""
        self.vx = -self.vx
        self.base_vx = -self.base_vx

    def bounce_y(self):
        """Отражает мяч по вертикали."""
        self.vy = -self.vy
        self.base_vy = -self.base_vy

    def get_rect(self):
        """Возвращает (x, y, w, h) bounding box мяча."""
        return (self.x - self.radius, self.y - self.radius,
                2 * self.radius, 2 * self.radius)
