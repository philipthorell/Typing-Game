import pygame as pg

from random import randint

from word import Word


class Gameplay:
    def __init__(self, screen, WORD_LIST, LIVES, NUM_OF_ENEMIES, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.screen = screen

        self.WORD_LIST = WORD_LIST
        self.words = []

        self.word_speed = 1

        self.LIVES = LIVES
        self.in_game_lives = self.LIVES
        self.NUM_OF_ENEMIES = NUM_OF_ENEMIES

        self.running = True
        self.lost = False
        self.started = False

        self.typed_word = False

    def start(self):
        for i in range(self.NUM_OF_ENEMIES):
            self.spawn_new_enemy()

        self.in_game_lives = self.LIVES

    def spawn_new_enemy(self):
        words_end = len(self.WORD_LIST) - 1
        enemy_word = (self.WORD_LIST[randint(0, words_end)])
        enemy_x = randint((-300), (-100))
        enemy_y = randint(int(self.HEIGHT / 8.333), int(self.HEIGHT - self.HEIGHT / 10))

        self.words.append(Word(
            enemy_x,
            enemy_y,
            self.word_speed,
            enemy_word,
            self.WIDTH,
            self.HEIGHT
        ))

        self.WORD_LIST.remove(enemy_word)

    def remove_enemy(self, enemy):
        self.WORD_LIST.append(enemy.word)

    def take_damage(self, enemy):
        self.in_game_lives -= 1
        self.words.remove(enemy)
        self.WORD_LIST.append(enemy.word)
        self.spawn_new_enemy()

    def add_score(self, enemy):
        self.words.remove(enemy)
        self.WORD_LIST.append(enemy.word)
        self.spawn_new_enemy()

    def update(self, text_input, word_speed, check_word):
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

    def draw_ui(self, screen: pg.Surface, score: int):
        font = pg.font.SysFont("Consolas", 25)
        lives_surf = font.render(f"Lives: {self.in_game_lives}", True, "white")
        lives_rect = lives_surf.get_rect(center=(self.WIDTH - 100, self.HEIGHT // 20))
        screen.blit(lives_surf, lives_rect)

        font = pg.font.SysFont("Consolas", 25)
        score_surf = font.render(f"Score: {score}", True, "white")
        score_rect = score_surf.get_rect(center=(self.WIDTH - 250, self.HEIGHT // 20))
        screen.blit(score_surf, score_rect)

    def draw(self, screen, score):
        for word in self.words:
            word.draw(screen)

        self.draw_ui(screen, score)
