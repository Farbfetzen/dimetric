# Copyright (C) 2020  Sebastian Henz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from math import floor

import pygame

from src import constants
from src.world_object import WorldObject


class World:
    def __init__(self, world_data, images):
        self.name = world_data["name"]
        self.sidelength = len(world_data["map"])

        # Check if map is square:
        for row in world_data["map"]:
            assert len(row) == self.sidelength, f"Map '{self.name}' is not square."

        # Overly long init split into multiple methods.
        self.margin = pygame.Vector2()
        self.offset = pygame.Vector2()
        self.surface = None
        self.rect = None
        self.surf_pos = pygame.Vector2()
        self.map_scroll_limit = pygame.Rect(0, 0, 0, 0)
        self.init_surface()
        self.visible_objects = []
        self.map_tiles = []
        self.init_tiles(world_data, images)
        self.path = []
        self.init_path(world_data)

        # highlight:
        image = images["highlight"]
        surface_pos = pygame.Vector2(self.world_pos_to_world_surf(0, 0))
        surface_pos.x -= image.get_width() / 2
        surface_pos.y -= (image.get_height() - constants.TILE_HEIGHT)
        self.highlight = WorldObject(
            "highlight",
            image,
            pygame.Vector2(0, 0),
            surface_pos,
            layer=-1
        )
        self.visible_objects.append(self.highlight)

        # Scroll can be -1, 0 or 1. Meaning left/up, none or right/down.
        self.scroll_direction = pygame.Vector2()

    def init_surface(self):
        # Add a margin of some tile sizes so other stuff fits on the world surface, too.
        self.margin.x = constants.TILE_WIDTH
        self.margin.y = constants.TILE_HEIGHT * 3
        surf_width = self.sidelength * constants.TILE_WIDTH + self.margin.x * 2
        surf_height = self.sidelength * constants.TILE_HEIGHT + self.margin.y * 2
        self.surface = pygame.Surface((surf_width, surf_height))

        # Position the map on the world surface. Offset is the position of
        # (0, 0) world coordinates on the world surface.
        self.offset.x = surf_width // 2
        self.offset.y = self.margin.y

        self.rect = self.surface.get_rect()
        self.rect.center = (
            constants.SMALL_DISPLAY_WIDTH // 2,
            constants.SMALL_DISPLAY_HEIGHT // 2
        )
        # Use surf_pos to track the floating point position because
        # rects can only hold integers.
        self.surf_pos.update(self.rect.topleft)

        # Collision rect for limiting the map scrolling. Makes sure that
        # parts of the map remain visible.
        self.map_scroll_limit.size = (
            constants.SMALL_DISPLAY_WIDTH + surf_width,
            constants.SMALL_DISPLAY_HEIGHT + surf_height
        )
        self.map_scroll_limit.center = self.rect.center

    def init_tiles(self, world_data, images):
        for world_y, row in enumerate(world_data["map"]):
            self.map_tiles.append([])
            for world_x, symbol in enumerate(row):
                tile_type = world_data["palette"][symbol]
                world_pos = pygame.Vector2(world_x, world_y)
                image = images[tile_type]
                x, y = self.world_pos_to_world_surf(world_x, world_y)
                # x and y locate the top corner of the base of the tile.
                # Convert to topleft of the image:
                surface_pos = pygame.Vector2(
                    x - image.get_width() / 2,
                    y - (image.get_height() - constants.TILE_HEIGHT)
                )
                tile = WorldObject(tile_type, image, world_pos, surface_pos)
                self.map_tiles[world_y].append(tile)
                self.visible_objects.append(tile)

    def init_path(self, world_data):
        path_start = None
        path_end = None
        path_raw = []
        for world_y, row in enumerate(world_data["map"]):
            for world_x, symbol in enumerate(row):
                tile_type = world_data["palette"][symbol]
                world_pos = pygame.Vector2(world_x, world_y)
                if tile_type == "path":
                    path_raw.append(world_pos)
                    if symbol == "S":
                        path_start = world_pos
                        path_raw.remove(world_pos)
                    elif symbol == "E":
                        path_end = world_pos
        if path_start is None or path_end is None:
            raise ValueError(f"Missing path start or end in map '{self.name}'.")

        self.path.append(path_start)
        while path_raw:
            x, y = self.path[-1]
            for neighbor in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if neighbor in path_raw:
                    neighbor_ = pygame.Vector2(neighbor)
                    self.path.append(neighbor_)
                    path_raw.remove(neighbor_)
                    break
            else:
                raise ValueError(f"Malformed path in map '{self.name}': Neighbor not found.")
        if self.path[-1] != path_end:
            raise ValueError(f"Malformed path in map '{self.name}': Ends at wrong position.")

    def world_pos_to_world_surf(self, world_x, world_y):
        # ATTENTION: Remember to account for the width and height of a sprite
        #   before blitting.
        x = (world_x - world_y) * constants.TILE_WIDTH_HALF + self.offset.x
        y = (world_x + world_y) * constants.TILE_HEIGHT_HALF + self.offset.y
        return x, y

    def small_display_to_world_pos(self, x, y):
        # Adapted from the code example in wikipedia:
        # https://en.wikipedia.org/wiki/Isometric_video_game_graphics#Mapping_screen_to_world_coordinates

        # Get x and y relative to the topleft corner of the bounding rectangle
        # of the map (not the rect of the map surface):
        x = x - self.rect.x - self.margin.x
        y = y - self.rect.y - self.margin.y

        virt_x = x / constants.TILE_WIDTH
        virt_y = y / constants.TILE_HEIGHT
        world_x = virt_y + (virt_x - self.sidelength / 2)
        world_y = virt_y - (virt_x - self.sidelength / 2)
        return world_x, world_y

    def small_display_to_tile_pos(self, x, y):
        # Important to use math.floor() instead of int() because int() rounds
        # towards zero which would introduce an off-by-one error along the
        # top edges of the map.
        world_x, world_y = self.small_display_to_world_pos(x, y)
        return floor(world_x), floor(world_y)

    def get_tile_at(self, x, y):
        if 0 <= x < self.sidelength and 0 <= y < self.sidelength:
            return self.map_tiles[y][x]
        return None

    def update(self, dt):
        if self.scroll_direction != (0, 0):
            self.scroll(
                self.scroll_direction.elementwise()
                * constants.WORLD_SCROLL_SPEED
                * dt
            )

    def scroll(self, rel):
        self.surf_pos += rel
        self.rect.topleft = self.surf_pos

        if not self.map_scroll_limit.contains(self.rect):
            # Limit scrolling such that the map does not disappear completely
            # from the screen. Only do this if the rect is not completely inside
            # the limit because otherwise surf_pos will constantly get changed
            # to integer rect coords which breaks scrolling with the mouse.
            self.rect.clamp_ip(self.map_scroll_limit)
            self.surf_pos.update(self.rect.topleft)

    def draw(self, target_surface):
        # self.surface.fill((0, 0, 0))
        self.visible_objects.sort()
        for v_obj in self.visible_objects:
            # noinspection PyTypeChecker
            self.surface.blit(v_obj.image, v_obj.surface_pos)
        # TODO: Check if surface.blits() is faster once there are more objects
        #  on screen: enemies, towers, projectiles.
        target_surface.blit(self.surface, self.rect)
