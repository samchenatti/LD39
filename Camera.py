import pygame

class Camera:
    def __init__(self, game):
        self.coord       = [0,0]
        self.target      = None
        self.window_size = game.get_window_size()
        self.game        = game
        self.camera_rect = pygame.Rect(game.get_window_size(), (0,0))

        self.game.camera_region = self.camera_rect

    def lock_on(self, entity):
        self.target = entity

    def logic(self):
        if self.target:
            self.coord[0] =  self.target.get_coord()[0] - self.window_size[1]/2
            self.coord[1] =  self.target.get_coord()[1] - self.window_size[0]/2

    def draw(self, screen):
        return
