from utils.constants import *


class PowerUp:
    """Падающий бонус."""

    COLORS = {
        POWERUP_WIDEN: (100, 200, 255),
        POWERUP_LIFE: (255, 80, 120),
        POWERUP_SLOW: (180, 255, 100),
    }

    LABELS = {
        POWERUP_WIDEN: 'W',
        POWERUP_LIFE: '+',
        POWERUP_SLOW: 'S',
    }

    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind
        self.size = POWERUP_SIZE
        self.alive = True

    def move(self, dt):
        """Опускает бонус вниз."""
        self.y += POWERUP_FALL_SPEED * dt

    def get_rect(self):
        s = self.size
        return (self.x - s // 2, self.y - s // 2, s, s)

    def color(self):
        return self.COLORS.get(self.kind, (255, 255, 255))
