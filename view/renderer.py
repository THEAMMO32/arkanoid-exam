import pygame
from view.colors import *
from utils.constants import *

class Renderer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.close_button_rect = pygame.Rect(width - CLOSE_BUTTON_SIZE - 10, 10, CLOSE_BUTTON_SIZE, CLOSE_BUTTON_SIZE)
        self.close_hover = False

    def draw(self, game_state):
        self.screen.fill(BLACK)

        # Платформа
        prect = game_state.paddle.get_rect()
        pygame.draw.rect(self.screen, PADDLE_COLOR, prect)

        # Мяч
        brect = game_state.ball.get_rect()
        pygame.draw.ellipse(self.screen, BALL_COLOR, brect)

        # Блоки
        for brick in game_state.bricks:
            if brick.alive:
                color = BRICK_COLOR_WEAK if brick.strength == 1 else BRICK_COLOR_STRONG
                pygame.draw.rect(self.screen, color, brick.get_rect())

        # Счёт и жизни
        score_txt = self.font.render(f"Score: {game_state.score}", True, WHITE)
        lives_txt = self.font.render(f"Lives: {game_state.lives}", True, WHITE)
        self.screen.blit(score_txt, (10, 10))
        self.screen.blit(lives_txt, (10, 50))

        # Состояния игры
        if game_state.state == STATE_GAME_OVER:
            text = self.big_font.render("GAME OVER", True, RED)
            self.screen.blit(text, (self.width//2 - text.get_width()//2, self.height//2))
            again = self.font.render("Press R to restart", True, WHITE)
            self.screen.blit(again, (self.width//2 - again.get_width()//2, self.height//2 + 60))
        elif game_state.state == STATE_WIN:
            text = self.big_font.render("YOU WIN!", True, GREEN)
            self.screen.blit(text, (self.width//2 - text.get_width()//2, self.height//2))
            again = self.font.render("Press R to restart", True, WHITE)
            self.screen.blit(again, (self.width//2 - again.get_width()//2, self.height//2 + 60))
        elif game_state.state == STATE_PAUSED:
            text = self.big_font.render("PAUSED", True, WHITE)
            self.screen.blit(text, (self.width//2 - text.get_width()//2, self.height//2))

        # ---- Кнопка закрытия ----
        color = CLOSE_BUTTON_HOVER_COLOR if self.close_hover else CLOSE_BUTTON_COLOR
        pygame.draw.rect(self.screen, color, self.close_button_rect)
        # Рисуем крестик
        margin = 10
        pygame.draw.line(self.screen, WHITE,
                         (self.close_button_rect.x + margin, self.close_button_rect.y + margin),
                         (self.close_button_rect.x + self.close_button_rect.width - margin, self.close_button_rect.y + self.close_button_rect.height - margin), 3)
        pygame.draw.line(self.screen, WHITE,
                         (self.close_button_rect.x + self.close_button_rect.width - margin, self.close_button_rect.y + margin),
                         (self.close_button_rect.x + margin, self.close_button_rect.y + self.close_button_rect.height - margin), 3)

        pygame.display.flip()

    def check_close_click(self, pos):
        """Возвращает True, если кликнули по кнопке закрытия."""
        return self.close_button_rect.collidepoint(pos)

    def update_hover(self, pos):
        """Обновляет состояние наведения на кнопку."""
        self.close_hover = self.close_button_rect.collidepoint(pos)