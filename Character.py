from Entity import Entity

class Character(Entity):
    def __init__(self, name, level):
        Entity.__init__(self, name, level)
        self.__hit_points       = 120
        self.__max_hp           = 120

        self.__repelling        = False
        self.__repelling_target = 0
        self.__repelling_acc    = 10

    def repell(self, distance, direction):
        if direction == "right":
            self.__repelling_target = self.get_coord()[0] + distance
        elif direction == "left":
            self.__repelling_target = self.get_coord()[0] - distance

        self.__repelling_acc = 10
        self.__repelling = True

    def change_hp(self, hp):
        self.__hit_points = hp

    def verify_hit(self, h):
        self.get_hitbox().colliderect()

    def deal_damage(self, d):
        if d < 1:
            self.__hit_points -= d * self.__max_hp
        else:
            self.__hit_points -= d

        self.blink()

    def get_hp(self):
        return self.__hit_points

    def get_max_hp(self):
        return self.__max_hp

    def logic(self):
        Entity.logic(self)

        if self.__repelling:
            self.lock_control(True)

            c = self.get_coord()

            offset = [0, 0]
            offset[0] = c[0]
            offset[1] = c[1]

            if c[0] > self.__repelling_target:
                if self.is_blocked("left"):
                    self.__repelling = False
                    self.lock_control(False)
                else:
                    c[0] -= 3 + self.__repelling_acc

            if c[0] < self.__repelling_target:
                if self.is_blocked("right"):
                    self.__repelling = False
                    self.lock_control(False)
                else:
                    c[0] += 3 + self.__repelling_acc

            if self.__repelling_acc >= 0:
                self.__repelling_acc -= 0.1

            if (c[0] >= self.__repelling_target and c[0] <= self.__repelling_target + 20):
                self.__repelling = False
                self.lock_control(False)

    def draw(self, screen):
        Entity.draw(self, screen)
