"""Отрисовка всех объектов игры."""

import pygame
from view.colors import *
from utils.constants import *
from utils.constants import WALL_COLOR
from model.powerup import PowerUp


class Renderer:
    """Отрисовка игрового поля, интерфейса и overlays."""

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
        """Отрисовывает полный кадр игры."""
        theme = game_state.theme
        self.screen.fill(theme['bg'])

        for ball in game_state.balls:
            for i, (tx, ty) in enumerate(ball.trail):
                alpha = int(40 + 140 * (i + 1) / max(1, len(ball.trail)))
                r = ball.radius - 1
                surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                c = (*theme['ball'], alpha)
                pygame.draw.circle(surf, c, (r, r), r)
                self.screen.blit(surf, (tx - r, ty - r))

        for brick in game_state.bricks:
            if brick.alive:
                self._draw_shadow_rect(brick.get_rect(), 2)
                if brick.indestructible:
                    color = theme['indestructible']
                    rect = brick.get_rect()
                    pygame.draw.rect(self.screen, color, rect)
                    pygame.draw.rect(self.screen, WHITE, rect, 2)
                    m = 6
                    pygame.draw.line(
                        self.screen, WHITE,
                        (rect[0] + m, rect[1] + m),
                        (rect[0] + rect[2] - m, rect[1] + rect[3] - m),
                        2
                    )
                    pygame.draw.line(
                        self.screen, WHITE,
                        (rect[0] + rect[2] - m, rect[1] + m),
                        (rect[0] + m, rect[1] + rect[3] - m),
                        2
                    )
                else:
                    color = (
                        theme['strong'] if brick.strength > 1
                        else theme['weak']
                    )
                    pygame.draw.rect(self.screen, color, brick.get_rect())

        for wall in game_state.walls:
            self._draw_shadow_rect(wall.get_rect(), 2)
            pygame.draw.rect(
                self.screen, WALL_COLOR, wall.get_rect(), border_radius=3
            )

        for pu in game_state.powerups:
            rect = pu.get_rect()
            pygame.draw.rect(
                self.screen, pu.color(), rect, border_radius=3
            )
            label = self.small_font.render(
                PowerUp.LABELS.get(pu.kind, '?'), True, BLACK
            )
            if isinstance(rect, tuple):
                center_x = rect[0] + rect[2] // 2
                center_y = rect[1] + rect[3] // 2
                center = (center_x, center_y)
            else:
                center = rect.center
            lr = label.get_rect(center=center)
            self.screen.blit(label, lr)

        for p in game_state.particles:
            surf = pygame.Surface((p.size * 2, p.size * 2), pygame.SRCALPHA)
            c = (*p.color, p.alpha())
            pygame.draw.rect(surf, c, (0, 0, p.size * 2, p.size * 2))
            self.screen.blit(surf, (p.x - p.size, p.y - p.size))

        prect = game_state.paddle.get_rect()
        self._draw_shadow_rect(prect, 3)
        paddle_color = theme['paddle']
        if game_state.invincibility_timer > 0:
            self._blink_accum += 1 / 60
            if self._blink_accum >= 0.1:
                self._blink_accum = 0
                self._blink_on = not self._blink_on
            if not self._blink_on:
                paddle_color = tuple(
                    min(255, c + 80) for c in paddle_color
                )
        pygame.draw.rect(
            self.screen, paddle_color, prect, border_radius=4
        )

        for ball in game_state.balls:
            brect = ball.get_rect()
            pygame.draw.ellipse(self.screen, theme['ball'], brect)

        score_txt = self.font.render(
            f"Счёт: {game_state.score}", True, WHITE
        )
        lives_txt = self.font.render(
            f"Жизни: {game_state.lives}", True, WHITE
        )
        self.screen.blit(score_txt, (10, 10))
        self.screen.blit(lives_txt, (10, 50))
        best_txt = self.font.render(
            f"Рекорд: {game_state.highscore}", True, WHITE
        )
        best_x = self.close_button_rect.x - 20 - best_txt.get_width()
        self.screen.blit(best_txt, (best_x, 10))

        self._draw_close_button()

        if game_state.state == STATE_PAUSED:
            self._draw_overlay("ПАУЗА", "P — продолжить")
        elif game_state.state == STATE_GAME_OVER:
            self._draw_overlay(
                "ИГРА ОКОНЧЕНА", "R — заново  M — меню"
            )
        elif game_state.state == STATE_WIN:
            subtitle = "R — повторить  M — меню"
            if game_state.difficulty < 2:
                subtitle += "  N — следующая сложность"
            self._draw_overlay("ПОБЕДА!", subtitle)

        pygame.display.flip()

    def _draw_shadow_rect(self, rect, offset):
        """Отрисовывает тень прямоугольника со смещением."""
        shadow = (rect[0] + offset, rect[1] + offset, rect[2], rect[3])
        pygame.draw.rect(self.screen, (0, 0, 0), shadow)

    def _draw_close_button(self):
        """Отрисовывает кнопку закрытия (✕) в правом верхнем углу."""
        color = (
            CLOSE_BUTTON_HOVER_COLOR if self.close_hover
            else CLOSE_BUTTON_COLOR
        )
        pygame.draw.rect(self.screen, color, self.close_button_rect)
        margin = 10
        r = self.close_button_rect
        pygame.draw.line(
            self.screen, WHITE,
            (r.x + margin, r.y + margin),
            (r.x + r.width - margin, r.y + r.height - margin),
            3
        )
        pygame.draw.line(
            self.screen, WHITE,
            (r.x + r.width - margin, r.y + margin),
            (r.x + margin, r.y + r.height - margin),
            3
        )

    def _draw_overlay(self, title, subtitle):
        """Отрисовывает полупрозрачный overlay с заголовком и подзаголовком."""
        s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 140))
        self.screen.blit(s, (0, 0))
        t = self.big_font.render(title, True, WHITE)
        self.screen.blit(
            t,
            (self.width // 2 - t.get_width() // 2, self.height // 2 - 40)
        )
        if subtitle:
            st = self.font.render(subtitle, True, (200, 200, 200))
            self.screen.blit(
                st,
                (
                    self.width // 2 - st.get_width() // 2,
                    self.height // 2 + 30
                )
            )

    def check_close_click(self, pos):
        """Проверяет, что клик попал в кнопку закрытия."""
        return self.close_button_rect.collidepoint(pos)

    def update_hover(self, pos):
        """Обновляет состояние hover для кнопки закрытия."""
        self.close_hover = self.close_button_rect.collidepoint(pos)
