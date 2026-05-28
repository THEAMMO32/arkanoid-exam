import pygame
import sys
from model.game_state import GameState
from view.renderer import Renderer
from controller.input_handler import InputHandler
from controller.game_controller import GameController
from utils.constants import FPS, STATE_RUNNING, STATE_MENU
from menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = self.screen.get_size()
        pygame.display.set_caption("Арканоид")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = None
        self.renderer = None
        self.input_handler = None
        self.game_controller = None
        self.current_state = STATE_MENU

    def set_difficulty(self, level):
        """Устанавливает параметры игры в зависимости от выбранного уровня."""
        global BALL_SPEED_X, BALL_SPEED_Y, PADDLE_WIDTH
        from utils.constants import BALL_SPEED_X, BALL_SPEED_Y, PADDLE_WIDTH
        if level == 0:  # Easy
            BALL_SPEED_X = 250
            BALL_SPEED_Y = -250
            PADDLE_WIDTH = 150
            self.brick_strength_mode = 'all_weak'
        elif level == 1:  # Medium
            BALL_SPEED_X = 350
            BALL_SPEED_Y = -350
            PADDLE_WIDTH = 120
            self.brick_strength_mode = 'default'
        else:  # Hard
            BALL_SPEED_X = 450
            BALL_SPEED_Y = -450
            PADDLE_WIDTH = 90
            self.brick_strength_mode = 'all_strong'

        # Пересоздаём игру с новыми параметрами
        self.game_state = GameState(self.width, self.height, self.brick_strength_mode)
        self.renderer = Renderer(self.screen, self.width, self.height)
        self.input_handler = InputHandler()
        self.game_controller = GameController(self.game_state)

    def run(self):
        while self.running:
            if self.current_state == STATE_MENU:
                menu = Menu(self.screen, self.width, self.height)
                selected = menu.run()
                if selected is not None:
                    self.set_difficulty(selected)
                    self.current_state = STATE_RUNNING
            elif self.current_state == STATE_RUNNING:
                dt = self.clock.tick(FPS) / 1000.0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.renderer.check_close_click(event.pos):
                            self.running = False
                    elif event.type == pygame.MOUSEMOTION:
                        self.renderer.update_hover(event.pos)
                    self.input_handler.handle_event(event, self.game_state)

                if self.input_handler.restart_request:
                    # рестарт с текущими параметрами сложности
                    self.game_state = GameState(self.width, self.height, self.brick_strength_mode)
                    self.game_controller = GameController(self.game_state)
                    self.input_handler.reset()
                    continue

                if self.game_state.state == STATE_RUNNING:
                    self.game_controller.update(
                        self.input_handler.left,
                        self.input_handler.right,
                        dt
                    )

                self.renderer.draw(self.game_state)

                # если игра закончена (win/game over) - можно вернуться в меню по нажатию R?
                # пока оставим как есть.
            else:
                pass

        pygame.quit()
        sys.exit()