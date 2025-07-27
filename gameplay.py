import pygame as pg

from collections.abc import Callable
from random import randint

from word import Word


class Gameplay:
    """
    Class to contain the gameplay details.
    """
    def __init__(self, screen: pg.Surface, LIVES: int, NUM_OF_ENEMIES: int):
        self.screen = screen

        self.WORD_LIST = []
        self.words = []

        self.word_speed = 1

        self.LIVES = LIVES
        self.in_game_lives = self.LIVES
        self.NUM_OF_ENEMIES = NUM_OF_ENEMIES

        self.running = True
        self.lost = False
        self.started = False

        # Track if a word has been typed
        self.typed_word = False

        self.lives_text = ""
        self.score_text = ""

    def get_word_pack(self, WORD_LIST: list[str], gameplay_words: tuple[str, str]) -> None:
        self.WORD_LIST = WORD_LIST
        self.lives_text = gameplay_words[0]
        self.score_text = gameplay_words[1]

    def start(self) -> None:
        for i in range(self.NUM_OF_ENEMIES):
            self.spawn_new_enemy()

        self.in_game_lives = self.LIVES

    def spawn_new_enemy(self) -> None:
        words_end = len(self.WORD_LIST) - 1
        enemy_word = (self.WORD_LIST[randint(0, words_end)])
        enemy_x = randint((-300), (-100))
        enemy_y = randint(60, int(450))

        self.words.append(Word(
            enemy_x,
            enemy_y,
            self.word_speed,
            enemy_word
        ))

        self.WORD_LIST.remove(enemy_word)

    def remove_enemy(self, enemy) -> None:
        self.WORD_LIST.append(enemy.word)

    def take_damage(self, enemy) -> None:
        self.in_game_lives -= 1
        self.words.remove(enemy)
        self.WORD_LIST.append(enemy.word)
        self.spawn_new_enemy()

    def add_score(self, enemy) -> None:
        self.words.remove(enemy)
        self.WORD_LIST.append(enemy.word)
        self.spawn_new_enemy()

    def update(self, text_input: str, word_speed: float, check_word: Callable) -> None:
        """

        :param text_input:
        :param word_speed:
        :param check_word:
        :return:
        """
        # Creates a list of the word's letters to be checked by the check_word() function.
        items_list = [word.letters for word in self.words]
        correct_text_list = [word.word for word in self.words]
        check_word(items_list, correct_text_list)

        for word in self.words:
            if text_input == word.word:
                self.add_score(word)
                self.typed_word = True

        if not self.started:
            self.word_speed = word_speed
            self.start()
            self.started = True

        if self.in_game_lives > 0:
            for word in self.words:
                word.update()
                word.move()
                if word.word_exited():
                    self.take_damage(word)
        else:  # DEAD
            for enemy in self.words:
                self.remove_enemy(enemy)
            self.words = []
            self.lost = True
            self.started = False

    def draw_ui(self, screen: pg.Surface, score: int) -> None:
        font = pg.font.SysFont("Consolas", 25)
        lives_surf = font.render(f"{self.lives_text}: {self.in_game_lives}", True, "white")
        lives_rect = lives_surf.get_rect(center=(900, 25))
        screen.blit(lives_surf, lives_rect)

        font = pg.font.SysFont("Consolas", 25)
        score_surf = font.render(f"{self.score_text}: {score}", True, "white")
        score_rect = score_surf.get_rect(center=(750, 25))
        screen.blit(score_surf, score_rect)

    def draw(self, screen, score) -> None:
        for word in self.words:
            word.draw(screen)

        self.draw_ui(screen, score)
