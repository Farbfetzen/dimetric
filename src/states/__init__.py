from .state import State
from .main_game import MainGame
from .main_menu import MainMenu
from .options_menu import OptionsMenu


game_states = {
    "MainMenu": MainMenu,
    "MainGame": MainGame,
    "OptionsMenu": OptionsMenu
}
