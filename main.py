import pygame as pg

from gameplay import Gameplay
from menu import MainMenu, GameOver


# TODO:
#   FIX, WHEN TYPING WRONG AT THE START, ALL WORDS SHOULD TURN RED
#   ADD, WORD-PACKS (INCLUDING CUSTOM WORD-PACKS)
#   FIX, SO THAT WHEN USER TYPES THE END OF A WORD WRONG AND CONTINUE TO TYPE, THEY ONLY NEED
#        TO REMOVE THE LAST LETTERS OF THE WORD (INSTEAD OF THE "INVISIBLE" ONES AT THE FAR BACK)
#   FIX, SO THAT WORDS CAN'T SPAWN INSIDE EACH OTHER


class Game:
    WIDTH, HEIGHT = 1000, 500  # Aspect ratio must be 2:1

    EASY_SPEED = 0.5  # 0.5
    NORMAL_SPEED = 1  # 1
    HARD_SPEED = 1.5  # 1.5
    LIVES = 3  # 3
    NUM_OF_ENEMIES = 5  # 5
    score = 0

    def __init__(self):

        S_WORDS = "swedish_words.txt"
        E_WORDS = "english_words.txt"

        with open(S_WORDS, "r") as file:
            WORD_LIST = [word.replace("\n", "") for word in file.readlines()]

        self.running = True
        self.word_speed = self.NORMAL_SPEED
        self.in_game_lives = self.LIVES

        pg.font.init()
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption("Typing Game")
        self.clock = pg.time.Clock()
        self.FPS = 60

        self.white_color = "white"
        self.green_color = "green"
        self.red_color = "red"

        self.text_input = ""

        self.main_menu = True
        self.gameplay = False
        self.game_over = False

        self.gameplay_screen = Gameplay(
            self.screen,
            WORD_LIST,
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

    def check_word(self, items_list: list[list[tuple[str, str]]], correct_text_list: list[str]):
        for idx, items in enumerate(items_list):
            correct_text = correct_text_list[idx]
            typed_letters = len(self.text_input)

            # Start with everything white
            for i in range(len(items)):
                items[i] = (correct_text[i], self.white_color)

            # Apply green color progressively if each letter is correct
            if typed_letters > 0 and self.text_input[0] == correct_text[0]:
                items[0] = (correct_text[0], self.green_color)

                for i in range(1, typed_letters):
                    try:
                        if items[i - 1][1] == self.green_color:
                            if self.text_input[i] == correct_text[i]:
                                items[i] = (correct_text[i], self.green_color)
                            else:
                                do_red = True
                                for items2 in items_list:
                                    if items2 == items:
                                        continue
                                    try:
                                        if items2[i][1] == self.green_color:
                                            do_red = False
                                    except IndexError:
                                        print("skipping word:", "".join([letters[0] for letters in items2]))
                                        continue
                                if do_red:
                                    items[i] = (correct_text[i], self.red_color)
                                else:
                                    for j in range(len(correct_text)):
                                        items[j] = (correct_text[j], self.white_color)

                        elif items[i - 1][1] == self.red_color:
                            items[i] = (correct_text[i], self.red_color)

                    except IndexError:
                        print(typed_letters)
                        print(i)
                        print("".join([letters[0] for letters in items]))
                        break

    def update(self):
        if self.main_menu:
            recv = self.main_menu_screen.update(self.text_input, self.check_word)
            if type(recv) is str:
                if recv == "s":
                    self.main_menu = False
                    self.gameplay = True
                    self.text_input = ""
                else:
                    self.running = False
            elif type(recv) is float or type(recv) is int:
                self.word_speed = recv
                self.text_input = ""

        elif self.gameplay:
            self.gameplay_screen.update(self.text_input, self.word_speed, self.check_word)
            if self.gameplay_screen.typed_word:
                self.text_input = ""
                self.score += 1
                self.gameplay_screen.typed_word = False
            if self.gameplay_screen.lost:
                self.gameplay = False
                self.game_over = True
                self.text_input = ""
                self.gameplay_screen.lost = False

        elif self.game_over:
            self.game_over_screen.update(self.text_input, self.check_word)
            if self.game_over_screen.main:
                self.game_over = False
                self.main_menu = True
                self.text_input = ""
                self.score = 0
                self.game_over_screen.main = False
            elif self.game_over_screen.exit:
                self.running = False

    def draw(self):
        self.screen.fill("black")
        if self.main_menu:
            self.main_menu_screen.draw(self.screen, self.text_input)

        elif self.gameplay:
            self.gameplay_screen.draw(self.screen, self.score)

        elif self.game_over:
            self.game_over_screen.draw(self.screen, self.text_input, self.score)

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
