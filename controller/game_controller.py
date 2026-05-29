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

        gs.ball.move(dt)

        r = BALL_RADIUS
        if gs.ball.x - r <= 0:
            gs.ball.x = r
            gs.ball.bounce_x()
        elif gs.ball.x + r >= gs.width:
            gs.ball.x = gs.width - r
            gs.ball.bounce_x()
        if gs.ball.y - r <= 0:
            gs.ball.y = r
            gs.ball.bounce_y()
        elif gs.ball.y + r >= gs.height:
            if gs.invincibility_timer <= 0:
                if self.audio:
                    self.audio.play_life_lost()
                gs.lose_life()
            return

        ball_rect = gs.ball.get_rect()
        paddle_rect = gs.paddle.get_rect()
        if ball_paddle_collision(ball_rect, paddle_rect, gs.ball):
            gs.ball.y = paddle_rect[1] - r
            if self._paddle_hit_cooldown <= 0 and self.audio:
                self.audio.play_paddle()
                self._paddle_hit_cooldown = 0.08
        self._paddle_hit_cooldown -= dt

        self._handle_brick_collisions()
        self._update_powerups(dt)

        if gs.state == STATE_RUNNING and gs.all_bricks_destroyed():
            advanced = gs.advance_level()
            if self.audio:
                if advanced:
                    self.audio.play_level()
                else:
                    self.audio.play_win()

    def _handle_brick_collisions(self):
        gs = self.game_state
        theme = gs.theme
        collision_occurred = True
        iterations = 0
        while collision_occurred and iterations < 20:
            collision_occurred = False
            iterations += 1
            ball_rect = gs.ball.get_rect()
            for brick in gs.bricks:
                if not brick.alive:
                    continue
                if not rect_collision(ball_rect, brick.get_rect()):
                    continue
                side = get_collision_side(ball_rect, brick.get_rect())
                if side in ('left', 'right'):
                    gs.ball.bounce_x()
                else:
                    gs.ball.bounce_y()
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
