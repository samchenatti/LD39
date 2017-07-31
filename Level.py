from Character import Character
from Camera import Camera
from TileSet import TileSet
from Input import Input
from Player import Player
import pygame

class Level:
    def __init__(self, game, tilemap):
        self.__game     = game

        self.__inputs   = []
        self.__players  = []
        self.__enemys   = []
        self.__objects  = []
        self.__NPCs     = []
        self.__camera   = Camera(game)
        self.__tile_map = None
        self.__tilemap  = tilemap
        # self.__camera.lock_on(self.__players[0])

    def change_game_scene(self, s):
        self.__game.change_scene(s)

    def get_player_list(self):
        return self.__players

    def get_enemy_list(self):
        return self.__enemys

    def remove_object(self, o):
        print(self.__objects)
        self.__objects.remove(o)

    def add_player(self, p):
        return self.__players.append(p)

    def add_object(self, o):
        self.__objects.append(o)

    def add_enemy(self, e):
        self.__enemys.append(e)

    def add_NPC(self, n):
        self.__NPCs.append(n)

    def get_tile_map(self):
        return self.__tile_map

    def get_camera(self):
        return self.__camera

    def get_tile_map(self):
        return self.__tile_map

    def load_resources(self):
        self.__game.change_fill_color((237, 143, 73))
        self.__tile_map = TileSet.load_data(self.__tilemap, self.__camera)

        for p in self.__players:
            p.load_resources()

        for e in self.__enemys:
            e.load_resources()

        for o in self.__objects:
            o.load_resources()

        for n in self.__NPCs:
            n.load_resources()

    def on_screen(self):
        for p in self.__players:
            p.set_level(self)

        for e in self.__enemys:
            e.set_level(self)

        for o in self.__objects:
            o.set_level(self)

        for n in self.__NPCs:
            n.set_level(self)

    def change_fill_color(self, c):
        self.__game.change_fill_color((237, 143, 73))


    def reboot(self):
        self.__game.load_scenes()

    def draw(self, screen):
        self.__tile_map.draw(screen)

        for o in self.__objects:
            o.draw(screen)

        for p in self.__players:
            p.draw(screen)

        for e in self.__enemys:
            e.draw(screen)

        for n in self.__NPCs:
            n.draw(screen)

        for n in self.__NPCs:
            n.draw_dialog(screen)

    def logic(self):
        self.__camera.logic()

        for o in self.__objects:
            o.logic()

        for p in self.__players:
            p.logic()

        for e in self.__enemys:
            e.logic()

        for n in self.__NPCs:
            n.logic()
