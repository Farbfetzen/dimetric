import os
import logging


logging.basicConfig(
    filename=".last_run.log",
    filemode="w",
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.DEBUG
)

# Must be done before importing Pygame:
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
os.environ["SDL_VIDEO_CENTERED"] = "1"

from src.game import Game


if __name__ == "__main__":
    logging.info("Initialize new game.")
    game = Game("main menu")
    game.run()
    logging.info("Game ended.")
