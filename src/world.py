"""Tile and world class."""

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


from collections import namedtuple
from math import floor

import pygame

import src.constants as const


class World:
    def __init__(self, world_data, images):
        self.name = world_data["name"]
        self.sidelength = len(world_data["map"])

        # Check if map is square:
        for row in world_data["map"]:
            if len(row) != len(world_data["map"]):
                raise ValueError(f"Map '{self.name}' is not square.")

        # Add a margin of some tile sizes so other stuff fits on the world surface, too.
        margin_x = const.TILE_WIDTH * 2
        margin_y = const.TILE_HEIGHT * 5
        surf_width = self.sidelength * const.TILE_WIDTH + margin_x
        surf_height = self.sidelength * const.TILE_HEIGHT + margin_y
        self.surface = pygame.Surface((surf_width, surf_height))

        # Center the map on the world surface. Offset is the position of
        # (0, 0) world coordinates on the world surface.
        self.offset_x = surf_width // 2
        self.offset_y = (surf_height // 2
                         - self.sidelength * const.TILE_HEIGHT_HALF)

        self.rect = self.surface.get_rect()
        self.rect.center = (const.SMALL_DISPLAY_WIDTH / 2, const.SMALL_DISPLAY_HEIGHT / 2)
        # Use surf_pos to track the floating point position because
        # rects can only hold integers.
        self.surf_pos = pygame.Vector2(self.rect.topleft)

        # Collision rect for limiting the map scrolling. Makes sure that
        # parts of the map remain visible.
        # FIXME: This will probably have to be modified when I implement zooming.
        #  Test by zooming in really close or far away and then scrolling to
        #  the edges.
        outer_margin_x = surf_width
        outer_margin_y = surf_height
        self.map_scroll_limit = pygame.Rect(
            0,
            0,
            const.SMALL_DISPLAY_WIDTH + outer_margin_x,
            const.SMALL_DISPLAY_HEIGHT + outer_margin_y
        )
        self.map_scroll_limit.center = self.rect.center

        # Scroll can be -1, 0 or 1. Meaning left/up, none or right/down.
        self.scroll_direction = pygame.Vector2()
        self.scroll_distance = pygame.Vector2(const.WORLD_SCROLL_SPEED)

        self.tiles = []  # Used for blitting
        self.tiles_nested = []  # Useful for finding a tile by world coordinates
        Tile = namedtuple(
            "Tile",
            ("type", "image", "world_x", "world_y", "topleft")
        )
        path_start = None
        path_end = None
        self.path_raw = set()
        for world_y, row in enumerate(world_data["map"]):
            self.tiles_nested.append([])
            for world_x, symbol in enumerate(row):
                tile_type = world_data["palette"][symbol]
                if tile_type == "path":
                    pos = (world_x, world_y)
                    self.path_raw.add(pos)
                    if symbol == "S":
                        path_start = pos
                        self.path_raw.remove(pos)
                    elif symbol == "E":
                        path_end = pos
                image = images[tile_type]
                x, y = self.world_pos_to_world_surf(world_x, world_y)
                # x and y locate the top corner of the base of the tile.
                # Convert to topleft of the image:
                top = x - image.get_width() / 2
                left = y - (image.get_height() - const.TILE_HEIGHT)
                tile = Tile(tile_type, image, world_x, world_y, (top, left))
                self.tiles_nested[world_y].append(tile)
                self.tiles.append(tile)

        if path_start is None or path_end is None:
            raise ValueError(f"Missing path start or end in map '{self.name}'.")
        self.path = [path_start]
        while self.path_raw:
            x, y = self.path[-1]
            for neighbor in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if neighbor in self.path_raw:
                    self.path.append(neighbor)
                    self.path_raw.remove(neighbor)
                    break
            else:
                raise ValueError(f"Malformed path in map '{self.name}': Neighbor not found.")
        if self.path[-1] != path_end:
            raise ValueError(f"Malformed path in map '{self.name}': Ends at wrong position.")

    def world_pos_to_world_surf(self, world_x, world_y):
        # ATTENTION: Remember to account for the width and height of a sprite
        #   before blitting.
        x = (world_x - world_y) * const.TILE_WIDTH_HALF + self.offset_x
        y = (world_x + world_y) * const.TILE_HEIGHT_HALF + self.offset_y
        return x, y

    def small_display_to_world_pos(self, x, y, tile=False):
        # Adapted from the code example in wikipedia:
        # https://en.wikipedia.org/wiki/Isometric_video_game_graphics#Mapping_screen_to_world_coordinates

        # Get x and y relative to the topleft corner of the bounding rectangle
        # of the map:
        x = x - self.rect.x - self.offset_x + self.sidelength * const.TILE_WIDTH_HALF
        y = y - self.rect.y - self.offset_y

        virt_x = x / const.TILE_WIDTH
        virt_y = y / const.TILE_HEIGHT
        world_x = virt_y + (virt_x - self.sidelength / 2)
        world_y = virt_y - (virt_x - self.sidelength / 2)

        # Remember: Coordinates are floats. If you want to allow negative
        # tile positions then you must use math.floor() and not int().
        # int() rounds towards zero which would introduce an off-by-one error
        # for negative tile positions.
        if tile:
            world_x = floor(world_x)
            world_y = floor(world_y)

        return world_x, world_y

    def get_tile_at(self, x, y):
        if 0 <= x < self.sidelength and 0 <= y < self.sidelength:
            return self.tiles_nested[y][x]
        return None

    def update(self, dt):
        if self.scroll_direction != (0, 0):
            self.scroll(
                self.scroll_direction.elementwise() * const.WORLD_SCROLL_SPEED * dt
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
        blit_list = [(tile.image, tile.topleft) for tile in self.tiles]
        self.surface.blits(blit_list, False)

        target_surface.blit(self.surface, self.rect)
