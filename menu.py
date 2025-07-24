from tkinter import END
from time import sleep


class MainMenu:
    def __init__(self, screen, canvas, text_area, SPEEDS, WIDTH, HEIGHT):
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT

        self.screen = screen
        self.canvas = canvas
        self.text_area = text_area

        self.EASY_SPEED, self.NORMAL_SPEED, self.HARD_SPEED = SPEEDS

        self.word_speed = self.NORMAL_SPEED

        self.running = True
        self.initialized = False

    def initialize(self):
        self.start_text = "start"
        self.start_items = []
        self.create_text_items(self.canvas, self.start_text, 400, 200, 80, self.start_items)

        self.exit_text = "exit"
        self.exit_items = []
        self.create_text_items(self.canvas, self.exit_text, 470, 400, 30, self.exit_items)

        self.easy_text = "easy"
        self.easy_items = []
        self.create_text_items(self.canvas, self.easy_text, 720, 150, 25, self.easy_items)

        self.normal_text = "normal"
        self.normal_items = []
        self.create_text_items(self.canvas, self.normal_text, 700, 200, 25, self.normal_items)

        self.hard_text = "hard"
        self.hard_items = []
        self.create_text_items(self.canvas, self.hard_text, 720, 250, 25, self.hard_items)

        self.arrow = self.canvas.create_text(830, 200, text="<", font=("Consolas", 25), fill="white")
        self.tip = self.canvas.create_text(150, self.HEIGHT - 40, text="(spacebar = clear text)", font=("Consolas", 15),
                                      fill="white")

        self.screen.bind("<Destroy>", self.close_window)
        self.screen.bind("<space>", self.clear_text_area)

    def close_window(self, event):
        self.running = False

    def start(self):
        self.initialize()

        return self.main_menu()

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

    def clear_text_area(self, event):
        self.text_area.delete(0, END)

    def create_text_items(self, canvas, text, x, y, font_size, items_list):
        for char in text:
            item_id = canvas.create_text(x, y, text=char, font=("Consolas", font_size), fill="white")
            items_list.append(item_id)
            x += 55 if font_size == 80 else 20  # Adjust x position based on font size

    def main_menu(self):

        while self.running:
            if self.text_area.get() == "start":
                self.text_area.delete(0, END)
                self.canvas.delete(self.arrow)
                self.canvas.delete(self.tip)

                items_lists = [
                    self.start_items,
                    self.exit_items,
                    self.easy_items,
                    self.normal_items,
                    self.hard_items
                ]
                for items_list in items_lists:
                    self.canvas.delete(*items_list)

                return True

            if self.text_area.get() == "exit":
                return False

            self.check_word(self.text_area.get(), self.start_items, self.start_text)
            self.check_word(self.text_area.get(), self.exit_items, self.exit_text)
            self.check_word(self.text_area.get(), self.easy_items, self.easy_text)
            self.check_word(self.text_area.get(), self.normal_items, self.normal_text)
            self.check_word(self.text_area.get(), self.hard_items, self.hard_text)

            if self.text_area.get() == "easy":
                self.canvas.coords(self.arrow, 830, 150)
                self.word_speed = self.EASY_SPEED
                self.text_area.delete(0, END)
            elif self.text_area.get() == "normal":
                self.canvas.coords(self.arrow, 830, 200)
                self.word_speed = self.NORMAL_SPEED
                self.text_area.delete(0, END)
            elif self.text_area.get() == "hard":
                self.canvas.coords(self.arrow, 830, 250)
                self.word_speed = self.HARD_SPEED
                self.text_area.delete(0, END)

            self.screen.update()
            sleep(0.01)


class GameOver:
    def __init__(self, screen, canvas, text_area, LIVES, WIDTH, HEIGHT):
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT

        self.screen = screen
        self.canvas = canvas
        self.text_area = text_area
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
