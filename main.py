import pygame as pg

from gameplay import Gameplay
from menu import MainMenu, GameOver


# TODO:
#   FIX, WHEN TYPING WRONG AT THE START, ALL WORDS SHOULD TURN RED
#   ADD, WORD-PACKS (INCLUDING CUSTOM WORD-PACKS)
#   FIX, SO THAT WHEN USER TYPES THE END OF A WORD WRONG AND CONTINUE TO TYPE, THEY ONLY NEED
#        TO REMOVE THE LAST LETTERS OF THE WORD (INSTEAD OF THE "INVISIBLE" ONES AT THE FAR BACK)
#   FIX, SO THAT WORDS CAN'T SPAWN INSIDE EACH OTHER
#   ADD, RETRY BUTTON AT GAME-OVER-SCREEN
#   FIX, SO THAT WORD CONSTANTLY SPAWN AND THE FREQUENCY DEPENDS ON THE DIFFICULTY


class Game:
    """
    Class to contain and tie together the whole game.
    """
    WIDTH, HEIGHT = 1000, 500  # Aspect ratio must be 2:1 (1000x500)

    EASY_SPEED = 0.5  # 0.5
    NORMAL_SPEED = 1  # 1
    HARD_SPEED = 1.5  # 1.5
    LIVES = 3  # 3
    NUM_OF_ENEMIES = 5  # 5

    score = 0

    def __init__(self):

        self.S_WORDS = "swedish_words.txt"
        self.E_WORDS = "english_words.txt"

        # Reads in the english words to start with.
        with open(self.E_WORDS, "r") as file:
            self.WORD_LIST = [word.replace("\n", "") for word in file.readlines()]

        self.running = True
        self.word_speed = self.NORMAL_SPEED
        self.in_game_lives = self.LIVES

        # Initializes pygame, with the screen, clock, caption, and FPS.
        pg.font.init()
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption("Typing Game")
        self.clock = pg.time.Clock()
        self.FPS = 60

        # Sets the colors that the letters in the game appear as.
        self.white_color = "white"
        self.green_color = "green"
        self.red_color = "red"

        # Contains the letters that the user types.
        self.text_input = ""

        # List of the typeable words in the respective parts of the game.
        self.title_words = []
        self.gameplay_words = []
        self.game_over_words = []

        # Keeps track of which part of the game the user is currently in.
        self.main_menu = True
        self.gameplay = False
        self.game_over = False

        # Initializes the different parts of the game.
        self.main_menu_screen = MainMenu(
            self.screen,
            (self.EASY_SPEED, self.NORMAL_SPEED, self.HARD_SPEED),
        )
        self.gameplay_screen = Gameplay(
            self.screen,
            self.LIVES,
            self.NUM_OF_ENEMIES,
        )
        self.game_over_screen = GameOver(
            self.screen,
            self.LIVES,
        )

        # Sets all the words to english to start with.
        self.english_words()

    def english_words(self) -> None:
        """
        Changes the words in main-menu, gameplay, and game-over, to English.
        :return: None
        """
        self.title_words = (
            "start", "exit", "easy", "medium", "hard",
            "(spacebar = clear the text)", "Languages"
        )
        self.gameplay_words = (
            "Lives", "Score"
        )
        self.game_over_words = (
            "GAME OVER", "Score", "main", "exit"
        )

        # Reads in and replaces the WORD_LIST from the given .txt file.
        with open(self.E_WORDS, "r") as file:
            self.WORD_LIST = [word.replace("\n", "") for word in file.readlines()]

        # Updates all the parts of the game to change their words.
        self.main_menu_screen.get_word_pack(self.title_words)
        self.gameplay_screen.get_word_pack(self.WORD_LIST, self.gameplay_words)
        self.game_over_screen.get_word_pack(self.game_over_words)

    def swedish_words(self) -> None:
        """
        Changes the words in main-menu, gameplay, and game-over, to Swedish.
        :return: None
        """
        self.title_words = (
            "starta", "avsluta", "lätt", "normal", "svår",
            "(mellanslag = rensa texten)", "Språk"
        )
        self.gameplay_words = (
            "Liv", "Poäng"
        )
        self.game_over_words = (
            "SPEL ÖVER", "Poäng", "main", "avsluta"
        )

        # Reads in and replaces the WORD_LIST from the given .txt file.
        with open(self.S_WORDS, "r") as file:
            self.WORD_LIST = [word.replace("\n", "") for word in file.readlines()]

        # Updates all the parts of the game to change their words.
        self.main_menu_screen.get_word_pack(self.title_words)
        self.gameplay_screen.get_word_pack(self.WORD_LIST, self.gameplay_words)
        self.game_over_screen.get_word_pack(self.game_over_words)

    def check_word(self, items_list: list[list[tuple[str, str]]], correct_text_list: list[str]) -> None:
        """
        Checks if the user has typed one of the words in the game, if the user starts typing
        one of the words, then the following letters of that said word turn green.
        If the user types the following letters wrong then the letters of the word turns red.
        :param items_list: A list of pygame surfaces that represent all the letters in a word.
        :param correct_text_list:  A string of the whole word.
        :return: None
        """
        # Go through the word-lists one by one.
        for idx, items in enumerate(items_list):
            correct_text = correct_text_list[idx]
            typed_letters = len(self.text_input)

            # Set every letter of the word as white to begin with.
            for i in range(len(items)):
                items[i] = (correct_text[i], self.white_color)

            # Sets the words first letter to green if the users first input is matching.
            if typed_letters > 0 and self.text_input[0] == correct_text[0]:
                items[0] = (correct_text[0], self.green_color)

                # Goes through the amount of letters typed by the user.
                for i in range(1, typed_letters):
                    try:
                        # Checks if the previous letter is green.
                        if items[i - 1][1] == self.green_color:
                            # Turns the letter green if it matches the typed letter.
                            if self.text_input[i] == correct_text[i]:
                                items[i] = (correct_text[i], self.green_color)
                            # Else turns it red to indicate that its wrong.
                            else:
                                do_red = True
                                # Checks if another word that starts with the same letters
                                # did match with the typed letter.
                                for items2 in items_list:
                                    # Skips the current word.
                                    if items2 == items:
                                        continue
                                    try:
                                        # Checks if another word's letters match.
                                        if items2[i][1] == self.green_color:
                                            do_red = False
                                    # If the user has typed more letters than the word
                                    # contains then just skip.
                                    except IndexError:
                                        print("skipping word:", "".join([letters[0] for letters in items2]))
                                        continue
                                # Make the letter red.
                                if do_red:
                                    items[i] = (correct_text[i], self.red_color)
                                # Else if another word is being typed correctly,
                                # then make this word's letters white again.
                                else:
                                    for j in range(len(correct_text)):
                                        items[j] = (correct_text[j], self.white_color)

                        # Else if the previous letter is red, then make this letter red too.
                        elif items[i - 1][1] == self.red_color:
                            items[i] = (correct_text[i], self.red_color)

                    # If the user has typed more letters than the word contains then just break.
                    except IndexError:
                        print("".join([letters[0] for letters in items]))
                        break

    def update(self) -> None:
        """
        Updates the various parts of the game, like the main-menu, gameplay, and game-over.
        :return: None
        """
        # Updates the main-menu things.
        if self.main_menu:

            # Updates the main-menu to check for words typed.
            self.main_menu_screen.update(self.text_input, self.check_word)

            # Checks if start is typed and starts the gameplay if so.
            if self.main_menu_screen.start_is_typed:
                self.text_input = ""
                self.main_menu = False
                self.gameplay = True
                # Resets the variable.
                self.main_menu_screen.start_is_typed = False

            # Checks if exit is typed and exits the game if so.
            elif self.main_menu_screen.exit_is_typed:
                self.running = False

            # Checks if any difficulty is typed and changes to that difficulty if so.
            elif self.main_menu_screen.easy_is_typed:
                self.text_input = ""
                self.word_speed = self.EASY_SPEED
                # Resets the variable.
                self.main_menu_screen.easy_is_typed = False
            elif self.main_menu_screen.medium_is_typed:
                self.text_input = ""
                self.word_speed = self.NORMAL_SPEED
                # Resets the variable.
                self.main_menu_screen.medium_is_typed = False
            elif self.main_menu_screen.hard_is_typed:
                self.text_input = ""
                self.word_speed = self.HARD_SPEED
                # Resets the variable.
                self.main_menu_screen.hard_is_typed = False

            # Checks if a language is typed and changes to that language if so.
            if self.main_menu_screen.change_to_swedish:
                self.text_input = ""
                self.swedish_words()
                # Resets the variable.
                self.main_menu_screen.change_to_swedish = False
            elif self.main_menu_screen.change_to_english:
                self.text_input = ""
                self.english_words()
                # Resets the variable.
                self.main_menu_screen.change_to_english = False

        # Updates the gameplay things.
        elif self.gameplay:

            # Update the gameplay screen to keep track of lives, score, and words typed.
            self.gameplay_screen.update(self.text_input, self.word_speed, self.check_word)

            # Checks if a word is typed and adds a score if so.
            if self.gameplay_screen.typed_word:
                self.text_input = ""
                self.score += 1
                # Resets the variable.
                self.gameplay_screen.typed_word = False

            # Checks if the player has lost, and changes to the game-over screen if so.
            if self.gameplay_screen.lost:
                self.text_input = ""
                self.gameplay = False
                self.game_over = True
                # Resets the variable.
                self.gameplay_screen.lost = False

        # Updates game-over things.
        elif self.game_over:

            # Updates the game-over screen to check for words typed.
            self.game_over_screen.update(self.text_input, self.check_word)

            # Checks if main is typed and changes to main-menu if so.
            if self.game_over_screen.main:
                self.text_input = ""
                self.game_over = False
                self.main_menu = True
                self.score = 0
                # Resets the variable.
                self.game_over_screen.main = False

            # Checks if exit is typed, and exits the game if so.
            elif self.game_over_screen.exit:
                self.running = False

    @staticmethod
    def create_word_surface(items: list[tuple[str, str]], font: pg.font.Font, padding=10):
        """
        Render a word from (char, color) items into a single surface,
        and return it with its rect.
        :param items:
        :param font:
        :param padding:
        :return:
        """
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

        return word_surface

    def draw_text(self, items: list, font_size: int, pos: tuple[int, int],
                  padding=10, placement=""):
        """

        :param items:
        :param font_size:
        :param pos:
        :param padding:
        :param placement:
        :return:
        """
        # Create the word surface
        font = pg.font.SysFont("Consolas", font_size)
        word_surface = self.create_word_surface(items, font, padding)
        rect = word_surface.get_rect()
        if placement == "tr":
            rect.topright = pos
        elif placement == "tl":
            rect.topleft = pos
        else:
            rect.center = pos  # Move the box around as needed
        self.screen.blit(word_surface, rect)

    def draw(self) -> None:
        """
        Draws every part of the game, like main-menu, gameplay, and game-over.
        :return: None
        """
        # Clears the screen by filling it with black.
        self.screen.fill("black")

        # Draws the main-menu.
        if self.main_menu:
            self.main_menu_screen.draw(self.screen, self.draw_text)

        # Draws the gameplay.
        elif self.gameplay:
            self.gameplay_screen.draw(self.screen, self.score, self.draw_text)

        # Draws the game-over.
        elif self.game_over:
            self.game_over_screen.draw(self.screen, self.score, self.draw_text)

    def run(self) -> None:
        """
        Runs the whole game loop.
        :return: None
        """
        while self.running:
            # Handle pygame events.
            for event in pg.event.get():
                # Closes the game if the top-right "x" is pressed.
                if event.type == pg.QUIT:
                    self.running = False

                # Checks if a key is pressed.
                if event.type == pg.KEYDOWN:
                    # Removes a letter if the backspace is pressed.
                    if event.key == pg.K_BACKSPACE:
                        self.text_input = self.text_input[:-1]
                    # Clears the text if space is pressed.
                    elif event.key == pg.K_SPACE:
                        self.text_input = ""
                    # Adds the letter to the text_input.
                    else:
                        self.text_input += event.unicode

            # Updates the game.
            self.update()

            # Draws the game.
            self.draw()

            # Updates the pygame window.
            pg.display.flip()

            # Makes sure this loop only passes a certain amount of times per second.
            self.clock.tick(self.FPS)


# Runs the game if the script is directly run (not imported).
if __name__ == "__main__":
    game = Game()
    game.run()
