from model.ball import Ball
from model.paddle import Paddle
from model.brick import Brick
from utils.constants import *

class GameState:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.score = 0
        self.lives = 3
        self.state = STATE_RUNNING

        # ----- Платформа (без изменений) -----
        self.paddle = Paddle(
            width//2 - PADDLE_WIDTH//2,
            height - PADDLE_HEIGHT - 10,
            PADDLE_WIDTH, PADDLE_HEIGHT,
            PADDLE_SPEED
        )

        # ----- Мяч (без изменений) -----
        self.ball = Ball(
            width//2,
            height - PADDLE_HEIGHT - 20,
            BALL_RADIUS,
            BALL_SPEED_X,
            BALL_SPEED_Y
        )

        # ----- Блоки: теперь динамически под ширину экрана -----
        # Настройки (можно менять)
        cols = BRICK_COLS            # количество блоков по горизонтали (10)
        rows = BRICK_ROWS            # количество рядов (5)
        margin_left = 20             # отступ слева (пиксели)
        margin_right = 20            # отступ справа
        gap_x = BRICK_GAP_X          # зазор между блоками по горизонтали (5)
        gap_y = BRICK_GAP_Y          # зазор между рядами по вертикали (5)
        brick_height = BRICK_HEIGHT  # фиксированная высота блока (20)

        # Вычисляем доступную ширину для всех блоков + зазоры
        available_width = width - margin_left - margin_right
        # Общая ширина всех зазоров между блоками
        total_gaps_width = gap_x * (cols - 1)
        # Ширина одного блока
        brick_width = (available_width - total_gaps_width) // cols

        # Если ширина получилась слишком маленькой, ставим минимум (например, 30)
        if brick_width < 30:
            brick_width = 30

        # Запоминаем параметры для дальнейшего использования (если понадобятся)
        self.brick_width = brick_width
        self.brick_height = brick_height

        # Генерация блоков
        self.bricks = []
        for row in range(rows):
            for col in range(cols):
                x = margin_left + col * (brick_width + gap_x)
                y = BRICK_OFFSET_Y + row * (brick_height + gap_y)
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