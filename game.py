import pygame
import sys
from model.game_state import GameState
from view.renderer import Renderer
from controller.input_handler import InputHandler
from controller.game_controller import GameController
from utils.constants import FPS, STATE_RUNNING

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = self.screen.get_size()
        pygame.display.set_caption("Арканоид")
        self.clock = pygame.time.Clock()
        self.running = True

        self.game_state = GameState(self.width, self.height)
        self.renderer = Renderer(self.screen, self.width, self.height)
        self.input_handler = InputHandler()
        self.game_controller = GameController(self.game_state)

    def restart(self):
        self.game_state = GameState(self.width, self.height)
        self.game_controller = GameController(self.game_state)
        self.input_handler.reset()

    def run(self):
        while self.running:
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
                self.restart()
                continue

            if self.game_state.state == STATE_RUNNING:
                self.game_controller.update(
                    self.input_handler.left,
                    self.input_handler.right,
                    dt
                )

            self.renderer.draw(self.game_state)

        pygame.quit()
        sys.exit()