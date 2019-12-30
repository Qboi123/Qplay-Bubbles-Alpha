import os
from PIL import Image

import pyglet

import image


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


def get_bubble_images():
    """generate and get bubble images


    :return:
    """

    # Initialize bubble dictionaries
    bub = dict()
    bub["Normal"] = dict()
    bub["Triple"] = dict()
    bub["Double"] = dict()
    bub["Kill"] = dict()
    bub["SpeedUp"] = dict()
    bub["SpeedDown"] = dict()
    bub["Ultimate"] = dict()
    bub["Up"] = dict()
    bub["Teleporter"] = dict()
    bub["SlowMotion"] = dict()
    bub["DoubleState"] = dict()
    bub["Protect"] = dict()
    bub["ShotSpdStat"] = dict()
    bub["HyperMode"] = dict()
    bub["TimeBreak"] = dict()
    bub["Confusion"] = dict()
    bub["Paralis"] = dict()
    bub["StoneBub"] = dict()
    bub["NoTouch"] = dict()
    bub["Key"] = dict()
    bub["Diamond"] = dict()
    bub["Present"] = dict()
    bub["SpecialKey"] = dict()

    # Import utils, for creating bubble in dynamic resolution
    import utils

    # Initialize minimum and maximum size of the bubbles
    _min = 21
    _max = 80

    # Adding the different resolutions to the bubbles
    for i in range(_min, _max + 1):
        bub["Normal"][i] = utils.createbubble_image((i, i), None, "white")
        bub["Double"][i] = utils.createbubble_image((i, i), None, "gold")
        bub["Triple"][i] = utils.createbubble_image((i, i), None, "blue", "#007fff", "#00ffff", "white")
        bub["SpeedDown"][i] = utils.createbubble_image((i, i), None, "#ffffff", "#a7a7a7", "#7f7f7f", "#373737")
        bub["SpeedUp"][i] = utils.createbubble_image((i, i), None, "#ffffff", "#7fff7f", "#00ff00", "#007f00")
        bub["Up"][i] = utils.createbubble_image((i, i), None, "#00ff00", "#00ff00", "#00000000", "#00ff00")
        bub["Ultimate"][i] = utils.createbubble_image((i, i), None, "gold", "gold", "orange", "gold")
        bub["Kill"][i] = utils.createbubble_image((i, i), None, "#7f0000", "#7f007f", "#7f0000", )
        bub["Teleporter"][i] = utils.createbubble_image((i, i), None, "#7f7f7f", "#7f7f7f", "#ff1020", "#373737")
        bub["SlowMotion"][i] = utils.createbubble_image((i, i), None, "#ffffffff", "#00000000", "#000000ff")
        bub["DoubleState"][i] = utils.createbubble_image((i, i), None, "gold", "#00000000", "gold", "gold")
        bub["Protect"][i] = utils.createbubble_image((i, i), None, "#00ff00", "#3fff3f", "#7fff7f", "#9fff9f")
        bub["ShotSpdStat"][i] = utils.createbubble_image((i, i), None, "#ff7f00", "#ff7f00", "gold")
        bub["HyperMode"][i] = utils.createbubble_image((i, i), None, "black", "black", "white", "black")
        bub["TimeBreak"][i] = utils.createbubble_image((i, i), None, "red", "orange", "yellow", "white")
        bub["Confusion"][i] = utils.createbubble_image((i, i), None, "black", "purple", "magenta", "white")
        bub["Paralis"][i] = utils.createbubble_image((i, i), None, "#ffff00", "#ffff00", "#ffff7f", "#ffffff")
        bub["StoneBub"][i] = utils.createbubble_image((i, i), None, "black", "orange", "yellow")
        bub["NoTouch"][i] = utils.createbubble_image((i, i), None, "#7f7f7f", "#7f7f7f", "#7f7f7f", "#373737")

    # Adding the static-resolution-bubbles.
    bub["Key"][60] = pyglet.resource.image(name="bubbles/key.png")
    bub["Diamond"][36] = pyglet.resource.image(name="bubbles/diamond.png")
    bub["Present"][40] = pyglet.resource.image(name="bubbles/present.png")
    # noinspection PyTypeChecker
    bub["Coin"] = pyglet.resource.image(name="bubbles/coin.png")
    bub["SpecialKey"][48] = pyglet.resource.image(name="bubbles/special_mode.png")
    return bub


# Index assets, and generate bubble images for all sizes.
# NOTE: The bubbles have dynamic size!
pyglet.resource.path = ['./assets']
pyglet.resource.reindex()

get_bubble_images()

