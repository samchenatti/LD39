import pygame
from Warpzone import Warpzone
from BossArea1 import BossArea1
from Intro import Intro
from Text import Text

class Game:
    def __init__(self):
        pygame.init()

        self.__status_text  = Text("Pre alpha (0.0.1) | FPS: ", 10, [15, 15])

        self.__width        = 1280
        self.__height       = 720
        self.__window_flags = pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF

        self.__screen       = pygame.display.set_mode((self.__width, self.__height ), self.__window_flags)

        self.__fill_color   = (0, 0, 0)

        self.__game_running = True

        self.__clock   = pygame.time.Clock()


        self.global_variables = {}
        self.global_variables["played_intro"] = True

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


            self.__status_text  = Text("Pre alpha (0.0.1) | FPS: " + str(int(self.__clock.get_fps())), 20, [100, 15])
            self.__status_text.draw(self.__screen, [120, 20])

            pygame.display.flip()

            self.__clock.tick(60)


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

if __name__ == '__main__':
    g = Game()
    g.main_loop()
