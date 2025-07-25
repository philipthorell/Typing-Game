import pygame as pg


class Word:

    def __init__(self,
                 x, y,
                 x_vel,
                 word,
                 SCREEN_WIDTH, SCREEN_HEIGHT):

        self.WIDTH = SCREEN_WIDTH
        self.HEIGHT = SCREEN_HEIGHT

        self.word = word
        self.letters = [(char, "white") for char in self.word]

        self.x = x
        self.y = y
        self.x_velocity = x_vel

        self.font = pg.font.SysFont("Consolas", 40)

        self.word_surface: pg.Surface | None = None
        self.word_rect: pg.Rect | None = None

    def word_exited(self):
        if self.word_rect.left >= self.WIDTH:
            return True
        return False

    def draw(self, screen):
        if self.word_surface is not None or self.word_rect is not None:
            screen.blit(self.word_surface, self.word_rect)

    def update(self):
        char_surfaces = []
        padding = 10
        total_width = 0
        max_height = 0

        # Render each character surface
        for char, color in self.letters:
            surf = self.font.render(char, True, color)
            char_surfaces.append(surf)
            total_width += surf.get_width() + padding
            max_height = max(max_height, surf.get_height())

        self.word_surface = pg.Surface((total_width, max_height), pg.SRCALPHA)
        x = 0
        for surf in char_surfaces:
            self.word_surface.blit(surf, (x, 0))
            x += surf.get_width() + padding

        self.word_rect = self.word_surface.get_rect()
        self.word_rect.center = (self.x, self.y)  # Move the box around as needed

    def move(self):
        self.x += self.x_velocity
