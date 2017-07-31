from Character import Character
from Sprite import AnimatedSprite
from Text import Text
import random, pygame

class Spiderboss(Character):
    def __init__(self, level):
        Character.__init__(self, "spiderboss", level)

        self.laser = Laser(self, level.get_camera())
        self.level = level
        self.wait_ticks = 0
        self.state      = "idle"
        self.HPDisplay  = HPDisplay(self, level)
        self.lock_control = False

    def load_resources(self):
        Character.load_resources(self)

        self.set_speed(1)
        self.change_state("idle")
        self.change_direction("front")
        self.walk_area  = self.get_level().get_tile_map().bossarea
        self.player = self.get_level().get_player_list()[0]
        self.set_speed(15)
        self.player_hitted = False
        # self.set_unbockable(True)
        self.walk_to()

        self.dead = False

    def logic(self):
        Character.logic(self)

        if self.lock_control: return

        if self.get_hp() <= 0:
            self.change_animstate("death")

            if self.get_actual_frame() == 15:
                self.dead = True

            if self.dead:
                self.change_animstate("deathidle")

            return


        if self.distance_from_player() <= 100 and self.state == "idle":
            if random.randint(0, 1) == 1:
                self.state = "smash"

        if self.state == "smash":
            self.change_animstate("smash_attack")

            if self.get_actual_frame() >= 3:
                self.player_hitted = True

                if not self.player_hitted:
                    r = pygame.Rect(self.get_coord()[0], self.get_coord()[1], self.get_rect()[2], self.get_rect()[3])
                    if self.player.test_collide(r):
                        self.player.deal_damage(0.2)

                if self.get_actual_frame() == 11:
                    self.player_hitted = False
                    self.state = "idle"

        if self.state == "idle":
            self.change_state("idle")

            self.wait_ticks += 1

            if self.wait_ticks == 120:
                print("Reached")
                self.wait_ticks = 0

                self.change_state == "move"
                self.walk_to()


        if self.state == "eye_attack":
            self.change_animstate("eye_attack")
            self.laser.logic()

            print(self.player.test_collide(self.laser.get_damage_area()))
            if self.player.test_collide(self.laser.get_damage_area()) and not self.player_hitted:
                self.player.deal_damage(0.3)
                self.player_hitted = True

            if self.get_actual_frame() == 11:
                self.laser.shoot()

            if self.get_actual_frame() == self.get_total_frames() - 1:
                self.player_hitted = False
                self.state = "idle"



        if self.state == "move":
            if self.get_coord()[0] < self.__dest[0]:
                self.walk("right")
            self.arrived()

            if self.get_coord()[1] < self.__dest[1]:
                self.walk("down")
            self.arrived()

            if self.get_coord()[0] > self.__dest[0]:
                self.walk("left")
            self.arrived()

            if self.get_coord()[1] > self.__dest[1]:
                self.walk("up")
            self.arrived()

    def arrived(self):
        if (self.get_coord()[0] >= self.__dest[0] and self.get_coord()[0] <= self.__dest[0] + 50 )  and   (self.get_coord()[1] >= self.__dest[1] and self.get_coord()[1] <= self.__dest[1] + 50 ):
            self.state = "eye_attack"
            self.wait_ticks += 0
            print("Changing")

    def draw(self, screen):
        Character.draw(self, screen)
        self.laser.draw(screen)
        self.HPDisplay.draw(screen)


    def walk_to(self, c=None):
        if c:
            self.__dest = c
            self.state = "walk"
            return        # if self.ru:
        #     pygame.draw.rect(screen, (255,255,255), self.ru)
        #     pygame.draw.rect(screen, (255,255,0), self.rd)
        #     pygame.draw.rect(screen, (0,255,255), self.rl)
        #     pygame.draw.rect(screen, (0,0,255), self.rr)

        a = self.walk_area
        b = self.player.get_coord()[0] - self.get_rect()[2]/2 - 40

        print("")
        print("Bossarea")
        print(a[0] + a[2])
        print("Player")
        print(b)
        print("")


        if b >= a[0] and b <= a[0] + a[2]:
            print("Target player")
            self.__dest = [b, random.randint(a[1], a[1] + a[3])]
        else:
            self.__dest = [random.randint(a[0], a[0] + a[2]), random.randint(a[1], a[1] + a[3])]

        self.state = "move"

class Laser():
    def __init__(self, font, camera):
        self.font = font
        self.laser = AnimatedSprite.load_data("spiderlaser", camera)["shoot"]
        self.shooting = False

    def shoot(self):
        self.shooting = True
        self.laser.set_actual_frame(0)

    def logic(self):
        self.laser.logic()
        self.p = [0, 0 ]

        if self.laser.get_actual_frame() == self.laser.get_total_frames() - 1:
            self.shooting = False

    def get_damage_area(self):
        if self.shooting:
            if self.laser.get_actual_frame() >= 0 and self.laser.get_actual_frame() <= 7:
                r = self.laser.get_rect()
                c = [0, 0, 0, 0]

                c[0] = self.font.get_coord()[0]
                c[1] = self.font.get_coord()[1]
                c[2] = r[2]
                c[3] = r[3]

                return pygame.Rect(c[0], c[1], c[2], c[3])
            else:
                return None

    def draw(self, screen):
        if self.shooting:
            c = self.font.get_coord()
            self.p = [0, 0]
            self.p[0] = c[0]
            self.p[1] = c[1]
            self.p[0] -= 5
            self.p[1] += 190
            self.laser.draw(self.p, screen, False)


class HPDisplay:
    def __init__(self, target, level):
        self.__level    = level
        self.__target   = target
        self.__hp_label = Text("100%", 15, [0, 0], level.get_camera(), color=(172, 50, 50))
        self.show = True

    def logic(self):
        return

    def draw(self, screen):
        if self.show == False: return

        s = str(int(self.__target.get_hp()/self.__target.get_max_hp() * 100)) + "%"

        self.__hp_label = Text(s, 15, [0, 0], self.__level.get_camera(), color=(172, 50, 50))

        p = [0, 0]
        c = self.__target.get_coord()

        p[0] = c[0]/2 + 35
        p[1] = c[1] + 187

        # print(self.__target.get_rect())
        p[0] = p[0] + self.__target.get_rect()[2]/2

        self.__hp_label.draw(screen, p)

        # self.__hologram["front_idle"].draw(self.__target.get_coord(), screen, False)
