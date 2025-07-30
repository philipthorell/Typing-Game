import pygame as pg

from collections.abc import Callable


class MainMenu:
    """
    Class that contains all the main-menu details.
    """
    def __init__(self, screen: pg.Surface):
        self.screen = screen

        self.running = True

        # Tracks if a certain word is typed.
        self.start_is_typed = False
        self.exit_is_typed = False
        self.easy_is_typed = False
        self.medium_is_typed = False
        self.hard_is_typed = False
        self.extreme_is_typed = False
        self.change_to_swedish = False
        self.change_to_english = False

        # Creates strings and lists of the typeable words.
        self.start_text = ""
        self.start_items = []
        self.exit_text = ""
        self.exit_items = []

        self.easy_text = ""
        self.easy_items = []
        self.medium_text = ""
        self.medium_items = []
        self.hard_text = ""
        self.hard_items = []
        self.extreme_text = ""
        self.extreme_items = []

        self.swedish_text = "svenska"
        self.swedish_items = [(char, "white") for char in self.swedish_text]
        self.english_text = "english"
        self.english_items = [(char, "white") for char in self.english_text]

        # Text for non-typeable words.
        self.tip_text = ""
        self.language_text = ""

        # Sets difficulty-arrow's Y position to point at medium.
        self.arrow_y = 200

    def get_word_pack(self, words: tuple) -> None:
        """
        Gets the language word-pack, and changes all words to that specific language.
        :param words: A tuple of all the word strings from the pack.
        :return: None
        """
        # Sets all the text-variables to a string of the word.
        # Sets all the items-variables to a list of the (letters & color) of the word.
        self.start_text = words[0]
        self.start_items = [(char, "white") for char in self.start_text]
        self.exit_text = words[1]
        self.exit_items = [(char, "white") for char in self.exit_text]
        self.easy_text = words[2]
        self.easy_items = [(char, "white") for char in self.easy_text]
        self.medium_text = words[3]
        self.medium_items = [(char, "white") for char in self.medium_text]
        self.hard_text = words[4]
        self.hard_items = [(char, "white") for char in self.hard_text]
        self.extreme_text = words[5]
        self.extreme_items = [(char, "white") for char in self.extreme_text]
        self.tip_text = words[6]
        self.language_text = words[7]

    def draw_arrow(self, screen: pg.Surface) -> None:
        """
        Draws the difficulty arrow, to indicate the selected difficulty.
        :param screen: A pygame surface to draw the arrow on.
        :return: None
        """
        # Gets the font and draws the text on the screen.
        font = pg.font.SysFont("Consolas", 25)
        arrow_surf = font.render("<", True, "white")
        arrow_rect = arrow_surf.get_rect(center=(880, self.arrow_y))
        screen.blit(arrow_surf, arrow_rect)

    def draw_tip(self, screen: pg.Surface) -> None:
        """
        Draws the tip that mentions how to clear the text in the top left corner.
        :param screen: A pygame surface to draw the tip on.
        :return: None
        """
        # Gets the font and draws the text on the screen.
        font = pg.font.SysFont("Consolas", 15)
        tip_surf = font.render(self.tip_text, True, "white")
        tip_rect = tip_surf.get_rect(center=(125, 25))
        screen.blit(tip_surf, tip_rect)

    def draw_language(self, screen: pg.Surface) -> None:
        """
        Draws the language indicator at the bottom left on the screen.
        :param screen: A pygame surface to draw the text on.
        :return: None
        """
        # Gets the font and draws the text on the screen.
        font = pg.font.SysFont("Consolas", 25)
        tip_surf = font.render(f"{self.language_text}:", True, "white")
        tip_rect = tip_surf.get_rect(topleft=(15, 390))
        screen.blit(tip_surf, tip_rect)

    def draw(self, screen: pg.Surface, draw_typeable_text: Callable) -> None:
        """
        Handles the drawing of all the main-menu texts.
        :param screen: A pygame surface to draw everything on.
        :param draw_typeable_text: A function that creates a surface and draws the typeable text.
        :return: None
        """
        # Draws the start and exit texts.
        draw_typeable_text(self.start_items, 80, (500, 200))
        draw_typeable_text(self.exit_items, 30, (500, 400))

        # Draws the difficulty texts.
        draw_typeable_text(self.easy_items, 25, (780, 150))
        draw_typeable_text(self.medium_items, 25, (780, 200))
        draw_typeable_text(self.hard_items, 25, (780, 250))
        draw_typeable_text(self.extreme_items, 25, (780, 300))

        # Draws the language texts.
        draw_typeable_text(self.swedish_items, 25, (100, 440))
        draw_typeable_text(self.english_items, 25, (100, 475))

        # Draws the non-typeable text.
        self.draw_language(screen)
        self.draw_arrow(screen)
        self.draw_tip(screen)

    def update(self, text_input: str, check_word: Callable) -> None:
        """
        Handles updating the main-menu screen by checking if the typeable words are typed.
        :param text_input: A string of the players typed letters.
        :param check_word: A function that change the colors of the words letters
        depending on if the player has typed them or not.
        :return: None
        """
        # Creates a list of all the typeable word's letters to be checked by
        # the check_word() function.
        items_list = [
            self.start_items, self.exit_items, self.easy_items, self.medium_items,
            self.hard_items, self.extreme_items, self.swedish_items, self.english_items
        ]
        # Creates a list of all the typeable words to be checked by the check_word() function.
        correct_text_list = [
            self.start_text, self.exit_text, self.easy_text, self.medium_text,
            self.hard_text, self.extreme_text, self.swedish_text, self.english_text
        ]
        # Changes the color of the word's letters if they are being typed.
        check_word(items_list, correct_text_list)

        # Checks if the typeable words are being typed.
        if text_input == self.start_text:
            self.start_is_typed = True
        elif text_input == self.exit_text:
            self.exit_is_typed = True

        elif text_input == self.easy_text:
            self.arrow_y = 150
            self.easy_is_typed = True
        elif text_input == self.medium_text:
            self.arrow_y = 200
            self.medium_is_typed = True
        elif text_input == self.hard_text:
            self.arrow_y = 250
            self.hard_is_typed = True
        elif text_input == self.extreme_text:
            self.arrow_y = 300
            self.extreme_is_typed = True

        elif text_input == self.swedish_text:
            self.change_to_swedish = True
        elif text_input == self.english_text:
            self.change_to_english = True


class GameOver:
    """
    Class that contain all the game-over details.
    """
    def __init__(self, screen: pg.Surface):
        self.screen = screen

        self.in_game_lives = 0

        self.running = True
        self.main = False
        self.exit = False

        # Creates strings and lists of the typeable words.
        self.main_text = ""
        self.main_items = []
        self.exit_text = ""
        self.exit_items = []
        self.game_over_text = ""
        self.score_text = ""

    def get_word_pack(self, words: tuple) -> None:
        """
        Gets the language word-pack, and changes all words to that specific language.
        :param words: A tuple of all the word strings from the pack.
        :return: None
        """
        # Sets all the text-variables to a string of the word.
        # Sets all the items-variables to a list of the (letters & color) of the word.
        self.game_over_text = words[0]
        self.score_text = words[1]
        self.main_text = words[2]
        self.main_items = [(char, "white") for char in self.main_text]
        self.exit_text = words[3]
        self.exit_items = [(char, "white") for char in self.exit_text]

    def update(self, text_input: str, check_word: Callable) -> None:
        """
        Handles updating the main-menu screen by checking if the typeable words are typed.
        :param text_input: A string of the players typed letters.
        :param check_word: A function that change the colors of the words letters
        depending on if the player has typed them or not.
        :return: None
        """
        # Creates lists of all the typeable word's letters and strings to be checked by
        # the check_word() function.
        items_list = [self.main_items, self.exit_items]
        correct_text_list = [self.main_text, self.exit_text]
        # Changes the color of the word's letters if they are being typed.
        check_word(items_list, correct_text_list)

        # Checks if the typeable words are being typed.
        if text_input == self.main_text:
            self.main = True
        if text_input == self.exit_text:
            self.exit = True

    def draw(self, screen: pg.Surface, score: int, draw_typeable_text: Callable) -> None:
        """
        Handles the drawing of all the game-over texts.
        :param screen: A pygame surface to draw everything on.
        :param score: An int of the players score
        :param draw_typeable_text: A function that creates a surface and draws the typeable text.
        :return: None
        """
        # Draws the start and exit texts
        draw_typeable_text(self.main_items, 30, (440, 370), padding=5, placement="tr")
        draw_typeable_text(self.exit_items, 30, (560, 370), padding=5, placement="tl")

        # Draws the GAME OVER text
        font = pg.font.SysFont("Consolas", 80)
        gg_surf = font.render(f"{self.game_over_text}", True, "red")
        gg_rect = gg_surf.get_rect(center=(500, 160))
        screen.blit(gg_surf, gg_rect)

        # Draws the score text
        font = pg.font.SysFont("Consolas", 40)
        score_surf = font.render(f"{self.score_text}: {score}", True, "white")
        score_rect = score_surf.get_rect(center=(500, 230))
        screen.blit(score_surf, score_rect)
