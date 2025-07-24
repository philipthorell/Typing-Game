from tkinter import END


class Word:

    def __init__(self,
                 canvas,
                 x, y,
                 x_vel,
                 word,
                 SCREEN_WIDTH, SCREEN_HEIGHT):

        self.WIDTH = SCREEN_WIDTH
        self.HEIGHT = SCREEN_HEIGHT

        self.canvas = canvas
        self.word = word
        self.image = [
            canvas.create_text(
                x + i * 20,
                y,
                text=word[i],
                font=("Consolas", int(min(SCREEN_WIDTH, SCREEN_HEIGHT) / 20.833)),
                fill="white"
            )
            for i in range(len(word))
        ]
        self.x_velocity = x_vel
        self.typed_letters = 0

    def word_exited(self):
        coordinates = self.canvas.coords(self.image[0])
        if coordinates[0] >= self.WIDTH:
            return True
        return False

    def move(self):
        for text_item2 in self.image:
            self.canvas.move(text_item2, self.x_velocity, 0)

    def word_typed(self, typed_word: str):

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
            return True

        return False
