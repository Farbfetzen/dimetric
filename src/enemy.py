import pygame

from src import resources


class Enemy:
    def __init__(self, enemy_type, path):
        self.type = enemy_type
        self.path = path
        self.image = resources.images[self.type]

        # FIXME: Achtung, ich muss hier unterscheiden zwischen width und height
        #     in world space und screen space! Das Rect ist für Kollisionen im
        #     world space gedacht. Das heißt ich muss sehr genau aufpassen, wie
        #     ich die Sachen benennen und zwischen world und screen umrechne.

        width, height = self.image.get_size()
        height_dimetric = width // 2
        self.offset_y = height_dimetric - height
        # Rect in world space, used for collision detection, not for blitting.
        self.rect = pygame.Rect(-1, -1, width, height_dimetric)
        print(self.rect)
        self.rect.center = path[0]

        self.hitpoints = 100
        self.speed = 1
        self.direction = pygame.Vector2(1, 0)

        print(path[0])
        print(self.rect.center)
        print(self.rect)

    def update(self, dt):
        pass
