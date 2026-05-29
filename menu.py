import pygame
from utils.constants import *


class Menu:
    """Главное меню и экран рекордов."""

    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 52)
        self.small_font = pygame.font.Font(None, 32)
        self.selected = 0
        self.mode = 'main'
        self.main_options = [
            'Легко',
            'Средне',
            'Сложно',
            'Рекорды',
            'Выход',
        ]

    def draw(self, highscore):
        """Рисует текущий экран меню."""
        self.screen.fill((12, 12, 28))
        title = self.font.render('АРКАНОИД', True, (255, 220, 100))
        self.screen.blit(title, title.get_rect(center=(self.width // 2, self.height // 5)))

        if self.mode == 'records':
            self._draw_records(highscore)
            return

        for i, option in enumerate(self.main_options):
            color = (255, 255, 80) if i == self.selected else (230, 230, 230)
            text = self.font.render(option, True, color)
            self.screen.blit(
                text,
                text.get_rect(center=(self.width // 2, self.height // 2 + i * 52))
            )
        hint = self.small_font.render(
            '↑↓ — выбор   Enter — подтвердить', True, (160, 160, 160)
        )
        self.screen.blit(hint, hint.get_rect(center=(self.width // 2, self.height - 70)))

    def _draw_records(self, highscore):
        """Экран лучшего счёта."""
        rec = self.font.render(f'Рекорд: {highscore}', True, (120, 255, 180))
        self.screen.blit(rec, rec.get_rect(center=(self.width // 2, self.height // 2)))
        back = self.small_font.render('Enter — назад', True, (180, 180, 180))
        self.screen.blit(back, back.get_rect(center=(self.width // 2, self.height // 2 + 60)))

    def handle_event(self, event):
        """Обрабатывает ввод. Возвращает действие или None."""
        if event.type != pygame.KEYDOWN:
            return None
        if self.mode == 'records':
            if event.key in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_BACKSPACE):
                self.mode = 'main'
            return None
        if event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.main_options)
        elif event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.main_options)
        elif event.key == pygame.K_RETURN:
            if self.selected <= 2:
                return ('start', self.selected)
            if self.selected == 3:
                self.mode = 'records'
            if self.selected == 4:
                return 'quit'
        return None
