from Entity import Entity

class Character(Entity):
    def __init__(self, name, level):
        Entity.__init__(self, name, level)
        self.__hit_points = 120
        self.__max_hp     = 120

    def change_hp(self, hp):
        self.__hit_points = hp

    def deal_damage(self, d):
        if d < 1:
            self.__hit_points -= d * self.__max_hp
        else:
            self.__hit_points -= d

    def get_hp(self):
        return self.__hit_points

    def get_max_hp(self):
        return self.__max_hp

    def logic(self):
        Entity.logic(self)

    def draw(self, screen):
        Entity.draw(self, screen)
