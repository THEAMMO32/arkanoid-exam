from model.collision import rect_collision, get_collision_side, ball_paddle_collision
from utils.constants import *


class GameController:
    """Игровая логика: движение, столкновения, бонусы."""

    def __init__(self, game_state, audio=None):
        self.game_state = game_state
        self.audio = audio
        self._paddle_hit_cooldown = 0.0

    def update(self, left_pressed, right_pressed, dt):
        gs = self.game_state
        if gs.state not in (STATE_RUNNING, STATE_LEVEL_CLEAR):
            gs.update_timers(dt)
            return

        gs.update_timers(dt)

        if gs.state == STATE_LEVEL_CLEAR:
            return

        direction = 0
        if left_pressed:
            direction = -1
        elif right_pressed:
            direction = 1
        gs.paddle.move(direction, dt, 0, gs.width)

        # Двигаем все мячи и обрабатываем границы
        lost_balls = []
        for ball in gs.balls:
            ball.move(dt)

            r = BALL_RADIUS
            if ball.x - r <= 0:
                ball.x = r
                ball.bounce_x()
            elif ball.x + r >= gs.width:
                ball.x = gs.width - r
                ball.bounce_x()
            if ball.y - r <= 0:
                ball.y = r
                ball.bounce_y()
            elif ball.y + r >= gs.height:
                lost_balls.append(ball)
                continue

            # Столкновение с платформой
            ball_rect = ball.get_rect()
            paddle_rect = gs.paddle.get_rect()
            if ball_paddle_collision(ball_rect, paddle_rect, ball):
                ball.y = paddle_rect[1] - r
                if self._paddle_hit_cooldown <= 0 and self.audio:
                    self.audio.play_paddle()
                    self._paddle_hit_cooldown = 0.08

        # Удаляем упавшие мячи
        for b in lost_balls:
            if b in gs.balls:
                gs.balls.remove(b)
        if lost_balls:
            # Теряем жизнь только если ВСЕ мячи упали
            if len(gs.balls) == 0:
                if gs.invincibility_timer <= 0:
                    if self.audio:
                        self.audio.play_life_lost()
                    gs.lose_life()
                return

        self._paddle_hit_cooldown -= dt

        self._handle_brick_collisions()
        self._handle_wall_collisions()
        self._update_powerups(dt)

        if gs.state == STATE_RUNNING and gs.all_bricks_destroyed():
            gs.state = STATE_WIN
            if self.audio:
                self.audio.play_win()

    def _handle_brick_collisions(self):
        gs = self.game_state
        theme = gs.theme
        for ball in gs.balls:
            collision_occurred = True
            iterations = 0
            while collision_occurred and iterations < 20:
                collision_occurred = False
                iterations += 1
                ball_rect = ball.get_rect()
                for brick in gs.bricks:
                    if not brick.alive:
                        continue
                    if not rect_collision(ball_rect, brick.get_rect()):
                        continue
                    side = get_collision_side(ball_rect, brick.get_rect())
                    r = ball.radius
                    if side == 'left':
                        ball.x = brick.x - r
                        ball.bounce_x()
                    elif side == 'right':
                        ball.x = brick.x + brick.width + r
                        ball.bounce_x()
                    elif side == 'top':
                        ball.y = brick.y - r
                        ball.bounce_y()
                    elif side == 'bottom':
                        ball.y = brick.y + brick.height + r
                        ball.bounce_y()
                    was_strong = brick.strength > 1
                    destroyed = brick.hit()
                    if self.audio:
                        self.audio.play_brick(strong=was_strong and not destroyed)
                    if destroyed:
                        gs.score += 10 * (gs.level_index + 1)
                        color = theme['strong'] if was_strong else theme['weak']
                        gs.spawn_particles(brick, color)
                        gs.maybe_drop_powerup(brick)
                    collision_occurred = True
                    break

    def _handle_wall_collisions(self):
        """Обработка столкновений мяча с неразрушаемыми стенками.
        Каждый мяч отскакивает только от одной стенки за кадр."""
        gs = self.game_state
        for ball in gs.balls:
            for wall in gs.walls:
                wall_rect = wall.get_rect()
                if not rect_collision(ball.get_rect(), wall_rect):
                    continue
                side = get_collision_side(ball.get_rect(), wall_rect)
                r = ball.radius
                if side == 'left':
                    ball.x = wall_rect[0] - r
                    ball.bounce_x()
                elif side == 'right':
                    ball.x = wall_rect[0] + wall_rect[2] + r
                    ball.bounce_x()
                elif side == 'top':
                    ball.y = wall_rect[1] - r
                    ball.bounce_y()
                elif side == 'bottom':
                    ball.y = wall_rect[1] + wall_rect[3] + r
                    ball.bounce_y()
                if self.audio:
                    self.audio.play_brick(strong=True)
                break  # один отскок за кадр

    def _update_powerups(self, dt):
        gs = self.game_state
        paddle_rect = gs.paddle.get_rect()
        remaining = []
        for pu in gs.powerups:
            if not pu.alive:
                continue
            pu.move(dt)
            if pu.y > gs.height + 30:
                continue
            if rect_collision(pu.get_rect(), paddle_rect):
                gs.apply_powerup(pu.kind)
                if self.audio:
                    self.audio.play_powerup()
                continue
            remaining.append(pu)
        gs.powerups = remaining
