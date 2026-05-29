import pygame
from view.colors import *
from utils.constants import *
from model.powerup import PowerUp

class Renderer:
    """Отрисовка всех объектов игры."""

    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 28)
        self.close_button_rect = pygame.Rect(
            width - CLOSE_BUTTON_SIZE - 10, 10,
            CLOSE_BUTTON_SIZE, CLOSE_BUTTON_SIZE
        )
        self.close_hover = False
        self._blink_on = True
        self._blink_accum = 0.0

    def draw(self, game_state):
        theme = game_state.theme
        self.screen.fill(theme['bg'])

        # След мяча
        for i, (tx, ty) in enumerate(game_state.ball.trail):
            alpha = int(40 + 140 * (i + 1) / max(1, len(game_state.ball.trail)))
            r = game_state.ball.radius - 1
            surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            c = (*theme['ball'], alpha)
            pygame.draw.circle(surf, c, (r, r), r)
            self.screen.blit(surf, (tx - r, ty - r))

        # Блоки
        for brick in game_state.bricks:
            if brick.alive:
                self._draw_shadow_rect(brick.get_rect(), 2)
                color = theme['strong'] if brick.strength > 1 else theme['weak']
                pygame.draw.rect(self.screen, color, brick.get_rect())

        # Power-ups
        for pu in game_state.powerups:
            rect = pu.get_rect()
            pygame.draw.rect(self.screen, pu.color(), rect, border_radius=3)
            label = self.small_font.render(PowerUp.LABELS.get(pu.kind, '?'), True, BLACK)
            # Исправлено: rect может быть кортежем или Rect, но .center не у кортежа
            if isinstance(rect, tuple):
                center_x = rect[0] + rect[2] // 2
                center_y = rect[1] + rect[3] // 2
                center = (center_x, center_y)
            else:
                center = rect.center
            lr = label.get_rect(center=center)
            self.screen.blit(label, lr)

        # Частицы
        for p in game_state.particles:
            surf = pygame.Surface((p.size * 2, p.size * 2), pygame.SRCALPHA)
            c = (*p.color, p.alpha())
            pygame.draw.rect(surf, c, (0, 0, p.size * 2, p.size * 2))
            self.screen.blit(surf, (p.x - p.size, p.y - p.size))

        # Платформа
        prect = game_state.paddle.get_rect()
        self._draw_shadow_rect(prect, 3)
        paddle_color = theme['paddle']
        if game_state.invincibility_timer > 0:
            self._blink_accum += 1 / 60
            if self._blink_accum >= 0.1:
                self._blink_accum = 0
                self._blink_on = not self._blink_on
            if not self._blink_on:
                paddle_color = tuple(min(255, c + 80) for c in paddle_color)
        pygame.draw.rect(self.screen, paddle_color, prect, border_radius=4)

        # Мяч
        brect = game_state.ball.get_rect()
        pygame.draw.ellipse(self.screen, theme['ball'], brect)

        # Текстовая информация
        score_txt = self.font.render(f"Счёт: {game_state.score}", True, WHITE)
        lives_txt = self.font.render(f"Жизни: {game_state.lives}", True, WHITE)
        lvl_txt = self.font.render(
            f"Уровень: {game_state.level_index + 1}/{LEVEL_COUNT}", True, WHITE
        )
        self.screen.blit(score_txt, (10, 10))
        self.screen.blit(lives_txt, (10, 50))
        self.screen.blit(lvl_txt, (10, 90))
        best_txt = self.font.render(f"Рекорд: {game_state.highscore}", True, WHITE)
        self.screen.blit(best_txt, (self.width - 180, 10))

        self._draw_close_button()

        # Экраны состояний
        if game_state.state == STATE_PAUSED:
            self._draw_overlay("ПАУЗА", "P — продолжить")
        elif game_state.state == STATE_LEVEL_CLEAR:
            n = game_state.level_index + 1
            self._draw_overlay(f"УРОВЕНЬ {n}", "")
        elif game_state.state == STATE_GAME_OVER:
            self._draw_overlay("ИГРА ОКОНЧЕНА", "R — заново  M — меню")
        elif game_state.state == STATE_WIN:
            self._draw_overlay("ПОБЕДА!", "R — заново  M — меню")

        pygame.display.flip()

    def _draw_shadow_rect(self, rect, offset):
        shadow = (rect[0] + offset, rect[1] + offset, rect[2], rect[3])
        pygame.draw.rect(self.screen, (0, 0, 0), shadow)

    def _draw_close_button(self):
        color = CLOSE_BUTTON_HOVER_COLOR if self.close_hover else CLOSE_BUTTON_COLOR
        pygame.draw.rect(self.screen, color, self.close_button_rect)
        margin = 10
        r = self.close_button_rect
        pygame.draw.line(
            self.screen, WHITE,
            (r.x + margin, r.y + margin),
            (r.x + r.width - margin, r.y + r.height - margin), 3
        )
        pygame.draw.line(
            self.screen, WHITE,
            (r.x + r.width - margin, r.y + margin),
            (r.x + margin, r.y + r.height - margin), 3
        )

    def _draw_overlay(self, title, subtitle):
        s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 140))
        self.screen.blit(s, (0, 0))
        t = self.big_font.render(title, True, WHITE)
        self.screen.blit(t, (self.width // 2 - t.get_width() // 2, self.height // 2 - 40))
        if subtitle:
            st = self.font.render(subtitle, True, (200, 200, 200))
            self.screen.blit(st, (self.width // 2 - st.get_width() // 2, self.height // 2 + 30))

    def check_close_click(self, pos):
        return self.close_button_rect.collidepoint(pos)

    def update_hover(self, pos):
        self.close_hover = self.close_button_rect.collidepoint(pos)