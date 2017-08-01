from Level import Level
from Spiderboss import Spiderboss
import pygame

class BossArea1(Level):
    def __init__(self, g):
        Level.__init__(self, g, "bosszone1")

        self.spider = Spiderboss(self)
        self.spider.set_coord([g.get_window_size()[0]/2, 0])
        self.spider.set_coord([65, 75])

        self.blink_mask  = pygame.Surface((1280, 720))
        self.blink_mask.fill((255,255,255))
        self.blink_ticks = 0
        self.blinking = True

        self.player = g.global_variables["player"]
        self.player.set_coord([1050, 700])

        self.add_player(self.player)
        self.add_enemy(self.spider)

        self.spider.lock_control = True
        self.intro = True
        self.show_dialog = False
        self.dialog_ticks = 300

        self.dialog = Dialog(self.spider, "")

    def on_screen(self):
        Level.on_screen(self)
        self.player.set_coord([1016, 674])

    def logic(self):
        Level.logic(self)

        if self.intro:
            if self.spider.distance_from_player() < 800:
                self.player.lock_control(True)
                self.player.change_state("idle")
                self.show_dialog = True

                self.dialog_ticks -= 1
                if self.dialog_ticks == 0:
                    self.show_dialog = False
                    self.player.lock_control(False)
                    self.spider.lock_control = False
                    self.intro = False


    def draw(self, screen):
        Level.draw(self, screen)

        if self.show_dialog == True:
            self.dialog.draw(screen)

    def blink_screen(self):
        return

class Dialog:
    def __init__(self, target, dialog):
        self.label  = pygame.image.load("Resources/spidertitles.png").convert()
        self.label.set_colorkey((255,0,255))
        self.target = target

    def draw(self, screen):
        t = self.target.get_coord()
        print(t)
        p = [0, 0]

        p[0] = t[0] + self.target.get_rect()[2] + 5
        p[1] = t[1] - self.target.get_rect()[3]/2 + 120

        screen.blit(self.label, p, self.label.get_rect())
