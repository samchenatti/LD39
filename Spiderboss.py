from Character import Character
from Sprite import AnimatedSprite
from Text import Text
from Player import HPDisplay
import random, pygame

class Spiderboss(Character):
    def __init__(self, level):
        Character.__init__(self, "spiderboss", level)

        self.laser = Laser(self, level.get_camera())
        self.level = level
        self.wait_ticks = 0
        self.state      = "idle"
        self.HPDisplay  = HPDisplay(self, level, offset=[15, 187], color=(255, 220, 220))
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

        self.add_hitbox(pygame.Rect((96, 228), (151, 23)))
        self.add_hitbox(pygame.Rect((63, 197), (218, 33)))
        self.add_hitbox(pygame.Rect((44, 164), (253, 33)))
        #Patas
        self.add_hitbox(pygame.Rect((297, 234), (19, 48)))
        self.add_hitbox(pygame.Rect((9, 234), (21, 49)))
        #CorpoSuperior
        self.add_hitbox(pygame.Rect((38, 84), (265, 81)))

        self.set_unbockable(True)

        self.dead = False

    def logic(self):
        Character.logic(self)

        if self.lock_control: return

        if self.get_hp() <= 0:
            self.change_animstate("death")
            self.shooting = False

            if self.get_actual_frame() == 15:
                self.dead = True

            if self.dead:
                self.change_animstate("deathidle")

            return


        if self.state == "repell":
            self.change_animstate("repell")
            if self.get_actual_frame() == self.get_total_frames() - 1:
                self.state = "idle"

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

                c = pygame.Rect((0,0), (0,0))

                c.x = self.player.get_coord()[0]
                c.y = self.player.get_coord()[1]
                c.width  = self.player.get_rect().width
                c.height = self.player.get_rect().height

                if self.test_collide(c):
                    self.state = "repell"

                    if self.player.get_coord()[0] < self.get_coord()[0] + self.get_rect().width/2:
                        self.player.repell(500, "left")
                    else:
                        self.player.repell(500, "right")

                    self.player.deal_damage(0.21)
                else:
                    self.change_state == "move"
                    self.walk_to()


        if self.state == "eye_attack":
            self.change_animstate("eye_attack")
            self.laser.logic()

            if not self.player_hitted and self.laser.dealing_damage and self.laser.shooting:
                for hb in self.laser.get_damage_area():
                    print(self.player.test_collide(hb))
                    if self.player.test_collide(hb):
                        self.player.deal_damage(0.3)
                        self.player_hitted = True

            if self.get_actual_frame() == 11:
                self.laser.shoot()

            if self.get_actual_frame() == self.get_total_frames() - 1:
                self.player_hitted = False
                self.state = "idle"



        if self.state == "move":
            c = pygame.Rect((0,0), (0,0))

            c.x = self.player.get_coord()[0]
            c.y = self.player.get_coord()[1]
            c.width  = self.player.get_rect().width
            c.height = self.player.get_rect().height


            if self.test_collide(c):
                self.state = "repell"

                if self.player.get_coord()[0] < self.get_coord()[0] + self.get_rect().width/2:
                    self.player.repell(500, "left")
                else:
                    self.player.repell(500, "right")

                    self.player.deal_damage(0.21)


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
        self.dealing_damage = False

        self.hba = pygame.Rect((0, 0), (0,0))
        self.hbb = pygame.Rect((0, 0), (0,0))
        self.hbc = pygame.Rect((0, 0), (0,0))
        self.hbd = pygame.Rect((0, 0), (0,0))
        self.hbe = pygame.Rect((0, 0), (0,0))
        self.hbf = pygame.Rect((0, 0), (0,0))
        self.hbg = pygame.Rect((0, 0), (0,0))
        self.hbh = pygame.Rect((0, 0), (0,0))

    def shoot(self):
        self.shooting = True
        self.laser.set_actual_frame(0)

    def logic(self):
        self.laser.logic()
        self.p = [0, 0 ]

        if self.laser.get_actual_frame() == self.laser.get_total_frames() - 1:
            self.shooting = False

        if self.laser.get_actual_frame() >= 0 and self.laser.get_actual_frame() <= 7:
            self.dealing_damage = True
        else:
            self.dealing_damage = False

    def get_damage_area(self):
        if self.shooting and self.dealing_damage:
            r = self.laser.get_rect()
            c = [0, 0, 0, 0]

            c[0] = self.font.get_coord()[0] - 5
            c[1] = self.font.get_coord()[1] + 190
            c[2] = r[2]
            c[3] = r[3]

            hitboxes = []

            self.hba = pygame.Rect((c[0] + 30, c[1] + 628), (279, 171))
            self.hbb = pygame.Rect((c[0] + 66, c[1] + 482), (211, 147))
            self.hbc = pygame.Rect((c[0] + 90, c[1] + 370), (166, 110))
            self.hbd = pygame.Rect((c[0] + 109, c[1] + 276), (128, 95))
            self.hbe = pygame.Rect((c[0] + 126, c[1] + 181), (92, 101))
            self.hbf = pygame.Rect((c[0] + 143, c[1] + 113), (62, 73))
            self.hbg = pygame.Rect((c[0] + 155, c[1] + 55), (38, 64))

            hitboxes.append(self.hba)
            hitboxes.append(self.hbb)
            hitboxes.append(self.hbc)
            hitboxes.append(self.hbd)
            hitboxes.append(self.hbe)
            hitboxes.append(self.hbf)
            hitboxes.append(self.hbg)
            hitboxes.append(self.hbh)

            return hitboxes

    def draw(self, screen):
        if self.shooting:
            c = self.font.get_coord()
            self.p = [0, 0]
            self.p[0] = c[0]
            self.p[1] = c[1]
            self.p[0] -= 5
            self.p[1] += 190
            self.laser.draw(self.p, screen, False)

            # pygame.draw.rect(screen, (255,255,255), self.hba)
            # pygame.draw.rect(screen, (255,255,255), self.hbb)
            # pygame.draw.rect(screen, (255,255,255), self.hbc)
            # pygame.draw.rect(screen, (255,255,255), self.hbd)
            # pygame.draw.rect(screen, (255,255,255), self.hbe)
            # pygame.draw.rect(screen, (255,255,255), self.hbf)
            # pygame.draw.rect(screen, (255,255,255), self.hbg)
            # pygame.draw.rect(screen, (255,255,255), self.hbh)
