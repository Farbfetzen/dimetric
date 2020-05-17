"""Parent state."""

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


class State:
    def __init__(self, data):
        self.done = False

        # Access the game data and extract the relevant info, for example
        # self.images = data["images"]["player_character"]
        # or
        # self.config = data["config"]["main_menu"]
        # Remember that this is a reference to the config and not a copy.
        # So if you modify this here then that specific sub-dictionary of the
        # config is modified for the whole app.

    def start(self, data):
        """Start or resume a state.
        Use the information from the previous state provided in data to set up
        this state.
        """
        self.done = False

    def close(self):
        """Quit or suspend a state.
        Use this for cleanup. Save relevant data in persistent_state_data to
        pass it to the next state. Set next_state_name to "quit" to
        immediately quit the app.
        """
        persistent_state_data = {"next_state_name": "quit"}
        return persistent_state_data

    def process_events(self):
        pass

    def update(self, dt):
        pass

    def draw(self, dest_surface):
        pass
