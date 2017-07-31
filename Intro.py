from Text import Text
from Input import Input
import pygame

class Intro:
    def __init__(self, game):
        c = [game.get_window_size()[1]/2, game.get_window_size()[0]/2]
        self.texts = []
        self.texts.append(pygame.image.load("Resources/intro/1.png"))
        self.texts.append(pygame.image.load("Resources/intro/2.png"))
        self.texts.append(pygame.image.load("Resources/intro/3.png"))
        self.texts.append(pygame.image.load("Resources/intro/4.png"))
        self.texts.append(pygame.image.load("Resources/intro/5.png").convert())

        self.game  = game
        self.ticks = 0

        self.image = 0

        self.input = Input(None, "keyboard")
        self.inputlag  = 0

        self.fadeout = 255

    def load_resources(self):
        return

    def logic(self):
        self.ticks += 1

        keys = self.input.get_input()

        self.inputlag += 1
        if self.inputlag >= 60:
            if keys["K_PUNCH"]:
                self.image += 1
                self.inputlag = 0

        if self.image >= 5:
            self.texts[4].set_alpha(self.fadeout)
            self.fadeout -= 1
            print(self.fadeout)
            if self.fadeout == 0:
                self.game.change_scene("warpzone")

    def draw(self, screen):
        self.game.change_fill_color((0, 0, 0))
        # print(self.texts[int(self.ticks/120)].pos)
        if self.image < 5:
            screen.blit(self.texts[self.image], (0, 0), self.texts[self.image].get_rect())
        else:
            print("HSAHUSHAU")
            screen.blit(self.texts[4], (0,0), self.texts[4].get_rect())
