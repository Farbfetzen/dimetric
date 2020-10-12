import os
import json
import logging

import pygame

from src.constants import DEFAULT_OPTIONS


images = {}
worlds = {}
options = {}


def load_images():
    for filename in os.listdir("images"):
        image = pygame.image.load(os.path.join("images", filename))
        image = image.convert_alpha()
        name = os.path.splitext(filename)[0]
        images[name] = image


def load_worlds():
    for filename in os.listdir("worlds"):
        with open(os.path.join("worlds", filename), "r") as file:
            world_data = json.load(file)
            worlds[world_data["name"]] = world_data


def load_options():
    try:
        with open("options.json", "r") as file:
            options.update(json.load(file))
    except FileNotFoundError:
        logging.error("Options file not found, using default options.")
        options.update(DEFAULT_OPTIONS)
        save_options()


def save_options():
    with open("options.json", "w") as file:
        json.dump(options, file, indent=4, sort_keys=True)


def load_all():
    load_options()
    load_images()
    load_worlds()
