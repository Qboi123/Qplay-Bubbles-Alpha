import pyglet as _pyglet
from typing import Dict as _Dict


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


def get_bubble_images():
    """Generate and get bubble images

    :return:
    """

    # Initialize bubble dictionaries
    bub = dict()
    bub["normal_bubble"] = dict()
    bub["triple_bubble"] = dict()
    bub["double_bubble"] = dict()
    bub["kill_bubble"] = dict()
    bub["speedup_bubble"] = dict()
    bub["slowdown_bubble"] = dict()
    bub["ultimate_bubble"] = dict()
    bub["life_bubble"] = dict()
    bub["teleporter_bubble"] = dict()
    bub["slow_motion_bubble"] = dict()
    bub["double_state_bubble"] = dict()
    bub["protection_bubble"] = dict()
    bub["shot_speed_status_bubble"] = dict()
    bub["hyper_mode_bubble"] = dict()
    bub["game_pause_bubble"] = dict()
    bub["confusion_bubble"] = dict()
    bub["paralis_bubble"] = dict()
    bub["stone_bubble"] = dict()
    bub["ghost_mode_bubble"] = dict()
    bub["key_bubble"] = dict()
    bub["diamond_bubble"] = dict()
    bub["present_bubble"] = dict()
    bub["coin_bubble"] = dict()
    bub["ultra_mode_bubble"] = dict()

    # Import utils, for creating bubble in dynamic resolution
    import utils

    # Initialize minimum and maximum size of the bubbles
    _min = 21
    _max = 80

    # Adding the different resolutions to the bubbles
    for i in range(_min, _max + 1):
        bub["normal_bubble"][i] = utils.createbubble_image((i, i), None, "white")
        bub["double_bubble"][i] = utils.createbubble_image((i, i), None, "gold")
        bub["triple_bubble"][i] = utils.createbubble_image((i, i), None, "blue", "#007fff", "#00ffff", "white")
        bub["slowdown_bubble"][i] = utils.createbubble_image((i, i), None, "#ffffff", "#a7a7a7", "#7f7f7f", "#373737")
        bub["speedup_bubble"][i] = utils.createbubble_image((i, i), None, "#ffffff", "#7fff7f", "#00ff00", "#007f00")
        bub["life_bubble"][i] = utils.createbubble_image((i, i), None, "#00ff00", "#00ff00", "#00000000", "#00ff00")
        bub["ultimate_bubble"][i] = utils.createbubble_image((i, i), None, "gold", "gold", "orange", "gold")
        bub["kill_bubble"][i] = utils.createbubble_image((i, i), None, "#7f0000", "#7f007f", "#7f0000", )
        bub["teleporter_bubble"][i] = utils.createbubble_image((i, i), None, "#7f7f7f", "#7f7f7f", "#ff1020", "#373737")
        bub["slow_motion_bubble"][i] = utils.createbubble_image((i, i), None, "#ffffffff", "#00000000", "#000000ff")
        bub["double_state_bubble"][i] = utils.createbubble_image((i, i), None, "gold", "#00000000", "gold", "gold")
        bub["protection_bubble"][i] = utils.createbubble_image((i, i), None, "#00ff00", "#3fff3f", "#7fff7f", "#9fff9f")
        bub["shot_speed_status_bubble"][i] = utils.createbubble_image((i, i), None, "#ff7f00", "#ff7f00", "gold")
        bub["hyper_mode_bubble"][i] = utils.createbubble_image((i, i), None, "black", "black", "white", "black")
        bub["game_pause_bubble"][i] = utils.createbubble_image((i, i), None, "red", "orange", "yellow", "white")
        bub["confusion_bubble"][i] = utils.createbubble_image((i, i), None, "black", "purple", "magenta", "white")
        bub["paralis_bubble"][i] = utils.createbubble_image((i, i), None, "#ffff00", "#ffff00", "#ffff7f", "#ffffff")
        bub["stone_bubble"][i] = utils.createbubble_image((i, i), None, "black", "orange", "yellow")
        bub["ghost_mode_bubble"][i] = utils.createbubble_image((i, i), None, "#7f7f7f", "#7f7f7f", "#7f7f7f", "#373737")

        center_image(bub["normal_bubble"][i])
        center_image(bub["double_bubble"][i])
        center_image(bub["triple_bubble"][i])
        center_image(bub["slowdown_bubble"][i])
        center_image(bub["speedup_bubble"][i])
        center_image(bub["life_bubble"][i])
        center_image(bub["ultimate_bubble"][i])
        center_image(bub["kill_bubble"][i])
        center_image(bub["teleporter_bubble"][i])
        center_image(bub["slow_motion_bubble"][i])
        center_image(bub["double_state_bubble"][i])
        center_image(bub["protection_bubble"][i])
        center_image(bub["shot_speed_status_bubble"][i])
        center_image(bub["hyper_mode_bubble"][i])
        center_image(bub["game_pause_bubble"][i])
        center_image(bub["confusion_bubble"][i])
        center_image(bub["paralis_bubble"][i])
        center_image(bub["stone_bubble"][i])
        center_image(bub["ghost_mode_bubble"][i])

    # Adding the static-resolution-bubbles.
    bub["key_bubble"][60] = _pyglet.resource.image(name="bubbles/key.png")
    bub["diamond_bubble"][36] = _pyglet.resource.image(name="bubbles/diamond.png")
    bub["present_bubble"][40] = _pyglet.resource.image(name="bubbles/present.png")
    bub["coin_bubble"][42] = _pyglet.resource.image(name="bubbles/coin.png")
    bub["ultra_mode_bubble"][48] = _pyglet.resource.image(name="bubbles/special_mode.png")

    center_image(bub["key_bubble"][60])
    center_image(bub["diamond_bubble"][36])
    center_image(bub["present_bubble"][40])
    center_image(bub["coin_bubble"][42])
    center_image(bub["ultra_mode_bubble"][48])
    return bub


# Index assets, and generate bubble images for all sizes.
# NOTE: The bubbles have dynamic size!
_pyglet.resource.path = ['./assets']
_pyglet.resource.reindex()

# Bubble images
bubbles: _Dict[str, _Dict[int, _pyglet.image.AbstractImage]] = get_bubble_images()

# Player image
player: _pyglet.image.AbstractImage = _pyglet.resource.image(name="sprites/player.png")
print(player.__dict__)
print(player.__repr__())
center_image(player)
