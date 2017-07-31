import json,pygame
import Entity as Entity
from Camera import Camera

class TileSet:
    def __init__(self, camera):
        self.tile_map         = None
        self.tile_map_front   = None
        self.cover_objects    = []
        self.block_objects    = []
        self.walk_path        = []
        self.walk_inclination = []
        self.player_spawn     = []
        self.objects          = {}
        self.camera           = camera
        self.images           = []
        self.bossarea        = None

    def logic(self):
        return

    def draw(self, screen):
        c = [0 - self.camera.coord[0], 0 - self.camera.coord[1]]

        if self.images:
            screen.blit(self.images[0][0], c, self.images[0][0].get_rect())

        screen.blit(self.tile_map, c, self.tile_map.get_rect())

        # for b in self.block_objects:
        #     pygame.draw.rect(screen, (255,255,255), b)

    def draw_front(self,screen):
        c = [0 - self.camera.coord[0], 0 - self.camera.coord[1]]
        screen.blit(self.tile_map_front, c, self.tile_map.get_rect())

    def create_tileset(self, data):
        h = data["tileheight"] * data["height"]
        w = data["width"] * data["tilewidth"]
        self.tile_map       =  pygame.Surface((w,h))
        self.tile_map_front =  pygame.Surface((w,h))
        self.tile_map.fill((255,0,255))
        self.tile_map_front.fill((255,0,255))
        self.tile_map.set_colorkey((255,0,255))
        self.tile_map_front.set_colorkey((255,0,255))

        tiles = []
        ix = 0
        for tileset in data["tilesets"]:
            sprite_sheet = pygame.image.load("Resources/" + tileset["image"])
            th = tileset["tileheight"]
            tw = tileset["tilewidth"]
            ih = tileset["imageheight"]
            iw = tileset["imagewidth"]

            for i in range(0, int(ih/th)):
                for j in range(0, int(iw/tw)):
                    tile = pygame.Surface((tw, th))
                    tile.set_colorkey((255,0,255))
                    tile.blit(sprite_sheet, (0, 0), pygame.Rect(j*tw, i*th, tw, th))
                    tiles.append([tile, th, tw])

        for layer in data["layers"]:
            if layer["type"] == "tilelayer":
                mh       = layer["height"]
                mw       = layer["width"]
                th       = data ["tileheight"]
                tw       = data ["tilewidth"]
                l        = pygame.Surface((self.tile_map.get_rect().width, self.tile_map.get_rect().height))

                l.set_colorkey((255,0,255))
                l.fill((255, 0, 255))

                k = 0
                for i in range(mh):
                    for j in range(mw):
                        tile = tiles[layer["data"][k] - 1]
                        # self.tile_map.blit(tile[0], (j*tw, i*th), tile[0].get_rect())
                        l.blit(tile[0], (j*tw, i*th), tile[0].get_rect())
                        k += 1

                if "properties" in layer:
                    if layer["properties"]["front"]:
                        self.tile_map_front.blit(l, (0,0), l.get_rect())
                else:
                    self.tile_map.blit(l, (0, 0), l.get_rect())


            if layer["type"] == "objectgroup":
                for obj in layer["objects"]:
                    x = obj["x"]
                    y = obj["y"]
                    w = obj["width"]
                    h = obj["height"]

                    if obj["type"] == "block":
                        self.block_objects.append(pygame.Rect((x,y),(w,h)))
                    if obj["type"] == "walk_path":
                        self.walk_path.append(pygame.Rect((x,y), (w,h)))
                    if obj["type"] == "walk_inclination":
                        self.walk_inclination.append(pygame.Rect((x,y), (w,h)))
                    if obj["type"] == "player_spawn":
                        self.player_spawn.append(pygame.Rect((x,y), (w,h)))
                    if obj["type"] == "cover":
                        self.cover_objects.append(pygame.Rect((x,y), (w,h)))
                    if obj["type"] == "bossarea":
                        self.bossarea = pygame.Rect((x,y), (w,h))
                    if obj["type"] == "b1":
                        self.b1 = pygame.Rect((x,y), (w,h))
                    else:
                        self.objects[obj["name"]] = pygame.Rect((x,y),(w,h))

            if layer["type"] == "imagelayer":
                i = pygame.image.load("Resources/" + layer["image"])
                i.set_colorkey((255,0,255))
                self.images.append([i, layer["x"], layer["y"]])



    def load_data(data, camera):
        n = data
        with open("Resources/" + data + ".json") as data_file:
            data = json.load(data_file)

        tileSet = TileSet(camera)
        tileSet.create_tileset(data)
        print("Tileset loaded: " + n)
        return tileSet
