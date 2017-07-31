from Character import Character
import pygame

class NPC(Character):
    def __init__(self, name, level, dialog):
        Character.__init__(self, name, level)
        self.dialog = dialog

    def load_resources(self):
        Character.load_resources(self)
        self.change_animstate("idle")
        self.dialog = Dialog(self, self.dialog)

    def logic(self):
        Character.logic(self)

        if self.distance_from_player() < 100:
            self.change_animstate("speak")
        else:
            self.change_animstate("idle")

    def draw(self, screen):
        Character.draw(self, screen)

    def draw_dialog(self, screen):
        if self.distance_from_player() < 100:
            self.dialog.draw(screen)

class Dialog:
    def __init__(self, target, dialog):
        self.label  = pygame.image.load("Resources/" + dialog + ".png")
        self.target = target

    def draw(self, screen):
        t = self.target.get_coord()
        print(t)
        p = [0, 0]

        p[0] = t[0] + self.target.get_rect()[2]/2 - self.label.get_rect()[2]/2
        p[1] = t[1] - self.target.get_rect()[3] - 25

        screen.blit(self.label, p, self.label.get_rect())
