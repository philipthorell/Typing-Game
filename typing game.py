import random
import time
from tkinter import *

WIDTH = 1000  # 1000 has to be HEIGHT * 2
HEIGHT = 500  # 500 has to be WIDTH / 2
EASY_SPEED = 0.5  # 0.5
NORMAL_SPEED = 1  # 1
HARD_SPEED = 1.5  # 1.5
LIVES = 3  # 3
NUM_OF_ENEMIES = 5  # 5
# Swedish words
#WORDS = ["hejsan", "tunnelbana", "lol", "skateboard", "ugn", "bord",
#         "vattenfall", "kossa", "hund", "katt", "kaka", "byggnad",
#         "badkar", "jord", "mobil", "hus", "ekorre", "vind"]
WORDS = ["car", "subway", "dog", "cat", "house", "cookie", "building",
         "hammer", "cow", "saw", "computer", "password", "speaker",
         "bed", "coffee", "phone", "glas", "chain", "keyboard"]


def start():

    class Enemy:

        def __init__(self, canvas, x, y, xVelocity, yVelocity, word):
            self.canvas = canvas
            self.word = word
            self.image = [canvas.create_text(x + i * 20, y, text=word[i], font=("Consolas", int(min(WIDTH, HEIGHT) / 20.833)), fill="white") for i in
                          range(len(word))]
            self.xVelocity = xVelocity
            self.yVelocity = yVelocity
            self.typed_letters = 0

        def move(self):
            global in_game_lives
            coordinates = self.canvas.coords(self.image[0])
            if coordinates[0] >= WIDTH:
                in_game_lives -= 1
                canvas.itemconfig(lives_text, text="Lives: {}".format(in_game_lives))
                self.canvas.delete(*self.image)
                enemies.remove(self)
                WORDS.append(self.word)
                self.spawn_new_enemy()
                return

            for text_item2 in self.image:
                self.canvas.move(text_item2, self.xVelocity, self.yVelocity)

        def check_word(self, typed_word):
            global score

            typed_letters = min(len(typed_word), len(self.word))

            # Check if the first letter is correct
            if typed_letters > 0 and typed_word[0] == self.word[0]:
                self.canvas.itemconfig(self.image[0], fill="#00FF00")  # Set the color to green

            # Check if subsequent letters are correct and the preceding letter is green
            for i in range(1, typed_letters):
                if typed_word[i] == self.word[i] and self.canvas.itemcget(self.image[i - 1], "fill") == "#00FF00":
                    self.canvas.itemconfig(self.image[i], fill="#00FF00")  # Set the color to green
                else:
                    for i in range(len(self.word)):
                        self.canvas.itemconfig(self.image[i], fill="white")
                    break  # Stop setting colors if the preceding letter is not green

            # Reset the color of remaining letters in self.word
            for i in range(typed_letters, len(self.word)):
                self.canvas.itemconfig(self.image[i], fill="white")

            if typed_word == self.word:
                score += 1
                canvas.itemconfig(score_text, text=f"Score: {score}")
                text_area.delete(0, END)
                self.canvas.delete(*self.image)
                enemies.remove(self)
                WORDS.append(self.word)
                self.spawn_new_enemy()

        def spawn_new_enemy(self):
            words_end = len(WORDS) - 1
            enemy_word = (WORDS[random.randint(0, words_end)])
            enemy_x = random.randint((-300), (-100))
            enemy_y = random.randint(int(HEIGHT/8.333), int(HEIGHT - HEIGHT/10))
            enemies.append(Enemy(canvas, enemy_x, enemy_y, word_speed, 0, enemy_word))
            WORDS.remove(enemy_word)

        def remove_enemies(self):
            self.canvas.delete(*self.image)
            WORDS.append(self.word)

    def on_key():
        typed_word = text_area.get()
        for enemy in enemies:
            enemy.check_word(typed_word)

    def clear_text_area(event):
        text_area.delete(0, END)

    lives_text = canvas.create_text(WIDTH-100, HEIGHT/20, text="Lives: {}".format(in_game_lives), font=("Consolas", int(min(WIDTH, HEIGHT)/25)), fill="white")
    score_text = canvas.create_text(WIDTH-250, HEIGHT/20, text=f"Score: {score}", font=("Consolas", int(min(WIDTH, HEIGHT)/25)), fill="white")

    enemies = []
    for i in range(NUM_OF_ENEMIES):
        words_end = len(WORDS) - 1
        enemy_word = (WORDS[random.randint(0, words_end)])
        enemy_x = random.randint((-300), (-100))
        enemy_y = random.randint(int(HEIGHT/8.333), int(HEIGHT - HEIGHT/10))
        enemies.append(Enemy(canvas, enemy_x, enemy_y, word_speed, 0, enemy_word))
        WORDS.remove(enemy_word)

    window.bind("<space>", clear_text_area)

    while running:
        if in_game_lives > 0:
            for enemy in enemies:
                enemy.move()
            on_key()
        else:
            text_area.delete(0, END)
            for enemy in enemies:
                enemy.remove_enemies()
            canvas.delete(lives_text)
            canvas.delete(score_text)
            game_over()

        window.update()
        time.sleep(0.01)


def main_menu():
    global word_speed, running

    def check_word(typed_word, items, text):

        typed_letters = min(len(typed_word), len(text))

        # Check if the first letter is correct
        if typed_letters > 0 and typed_word[0] == text[0]:
            canvas.itemconfig(items[0], fill="#00FF00")  # Set the color to green

        # Check if subsequent letters are correct and the preceding letter is green
        for i in range(1, typed_letters):
            if typed_word[i] == text[i] and canvas.itemcget(items[i - 1], "fill") == "#00FF00":
                canvas.itemconfig(items[i], fill="#00FF00")  # Set the color to green
            else:
                for i in range(len(text)):
                    canvas.itemconfig(items[i], fill="white")
                break  # Stop setting colors if the preceding letter is not green

        # Reset the color of remaining letters in self.word
        for i in range(typed_letters, len(text)):
            canvas.itemconfig(items[i], fill="white")

    def clear_text_area(event):
        text_area.delete(0, END)

    def create_text_items(canvas, text, x, y, font_size, items_list):
        for char in text:
            item_id = canvas.create_text(x, y, text=char, font=("Consolas", font_size), fill="white")
            items_list.append(item_id)
            x += 55 if font_size == 80 else 20  # Adjust x position based on font size

    start_text = "start"
    start_items = []
    create_text_items(canvas, start_text, 400, 200, 80, start_items)

    exit_text = "exit"
    exit_items = []
    create_text_items(canvas, exit_text, 470, 400, 30, exit_items)

    easy_text = "easy"
    easy_items = []
    create_text_items(canvas, easy_text, 720, 150, 25, easy_items)

    normal_text = "normal"
    normal_items = []
    create_text_items(canvas, normal_text, 700, 200, 25, normal_items)

    hard_text = "hard"
    hard_items = []
    create_text_items(canvas, hard_text, 720, 250, 25, hard_items)

    arrow = canvas.create_text(830, 200, text="<", font=("Consolas", 25), fill="white")
    tip = canvas.create_text(150, HEIGHT - 40, text="(spacebar = clear text)", font=("Consolas", 15), fill="white")

    window.bind("<space>", clear_text_area)

    while running:
        if text_area.get() == "start":
            text_area.delete(0, END)

            canvas.delete(arrow)
            canvas.delete(tip)

            items_lists = [start_items, exit_items, easy_items, normal_items, hard_items]
            for items_list in items_lists:
                canvas.delete(*items_list)

            start()
            break

        if text_area.get() == "exit":
            window.destroy()
            break

        check_word(text_area.get(), start_items, start_text)
        check_word(text_area.get(), exit_items, exit_text)
        check_word(text_area.get(), easy_items, easy_text)
        check_word(text_area.get(), normal_items, normal_text)
        check_word(text_area.get(), hard_items, hard_text)

        if text_area.get() == "easy":
            canvas.coords(arrow, 830, 150)
            word_speed = EASY_SPEED
            text_area.delete(0, END)
        elif text_area.get() == "normal":
            canvas.coords(arrow, 830, 200)
            word_speed = NORMAL_SPEED
            text_area.delete(0, END)
        elif text_area.get() == "hard":
            canvas.coords(arrow, 830, 250)
            word_speed = HARD_SPEED
            text_area.delete(0, END)

        window.update()
        time.sleep(0.01)


def game_over():
    global in_game_lives, score

    def check_word(typed_word, items, text):

        typed_letters = min(len(typed_word), len(text))

        # Check if the first letter is correct
        if typed_letters > 0 and typed_word[0] == text[0]:
            canvas.itemconfig(items[0], fill="#00FF00")  # Set the color to green

        # Check if subsequent letters are correct and the preceding letter is green
        for i in range(1, typed_letters):
            if typed_word[i] == text[i] and canvas.itemcget(items[i - 1], "fill") == "#00FF00":
                canvas.itemconfig(items[i], fill="#00FF00")  # Set the color to green
            else:
                for i in range(len(text)):
                    canvas.itemconfig(items[i], fill="white")
                break  # Stop setting colors if the preceding letter is not green

        # Reset the color of remaining letters in self.word
        for i in range(typed_letters, len(text)):
            canvas.itemconfig(items[i], fill="white")

    def create_text_items(canvas, text, x, y, items_list):
        for char in text:
            item_id = canvas.create_text(x, y, text=char, font=("Consolas", 25), fill="white")
            items_list.append(item_id)
            x += 20

    main_text = "main"
    main_items = []
    create_text_items(canvas, main_text, 470, HEIGHT/2+HEIGHT/5+HEIGHT/24, main_items)

    exit_text = "exit"
    exit_items = []
    create_text_items(canvas, exit_text, 470, HEIGHT/2+HEIGHT/3, exit_items)

    game_over_text = canvas.create_text(WIDTH/2, HEIGHT/2-HEIGHT/4+HEIGHT/8, text="GAME OVER", font=("Consolas", 80),fill="#FF0000")
    score_text = canvas.create_text(WIDTH/2, HEIGHT/2+HEIGHT/4-HEIGHT/8-HEIGHT/16-HEIGHT/32,text=f"score: {score}", font=("Consolas", 40), fill="white")

    in_game_lives += LIVES
    score = 0

    while running:
        if text_area.get() == "main":
            text_area.delete(0, END)
            canvas.delete(*main_items)
            canvas.delete(*exit_items)
            canvas.delete(game_over_text)
            canvas.delete(score_text)
            main_menu()
            break

        check_word(text_area.get(), main_items, main_text)
        check_word(text_area.get(), exit_items, exit_text)

        if text_area.get() == "exit":
            window.destroy()

        window.update()
        time.sleep(0.01)


def close_window(event):
    global running
    running = False


score = 0
running = True
word_speed = NORMAL_SPEED
in_game_lives = LIVES

window = Tk()
window.title("Typing Game")
window.geometry(f"{WIDTH}x{HEIGHT}")
window.resizable(False, False)

text_area = Entry(window)
text_area.place(x=0, y=0)
text_area.focus()

typed_word = text_area.get()

canvas = Canvas(window, width=WIDTH, height=HEIGHT, background="black")
canvas.pack()

window.bind("<Destroy>", close_window)

main_menu()

window.mainloop()
