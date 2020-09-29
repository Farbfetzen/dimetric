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


from src.helpers import main_to_small_display_int


class State:
    def __init__(self, game, dev_overlay=None):
        self.game = game
        if dev_overlay is None:
            self.dev_overlay = StateDevOverlay(self)
        else:
            self.dev_overlay = dev_overlay(self)
        self.mouse_pos = pygame.Vector2()
        self.persistent_state_data = {}
        self.buttons = ()

    def resume(self, persistent_state_data):
        """Resume an already instantiated state.
        Use the information provided by the previous state to modify
        this state.
        """
        self.persistent_state_data = persistent_state_data
        self.dev_overlay.is_visible = persistent_state_data["dev_overlay_visible"]

        # Make sure button image == hover image when starting the state without
        # moving the mouse. This is necessary because in most states the mouse
        # position is only updated during the event loop:
        mouse_pos_int = main_to_small_display_int(*pygame.mouse.get_pos())
        for b in self. buttons:
            if b.collidepoint(mouse_pos_int):
                break

    def close(self, next_state_name=None):
        """Quit or suspend a state.
        Use this for cleanup. Save relevant data in persistent_state_data to
        pass it to the next state. Set next_state_name to "quit" to
        immediately quit the app.
        """
        if next_state_name is None:
            self.game.quit()
            return
        self.persistent_state_data["dev_overlay_visible"] = self.dev_overlay.is_visible
        self.game.change_states(next_state_name)

    def process_event(self, event, event_manager):
        if event.type == pygame.QUIT:
            self.close()
        elif event.type == pygame.KEYDOWN:
            if event.key == event_manager.k_dev:
                self.dev_overlay.is_visible = not self.dev_overlay.is_visible
        elif ((event.type == pygame.MOUSEMOTION
               or event.type == pygame.MOUSEBUTTONDOWN)
              and self.buttons):
            mouse_pos = main_to_small_display_int(*event.pos)
            for b in self.buttons:
                if (b.collidepoint(mouse_pos)
                        and event.type == pygame.MOUSEBUTTONDOWN
                        and event.button == 1):
                    b.action()
                    break

    def update(self, dt):
        pass

    def draw(self, target_surface):
        raise NotImplementedError


class StateDevOverlay:
    def __init__(self, state):
        self.state = state
        self.is_visible = True
        self.dev_font = pygame.freetype.SysFont(
            "inconsolata, consolas, monospace",
            19
        )
        self.dev_line_hight = self.dev_font.get_sized_height()
        self.dev_color = (250, 250, 250)
        self.dev_font.fgcolor = self.dev_color
        self.dev_margin = pygame.Vector2(10, 10)

        self.fps_text = ""
        self.fps_surf = None
        self.fps_rect = None

    def update(self, clock):
        new_fps_text = f"FPS: {int(clock.get_fps())}"
        if new_fps_text != self.fps_text:
            self.fps_text = new_fps_text
            self.fps_text, self.fps_rect = self.dev_font.render(self.fps_text)
            self.fps_rect.topleft = self.dev_margin

    def draw(self, target_surface):
        target_surface.blit(self.fps_text, self.fps_rect)
