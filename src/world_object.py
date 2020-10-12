from dataclasses import dataclass

import pygame


@dataclass
class WorldObject:
    type: str
    image: pygame.Surface
    world_pos: pygame.Vector2
    surface_pos: pygame.Vector2
    layer: int = 0

    def __lt__(self, other):
        return ((self.world_pos.x, self.world_pos.y, self.layer) <
                (other.world_pos.x, other.world_pos.y, other.layer))
