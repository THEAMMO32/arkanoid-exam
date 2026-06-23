"""Модель падающего бонуса."""

from utils.constants import *


class PowerUp:
    """Падающий бонус, который ловит платформа."""

    COLORS = {
        POWERUP_WIDEN: (60, 180, 255),
        POWERUP_LIFE: (255, 60, 100),
        POWERUP_SLOW: (120, 255, 120),
        POWERUP_MULTI: (255, 200, 40),
    }

    LABELS = {
        POWERUP_WIDEN: '⇔',
        POWERUP_LIFE: '♥',
        POWERUP_SLOW: '▼',
        POWERUP_MULTI: '✦',
    }

    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind
        self.size = 16
        self.alive = True

    def move(self, dt):
        """Опускает бонус вниз с постоянной скоростью."""
        self.y += POWERUP_FALL_SPEED * dt

    def get_rect(self):
        """Возвращает (x, y, w, h) bounding box бонуса."""
        s = self.size
        return (self.x - s // 2, self.y - s // 2, s, s)

    def color(self):
        """Возвращает цвет бонуса по его типу."""
        return self.COLORS.get(self.kind, (255, 255, 255))
