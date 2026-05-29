import pygame
import sys
from utils.constants import *


class InputHandler:
    """Обработка ввода с клавиатуры."""

    def __init__(self):
        self.left = False
        self.right = False
        self.restart_request = False
        self.menu_request = False

    def handle_event(self, event, game_state):
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
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.left = False
            elif event.key == pygame.K_RIGHT:
                self.right = False

    def reset(self):
        self.left = False
        self.right = False
        self.restart_request = False
        self.menu_request = False
