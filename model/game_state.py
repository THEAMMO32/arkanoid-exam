from model.ball import Ball
from model.paddle import Paddle
from model.brick import Brick
from utils.constants import *

class GameState:

    def __init__(self, width, height, strength_mode='default'):
        self.width = width
        self.height = height
        self.score = 0
        self.lives = 3
        self.state = STATE_RUNNING

        self.paddle = Paddle(
            width//2 - PADDLE_WIDTH//2,
            height - PADDLE_HEIGHT - 10,
            PADDLE_WIDTH, PADDLE_HEIGHT,
            PADDLE_SPEED
        )

        self.ball = Ball(
            width//2,
            height - PADDLE_HEIGHT - 20,
            BALL_RADIUS,
            BALL_SPEED_X,
            BALL_SPEED_Y
        )

        brick_width = BRICK_WIDTH
        brick_height = BRICK_HEIGHT
        gap_x = BRICK_GAP_X
        gap_y = BRICK_GAP_Y

        margin = 10
        available_width = width - 2 * margin
        cols = (available_width + gap_x) // (brick_width + gap_x)
        if cols < 1:
            cols = 1

        total_width = cols * (brick_width + gap_x) - gap_x
        start_x = (width - total_width) // 2

        rows = BRICK_ROWS

        self.bricks = []
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (brick_width + gap_x)
                y = BRICK_OFFSET_Y + row * (brick_height + gap_y)
                if strength_mode == 'all_weak':
                    strength = 1
                elif strength_mode == 'all_strong':
                    strength = 2
                else:
                    strength = 2 if row >= rows - 2 else 1
                self.bricks.append(Brick(x, y, brick_width, brick_height, strength))

    def get_alive_bricks(self):
        return [b for b in self.bricks if b.alive]

    def all_bricks_destroyed(self):
        return len(self.get_alive_bricks()) == 0

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.state = STATE_GAME_OVER
        else:
            self.ball.x = self.width//2
            self.ball.y = self.height - PADDLE_HEIGHT - 20
            self.ball.vx = BALL_SPEED_X
            self.ball.vy = BALL_SPEED_Y
            self.paddle.x = self.width//2 - PADDLE_WIDTH//2