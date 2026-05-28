import pygame
from utils.constants import STATE_MENU, STATE_RUNNING

class Menu:
    """Экран меню с выбором уровня сложности."""

    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        self.selected = 0
        self.options = ['Level 1', 'Level 2', 'Level 3']
        self.running = True

    def draw(self):
        self.screen.fill((0, 0, 0))
        title = self.font.render('ARKANOID', True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.width//2, self.height//4))
        self.screen.blit(title, title_rect)

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(self.width//2, self.height//2 + i * 50))
            self.screen.blit(text, text_rect)

        info = self.small_font.render('Use UP/DOWN to select, ENTER to start', True, (200, 200, 200))
        info_rect = info.get_rect(center=(self.width//2, self.height - 100))
        self.screen.blit(info, info_rect)

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.selected  # 0,1,2
        return None

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                selected_level = self.handle_event(event)
                if selected_level is not None:
                    return selected_level
            self.draw()
            pygame.time.delay(30)