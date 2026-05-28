from model.collision import rect_collision, get_collision_side, ball_paddle_collision
from utils.constants import *

class GameController:

    def __init__(self, game_state):
        self.game_state = game_state

    def update(self, left_pressed, right_pressed, dt):
        if self.game_state.state != STATE_RUNNING:
            return

        direction = 0
        if left_pressed:
            direction = -1
        elif right_pressed:
            direction = 1
        self.game_state.paddle.move(direction, dt, 0, self.game_state.width)

        self.game_state.ball.move(dt)

        if self.game_state.ball.x - BALL_RADIUS <= 0:
            self.game_state.ball.x = BALL_RADIUS
            self.game_state.ball.bounce_x()
        elif self.game_state.ball.x + BALL_RADIUS >= self.game_state.width:
            self.game_state.ball.x = self.game_state.width - BALL_RADIUS
            self.game_state.ball.bounce_x()
        if self.game_state.ball.y - BALL_RADIUS <= 0:
            self.game_state.ball.y = BALL_RADIUS
            self.game_state.ball.bounce_y()
        elif self.game_state.ball.y + BALL_RADIUS >= self.game_state.height:
            self.game_state.lose_life()
            return

        ball_rect = self.game_state.ball.get_rect()
        paddle_rect = self.game_state.paddle.get_rect()
        if ball_paddle_collision(ball_rect, paddle_rect, self.game_state.ball):
            self.game_state.ball.y = paddle_rect[1] - BALL_RADIUS

        # Обработка коллизий с блоками: повторяем, пока есть столкновения
        collision_occurred = True
        max_iterations = 20  # защита от бесконечного цикла
        iterations = 0
        while collision_occurred and iterations < max_iterations:
            collision_occurred = False
            ball_rect = self.game_state.ball.get_rect()
            for brick in self.game_state.bricks:
                if not brick.alive:
                    continue
                brick_rect = brick.get_rect()
                if rect_collision(ball_rect, brick_rect):
                    side = get_collision_side(ball_rect, brick_rect)
                    if side in ('left', 'right'):
                        self.game_state.ball.bounce_x()
                    else:
                        self.game_state.ball.bounce_y()
                    if brick.hit():
                        self.game_state.score += 10
                    collision_occurred = True
                    break  # после отскока выходим из цикла поиска, затем снова проверяем
            iterations += 1

        if self.game_state.all_bricks_destroyed():
            self.game_state.state = STATE_WIN