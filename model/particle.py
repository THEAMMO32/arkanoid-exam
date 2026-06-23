"""Модель частицы для визуального эффекта разрушения кирпича."""

import random
from utils.constants import PARTICLE_LIFETIME


class Particle:
    """Визуальная частица, появляющаяся при разрушении кирпича."""

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-220, 220)
        self.vy = random.uniform(-280, -80)
        self.size = random.randint(3, 6)
        self.color = color
        self.life = PARTICLE_LIFETIME
        self.max_life = PARTICLE_LIFETIME

    def update(self, dt):
        """Смещает частицу и уменьшает оставшееся время жизни."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 400 * dt
        self.life -= dt

    def is_alive(self):
        """Возвращает True, если частица ещё видима."""
        return self.life > 0

    def alpha(self):
        """Возвращает прозрачность от 0 до 255 на основе оставшейся жизни."""
        if self.max_life <= 0:
            return 255
        return max(0, min(255, int(255 * self.life / self.max_life)))
