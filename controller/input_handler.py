import pygame
from utils.constants import STATE_PAUSED

class InputHandler:
    def __init__(self):
        self.left = False
        self.right = False
        self.restart_request = False

    def handle_event(self, event, game_state):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.left = True
            elif event.key == pygame.K_RIGHT:
                self.right = True
            elif event.key == pygame.K_p:
                if game_state.state == STATE_PAUSED:
                    game_state.state = STATE_RUNNING
                else:
                    game_state.state = STATE_PAUSED
            elif event.key == pygame.K_r:
                self.restart_request = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.left = False
            elif event.key == pygame.K_RIGHT:
                self.right = False

    def reset(self):
        self.left = False
        self.right = False
        self.restart_request = False
