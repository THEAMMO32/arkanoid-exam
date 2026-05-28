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

    def draw(self, game_state):
        self.screen.fill(BLACK)

        prect = game_state.paddle.get_rect()
        pygame.draw.rect(self.screen, PADDLE_COLOR, prect)

        brect = game_state.ball.get_rect()
        pygame.draw.ellipse(self.screen, BALL_COLOR, brect)

        for brick in game_state.bricks:
            if brick.alive:
                color = BRICK_COLOR_WEAK if brick.strength == 1 else BRICK_COLOR_STRONG
                pygame.draw.rect(self.screen, color, brick.get_rect())

        score_txt = self.font.render(f"Score: {game_state.score}", True, WHITE)
        lives_txt = self.font.render(f"Lives: {game_state.lives}", True, WHITE)
        self.screen.blit(score_txt, (10, 10))
        self.screen.blit(lives_txt, (10, 50))

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

        pygame.display.flip()