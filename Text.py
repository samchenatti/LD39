import pygame

class Text:
    def __init__(self, text, size, pos, camera=None, color=None):
        font         = pygame.font.Font("font.ttf", size)

        if color == None:
            color = (255,255,255)

        self.label   = font.render(text, True, color)
        self.pos     = (int(pos[0] - (self.label.get_rect().width/2)), int(pos[1] - self.label.get_rect().height/2))
        self.camera  = camera
        self.color   = color

    # def draw(self, surface):
    #     surface.blit(self.label, self.pos)

    def draw(self, surface, pos):
        if pos != None:
            self.pos     = (pos[0] - (self.label.get_rect().width/2), pos[1] - self.label.get_rect().height/2)
        surface.blit(self.label, self.pos)
