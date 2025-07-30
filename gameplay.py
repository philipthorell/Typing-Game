import pygame as pg

from collections.abc import Callable
from random import randint, choice

from word import Word


class Gameplay:
    """
    Class to contain the gameplay details.
    """
    def __init__(self, screen: pg.Surface):
        self.screen = screen

        self.WORD_LIST = []
        self.words = []

        self.word_speed = 1

        self.in_game_lives = 0

        self.running = True
        self.lost = False
        self.started = False

        # Track if a word has been typed
        self.typed_word = False

        self.lives_text = ""
        self.score_text = ""

        self.last_time = 0

        # Word-enemies y positions
        self.y_pos = [10 + (i * 40) for i in range(1, 11)]

    def get_word_pack(self, WORD_LIST: list[str], words: tuple[str, str]) -> None:
        """
        Gets the language word-pack, and changes all words to that specific language.
        :param WORD_LIST: A list of
        :param words: A tuple of all the word strings from the pack.
        :return: None
        """
        # Change the WORD_LIST to the new word-pack.
        self.WORD_LIST = WORD_LIST
        # Change the texts to the new language.
        self.lives_text = words[0]
        self.score_text = words[1]

    def reset(self, lives) -> None:
        """
        Resets the players lives.
        :return: None
        """
        self.in_game_lives = lives

    def spawn_new_enemy(self, difficulty: str) -> None:
        """
        Spawn a new word-enemy, and temporarily remove the random word from the WORD_LIST
        to get different words each time.
        :return: None
        """
        # Pick a random word from WORD_LIST and give it random starting coordinates.
        if difficulty == "easy":
            new_word_list = [word for word in self.WORD_LIST if len(word) < 7]
            enemy_x = -150
        elif difficulty == "hard" or difficulty == "medium":
            new_word_list = [word for word in self.WORD_LIST]
            enemy_x = -300
        elif difficulty == "extreme":
            new_word_list = [word for word in self.WORD_LIST if len(word) > 4]
            enemy_x = -400

        words_end = len(new_word_list) - 1
        enemy_word = (new_word_list[randint(0, words_end)])

        y_positions = self.y_pos.copy()

        for word in self.words:
            if word.y in y_positions:
                y_positions.remove(word.y)

        if len(y_positions) == 0:
            y_positions = self.y_pos.copy()
            y_positions.remove(self.words[-1].y)

        enemy_y = choice(y_positions)

        # Create a new word-enemy instance and append it to the words list.
        self.words.append(Word(
            enemy_x,
            enemy_y,
            self.word_speed,
            enemy_word
        ))

        # Temporarily remove the chosen random word from the WORD_LIST list.
        self.WORD_LIST.remove(enemy_word)

    def take_damage(self, enemy: Word) -> None:
        """
        Removes a life and removes the enemy and spawns a new one.
        :param enemy: A word-enemy instance of the Word class.
        :return: None
        """
        self.in_game_lives -= 1
        self.words.remove(enemy)
        self.WORD_LIST.append(enemy.word)

    def add_score(self, enemy: Word) -> None:
        """
        Sets typed_word to True so that a point gets added to the score, and removes
        the typed word-enemy and spawns in a new one.
        :param enemy: A word-enemy instance of the Word class.
        :return: None
        """
        self.typed_word = True
        self.words.remove(enemy)
        self.WORD_LIST.append(enemy.word)

    def update(self,
               text_input: str,
               word_speed: float,
               spawn_time: int,
               lives: int,
               difficulty: str,
               check_word: Callable) -> None:
        """
        Handles the updating of the players lives, score, and word-enemy details.
        :param text_input: A string of the players typed letters.
        :param word_speed: The speed/difficulty of the word-enemies.
        :param check_word: A function that checks if letters of the word-enemies is typed.
        :return: None
        """
        current_time = pg.time.get_ticks()
        # Creates a list of the word-enemies letters to be checked by the check_word() function.
        items_list = [word.letters for word in self.words]
        correct_text_list = [word.word for word in self.words]
        # Changes the color of the word-enemies letters if they are being typed.
        check_word(items_list, correct_text_list)

        # Checks if a word-enemy is typed, and adds a score and removes the word if so.
        for word in self.words:
            if text_input == word.word:
                self.add_score(word)

        # Spawns in the enemies at the start of the game.
        if not self.started:
            self.word_speed = word_speed
            self.reset(lives)
            self.started = True

        # Update the word-enemies if the player is alive.
        if self.in_game_lives > 0:
            # Spawn enemies
            if current_time - self.last_time > spawn_time:
                self.last_time = current_time
                self.spawn_new_enemy(difficulty)
            # Update and move all the word-enemies.
            for word in self.words:
                word.move()
                # Loose a life if the word-enemy exits the screen.
                if word.word_exited():
                    self.take_damage(word)

        # Append back all the enemy word to the WORD_LIST and go to game-over if the player lost.
        else:
            for enemy in self.words:
                self.WORD_LIST.append(enemy.word)
            self.words = []
            self.lost = True
            self.started = False

    def draw_ui(self, screen: pg.Surface, score: int) -> None:
        """
        Draws the score and the lives of the player.
        :param screen: A pygame surface to draw the score and lives on.
        :param score: The score that the player currently has.
        :return: None
        """
        # Draws the lives text.
        font = pg.font.SysFont("Consolas", 25)
        lives_surf = font.render(f"{self.lives_text}: {self.in_game_lives}", True, "white")
        lives_rect = lives_surf.get_rect(center=(900, 25))
        screen.blit(lives_surf, lives_rect)

        # Draws the score text.
        font = pg.font.SysFont("Consolas", 25)
        score_surf = font.render(f"{self.score_text}: {score}", True, "white")
        score_rect = score_surf.get_rect(center=(750, 25))
        screen.blit(score_surf, score_rect)

    def draw(self, screen: pg.Surface, score: int, draw_text: Callable) -> None:
        """
        Handles the drawing of the enemies and UI.
        :param screen: A pygame surface to draw everything on.
        :param score: The amount of score that the player currently has.
        :param draw_text: A function that draws typeable text.
        :return: None
        """
        for word in self.words:
            word.draw(draw_text)

        self.draw_ui(screen, score)
