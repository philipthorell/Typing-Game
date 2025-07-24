import pygame as pg

from gameplay import Gameplay
from menu import MainMenu, GameOver


class Game:
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

        pg.font.init()
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption("Typing Game")
        self.clock = pg.time.Clock()
        self.FPS = 60

        self.text_input = ""

        self.main_menu = True
        self.gameplay = False
        self.game_over = False

        self.gameplay_screen = Gameplay(
            self.screen,
            WORD_LIST,
            self.NORMAL_SPEED,
            self.LIVES,
            self.NUM_OF_ENEMIES,
            self.WIDTH,
            self.HEIGHT
        )
        self.main_menu_screen = MainMenu(
            self.screen,
            (self.EASY_SPEED, self.NORMAL_SPEED, self.HARD_SPEED),
            self.WIDTH,
            self.HEIGHT
        )
        self.game_over_screen = GameOver(
            self.screen,
            self.LIVES,
            self.WIDTH,
            self.HEIGHT
        )

    def update(self):
        if self.main_menu:
            recv = self.main_menu_screen.start(self.text_input)
            if type(recv) is str:
                if recv == "s":
                    self.main_menu = False
                    self.gameplay = True
                else:
                    self.running = False
            elif type(recv) is float or type(recv) is int:
                self.word_speed = recv
                self.text_input = ""

        elif self.gameplay:
            pass

        elif self.game_over:
            pass

    def draw(self):
        self.screen.fill("black")
        if self.main_menu:
            self.main_menu_screen.draw(self.screen, self.text_input)

        elif self.gameplay:
            pass

        elif self.game_over:
            pass

    def run(self):
        while self.running:
            # Handle events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.text_input = self.text_input[:-1]
                    elif event.key == pg.K_SPACE:
                        self.text_input = ""
                    else:
                        self.text_input += event.unicode

            self.update()

            self.draw()

            pg.display.flip()

            self.clock.tick(self.FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
