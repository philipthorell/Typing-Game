from collections.abc import Callable


class Word:
    """
    Class that contains the information about the word-enemy.
    """
    def __init__(self, x, y, x_vel, word):
        # Creates a list of the letters for the word.
        self.word = word
        self.letters = [(char, "white") for char in self.word]

        self.x = x
        self.y = y
        self.x_velocity = x_vel

        self.width = 0
        self.height = 0

        self.font_size = 40

    def word_exited(self) -> bool:
        """
        Checks if the word has exited the screen.
        :return: True or False depending on if the word has exited the screen.
        """
        if self.x >= 1000:
            return True
        return False

    def draw(self, draw_text: Callable) -> None:
        """
        Draws the word-enemy on to the screen.
        :param draw_text: A function that draws typeable text.
        :return: None
        """
        rect = draw_text(self.letters, self.font_size, (self.x, self.y), placement="tl")
        self.width = rect.width
        self.height = rect.height

    def move(self) -> None:
        """
        Moves the word to the right.
        :return: None
        """
        self.x += self.x_velocity
