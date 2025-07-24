from tkinter import Tk, Entry, Canvas, END

from game import Game
from menu import MainMenu, GameOver


class Window:
    WIDTH, HEIGHT = 1000, 500  # Aspect ratio must be 2:1

    EASY_SPEED = 0.5  # 0.5
    NORMAL_SPEED = 1  # 1
    HARD_SPEED = 1.5  # 1.5
    LIVES = 3  # 3
    NUM_OF_ENEMIES = 5  # 5

    def __init__(self):

        S_WORDS = "swedish_words.txt"
        E_WORDS = "english_words.txt"

        with open(S_WORDS, "r") as file:
            WORD_LIST = file.readlines()

        self.running = True
        self.word_speed = self.NORMAL_SPEED
        self.in_game_lives = self.LIVES

        self.screen = Tk()
        self.screen.title("Typing Game")
        self.screen.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.screen.resizable(False, False)

        self.text_area = Entry(self.screen)
        self.text_area.place(x=0, y=0)
        self.text_area.focus()

        self.typed_word = self.text_area.get()

        self.canvas = Canvas(
            self.screen,
            width=self.WIDTH,
            height=self.HEIGHT,
            background="black"
        )
        self.canvas.pack()

        self.screen.bind("<Destroy>", self.close_window)

        self.game = Game(
            self.screen,
            self.canvas,
            WORD_LIST,
            self.NORMAL_SPEED,
            self.text_area,
            self.LIVES,
            self.NUM_OF_ENEMIES,
            self.WIDTH,
            self.HEIGHT
        )
        self.main_menu = MainMenu(
            self.screen,
            self.canvas,
            self.text_area,
            (self.EASY_SPEED, self.NORMAL_SPEED, self.HARD_SPEED),
            self.WIDTH,
            self.HEIGHT
        )
        self.game_over = GameOver(
            self.screen,
            self.canvas,
            self.text_area,
            self.LIVES,
            self.WIDTH,
            self.HEIGHT
        )

    def clear_text_area(self, event):
        self.text_area.delete(0, END)

    def close_window(self, event):
        self.running = False

    def loop(self):
        while self.running:
            if not self.main_menu.start():
                print("MENU")
                break
            if not self.game.start():
                print("GAME")
                break
            if not self.game_over.start():
                print("GAME-OVER")
                break

            self.screen.update()


if __name__ == "__main__":
    window = Window()
    window.loop()
