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


import pygame

from src import resources
from src import helpers


class EventManager:
    def __init__(self):
        controls = resources.options["controls"]
        self.k_escape = pygame.K_ESCAPE
        self.k_scroll_left = pygame.key.key_code(controls["scroll_left"])
        self.k_scroll_right = pygame.key.key_code(controls["scroll_right"])
        self.k_scroll_up = pygame.key.key_code(controls["scroll_up"])
        self.k_scroll_down = pygame.key.key_code(controls["scroll_down"])
        self.mouse_map_scroll_button_index = controls["mouse_scroll_button_index"]
        self.k_dev = pygame.key.key_code(controls["dev"])

    def process_events(self, scene):
        # Looping through the events here and sending them to the game scenes
        # may make it easier to implement multiple concurrently active scenes
        # in the future. In that case this method would accept a list of scenes
        # and send each event to all scenes. If one scene found it useful then
        # the other scenes should not get the event.
        scene.mouse_pos.update(
            helpers.main_to_small_display_int(*pygame.mouse.get_pos())
        )
        for event in pygame.event.get():
            scene.process_event(event, self)
