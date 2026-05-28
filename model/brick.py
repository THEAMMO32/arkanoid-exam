class Brick:
    def __init__(self, x, y, width, height, strength):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.strength = strength
        self.alive = True

    def hit(self):
        if not self.alive:
            return False
        self.strength -= 1
        if self.strength <= 0:
            self.alive = False
            return True
        return False

    def get_rect(self):
        return (self.x, self.y, self.width, self.height)