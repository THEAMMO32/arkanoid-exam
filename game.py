"""Главный класс игры: инициализация, игровой цикл, переходы состояний."""

import pygame
import sys
from model.game_state import GameState
from view.renderer import Renderer
from controller.input_handler import InputHandler
from controller.game_controller import GameController
from utils.constants import *
from utils.highscore import load_highscore, save_highscore
from utils.audio import AudioManager
from menu import Menu


class Game:
    """Главный цикл приложения."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = self.screen.get_size()
        pygame.display.set_caption("Арканоид")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = STATE_MENU
        self.difficulty = 1
        self.highscore = load_highscore()
        self.audio = AudioManager()
        self.audio.start_music()
        self.game_state = None
        self.renderer = None
        self.input_handler = None
        self.game_controller = None
        self.menu = Menu(self.screen, self.width, self.height)
        self._prev_play_state = None

    def start_game(self, difficulty):
        """Начинает новую сессию с выбранной сложностью."""
        self.difficulty = difficulty
        self.game_state = GameState(
            self.width, self.height,
            difficulty=difficulty,
            highscore=self.highscore,
            speed_mul=1.0
        )
        self.renderer = Renderer(self.screen, self.width, self.height)
        self.input_handler = InputHandler()
        self.game_controller = GameController(self.game_state, self.audio)
        self.current_state = STATE_RUNNING
        self._prev_play_state = STATE_RUNNING

    def restart_game(self):
        """Перезапускает текущую сложность заново (счёт сбрасывается)."""
        self._prev_play_state = None
        self.start_game(self.difficulty)

    def restart_current_level(self):
        """Повторяет текущую сложность, сохраняя набранный счёт."""
        saved_score = self.game_state.score
        self.start_game(self.difficulty)
        self.game_state.score = saved_score
        self._prev_play_state = STATE_RUNNING

    def update_highscore(self):
        """Сохраняет рекорд при улучшении счёта."""
        if self.game_state and self.game_state.score > self.highscore:
            self.highscore = self.game_state.score
            self.game_state.highscore = self.highscore
            save_highscore(self.highscore)

    def run(self):
        """Основной игровой цикл."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            if self.current_state == STATE_MENU:
                self._run_menu()
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.renderer and self.renderer.check_close_click(
                        event.pos
                    ):
                        self.running = False
                elif event.type == pygame.MOUSEMOTION and self.renderer:
                    self.renderer.update_hover(event.pos)
                self.input_handler.handle_event(event, self.game_state)

            if self.input_handler.menu_request:
                self.menu.set_results(
                    self.game_state.score, self.highscore
                )
                self.current_state = STATE_MENU
                self.input_handler.reset()
                self.audio.resume_music()
                continue

            if self.input_handler.restart_request:
                if self.game_state.state == STATE_WIN:
                    self.restart_current_level()
                else:
                    self.restart_game()
                continue

            if self.game_state.state == STATE_PAUSED:
                self.audio.pause_music()
            else:
                self.audio.resume_music()

            if self.game_state.state == STATE_RUNNING:
                self.game_controller.update(
                    self.input_handler.left,
                    self.input_handler.right,
                    dt
                )
            elif self.game_state.state == STATE_WIN:
                self.game_controller.update(0, 0, dt)

            self.update_highscore()
            self._play_state_sounds()

            if self.input_handler.next_level_request:
                self.input_handler.reset()
                if self.game_state.difficulty < 2:
                    saved_score = self.game_state.score
                    self.start_game(self.game_state.difficulty + 1)
                    self.game_state.score = saved_score
                else:
                    self.menu.set_results(
                        self.game_state.score, self.highscore
                    )
                    self.current_state = STATE_MENU
                    continue

            self.renderer.draw(self.game_state)

        pygame.quit()
        sys.exit()

    def _run_menu(self):
        """Кадр главного меню."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            action = self.menu.handle_event(event)
            if action == 'quit':
                self.running = False
                return
            if action == 'back_to_menu':
                self.menu.mode = 'main'
                self.menu.selected = 0
                return
            if isinstance(action, tuple) and action[0] == 'start':
                self.start_game(action[1])
                return
        self.menu.draw(self.highscore)
        pygame.display.flip()
        self.clock.tick(FPS)

    def _play_state_sounds(self):
        """Проигрывает звук один раз при смене состояния."""
        st = self.game_state.state
        if st != self._prev_play_state:
            if st == STATE_GAME_OVER and self.audio:
                self.audio.play_lose()
            self._prev_play_state = st
