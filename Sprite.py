import json,pygame
from Camera import Camera

class AnimatedSprite:
    def __init__(self, camera):
        self.frames       = []
        self.actual_frame = 0
        self.data_path    = None
        self.frame_rate   = 0.1
        self.ticks        = 0
        self.camera       = camera
        self.lock_on_last = False
        self.locked       = False
        self.hide         = False
        self.total_frames = 0

    def create_animation(self, tag, frames, image, name, locked):
        self.lock_on_last  = locked

        first_frame = tag["from"]
        last_frame  = tag["to"]

        sprite_sheet = pygame.image.load(image)

        for frame in range(first_frame, last_frame + 1):
            #Defines the region to be blitted
            f = name + " " + str(frame) + ".ase"
            left   = frames[f]["frame"]["x"]
            top    = frames[f]["frame"]["y"]
            width  = frames[f]["frame"]["w"]
            height = frames[f]["frame"]["h"]
            rect   = pygame.Rect(left, top, width, height)

            #Load the frame to memmory
            tmp_frame = pygame.Surface((width, height))
            tmp_frame.blit(sprite_sheet, (0,0), rect)
            tmp_frame.set_colorkey((255,0,255))

            self.frames.append(tmp_frame)

        self.total_frames = len(self.frames)

    def set_actual_frame(self, f):
        self.actual_frame = f

    def get_actual_frame(self):
        return self.actual_frame

    def get_total_frames(self):
        return self.total_frames

    #Factory
    def load_data(data, camera):
        print(data + " loaded")
        name = data.split(".")[0]
        with open("Resources/" + data + ".json") as data_file:
            data = json.load(data_file)

        animations = {}
        image  = data["meta"]["image"]
        frames = data["frames"]

        if "lock_on_last" in data["meta"]:
            l = True
        else:
            l = False

        for tag in data["meta"]["frameTags"]:
            animations[tag["name"]] = AnimatedSprite(camera)
            animations[tag["name"]].create_animation(tag, frames, image, name, l)

        return animations

    def logic(self):
        self.ticks += 1

        # if self.ticks/(60 * self.frame_rate) == 1:
        if self.ticks/60 >= self.frame_rate:
            self.actual_frame += 1
            self.ticks = 0

        if self.actual_frame == len(self.frames):
            self.actual_frame = 0
            # if self.lock_on_last:
                # self.locked = True

    def locked():
        return self.locked

    def get_rect(self):
        return self.frames[self.actual_frame].get_rect()

    def draw(self, coord, surface, left, lockOn=None):
        if self.frames[self.actual_frame].get_rect().colliderect(self.camera.camera_rect): print('not rect')
        if self.hide: return

        frame  = self.frames[self.actual_frame]
        rect   = frame.get_rect()

        coord  = [coord[0] - self.camera.coord[0], coord[1] - self.camera.coord[1]]

        if left:
            if lockOn:
                coord[0] = coord[0] - (self.frames[self.actual_frame].get_rect().width - lockOn.get_rect().width)

            surface.blit(pygame.transform.flip(frame, True, False), coord, frame.get_rect())

        else:
            surface.blit(frame, coord, frame.get_rect())
