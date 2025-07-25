import pygame as pg


class MainMenu:
    def __init__(self, screen, SPEEDS, WIDTH, HEIGHT):
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT

        self.screen = screen

        self.EASY_SPEED, self.NORMAL_SPEED, self.HARD_SPEED = SPEEDS

        self.word_speed = self.NORMAL_SPEED

        self.running = True

        self.start_text = "start"
        self.start_items = [(char, "white") for char in self.start_text]
        self.exit_text = "exit"
        self.exit_items = [(char, "white") for char in self.exit_text]
        self.easy_text = "easy"
        self.easy_items = [(char, "white") for char in self.easy_text]
        self.normal_text = "normal"
        self.normal_items = [(char, "white") for char in self.normal_text]
        self.hard_text = "hard"
        self.hard_items = [(char, "white") for char in self.hard_text]

        self.arrow_y = 200

    @staticmethod
    def create_word_surface(items: list[tuple[str, str]],
                            font: pg.font.Font, padding=10):
        """Render a word from (char, color) items into a single surface, and return it with its rect."""
        char_surfaces = []
        total_width = 0
        max_height = 0

        # Render each character surface
        for char, color in items:
            surf = font.render(char, True, color)
            char_surfaces.append(surf)
            total_width += surf.get_width() + padding
            max_height = max(max_height, surf.get_height())

        word_surface = pg.Surface((total_width, max_height), pg.SRCALPHA)
        x = 0
        for surf in char_surfaces:
            word_surface.blit(surf, (x, 0))
            x += surf.get_width() + padding

        return word_surface, word_surface.get_rect()

    def draw_text(self, screen: pg.Surface, text_input: str, items: list,
                  text: str, font_size: int, pos: tuple[int, int]):

        # Create the word surface
        font = pg.font.SysFont("Consolas", font_size)
        word_surface, word_rect = self.create_word_surface(items, font)
        word_rect.center = pos  # Move the box around as needed
        screen.blit(word_surface, word_rect)

    def draw_arrow(self, screen: pg.Surface):
        font = pg.font.SysFont("Consolas", 25)
        arrow_surf = font.render("<", True, "white")
        arrow_rect = arrow_surf.get_rect(center=(870, self.arrow_y))
        screen.blit(arrow_surf, arrow_rect)

    def draw_tip(self, screen: pg.Surface):
        font = pg.font.SysFont("Consolas", 15)
        tip_surf = font.render("(spacebar = clear text)", True, "white")
        tip_rect = tip_surf.get_rect(center=(115, self.HEIGHT - 25))
        screen.blit(tip_surf, tip_rect)

    def draw(self, screen: pg.Surface, text_input):
        self.draw_text(screen, text_input, self.start_items, self.start_text,
                       80, (self.WIDTH // 2, 200))
        self.draw_text(screen, text_input, self.exit_items, self.exit_text,
                       30, (self.WIDTH // 2, 400))

        self.draw_text(screen, text_input, self.easy_items, self.easy_text,
                       25, (780, 150))
        self.draw_text(screen, text_input, self.normal_items, self.normal_text,
                       25, (780, 200))
        self.draw_text(screen, text_input, self.hard_items, self.hard_text,
                       25, (780, 250))

        self.draw_arrow(screen)
        self.draw_tip(screen)

    def update(self, text_input, check_word):
        items_list = [
            self.start_items, self.exit_items, self.easy_items,
            self.normal_items, self.hard_items
        ]
        correct_text_list = [
            self.start_text, self.exit_text, self.easy_text,
            self.normal_text, self.hard_text
        ]
        check_word(items_list, correct_text_list)

        if text_input == self.start_text:
            return "s"

        elif text_input == self.exit_text:
            return "e"

        elif text_input == self.easy_text:
            self.arrow_y = 150
            return self.EASY_SPEED

        elif text_input == self.normal_text:
            self.arrow_y = 200
            return self.NORMAL_SPEED

        elif text_input == self.hard_text:
            self.arrow_y = 250
            return self.HARD_SPEED


class GameOver:
    def __init__(self, screen, LIVES, WIDTH, HEIGHT):
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT

        self.screen = screen
        self.LIVES = LIVES

        self.in_game_lives = 0

        self.running = True
        self.main = False
        self.exit = False

        self.main_text = "main"
        self.main_items = [(char, "white") for char in self.main_text]
        self.exit_text = "exit"
        self.exit_items = [(char, "white") for char in self.exit_text]

    def initialize(self):
        self.in_game_lives = self.LIVES

    def update(self, text_input, check_word):
        items_list = [self.main_items, self.exit_items]
        correct_text_list = [self.main_text, self.exit_text]
        check_word(items_list, correct_text_list)

        if text_input == self.main_text:
            self.main = True

        if text_input == self.exit_text:
            self.exit = True

    @staticmethod
    def create_word_surface(items: list[tuple[str, str]],
                            font: pg.font.Font, padding=10):
        """Render a word from (char, color) items into a single surface, and return it with its rect."""
        char_surfaces = []
        total_width = 0
        max_height = 0

        # Render each character surface
        for char, color in items:
            surf = font.render(char, True, color)
            char_surfaces.append(surf)
            total_width += surf.get_width() + padding
            max_height = max(max_height, surf.get_height())

        word_surface = pg.Surface((total_width, max_height), pg.SRCALPHA)
        x = 0
        for surf in char_surfaces:
            word_surface.blit(surf, (x, 0))
            x += surf.get_width() + padding

        return word_surface, word_surface.get_rect()

    def draw_text(self, screen: pg.Surface, items: list, font_size: int,
                  pos: tuple[int, int], padding: int = 10):

        # Create the word surface
        font = pg.font.SysFont("Consolas", font_size)
        word_surface, word_rect = self.create_word_surface(items, font, padding)
        word_rect.center = pos  # Move the box around as needed
        screen.blit(word_surface, word_rect)

    def draw(self, screen, text_input, score):
        self.draw_text(screen, self.main_items, 30,
                       (self.WIDTH // 2 - 70, 370), padding=5)

        self.draw_text(screen, self.exit_items, 30,
                       (self.WIDTH // 2 + 70, 370), padding=5)

        font = pg.font.SysFont("Consolas", 80)
        gg_surf = font.render("GAME OVER", True, "red")
        gg_rect = gg_surf.get_rect(center=(self.WIDTH // 2, 160))
        screen.blit(gg_surf, gg_rect)

        font = pg.font.SysFont("Consolas", 40)
        score_surf = font.render(f"score: {score}", True, "white")
        score_rect = score_surf.get_rect(center=(self.WIDTH // 2, 230))
        screen.blit(score_surf, score_rect)
