from Entity import Entity

class Timemachine(Entity):
    def __init__(self, name, level):
        Entity.__init__(self, name, level)

        self.__ticks = 0
        self.__level = level
        self.end = False

        self.change_state("spawning")
        self.change_direction("front")

    def logic(self):
        Entity.logic(self)

        if self.get_actual_frame() == 36:
            self.__level.remove_object(self)
            self.end = True

    def draw(self, screen):
        Entity.draw(self, screen)

    def load_resources(self):
        Entity.load_resources(self)
