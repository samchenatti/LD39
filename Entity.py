from Sprite import AnimatedSprite
import pygame, math

class Entity:
    def __init__(self, name, level):
        self.__name          = name
        self.__coord         = [0, 0]
        self.__animations    = None
        self.__actual_state  = "idle"
        self.__looking       = "right"
        self.__level         = level
        self.__blocked       = {"up": False, "left": False, "down": False, "right": False}
        self.__base_speed    = 3
        self.__speed         = 5
        self.__aceleration   = 1
        self.__anim_state    = "side_walk"
        self.__visible       = True
        self.__diagonal      = False

        self.__jumping       = False
        self.__punching      = False

        self.__unblockable   = False

        self.ru = None
        self.rd = None
        self.rl = None
        self.rr = None

    def set_visible(self, b):
        self.__visible = b

    def set_speed(self, s):
        self.__speed = s

    def get_level(self):
        return self.__level

    def get_coord(self):
        return self.__coord

    def set_coord(self, c):
        self.__coord = c

    def load_resources(self):
        self.__animations = AnimatedSprite.load_data(self.__name, self.__level.get_camera())

    def set_unbockable(self, b):
        self.__unblockable = b

        if b:
            self.__blocked["left"]  = False
            self.__blocked["right"] = False
            self.__blocked["up"]    = False
            self.__blocked["down"]  = False

    def logic(self):
        self.__animations[self.__anim_state].logic()
        if not self.__unblockable:
            self.verify_block()

        if self.__jumping:
            a = self.__animations[self.__anim_state]
            if a.get_actual_frame() == a.get_total_frames() - 1:
                self.__jumping = False
                a.set_actual_frame(0)

        if self.__punching:
            a = self.__animations[self.__anim_state]
            if a.get_actual_frame() == a.get_total_frames() - 1:
                self.__punching = False
                # a.set_actual_frame(0)

    def is_punching(self):
        return self.__punching

    def get_rect(self):
        return self.__animations[self.__anim_state].get_rect()
        # return self.__animations[self.__looking + "_" + self.__actual_state].get_rect()

    def get_actual_frame(self):
        return self.__animations[self.__anim_state].get_actual_frame()

    def get_state(self):
        if self.__looking == "right" or self.__looking == "left":
            s = "side_" + self.__actual_state

        return self.__actual_state
        if not self.__unblockable:
            self.verify_block()
    def draw(self, screen):
        if not self.__visible:
            return

        if self.__diagonal:
            if self.__diagonal[0] == "up":
                if self.__diagonal[1] == "right":
                    self.__animations["updiagonal_" + self.__actual_state].draw(self.__coord, screen, False)
                else:
                    self.__animations["updiagonal_" + self.__actual_state].draw(self.__coord, screen, True)

            elif self.__diagonal[0] == "down":
                if self.__diagonal[1] == "right":
                    self.__animations["downdiagonal_" + self.__actual_state].draw(self.__coord, screen, True)
                else:
                    self.__animations["downdiagonal_" + self.__actual_state].draw(self.__coord, screen, False)
            return

        if self.__looking == "right" or self.__looking == "left":
            self.__anim_state = "side_" + self.__actual_state

            if self.__looking == "left":
                self.__animations[self.__anim_state].draw(self.__coord, screen, True)
                return

            self.__animations[self.__anim_state].draw(self.__coord, screen, False)
            return

        self.__animations[self.__anim_state].draw(self.__coord, screen, False)
        self.screen = screen

        # if self.ru:
        #     pygame.draw.rect(screen, (255,255,255), self.ru)
        #     pygame.draw.rect(screen, (255,255,0), self.rd)
        #     pygame.draw.rect(screen, (0,255,255), self.rl)
        #     pygame.draw.rect(screen, (0,0,255), self.rr)


    def set_level(self, level):
        self.__level = level

    def get_total_frames(self):
        return self.__animations[self.__anim_state].get_total_frames()

    def verify_walk(self):
        r = self.__animations[self.__anim_state].get_rect()
        r = pygame.Rect((self.__coord[0],self.__coord[1] + r.h/2),(r.w,r.h/2))

        for walk in self.__level.get_tile_map().walk_path:
            if walk.colliderect(r):
                return

    def verify_block(self):
        r  = self.__animations[self.__anim_state].get_rect()

        ru = pygame.Rect((self.__coord[0] + r.w/4, self.__coord[1] + 5),(r.w/2,r.h/8))
        rd = pygame.Rect((self.__coord[0] + r.w/4, self.__coord[1] + r.h - 10),(r.w/2,r.h/8))
        rl = pygame.Rect((self.__coord[0],self.__coord[1] + r.h/4),(r.w/8,r.h/2))
        rr = pygame.Rect((self.__coord[0] + r.w,self.__coord[1] + r.h/4),(r.w/8,r.h/2))

        self.ru = ru
        self.rd = rd
        self.rl = rl
        self.rr = rr

        self.__blocked["left"]  = False
        self.__blocked["right"] = False
        self.__blocked["up"]    = False
        self.__blocked["down"]  = False

        for block in self.__level.get_tile_map().block_objects:
            if block.colliderect(rl):
                self.__blocked["left"] = True

            if block.colliderect(ru):
                self.__blocked["up"] = True

            if block.colliderect(rd):
                self.__blocked["down"] = True

            if block.colliderect(rr):
                self.__blocked["right"] = True

    def is_visible(self):
        return self.__visible

    def walk(self, dir, diagonal=False):
        self.__diagonal = False
        if dir == "right" and not self.__blocked["right"]:
            self.__coord[0] += self.__speed
            self.change_direction("right")
            self.change_state("walk")

        if dir == "left" and not self.__blocked["left"]:
            self.__coord[0] -= self.__speed
            self.change_direction("left")
            self.change_state("walk")

        if dir == "up" and not self.__blocked["up"]:
            self.__coord[1] -= self.__speed
            self.change_direction("back")
            self.change_state("walk")

        if dir == "down" and not self.__blocked["down"]:
            self.__coord[1] += self.__speed
            self.change_direction("front")
            self.change_state("walk")

        if dir == "updiagonal_right_" and (not self.__blocked["up"] and not self.__blocked["right"]):
            self.__coord[1] -= self.__speed
            self.__coord[0] += self.__speed
            self.__diagonal = ["up", "right"]

            self.change_direction("updiagonal")
            self.change_state("walk")

        if dir == "updiagonal_left_" and (not self.__blocked["up"] and not self.__blocked["right"]):
            self.__coord[1] -= self.__speed
            self.__coord[0] -= self.__speed
            self.__diagonal = ["up", "left"]

            self.change_direction("updiagonal")
            self.change_state("walk")

        if dir == "downdiagonal_left_" and (not self.__blocked["up"] and not self.__blocked["right"]):
            self.__coord[1] += self.__speed
            self.__coord[0] -= self.__speed
            self.__diagonal = ["down", "left"]

            self.change_direction("downdiagonal")
            self.change_state("walk")

        if dir == "downdiagonal_right_" and (not self.__blocked["up"] and not self.__blocked["right"]):
            self.__coord[1] += self.__speed
            self.__coord[0] += self.__speed
            self.__diagonal = ["down", "right"]

            self.change_direction("downdiagonal")
            self.change_state("walk")

        if dir == "jump":
            self.change_state("jump")
            self.__jumping = True

        if dir == "punch":
            self.change_state("punch")

            p = pygame.Rect(self.__coord[0], self.__coord[1], self.get_rect()[2], self.get_rect()[3])
            for e in self.__level.get_enemy_list():
                if e.test_collide(p):
                    e.deal_damage(0.1)

            self.__jumping = True

    def is_jumping(self):
        return self.__jumping

    def get_animstate(self):
        return self.__anim_state

    def change_animstate(self, s=None):
        if s:
            if s == self.__anim_state: return

            self.__looking = "front"
            self.__anim_state = s
            self.__animations[self.__anim_state].set_actual_frame(0)
            return

        if self.__looking == "right" or self.__looking == "left":
            self.__anim_state = "side_" + self.__actual_state
            return

        self.__anim_state = self.__looking + "_" + self.__actual_state

    def change_direction(self, dir):
        self.__looking = dir
        self.change_animstate()

    def change_state(self, state):
        if state != self.__actual_state:
            self.__actual_state = state
        self.change_animstate()

    def distance_from_player(self):
        p = self.__level.get_player_list()[0].get_coord()
        return self.dist([self.__coord[0], self.__coord[1]], [p[0], p[1]])

    def test_collide(self, r1):
        if r1 == None: return

        r2 = [0, 0, 0, 0]
        r2[0] = self.__coord[0]
        r2[1] = self.__coord[1]

        r2[2] = self.__animations[self.__anim_state].get_rect()[2]
        r2[3] = self.__animations[self.__anim_state].get_rect()[3]

        r2 = pygame.Rect(r2[0], r2[1], r2[2], r2[3])
        return r1.colliderect(r2)

    def reboot(self):
        self.__level.reboot()


    def dist(self, e1, e2):
        x1 = int(e1[0])
        y1 = int(e1[1])
        x2 = int(e2[0])
        y2 = int(e2[1])

        return math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

    def is_blocked(self):
        return self.__blocked["up"] or self.__blocked["down"] or self.__blocked["left"] or self.__blocked["right"]
