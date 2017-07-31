from Level import Level
from Player import Player
from Input import Input
from Timemachine import Timemachine
from Spiderboss import Spiderboss
from NPC import NPC
import pygame

class Warpzone(Level):
    def __init__(self, g):
        Level.__init__(self, g, "warpzone")

        self.npc1 = NPC("npc1", self, "dialog1")
        self.npc1.set_coord([170, 100])

        self.npc2 = NPC("npc2", self, "dialog2")
        self.npc2.set_coord([967, 309])

        self.npc3 = NPC("npc3", self, "dialog3")
        self.npc3.set_coord([300, 497])

        self.npc4 = NPC("npc4", self, "dialog4")
        self.npc4.set_coord([147, 290])

        self.player = Player("roboot2", self, Input(None, "keyboard"))
        self.player.set_visible(False)

        self.time_machine = Timemachine("timemachine", self)
        self.time_machine.set_coord([g.get_window_size()[1]/2, g.get_window_size()[0]/2])

        self.add_object(self.time_machine)
        self.add_player(self.player)
        self.add_NPC(self.npc1)
        self.add_NPC(self.npc2)
        self.add_NPC(self.npc3)
        self.add_NPC(self.npc4)

        self.fade_ticks = 255
        self.black = pygame.Surface((g.get_window_size()[1], g.get_window_size()[0]))
        self.black.fill([0, 0, 0])

        self.intro_end = False

        g.global_variables["player"]   = self.player


    def load_resources(self):
        Level.load_resources(self)

        # self.b1 = self.get_tile_map().b1

    def on_screen(self):
        Level.on_screen(self)
        self.change_fill_color((237, 143, 73))


    def draw(self, screen):
        Level.draw(self, screen)

        if self.fade_ticks >= 0:
            screen.blit(self.black, (0, 0), self.black.get_rect())

    def logic(self):
        Level.logic(self)
        self.fade_ticks -= 1

        self.black.set_alpha(self.fade_ticks)

        if self.player.test_collide(self.get_tile_map().b1):
            self.change_game_scene("bossarea1")

        if self.time_machine.end == True and self.intro_end == False:
            self.player.lock_control(False)
            self.player.set_coord([640 + 46, 360 + 64])
            self.player.set_visible(True)
            self.intro_end = True
