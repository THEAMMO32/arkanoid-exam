from model.ball import Ball
from model.paddle import Paddle
from model.brick import Brick
from utils.constants import *

class GameState:
    """Основное состояние игры: модель."""

    def __init__(self, width, height):
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

        total_width = BRICK_COLS * (BRICK_WIDTH + BRICK_GAP_X) - BRICK_GAP_X
        start_x = (width - total_width) // 2

        self.bricks = []
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = start_x + col * (BRICK_WIDTH + BRICK_GAP_X)
                y = BRICK_OFFSET_Y + row * (BRICK_HEIGHT + BRICK_GAP_Y)
                strength = 2 if row >= BRICK_ROWS - 2 else 1
                self.bricks.append(Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT, strength))

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