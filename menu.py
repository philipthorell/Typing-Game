import pygame as pg


class MainMenu:
    def __init__(self, screen, SPEEDS, WIDTH, HEIGHT):
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT

        self.screen = screen

        self.EASY_SPEED, self.NORMAL_SPEED, self.HARD_SPEED = SPEEDS

        self.word_speed = self.NORMAL_SPEED

        self.running = True

        self.start_text = "start"
        self.start_items = [(char, (255, 255, 255)) for char in self.start_text]
        self.exit_text = "exit"
        self.exit_items = [(char, (255, 255, 255)) for char in self.exit_text]
        self.easy_text = "easy"
        self.easy_items = [(char, (255, 255, 255)) for char in self.easy_text]
        self.normal_text = "normal"
        self.normal_items = [(char, (255, 255, 255)) for char in self.normal_text]
        self.hard_text = "hard"
        self.hard_items = [(char, (255, 255, 255)) for char in self.hard_text]

        self.arrow_y = 200

    def check_word(self, typed_word: str, items: list[tuple[str, tuple[int, int, int]]], correct_text: str):
        typed_letters = min(len(typed_word), len(correct_text))

        # Start with everything white
        for i in range(len(items)):
            items[i] = (correct_text[i], (255, 255, 255))  # white

        # Apply green color progressively if each letter is correct
        if typed_letters > 0 and typed_word[0] == correct_text[0]:
            items[0] = (correct_text[0], (0, 255, 0))  # green

            for i in range(1, typed_letters):
                if typed_word[i] == correct_text[i] and items[i - 1][1] == (0, 255, 0):
                    items[i] = (correct_text[i], (0, 255, 0))  # green
                else:
                    break

    @staticmethod
    def create_word_surface(items: list[tuple[str, tuple[int, int, int]]],
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

        self.check_word(text_input, items, text)
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

    def start(self, text_input):
        if text_input == self.start_text:
            return "s"

        elif text_input == self.exit_text:
            print("EXIT")
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

        self.score = 0
        self.in_game_lives = 0

        self.running = True

        self.main_text = "main"
        self.main_items = []
        self.exit_text = "exit"
        self.exit_items = []

    def initialize(self):
        self.create_text_items(
            self.canvas,
            self.main_text,
            470,
            self.HEIGHT / 2 + self.HEIGHT / 5 + self.HEIGHT / 24,
            self.main_items
        )
        self.create_text_items(
            self.canvas,
            self.exit_text,
            470,
            self.HEIGHT / 2 + self.HEIGHT / 3,
            self.exit_items
        )

        self.game_over_text = self.canvas.create_text(
            self.WIDTH / 2,
            self.HEIGHT / 2 - self.HEIGHT / 4 + self.HEIGHT / 8,
            text="GAME OVER",
            font=("Consolas", 80),
            fill="#FF0000"
        )
        self.score_text = self.canvas.create_text(
            self.WIDTH / 2,
            self.HEIGHT / 2 + self.HEIGHT / 4 - self.HEIGHT / 8 - self.HEIGHT / 16 - self.HEIGHT / 32,
            text=f"score: {self.score}",
            font=("Consolas", 40),
            fill="white"
        )

        self.in_game_lives = self.LIVES
        self.score = 0

        self.screen.bind("<Destroy>", self.close_window)

    def close_window(self, event):
        self.running = False

    def start(self):
        self.initialize()

        return self.game_over()

    def check_word(self, typed_word, items, text):

        typed_letters = min(len(typed_word), len(text))

        # Check if the first letter is correct
        if typed_letters > 0 and typed_word[0] == text[0]:
            self.canvas.itemconfig(items[0], fill="#00FF00")  # Set the color to green

        # Check if subsequent letters are correct and the preceding letter is green
        for i in range(1, typed_letters):
            if typed_word[i] == text[i] and self.canvas.itemcget(items[i - 1], "fill") == "#00FF00":
                self.canvas.itemconfig(items[i], fill="#00FF00")  # Set the color to green
            else:
                for i in range(len(text)):
                    self.canvas.itemconfig(items[i], fill="white")
                break  # Stop setting colors if the preceding letter is not green

        # Reset the color of remaining letters in self.word
        for i in range(typed_letters, len(text)):
            self.canvas.itemconfig(items[i], fill="white")

    def create_text_items(self, canvas, text, x, y, items_list):
        for char in text:
            item_id = canvas.create_text(x, y, text=char, font=("Consolas", 25), fill="white")
            items_list.append(item_id)
            x += 20

    def game_over(self):
        while self.running:
            if self.text_area.get() == self.main_text:
                self.text_area.delete(0, END)
                self.canvas.delete(*self.main_items)
                self.canvas.delete(*self.exit_items)
                self.canvas.delete(self.game_over_text)
                self.canvas.delete(self.score_text)
                self.main_items = []
                self.exit_items = []
                return True

            self.check_word(self.text_area.get(), self.main_items, self.main_text)
            self.check_word(self.text_area.get(), self.exit_items, self.exit_text)

            if self.text_area.get() == self.exit_text:
                return False

            self.screen.update()
            sleep(0.01)
