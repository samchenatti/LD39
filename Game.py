import pygame
from Warpzone import Warpzone
from BossArea1 import BossArea1
from Intro import Intro

class Game:
    def __init__(self):
        pygame.init()

        self.__width        = 1280
        self.__height       = 720
        self.__window_flags = pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF

        self.__screen       = pygame.display.set_mode((self.__width, self.__height ), self.__window_flags)

        self.__fill_color   = (0, 0, 0)

        self.__game_running = True

        self.__clock   = pygame.time.Clock()


        self.global_variables = {}
        self.global_variables["played_intro"] = False

        self.load_scenes()

    def main_loop(self):
        while(self.__game_running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT or  pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.__game_running = False

            # Logic cycle
            self.__actual_scene.logic()

            # Draw cycle
            self.__screen.fill(self.__fill_color)
            self.__actual_scene.draw(self.__screen)

            pygame.display.flip()

            self.__clock.tick(60)

            # print(self.__clock.get_fps())

    def load_scenes(self):
        w  = Warpzone(self)
        w.load_resources()

        b1 = BossArea1(self)
        b1.load_resources()

        self.global_variables["warpzone"] = w
        self.global_variables["bossarea1"] = b1

        if self.global_variables["played_intro"] == False:
            i = Intro(self)
            i.load_resources()
            self.global_variables["played_intro"] = True
            self.__actual_scene = i
        else:
            self.__actual_scene = w

    def get_window_size(self):
        return [self.__height, self.__width]

    def change_scene(self, s):
        self.__actual_scene = self.global_variables[s]
        self.__actual_scene.on_screen()

    def change_fill_color(self, c):
        print("Fill changed")
        self.__fill_color = c

g = Game()
g.main_loop()
