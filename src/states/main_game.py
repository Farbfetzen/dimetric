"""Main game state"""

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


import src.states.state


class MainGame(src.states.state.State):
    def __init__(self, data, map_name):
        super().__init__(data)
        self.map = data["maps"][map_name]

    # camera_offset_x = display_rect.centerx - constants.TILE_WIDTH_HALF
    # camera_offset_y = display_rect.centery - constants.TILE_HEIGHT_HALF * len(map_data)

    def process_events(self):
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         running = False
        #     elif event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_ESCAPE:
        #             running = False
        #     elif event.type == pygame.MOUSEMOTION:
        #         if event.buttons[2]:  # right mouse button
        #             OFFSET_X += event.rel[0]
        #             OFFSET_Y += event.rel[1]
        #     elif event.type == pygame.MOUSEBUTTONDOWN:
        #         print(screen_to_map(*event.pos))
        # pressed = pygame.key.get_pressed()
        # map_scroll_distance = MAP_SCROLL_SPEED * dt
        # if pressed[pygame.K_w]:
        #     OFFSET_Y -= map_scroll_distance
        # if pressed[pygame.K_a]:
        #     OFFSET_X -= map_scroll_distance
        # if pressed[pygame.K_s]:
        #     OFFSET_Y += map_scroll_distance
        # if pressed[pygame.K_d]:
        #     OFFSET_X += map_scroll_distance
        pass

    def draw(self, dest_surface):
        # display.fill(BACKGROUND_COLOR)
        # for map_y, row in enumerate(map_data):
        #     for map_x, i in enumerate(row):
        #         tile = tiles[i]
        #         display.blit(tile, map_to_screen(map_x, map_y, *tile_offsets[i]))
        #
        # # pygame.draw.circle(display, pygame.Color("red"), (OFFSET_X, OFFSET_Y), 1)
        # # pygame.draw.circle(display, pygame.Color("orange"), display_rect.center, 1)
        #
        # # Highlight the outline of a tile when the mouse is over the map.
        # # TODO: highlight the top of the platform
        # # TODO: snap to grid when mouse is over the raised part of a platform, not
        # #   only over the base.
        # mouse_pos = pygame.mouse.get_pos()
        # mouse_map_pos = screen_to_map(*mouse_pos)
        # if any(0 > pos or pos > len(map_data) - 1 for pos in mouse_map_pos):
        #     tile = tiles[2]
        #     rect = tile.get_rect(center=mouse_pos)
        #     display.blit(tiles[2], rect)
        # else:
        #     display.blit(
        #         tiles[2],
        #         map_to_screen(
        #             mouse_map_pos[0],
        #             mouse_map_pos[1],
        #             *tile_offsets[2]
        #         )
        #     )
        pass
