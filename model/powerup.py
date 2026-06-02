from utils.constants import *


class PowerUp:
    """Падающий бонус с красивой иконкой."""

    COLORS = {
        POWERUP_WIDEN: (60, 180, 255),
        POWERUP_LIFE: (255, 60, 100),
        POWERUP_SLOW: (120, 255, 120),
        POWERUP_MULTI: (255, 200, 40),
    }

    # Символы юникода для красивых иконок
    LABELS = {
        POWERUP_WIDEN: '⇔',    # расширение платформы
        POWERUP_LIFE: '♥',     # дополнительная жизнь
        POWERUP_SLOW: '▼',     # замедление
        POWERUP_MULTI: '✦',    # несколько мячей
    }

    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind
        self.size = 16  # увеличен размер для читаемой иконки
        self.alive = True

    def move(self, dt):
        """Опускает бонус вниз."""
        self.y += POWERUP_FALL_SPEED * dt

    def get_rect(self):
        s = self.size
        return (self.x - s // 2, self.y - s // 2, s, s)

    def color(self):
        return self.COLORS.get(self.kind, (255, 255, 255))
