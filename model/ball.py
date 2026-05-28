class Ball:
    def __init__(self, x, y, radius, vx, vy):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = vx
        self.vy = vy

    def move(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def bounce_x(self):
        self.vx = -self.vx

    def bounce_y(self):
        self.vy = -self.vy

    def get_rect(self):
        return (self.x - self.radius, self.y - self.radius,
                2 * self.radius, 2 * self.radius)