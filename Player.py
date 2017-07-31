import pygame
from Character import Character
from Sprite import AnimatedSprite
from Text import Text

class Player(Character):
    def __init__(self, name, level, input):
        Character.__init__(self, name, level)
        self.__input = input
        self.__lock_control = True

        self.__hp_marker = HPDisplay(self, level)

        self.set_speed(2)
        self.set_coord([100, 100])
        self.change_direction("front")

        self.ticks = 0

    def load_resources(self):
        Character.load_resources(self)

    def lock_control(self, b):
        self.__lock_control = b

    def logic(self):
        Character.logic(self)

        if self.get_hp() <= 0:
            self.change_animstate("death")
            self.__hp_marker.show = False

            if self.get_actual_frame() == 21:
                self.reboot()

            return

        if self.__lock_control or self.is_jumping() or self.is_punching():
            return

        keys = self.__input.get_input()
        if keys["K_RIGHT"]:
            if keys["K_UP"]:
                self.walk("updiagonal_right_")
            elif keys["K_DOWN"]:
                self.walk("downdiagonal_right_")
            else:
                self.walk("right")

        elif keys["K_LEFT"]:
            if keys["K_UP"]:
                self.walk("updiagonal_left_")
            elif keys["K_DOWN"]:
                self.walk("downdiagonal_left_")
            else:
                self.walk("left")

        elif keys["K_UP"]:
            self.walk("up")

        elif keys["K_DOWN"]:
            self.walk("down")


        if keys["K_JUMP"]:
            self.walk("jump")

        if keys["K_PUNCH"]:
            self.walk("punch")

        if not keys["K_LEFT"] and not keys["K_RIGHT"] and not keys["K_UP"] and not keys["K_DOWN"] and not self.is_jumping():
            self.change_state("idle")

        self.ticks += 1

        if self.ticks % 60 == 0:
            self.deal_damage(1)


    def draw(self, screen):
        Character.draw(self, screen)

        if self.is_visible():
            self.__hp_marker.draw(screen)


class HPDisplay:
    def __init__(self, target, level):
        self.__level    = level
        self.__target   = target
        self.__hp_label = Text("100%", 15, [0, 0], level.get_camera())
        self.__hologram = AnimatedSprite.load_data("hologram", self.__level.get_camera())
        self.show = True

    def logic(self):
        return

    def draw(self, screen):
        if self.show == False: return

        s = str(int(self.__target.get_hp()/self.__target.get_max_hp() * 100)) + "%"

        self.__hp_label = Text(s, 15, [0, 0], self.__level.get_camera())

        p = [0, 0]
        c = self.__target.get_coord()

        p[0] = c[0]
        p[1] = c[1]

        # print(self.__target.get_rect())
        p[0] = p[0] + self.__target.get_rect()[2]/2

        self.__hp_label.draw(screen, p)

        # self.__hologram["front_idle"].draw(self.__target.get_coord(), screen, False)
