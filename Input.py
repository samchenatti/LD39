import pygame

class Input():
    def __init__(self, joystick, type):
        self.type     = type
        self.joystick = joystick
        self.states   = {"K_RIGHT": False, "K_LEFT": False}

        if self.joystick:
            joystick.init()

    def get_input(self):
        if self.type == "keyboard":
            keys  = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                self.states["K_RIGHT"] = True
            else:
                self.states["K_RIGHT"] = False

            if keys[pygame.K_LEFT]:
                self.states["K_LEFT"] = True
            else:
                self.states["K_LEFT"] = False

            if keys[pygame.K_UP]:
                self.states["K_UP"] = True
            else:
                self.states["K_UP"] = False

            if keys[pygame.K_DOWN]:
                self.states["K_DOWN"] = True
            else:
                self.states["K_DOWN"] = False

            if keys[pygame.K_SPACE]:
                self.states["K_JUMP"] = True
            else:
                self.states["K_JUMP"] = False

            if keys[pygame.K_LSHIFT]:
                self.states["K_RUN"] = True
            else:
                self.states["K_RUN"] = False

            if keys[pygame.K_a]:
                self.states["K_PUNCH"] = True
            else:
                self.states["K_PUNCH"] = False

            if keys[pygame.K_e]:
                self.states["K_ACTION"] = True
            else:
                self.states["K_ACTION"] = False

            if keys[pygame.K_r]:
                self.states["K_RELOAD"] = True
            else:
                self.states["K_RELOAD"] = False

            return self.states

        #Por agora so funciona com DS3
        if self.joystick.get_button(5):
            self.states["K_RIGHT"] = True
        else:
            self.states["K_RIGHT"] = False

        if self.joystick.get_button(7):
            self.states["K_LEFT"] = True
        else:
            self.states["K_LEFT"] = False

        if self.joystick.get_button(8):
            self.states["K_RUN"] = True
        else:
            self.states["K_RUN"] = False

        if self.joystick.get_button(9):
            self.states["K_FIRE"] = True
        else:
            self.states["K_FIRE"] = False

        if self.joystick.get_button(14):
            self.states["K_ACTION"] = True
        else:
            self.states["K_ACTION"] = False

        if self.joystick.get_button(15):
            self.states["K_RELOAD"] = True
        else:
            self.states["K_RELOAD"] = False

        return self.states

    def no_input(self):
        for i in [5, 7, 8, 9, 14]:
            if self.joystick.get_button(i):
                return False

        return True
