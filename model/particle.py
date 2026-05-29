import random
from utils.constants import PARTICLE_LIFETIME

class Particle:
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
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 400 * dt
        self.life -= dt

    def is_alive(self):
        return self.life > 0

    def alpha(self):
        if self.max_life <= 0:
            return 255
        return max(0, min(255, int(255 * self.life / self.max_life)))