import random
from model.ball import Ball
from model.paddle import Paddle
from model.powerup import PowerUp
from model.particle import Particle
from utils.constants import *
from utils.level_loader import build_bricks_for_level, build_walls_for_level, get_theme

class GameState:
    def __init__(self, width, height, difficulty=1, level_index=0,
                 highscore=0, speed_mul=1.0):
        self.width = width
        self.height = height
        self.difficulty = difficulty
        self.level_index = level_index
        self.highscore = highscore
        diff_mul = DIFFICULTY_SPEED.get(difficulty, 1.0)
        self.speed_mul = speed_mul * diff_mul
        self.score = 0
        self.lives = 3
        self.state = STATE_RUNNING
        self.theme = get_theme(level_index)
        self.particles = []
        self.powerups = []
        self.invincibility_timer = 0.0
        self.wide_timer = 0.0
        self.slow_timer = 0.0
        self.level_clear_timer = 0.0
        self.strength_mode = DIFFICULTY_STRENGTH.get(difficulty, 'default')

        pw = PADDLE_WIDTH
        if difficulty == 2:
            pw = max(90, PADDLE_WIDTH - 30)
        elif difficulty == 0:
            pw = PADDLE_WIDTH + 20

        self.paddle = Paddle(
            width // 2 - pw // 2,
            height - PADDLE_HEIGHT - 10,
            pw, PADDLE_HEIGHT,
            PADDLE_SPEED
        )
        self.paddle.base_width = pw

        bx = BALL_SPEED_X * speed_mul
        by = BALL_SPEED_Y * speed_mul
        self.balls = [Ball(
            width // 2,
            height - PADDLE_HEIGHT - 20,
            BALL_RADIUS,
            bx, by
        )]
        self.bricks, layout_walls = build_bricks_for_level(
            width, height, level_index, self.strength_mode
        )
        self.walls = build_walls_for_level(
            width, height, difficulty, level_index
        ) + layout_walls

    def get_alive_bricks(self):
        return [b for b in self.bricks if b.alive]

    def all_bricks_destroyed(self):
        return len(self.get_alive_bricks()) == 0

    def spawn_particles(self, brick, color):
        cx = brick.x + brick.width / 2
        cy = brick.y + brick.height / 2
        for _ in range(PARTICLE_COUNT):
            self.particles.append(Particle(cx, cy, color))

    def maybe_drop_powerup(self, brick):
        if random.random() > POWERUP_DROP_CHANCE:
            return
        cx = brick.x + brick.width / 2
        cy = brick.y + brick.height / 2
        kind = random.choice([POWERUP_WIDEN, POWERUP_LIFE, POWERUP_SLOW, POWERUP_MULTI])
        self.powerups.append(PowerUp(cx, cy, kind))

    def apply_powerup(self, kind):
        if kind == POWERUP_WIDEN:
            self.paddle.widen(PADDLE_WIDE_BONUS, self.width)
            self.wide_timer += POWERUP_DURATION  # progressive stack
        elif kind == POWERUP_LIFE:
            self.lives += 1
        elif kind == POWERUP_SLOW:
            for ball in self.balls:
                ball.apply_slow()
            self.slow_timer = POWERUP_DURATION
        elif kind == POWERUP_MULTI:
            # Создать копию случайного существующего мяча
            if self.balls:
                src = random.choice(self.balls)
                bx = BALL_SPEED_X * self.speed_mul
                by = BALL_SPEED_Y * self.speed_mul
                new_ball = Ball(src.x, src.y, BALL_RADIUS, bx, by)
                if self.slow_timer > 0:
                    new_ball.apply_slow()
                self.balls.append(new_ball)

    def update_timers(self, dt):
        if self.invincibility_timer > 0:
            self.invincibility_timer -= dt
        if self.wide_timer > 0:
            self.wide_timer -= dt
            if self.wide_timer <= 0:
                self.paddle.reset_width()
        if self.slow_timer > 0:
            self.slow_timer -= dt
            if self.slow_timer <= 0:
                for ball in self.balls:
                    ball.restore_speed()
        if self.state == STATE_LEVEL_CLEAR:
            self.level_clear_timer -= dt
            if self.level_clear_timer <= 0:
                self.state = STATE_RUNNING

        alive_p = []
        for p in self.particles:
            p.update(dt)
            if p.is_alive():
                alive_p.append(p)
        self.particles = alive_p

    def reset_ball_paddle(self):
        bx = BALL_SPEED_X * self.speed_mul
        by = BALL_SPEED_Y * self.speed_mul
        self.balls = [Ball(
            self.width // 2,
            self.height - PADDLE_HEIGHT - 20,
            BALL_RADIUS,
            bx, by
        )]
        if self.slow_timer > 0:
            self.balls[0].apply_slow()
        self.paddle.x = self.width // 2 - self.paddle.width // 2

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.state = STATE_GAME_OVER
        else:
            self.reset_ball_paddle()
            self.invincibility_timer = INVINCIBILITY_DURATION

    def advance_level(self):
        next_level = self.level_index + 1
        if next_level >= LEVEL_COUNT:
            self.state = STATE_WIN
            return False
        self.level_index = next_level
        self.theme = get_theme(self.level_index)
        self.bricks, layout_walls = build_bricks_for_level(
            self.width, self.height, self.level_index, self.strength_mode
        )
        self.walls = build_walls_for_level(
            self.width, self.height, self.difficulty, self.level_index
        ) + layout_walls
        self.speed_mul *= 1.06
        bx = BALL_SPEED_X * self.speed_mul
        by = BALL_SPEED_Y * self.speed_mul
        self.balls = [Ball(
            self.width // 2,
            self.height - PADDLE_HEIGHT - 20,
            BALL_RADIUS,
            bx, by
        )]
        self.reset_ball_paddle()
        self.state = STATE_LEVEL_CLEAR
        self.level_clear_timer = LEVEL_CLEAR_DELAY
        return True