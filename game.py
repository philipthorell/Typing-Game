from random import randint
from tkinter import END
from time import sleep

from word import Word


class Game:
    def __init__(self,
                 screen,
                 canvas,
                 WORD_LIST,
                 word_speed,
                 text_area,
                 LIVES,
                 NUM_OF_ENEMIES,
                 WIDTH,
                 HEIGHT):
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT

        self.screen = screen

        self.canvas = canvas

        self.WORD_LIST = WORD_LIST
        self.words = []

        self.word_speed = word_speed

        self.text_area = text_area

        self.LIVES = LIVES
        self.in_game_lives = 0
        self.score = 0
        self.NUM_OF_ENEMIES = NUM_OF_ENEMIES

        self.running = True

    def initialize(self):
        self.in_game_lives = self.LIVES
        self.score = 0

        self.lives_text = self.canvas.create_text(
            self.WIDTH - 100,
            self.HEIGHT / 20,
            text=f"Lives: {self.in_game_lives}",
            font=("Consolas", int(min(self.WIDTH, self.HEIGHT) / 25)),
            fill="white"
        )
        self.score_text = self.canvas.create_text(
            self.WIDTH - 250,
            self.HEIGHT / 20,
            text=f"Score: {self.score}",
            font=("Consolas", int(min(self.WIDTH, self.HEIGHT) / 25)),
            fill="white"
        )

        for i in range(self.NUM_OF_ENEMIES):
            self.spawn_new_enemy()

        self.screen.bind("<Destroy>", self.close_window)

    def close_window(self, event):
        self.running = False

    def start(self):
        self.initialize()

        return self.play()

    def on_key(self):
        typed_word = self.text_area.get()
        for word in self.words:
            word.word_typed(typed_word)

    def spawn_new_enemy(self):
        words_end = len(self.WORD_LIST) - 1
        enemy_word = (self.WORD_LIST[randint(0, words_end)])
        enemy_x = randint((-300), (-100))
        enemy_y = randint(int(self.HEIGHT / 8.333), int(self.HEIGHT - self.HEIGHT / 10))

        self.words.append(Word(
            self.canvas,
            enemy_x,
            enemy_y,
            self.word_speed,
            enemy_word,
            self.WIDTH,
            self.HEIGHT
        ))

        self.WORD_LIST.remove(enemy_word)

    def remove_enemy(self, enemy):
        self.canvas.delete(*enemy.image)
        self.WORD_LIST.append(enemy.word)

    def take_damage(self, enemy):
        self.in_game_lives -= 1
        self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.in_game_lives}")
        self.canvas.delete(*enemy.image)
        self.words.remove(enemy)
        self.WORD_LIST.append(enemy.word)
        self.spawn_new_enemy()

    def add_score(self, enemy):
        self.score += 1
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.text_area.delete(0, END)
        self.canvas.delete(*enemy.image)
        self.words.remove(enemy)
        self.WORD_LIST.append(enemy.word)
        self.spawn_new_enemy()

    def play(self):

        while self.running:
            if self.in_game_lives > 0:
                for enemy in self.words:
                    enemy.move()
                    if enemy.word_exited():
                        self.take_damage(enemy)
                    if enemy.word_typed(self.text_area.get()):
                        self.add_score(enemy)
                self.on_key()
            else:
                self.text_area.delete(0, END)
                for enemy in self.words:
                    self.remove_enemy(enemy)
                self.words = []
                self.canvas.delete(self.lives_text)
                self.canvas.delete(self.score_text)
                return True

            self.screen.update()
            sleep(0.01)
