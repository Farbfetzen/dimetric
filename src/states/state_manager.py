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


from src.states import main_game, main_menu, options_menu


class StateManager:
    def __init__(self, initial_state_name):
        self.states = {
            "main menu": main_menu.MainMenu,
            "options menu": options_menu.OptionsMenu,
            "main game": main_game.MainGame
        }
        self.current_state = self.states[initial_state_name]()

    def update(self):
        # TODO: Some states must be interruptible without losing data. E.G. the
        #  main game instance should continue after pausing without creating
        #  a new instance.
        if self.current_state.is_done:
            persistent_state_data = self.current_state.persistent_state_data
            next_state_name = persistent_state_data["next_state_name"]
            if next_state_name == "quit":
                # TODO: If there are unsaved changes, ask if they should be
                #  saved, discarded or if the exit should be canceled.
                return False
            elif next_state_name == "MainGame":
                world_name = persistent_state_data["world_name"]
                state = self.states[next_state_name](world_name)
            else:
                state = self.states[next_state_name]()
            state.resume(persistent_state_data)
        return True
