"""Обработка ввода с клавиатуры."""

import pygame
import sys
from utils.constants import *


class InputHandler:
    """Переводит нажатия клавиш в флаги и запросы для игрового цикла."""

    def __init__(self):
        self.left = False
        self.right = False
        self.restart_request = False
        self.menu_request = False
        self.next_level_request = False

    def handle_event(self, event, game_state):
        """Обрабатывает одно событие pygame и обновляет флаги."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.left = True
            elif event.key == pygame.K_RIGHT:
                self.right = True
            elif event.key == pygame.K_p:
                if game_state.state == STATE_PAUSED:
                    game_state.state = STATE_RUNNING
                elif game_state.state == STATE_RUNNING:
                    game_state.state = STATE_PAUSED
            elif event.key == pygame.K_r:
                self.restart_request = True
            elif event.key == pygame.K_m:
                if game_state.state in (STATE_GAME_OVER, STATE_WIN):
                    self.menu_request = True
            elif event.key == pygame.K_n:
                if game_state.state == STATE_WIN and game_state.difficulty < 2:
                    self.next_level_request = True
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.left = False
            elif event.key == pygame.K_RIGHT:
                self.right = False

    def reset(self):
        """Сбрасывает все флаги ввода."""
        self.left = False
        self.right = False
        self.restart_request = False
        self.menu_request = False
        self.next_level_request = False
